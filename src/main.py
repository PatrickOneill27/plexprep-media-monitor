# PlexPrep Media Monitor
# This script scans the media library, detects files,
# identifies media type, checks naming, and logs results.

from pathlib import Path
from datetime import datetime
import re
import csv

# Root folder
media_folder = Path("test_media")

# Log file path
log_file = Path("data/logs.csv")


def check_naming(file_name, media_type):
    """
    Checks if file follows basic Plex naming rules
    """

    if media_type == "TV Show":
        # Looks for S01E01 pattern
        if re.search(r"S\d{2}E\d{2}", file_name, re.IGNORECASE):
            return "valid"
        return "needs_rename"

    elif media_type == "Movie":
        # Looks for year like (1999) or 1999
        if re.search(r"\d{4}", file_name):
            return "valid"
        return "needs_rename"

    return "unknown"


def log_event(file_path, media_type, status):
    """
    Writes scan results to CSV file
    """
    with open(log_file, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now(),
            file_path,
            media_type,
            status,
            "scanned"
        ])


def scan_media_library():
    """
    Scans the media library, checks file naming,
    logs results, and returns scan data.
    """

    results = []

    print("Scanning media library...\n")

    for file in media_folder.rglob("*"):
        if file.is_file():

            # Detect type
            path_parts = [part.lower() for part in file.parts]

            if "movies" in path_parts:
                media_type = "Movie"
            elif "tv" in path_parts:
                media_type = "TV Show"
            else:
                media_type = "Unknown"

            # Check naming
            status = check_naming(file.name, media_type)

            # Store result for Flask/API use
            result = {
                "file": str(file),
                "type": media_type,
                "status": status
            }

            results.append(result)

            # Output result to terminal
            print(f"[{media_type}] {file} -> {status}")

            # Log result
            log_event(str(file), media_type, status)

    print("\nScan complete.")

    return results


if __name__ == "__main__":
    scan_media_library()
