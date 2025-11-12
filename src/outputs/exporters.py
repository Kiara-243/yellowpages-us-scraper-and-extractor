import csv
import json
import logging
from pathlib import Path
from typing import Any, Dict, Iterable, List

from extractors.utils_formatting import to_pretty_json

logger = logging.getLogger(__name__)

def export_to_json(records: List[Dict[str, Any]], output_path: Path) -> None:
    """
    Write records to a JSON file.
    """
    logger.debug("Exporting %d records to JSON at %s", len(records), output_path)
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

def _flatten_record(record: Dict[str, Any]) -> Dict[str, Any]:
    """
    Flatten nested dictionaries or lists into JSON strings for CSV export.
    """
    flat: Dict[str, Any] = {}
    for key, value in record.items():
        if isinstance(value, (dict, list)):
            flat[key] = to_pretty_json(value)
        else:
            flat[key] = value
    return flat

def export_to_csv(records: Iterable[Dict[str, Any]], output_path: Path) -> None:
    """
    Export records to a CSV file. Nested structures are JSON-encoded.
    """
    records_list = list(records)
    logger.debug("Exporting %d records to CSV at %s", len(records_list), output_path)
    if not records_list:
        with output_path.open("w", encoding="utf-8", newline="") as f:
            f.write("")  # Create an empty file
        return

    # Collect all field names across records
    fieldnames: List[str] = []
    for rec in records_list:
        for key in rec.keys():
            if key not in fieldnames:
                fieldnames.append(key)

    with output_path.open("w", encoding="utf-8", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for rec in records_list:
            flat = _flatten_record(rec)
            writer.writerow(flat)