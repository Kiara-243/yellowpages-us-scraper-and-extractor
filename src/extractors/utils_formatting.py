import json
import re
from typing import Any, Dict, List

from bs4 import BeautifulSoup

def clean_text(value: str) -> str:
    """
    Normalize whitespace in text.
    """
    if value is None:
        return ""
    return re.sub(r"\s+", " ", value).strip()

def extract_phone(listing_soup: BeautifulSoup) -> str:
    """
    Extract a phone number from a listing.
    """
    phone_tag = listing_soup.find("div", class_="phones") or listing_soup.find(
        "a",
        href=lambda h: h and "tel:" in h,
    )
    if phone_tag:
        text = phone_tag.get_text() if phone_tag.name != "a" else phone_tag.get("href", "")
        text = text.replace("tel:", "")
        return clean_text(text)
    # Fallback: look for typical phone pattern in text
    match = re.search(
        r"(\(?\d{3}\)?\s*[-.]?\s*\d{3}\s*[-.]?\s*\d{4})",
        listing_soup.get_text(" "),
    )
    return clean_text(match.group(1)) if match else ""

def extract_address(listing_soup: BeautifulSoup) -> str:
    """
    Extract a postal address block.
    """
    addr_tag = listing_soup.find("div", class_="street-address")
    city_state_zip_tag = listing_soup.find("div", class_="locality")
    parts: List[str] = []
    if addr_tag:
        parts.append(clean_text(addr_tag.get_text()))
    if city_state_zip_tag:
        parts.append(clean_text(city_state_zip_tag.get_text()))
    if parts:
        return ", ".join(parts)
    # Fallback: generic address patterns
    maybe_address = listing_soup.find("p", class_="adr")
    if maybe_address:
        return clean_text(maybe_address.get_text(" "))
    return ""

def extract_email_from_text(text: str) -> str:
    """
    Extract a first email address found in text, if any.
    """
    match = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
    return match.group(0) if match else ""

def extract_ratings(listing_soup: BeautifulSoup) -> Dict[str, Any]:
    """
    Extract Yellowpages ratings info (and future external ratings).
    """
    ratings: Dict[str, Any] = {}

    # YP star rating is often represented with aria-label or "result-rating" classes.
    rating_tag = listing_soup.find(
        attrs={"aria-label": re.compile(r"\d+(\.\d+)? star rating")},
    )
    if rating_tag:
        match = re.search(r"(\d+(\.\d+)?)", rating_tag["aria-label"])
        if match:
            ratings["yellowpages"] = match.group(1)

    # Fallback: numeric rating text
    text = listing_soup.get_text(" ")
    match = re.search(r"(\d+(\.\d+)?)\s*star", text, re.IGNORECASE)
    if "yellowpages" not in ratings and match:
        ratings["yellowpages"] = match.group(1)

    return ratings

def extract_categories(listing_soup: BeautifulSoup) -> List[str]:
    """
    Extract business categories / tags.
    """
    categories: List[str] = []
    categories_block = listing_soup.find("div", class_="categories")
    if categories_block:
        for a in categories_block.find_all("a"):
            val = clean_text(a.get_text())
            if val:
                categories.append(val)

    if not categories:
        # Fallback: look for <span class="category"> etc.
        for span in listing_soup.find_all(
            ["span", "a"],
            class_=lambda c: c and "category" in c,
        ):
            val = clean_text(span.get_text())
            if val:
                categories.append(val)

    # Deduplicate
    return sorted(set(categories))

def extract_hours(listing_soup: BeautifulSoup) -> List[Dict[str, str]]:
    """
    Extract opening hours as a list of {day, time}.
    """
    hours: List[Dict[str, str]] = []

    hours_block = listing_soup.find("div", class_="open-hours") or listing_soup.find(
        "div",
        class_=lambda c: c and "hours" in c,
    )
    if not hours_block:
        return hours

    for li in hours_block.find_all("li"):
        text = clean_text(li.get_text(" "))
        if not text:
            continue
        # Split "Mon - Fri: 9:00 am - 6:00 pm" into day and time
        if ":" in text:
            day_part, time_part = text.split(":", 1)
            hours.append({"day": clean_text(day_part), "time": clean_text(time_part)})
        else:
            hours.append({"day": "", "time": text})
    return hours

def extract_gallery_urls(listing_soup: BeautifulSoup) -> List[str]:
    """
    Extract gallery image URLs if present.
    """
    urls: List[str] = []
    for img in listing_soup.find_all("img"):
        src = img.get("src") or img.get("data-src")
        if not src:
            continue
        if "ypcdn.com" in src or "yellowpages" in src:
            urls.append(src)
    return list(dict.fromkeys(urls))  # dedupe while preserving order

def extract_reviews(listing_soup: BeautifulSoup) -> List[Dict[str, Any]]:
    """
    Extract basic reviews that might be embedded in listing (if present).
    """
    reviews: List[Dict[str, Any]] = []

    review_blocks = listing_soup.find_all(
        "div",
        class_=lambda c: c and ("review" in c or "ratings" in c),
    )
    for rb in review_blocks:
        reviewer = rb.find("span", class_="reviewer")
        date = rb.find("span", class_="date") or rb.find("span", class_="review-date")
        rating = rb.find(
            attrs={"aria-label": re.compile(r"\d+(\.\d+)? star rating")},
        )
        content = rb.find("p") or rb

        rating_value = 0
        if rating and rating.has_attr("aria-label"):
            match = re.search(r"(\d+(\.\d+)?)", rating["aria-label"])
            if match:
                try:
                    rating_value = float(match.group(1))
                except ValueError:
                    rating_value = 0

        reviews.append(
            {
                "reviewer": clean_text(reviewer.get_text()) if reviewer else "",
                "reviewDate": clean_text(date.get_text()) if date else "",
                "reviewRating": rating_value,
                "reviewContent": clean_text(content.get_text(" ")),
            }
        )

    # Deduplicate by reviewer + content
    deduped: List[Dict[str, Any]] = []
    seen_keys = set()
    for r in reviews:
        key = (r["reviewer"], r["reviewContent"])
        if key in seen_keys:
            continue
        seen_keys.add(key)
        deduped.append(r)
    return deduped

def extract_general_info(listing_soup: BeautifulSoup) -> str:
    """
    Extract a general description of the business if present.
    """
    desc_tag = listing_soup.find("p", class_="body-text") or listing_soup.find(
        "div",
        class_="general-info",
    )
    if desc_tag:
        return clean_text(desc_tag.get_text(" "))

    # Fallback: a short snippet near listing header
    header = listing_soup.find("h2") or listing_soup.find("h3")
    if header and header.find_next_sibling("p"):
        return clean_text(header.find_next_sibling("p").get_text(" "))

    return ""

def to_pretty_json(data: Any) -> str:
    """
    Convenience helper for pretty-printing JSON, useful inside other modules.
    """
    return json.dumps(data, indent=2, ensure_ascii=False)