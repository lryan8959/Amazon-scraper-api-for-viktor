import os
import time
import random
import asyncio
import uuid
from contextlib import asynccontextmanager
from typing import List, Optional

from fastapi import FastAPI, HTTPException, Security, Query
from fastapi.responses import JSONResponse
from fastapi.security import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from playwright.async_api import async_playwright

import scraper

# Configuration
API_KEYS = {k.strip() for k in os.getenv("API_KEYS", "demo-key-12345").split(",") if k.strip()}
CACHE_TTL = int(os.getenv("CACHE_TTL", "3600"))
MAX_BATCH = int(os.getenv("MAX_BATCH", "5"))
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "85"))
MAX_CACHE = 500
MAX_JOBS = 200

key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


def require_key(key: Optional[str] = Security(key_header)):
    if not API_KEYS:
        raise HTTPException(503, "Server misconfigured: no API_KEYS set")
    if not key or key not in API_KEYS:
        raise HTTPException(401, "Invalid or missing API key")
    return key


class State:
    pw = None
    browser = None
    context = None
    page = None
    zip_ok = False
    dirty = True
    warming = False


S = State()
LOCK = asyncio.Lock()
CACHE = {}
INFLIGHT = {}
JOBS = {}


async def launch_browser():
    args = {
        "headless": True,
        "args": [
            "--disable-blink-features=AutomationControlled",
            "--no-sandbox",
            "--disable-dev-shm-usage"
        ]
    }
    if scraper.PROXY:
        args["proxy"] = scraper.PROXY
    S.browser = await S.pw.chromium.launch(**args)


async def new_session():
    if S.browser is None or not S.browser.is_connected():
        await launch_browser()
    if S.context:
        try:
            await S.context.close()
        except Exception:
            pass

    ctx = await S.browser.new_context(
        user_agent=scraper.UA,
        locale="en-US",
        timezone_id="America/New_York",
        viewport={"width": 1366, "height": 900},
        extra_http_headers={"Accept-Language": "en-US,en;q=0.9"},
    )

    await ctx.add_cookies([
        {"name": "i18n-prefs", "value": "USD", "domain": ".amazon.com", "path": "/"},
        {"name": "lc-main", "value": "en_US", "domain": ".amazon.com", "path": "/"},
    ])

    await ctx.add_init_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )

    S.context = ctx
    S.page = await ctx.new_page()
    S.zip_ok = True

    if scraper.US_ZIP:
        try:
            S.zip_ok = await scraper.ensure_us_location(S.page, scraper.US_ZIP)
        except Exception as e:
            print("Location setup error:", str(e).splitlines()[0])
            S.zip_ok = False

    S.dirty = False


async def warmup():
    S.warming = True
    print("Warmup started ...")
    async with LOCK:
        try:
            await new_session()
            print(f"Warmup done. us_location_ok={S.zip_ok}")
        except Exception as e:
            print("Warmup error:", str(e).splitlines()[0])
            S.dirty = True
    S.warming = False


@asynccontextmanager
async def lifespan(app):
    S.pw = await async_playwright().start()
    await launch_browser()
    asyncio.create_task(warmup())
    yield
    try:
        await S.browser.close()
    except Exception:
        pass
    await S.pw.stop()


