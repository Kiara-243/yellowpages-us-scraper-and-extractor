import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Any, Dict, List

# Ensure local src directory is importable
CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

from extractors.yp_parser import fetch_businesses
from outputs.exporters import export_to_json, export_to_csv
from config_loader import load_settings  # defined below in this file

def configure_logging(verbose: bool = False) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    )

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Yellowpages US Scraper and Extractor - CLI runner"
    )
    parser.add_argument(
        "--input",
        type=str,
        default=str(CURRENT_DIR.parent / "data" / "inputs.sample.json"),
        help="Path to JSON input configuration file.",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=str(CURRENT_DIR.parent / "data" / "output.json"),
        help="Path to output file (JSON or CSV based on config).",
    )
    parser.add_argument(
        "--settings",
        type=str,
        default=str(CURRENT_DIR / "config" / "settings.example.json"),
        help="Path to settings JSON file.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose (debug) logging.",
    )
    return parser.parse_args()

def load_input_config(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Input configuration file not found: {path}")
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

def run_scraper(
    input_cfg: Dict[str, Any],
    settings: Dict[str, Any],
) -> List[Dict[str, Any]]:
    keywords = input_cfg.get("keywords") or []
    locations = input_cfg.get("locations") or []
    max_results_per_keyword = int(input_cfg.get("max_results_per_keyword", 50))
    sort_by = input_cfg.get("sort_by", "best_match")

    if not keywords or not locations:
        raise ValueError("Input configuration must define non-empty 'keywords' and 'locations'.")

    logging.info("Starting Yellowpages scraping run")
    logging.info("Keywords: %s", keywords)
    logging.info("Locations: %s", locations)
    logging.info("Max results per keyword: %s", max_results_per_keyword)
    logging.info("Sort by: %s", sort_by)

    all_records: List[Dict[str, Any]] = []
    for keyword in keywords:
        for location in locations:
            logging.info("Fetching businesses for keyword='%s', location='%s'", keyword, location)
            try:
                records = fetch_businesses(
                    keyword=keyword,
                    location=location,
                    max_results=max_results_per_keyword,
                    sort_by=sort_by,
                    settings=settings,
                )
                logging.info("Fetched %d records for '%s' in '%s'", len(records), keyword, location)
                all_records.extend(records)
            except Exception as exc:  # noqa: BLE001
                logging.exception(
                    "Failed to fetch businesses for keyword='%s', location='%s': %s",
                    keyword,
                    location,
                    exc,
                )
    logging.info("Total records collected: %d", len(all_records))
    return all_records

def write_output(
    records: List[Dict[str, Any]],
    output_path: Path,
    output_format: str,
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if output_format.lower() == "csv":
        export_to_csv(records, output_path)
    else:
        export_to_json(records, output_path)
    logging.info("Output written to %s (%s)", output_path, output_format.upper())

def load_settings_with_defaults(path: Path) -> Dict[str, Any]:
    try:
        return load_settings(path)
    except FileNotFoundError:
        logging.warning(
            "Settings file not found at %s, using built-in defaults.",
            path,
        )
        # Minimal sensible defaults
        return {
            "base_url": "https://www.yellowpages.com",
            "user_agent": "YellowpagesScraperBot/1.0 (+https://bitbash.dev)",
            "timeout_seconds": 15,
            "max_pages_per_search": 5,
            "retry_attempts": 2,
            "retry_backoff_seconds": 1.5,
        }

def main() -> None:
    args = parse_args()
    configure_logging(verbose=args.verbose)

    input_path = Path(args.input).resolve()
    output_path = Path(args.output).resolve()
    settings_path = Path(args.settings).resolve()

    logging.debug("Input config path: %s", input_path)
    logging.debug("Output path: %s", output_path)
    logging.debug("Settings path: %s", settings_path)

    input_cfg = load_input_config(input_path)
    settings = load_settings_with_defaults(settings_path)

    output_format = input_cfg.get("output_format", "json").lower()
    if output_format not in {"json", "csv"}:
        logging.warning(
            "Unsupported output_format '%s' in input config; falling back to JSON.",
            output_format,
        )
        output_format = "json"

    records = run_scraper(input_cfg=input_cfg, settings=settings)
    write_output(records, output_path, output_format)

# Lightweight settings loader kept in same file to avoid extra modules
def load_settings(path: Path) -> Dict[str, Any]:
    """
    Load scraper settings from a JSON file.
    """
    if not path.exists():
        raise FileNotFoundError(f"Settings file not found: {path}")
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

if __name__ == "__main__":
    main()