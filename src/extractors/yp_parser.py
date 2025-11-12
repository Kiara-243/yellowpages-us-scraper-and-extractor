import logging
import math
import random
import time
from typing import Any, Dict, List, Optional
from urllib.parse import urlencode

import requests
from bs4 import BeautifulSoup

from .utils_formatting import (
    clean_text,
    extract_address,
    extract_categories,
    extract_email_from_text,
    extract_gallery_urls,
    extract_general_info,
    extract_hours,
    extract_phone,
    extract_ratings,
    extract_reviews,
)

logger = logging.getLogger(__name__)

def _build_search_url(
    base_url: str,
    keyword: str,
    location: str,
    page: int,
    sort_by: str,
) -> str:
    """
    Build a Yellowpages search URL for keyword + location + page.
    """
    params = {
        "search_terms": keyword,
        "geo_location_terms": location,
        "page": page,
    }

    # Map human readable sort choices to YP sort codes where applicable
    sort_mapping = {
        "best_match": "best",
        "distance": "distance",
        "rating": "rating",
        "name": "name",
    }
    sort_code = sort_mapping.get(sort_by, "best")
    params["sort"] = sort_code

    return f"{base_url.rstrip('/')}/search?{urlencode(params)}"

def _get_with_retries(
    url: str,
    headers: Dict[str, str],
    timeout: int,
    retry_attempts: int,
    retry_backoff_seconds: float,
) -> Optional[requests.Response]:
    """
    Perform a GET request with basic retry logic.
    """
    for attempt in range(1, retry_attempts + 1):
        try:
            logger.debug("GET %s (attempt %d)", url, attempt)
            response = requests.get(url, headers=headers, timeout=timeout)
            if response.status_code == 200:
                return response
            logger.warning(
                "Received status %s from %s",
                response.status_code,
                url,
            )
        except requests.RequestException as exc:
            logger.warning("Request error for %s: %s", url, exc)
        if attempt < retry_attempts:
            sleep_for = retry_backoff_seconds * attempt + random.uniform(0, 0.5)
            logger.debug("Sleeping %.2f seconds before retry", sleep_for)
            time.sleep(sleep_for)
    logger.error("Failed to GET %s after %d attempts", url, retry_attempts)
    return None

def _parse_listing(listing_soup: BeautifulSoup) -> Dict[str, Any]:
    """
    Parse a single business listing block into a structured dictionary.
    This is designed to tolerate minor HTML changes by relying on generic patterns.
    """
    # Name
    name_tag = (
        listing_soup.find("a", class_="business-name")
        or listing_soup.find("a", {"itemprop": "name"})
        or listing_soup.find("h2")
    )
    name = clean_text(name_tag.get_text()) if name_tag else ""

    # Address
    address = extract_address(listing_soup)

    # Phone
    phone = extract_phone(listing_soup)

    # Website link
    website_tag = listing_soup.find("a", class_="track-visit-website") or listing_soup.find(
        "a", string=lambda s: s and "Website" in s
    )
    website = website_tag.get("href") if website_tag else ""

    # Email (YP rarely shows raw emails; try to infer from website block or text)
    email = extract_email_from_text(listing_soup.get_text(" "))

    ratings = extract_ratings(listing_soup)
    categories = extract_categories(listing_soup)
    hours = extract_hours(listing_soup)
    gallery = extract_gallery_urls(listing_soup)
    yp_reviews = extract_reviews(listing_soup)
    general_info = extract_general_info(listing_soup)

    return {
        "name": name,
        "address": address,
        "phone": phone,
        "email": email,
        "website": website,
        "ratings": ratings,
        "categories": categories,
        "hours": hours,
        "gallery": gallery,
        "ypReviews": yp_reviews,
        "generalInfo": general_info,
    }

def _extract_listings(page_html: str) -> List[Dict[str, Any]]:
    soup = BeautifulSoup(page_html, "html.parser")

    # Yellowpages listings are often under 'div.result' or 'div.srp-listing'
    listing_blocks = soup.find_all(
        "div",
        class_=lambda c: c and ("result" in c or "srp-listing" in c),
    )

    logger.debug("Found %d listing blocks on page", len(listing_blocks))
    records: List[Dict[str, Any]] = []
    for block in listing_blocks:
        try:
            record = _parse_listing(block)
            if record.get("name"):
                records.append(record)
        except Exception as exc:  # noqa: BLE001
            logger.exception("Failed to parse a listing: %s", exc)
    return records

def _estimate_total_pages(
    first_page_records: int,
    max_results: int,
    max_pages_per_search: int,
    approx_results_per_page: int = 30,
) -> int:
    """
    Roughly estimate how many pages we should iterate through. If the first page
    returns fewer items, scale pages proportionally.
    """
    if first_page_records <= 0:
        return 1
    # naive estimate: how many pages needed for max_results
    pages_for_max = math.ceil(max_results / max(first_page_records, approx_results_per_page))
    return min(max_pages_per_search, max(1, pages_for_max))

def fetch_businesses(
    keyword: str,
    location: str,
    max_results: int,
    sort_by: str,
    settings: Dict[str, Any],
) -> List[Dict[str, Any]]:
    """
    Fetch business listings for a given keyword and location from Yellowpages.
    Returns a list of dict records.
    """
    base_url = settings.get("base_url", "https://www.yellowpages.com")
    timeout = int(settings.get("timeout_seconds", 15))
    max_pages_per_search = int(settings.get("max_pages_per_search", 5))
    retry_attempts = int(settings.get("retry_attempts", 2))
    retry_backoff_seconds = float(settings.get("retry_backoff_seconds", 1.5))

    headers = {
        "User-Agent": settings.get(
            "user_agent",
            "YellowpagesScraperBot/1.0 (+https://bitbash.dev)",
        ),
        "Accept-Language": "en-US,en;q=0.9",
    }

    all_records: List[Dict[str, Any]] = []
    first_page_estimated = False
    total_pages = max_pages_per_search

    for page in range(1, max_pages_per_search + 1):
        if len(all_records) >= max_results:
            logger.debug("Reached requested max_results=%d", max_results)
            break

        url = _build_search_url(
            base_url=base_url,
            keyword=keyword,
            location=location,
            page=page,
            sort_by=sort_by,
        )

        response = _get_with_retries(
            url=url,
            headers=headers,
            timeout=timeout,
            retry_attempts=retry_attempts,
            retry_backoff_seconds=retry_backoff_seconds,
        )
        if response is None:
            logger.warning("Skipping page %d due to repeated failures", page)
            continue

        page_records = _extract_listings(response.text)
        logger.info(
            "Parsed %d records from page %d (keyword='%s', location='%s')",
            len(page_records),
            page,
            keyword,
            location,
        )

        if page == 1 and not first_page_estimated:
            total_pages = _estimate_total_pages(
                first_page_records=len(page_records),
                max_results=max_results,
                max_pages_per_search=max_pages_per_search,
            )
            first_page_estimated = True
            logger.debug("Estimated total pages to fetch: %d", total_pages)

        all_records.extend(page_records)

        if len(page_records) == 0:
            logger.info("No more records on page %d, stopping early.", page)
            break

        if page >= total_pages:
            logger.debug("Reached estimated total_pages=%d, stopping.", total_pages)
            break

    # Trim to max_results
    if len(all_records) > max_results:
        all_records = all_records[:max_results]

    return all_records