app = FastAPI(
    title="Amazon Product Scraper API",
    version="1.1",
    lifespan=lifespan,
    description="Scrapes Amazon product data by ASIN"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def parse_asin(value: str) -> str:
    asin = scraper.find_asin(value or "")
    if not asin:
        raise HTTPException(400, f"Could not find an ASIN in: {value}")
    return asin


async def scrape_asin(asin: str, fresh: bool = False) -> dict:
    hit = CACHE.get(asin)
    if hit and not fresh and CACHE_TTL and time.time() - hit[0] < CACHE_TTL:
        return {**hit[1], "cached": True}

    async with LOCK:
        hit = CACHE.get(asin)
        if hit and not fresh and CACHE_TTL and time.time() - hit[0] < CACHE_TTL:
            return {**hit[1], "cached": True}

        print(f"[{asin}] scraping ...")
        last_err = "unknown error"
        record = None

        for attempt in range(scraper.MAX_RETRIES + 1):
            try:
                if S.page is None or S.dirty:
                    await new_session()
                if scraper.US_ZIP and scraper.REQUIRE_US_ZIP and not S.zip_ok:
                    S.dirty = True
                    raise RuntimeError("Could not set US delivery location")
                record = await scraper.scrape_one(S.page, asin)
                break
            except Exception as e:
                last_err = str(e).split("\n")[0]
                print(f"[{asin}] attempt {attempt + 1} failed: {last_err}")
                S.dirty = True
                if attempt < scraper.MAX_RETRIES:
                    await asyncio.sleep(random.uniform(2, 4))

        if record is None:
            raise HTTPException(502, f"Scrape failed after retries: {last_err}")

    if record.get("status") == "not_found":
        raise HTTPException(404, f"Product {asin} not found on Amazon")

    print(f"[{asin}] done")
    record["cached"] = False

    if CACHE_TTL:
        if len(CACHE) >= MAX_CACHE:
            CACHE.pop(next(iter(CACHE)))
        CACHE[asin] = (time.time(), record)

    return record


def scrape_task(asin: str, fresh: bool) -> asyncio.Task:
    t = INFLIGHT.get(asin)
    if t is None or t.done():
        t = asyncio.create_task(scrape_asin(asin, fresh))
        INFLIGHT[asin] = t

        def _done(task, asin=asin):
            if INFLIGHT.get(asin) is task:
                INFLIGHT.pop(asin, None)
            if not task.cancelled():
                task.exception()

        t.add_done_callback(_done)
    return t


async def scrape_with_deadline(asin: str, fresh: bool):
    task = scrape_task(asin, fresh)
    try:
        return await asyncio.wait_for(asyncio.shield(task), REQUEST_TIMEOUT)
    except asyncio.TimeoutError:
        return JSONResponse(status_code=504, content={
            "status": "processing",
            "asin": asin,
            "detail": "Still scraping. Retry in 15-30 seconds or use POST /v1/jobs."
        })


async def run_job(job_id: str, inputs: List[str], fresh: bool):
    job = JOBS[job_id]
    job["status"] = "running"

    for i, u in enumerate(inputs):
        try:
            res = await scrape_task(parse_asin(u), fresh)
        except HTTPException as e:
            res = {
                "input": u,
                "status": "error",
                "http_status": e.status_code,
                "error": e.detail
            }
        except Exception as e:
            res = {
                "input": u,
                "status": "error",
                "http_status": 500,
                "error": str(e)
            }

        job["products"].append(res)

        if i < len(inputs) - 1 and not res.get("cached") and res.get("status") == "ok":
            await asyncio.sleep(random.uniform(3, 6))

    ok = sum(1 for r in job["products"] if r.get("status") == "ok")
    job.update(
        status="done",
        successful=ok,
        failed=len(job["products"]) - ok,
        finished_at=time.time()
    )


def create_job(inputs: List[str], fresh: bool) -> dict:
    if len(JOBS) >= MAX_JOBS:
        JOBS.pop(next(iter(JOBS)))

    job_id = uuid.uuid4().hex[:12]
    JOBS[job_id] = {
        "job_id": job_id,
        "status": "queued",
        "total": len(inputs),
        "products": [],
        "created_at": time.time()
    }

    asyncio.create_task(run_job(job_id, inputs, fresh))
    return {
        "job_id": job_id,
        "status": "queued",
        "poll": f"/v1/jobs/{job_id}"
    }


# Models
class ProductRequest(BaseModel):
    url: str
    fresh: bool = False


class BatchRequest(BaseModel):
    urls: List[str]
    fresh: bool = False


# Routes
@app.get("/")
def root():
    return {
        "name": "Amazon Product Scraper API",
        "docs": "/docs",
        "health": "/health",
        "version": "1.1"
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
        "version": "1.1",
        "browser_running": bool(S.browser and S.browser.is_connected()),
        "warming_up": S.warming,
        "session_ready": S.page is not None and not S.dirty,
        "us_location_ok": S.zip_ok,
        "delivery_zip": scraper.US_ZIP,
        "cached_products": len(CACHE),
        "jobs": len(JOBS),
    }


@app.get("/v1/product")
async def get_product(
    url: str = Query(..., description="Amazon product link or ASIN"),
    fresh: bool = False,
    key: str = Security(require_key)
):
    return await scrape_with_deadline(parse_asin(url), fresh)


@app.post("/v1/product")
async def post_product(body: ProductRequest, key: str = Security(require_key)):
    return await scrape_with_deadline(parse_asin(body.url), body.fresh)


@app.post("/v1/jobs", status_code=202)
async def post_job(body: BatchRequest, key: str = Security(require_key)):
    if not body.urls:
        raise HTTPException(400, "urls is empty")
    if len(body.urls) > MAX_BATCH:
        raise HTTPException(400, f"Max {MAX_BATCH} products per job")
    return create_job(body.urls, body.fresh)


@app.get("/v1/jobs/{job_id}")
async def get_job(job_id: str, key: str = Security(require_key)):
    job = JOBS.get(job_id)
    if not job:
        raise HTTPException(404, "Job not found")
    return job


@app.post("/v1/products", status_code=202)
async def post_products(body: BatchRequest, key: str = Security(require_key)):
    if len(body.urls) > MAX_BATCH:
        raise HTTPException(400, f"Max {MAX_BATCH} products per request")
    return create_job(body.urls, body.fresh)
