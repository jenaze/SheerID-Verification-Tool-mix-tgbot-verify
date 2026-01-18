"""
Anti-Detection Module for SheerID Verification
Adapted from SheerID-Verification-Tool for tgbot-verify

Features:
- Random User-Agent rotation
- Browser-like headers with NewRelic tracking
- Random fingerprint generation
- Async delay between requests
"""

import random
import hashlib
import time
import uuid
import base64
import json
import asyncio
from typing import Dict, Tuple

# ============ USER AGENTS ============
USER_AGENTS = [
    # Chrome Windows
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    # Chrome Mac
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
    # Firefox
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:134.0) Gecko/20100101 Firefox/134.0",
    # Edge
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0",
    # Safari
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.2 Safari/605.1.15",
]

RESOLUTIONS = ["1920x1080", "1366x768", "1536x864", "1440x900", "2560x1440"]
TIMEZONES = [-8, -7, -6, -5, -4, 0, 1, 2, 8]
LANGUAGES = ["en-US,en;q=0.9", "en-US,en;q=0.9,es;q=0.8", "en-GB,en;q=0.9"]
PLATFORMS = [
    ("Windows", '"Windows"', '"Chromium";v="132", "Google Chrome";v="132"'),
    ("macOS", '"macOS"', '"Chromium";v="132", "Google Chrome";v="132"'),
]


def get_random_user_agent() -> str:
    """Get a random User-Agent string"""
    return random.choice(USER_AGENTS)


def get_fingerprint() -> str:
    """Generate realistic browser fingerprint hash"""
    components = [
        str(int(time.time() * 1000)),
        str(random.random()),
        random.choice(RESOLUTIONS),
        str(random.choice(TIMEZONES)),
        random.choice(LANGUAGES).split(",")[0],
        random.choice(["Win32", "MacIntel", "Linux x86_64"]),
        str(random.randint(2, 16)),   # CPU cores
        str(random.randint(4, 32)),   # Device memory
        str(uuid.uuid4()),
    ]
    return hashlib.md5("|".join(components).encode()).hexdigest()


def generate_newrelic_headers() -> Dict[str, str]:
    """Generate NewRelic tracking headers required by SheerID API"""
    trace_id = uuid.uuid4().hex + uuid.uuid4().hex[:8]
    trace_id = trace_id[:32]
    span_id = uuid.uuid4().hex[:16]
    timestamp = int(time.time() * 1000)
    
    payload = {
        "v": [0, 1],
        "d": {
            "ty": "Browser",
            "ac": "364029",
            "ap": "134291347",
            "id": span_id,
            "tr": trace_id,
            "ti": timestamp
        }
    }
    
    return {
        "newrelic": base64.b64encode(json.dumps(payload).encode()).decode(),
        "traceparent": f"00-{trace_id}-{span_id}-01",
        "tracestate": f"364029@nr=0-1-364029-134291347-{span_id}----{timestamp}"
    }


def get_headers() -> Dict[str, str]:
    """Generate browser-like headers for SheerID API calls"""
    ua = get_random_user_agent()
    platform = random.choice(PLATFORMS)
    language = random.choice(LANGUAGES)
    nr_headers = generate_newrelic_headers()
    
    return {
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": language,
        "cache-control": "no-cache",
        "content-type": "application/json",
        "sec-ch-ua": platform[2],
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": platform[1],
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": ua,
        "clientversion": "2.158.0",
        "clientname": "jslib",
        "origin": "https://services.sheerid.com",
        "referer": "https://services.sheerid.com/",
        **nr_headers
    }


async def random_delay(min_ms: int = 200, max_ms: int = 600):
    """Async random delay to avoid detection"""
    await asyncio.sleep(random.randint(min_ms, max_ms) / 1000)
