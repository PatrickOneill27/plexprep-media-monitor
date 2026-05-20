# PlexPrep Media Monitor
# This script scans the media library, detects files,
# identifies media type, checks naming, logs results,
# checks storage usage, and suggests Plex-friendly rename options.
import requests
from pathlib import Path
from datetime import datetime
import re
import csv
import shutil

# Root folder containing the simulated media library
media_folder = Path("test_media")

# Log file path
log_file = Path("data/logs.csv")
SUBTITLE_EXTENSIONS = {".srt"}

def check_naming(file_name, media_type):
    """
    Checks if file follows basic Plex naming rules.
    """
    if media_type == "Subtitle":
        if re.search(r"S\d{2}E\d{2}", file_name, re.IGNORECASE):
            return "subtitle_matched"
        return "manual_review"
    
    if media_type == "TV Show":
        # Looks for S01E01 pattern
        if re.search(r"S\d{2}E\d{2}", file_name, re.IGNORECASE):
            return "valid"
        return "needs_rename"

    elif media_type == "Movie":
        # Looks for year like 1999 or (1999)
        if re.search(r"\d{4}", file_name):
            return "valid"
        return "needs_rename"

    return "unknown"


def log_event(file_path, media_type, status):
    """
    Writes scan results to CSV file.
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


def get_storage_stats():
    """
    Returns storage usage statistics.
    """

    total, used, free = shutil.disk_usage(".")

    return {
        "total_gb": round(total / (1024**3), 2),
        "used_gb": round(used / (1024**3), 2),
        "free_gb": round(free / (1024**3), 2),
        "usage_percent": round((used / total) * 100, 1)
    }

def fetch_tv_metadata(show_name, season, episode):
    """
    Fetches TV episode metadata from TVMaze API using show name,
    season number, and episode number.
    """

    try:
        # First find the show
        search_url = f"https://api.tvmaze.com/singlesearch/shows?q={show_name}"
        search_response = requests.get(search_url, timeout=5)

        if search_response.status_code != 200:
            return None

        show_data = search_response.json()
        show_id = show_data["id"]

        # Then fetch exact episode by season and episode number
        episode_url = (
            f"https://api.tvmaze.com/shows/{show_id}/episodebynumber"
            f"?season={season}&number={episode}"
        )

        episode_response = requests.get(episode_url, timeout=5)

        if episode_response.status_code != 200:
            return None

        episode_data = episode_response.json()

        return {
            "title": episode_data.get("name", "Unknown Title"),
            "airdate": episode_data.get("airdate", "Unknown airdate"),
            "runtime": episode_data.get("runtime", "Unknown runtime")
        }

    except Exception:
        return None

def generate_rename_suggestion(file_path, media_type, suggested_tracker):
    """
    Generates a Plex-friendly rename suggestion.

    For TV shows, it uses the show folder, season folder,
    and next available episode number.

    For movies, it uses the movie folder name.
    """

    # Movie rename suggestions
    if media_type == "Movie":
        try:
            movie_folder = file_path.parts[-2]
            extension = file_path.suffix

            suggested_name = movie_folder.replace(" ", ".") + extension

            return suggested_name

        except IndexError:
            return ""

    # TV rename suggestions
    if media_type != "TV Show":
        return ""

    parts = file_path.parts

    try:
        show_name = parts[-3]
        season_folder = parts[-2]
        extension = file_path.suffix

        season_match = re.search(r"\d+", season_folder)

        if not season_match:
            return ""

        season = int(season_match.group())
        season_path = file_path.parent
        tracker_key = str(season_path)

        highest_episode = 0

        for existing_file in season_path.iterdir():
            if existing_file.is_file():
                episode_match = re.search(
                    r"S\d{2}E(\d{2})",
                    existing_file.name,
                    re.IGNORECASE
                )

                if episode_match:
                    episode_num = int(episode_match.group(1))

                    if episode_num > highest_episode:
                        highest_episode = episode_num

        if tracker_key not in suggested_tracker:
            suggested_tracker[tracker_key] = highest_episode

        suggested_tracker[tracker_key] += 1
        next_episode = suggested_tracker[tracker_key]

        episode_check = fetch_tv_metadata(
            show_name,
            season,
            next_episode
        )

        if not episode_check:
            return "MANUAL_REVIEW_REQUIRED"

        suggested_name = (
            f"{show_name.replace(' ', '.')}"
            f".S{season:02d}E{next_episode:02d}"
            f"{extension}"
        )

        return suggested_name

    except IndexError:
        return ""

    return ""

def apply_safe_renames():
    """
    Safely renames files that need renaming using generated suggestions.
    Only files with valid rename suggestions are changed.
    """

    results = scan_media_library()
    renamed_files = []

    for item in results:
        if item["status"] == "needs_rename" and item["suggested_name"]:
            old_path = Path(item["file"])
            new_path = old_path.parent / item["suggested_name"]

            if old_path.exists() and not new_path.exists():
                old_path.rename(new_path)

                renamed_files.append({
                    "old_file": str(old_path),
                    "new_file": str(new_path),
                    "status": "renamed"
                })

    return renamed_files

def scan_media_library():
    """
    Scans the media library, checks file naming,
    logs results, and returns scan data.
    """

    results = []
    suggested_tracker = {}

    print("Scanning media library...\n")

    for file in media_folder.rglob("*"):
        if file.is_file():

            path_parts = [part.lower() for part in file.parts]

            if file.suffix.lower() in SUBTITLE_EXTENSIONS:
                media_type = "Subtitle"
            elif "movies" in path_parts:
                media_type = "Movie"
            elif "tv" in path_parts:
                media_type = "TV Show"
            else:
                media_type = "Unknown"

            status = check_naming(file.name, media_type)
            metadata = None

            # Subtitle metadata
            if media_type == "Subtitle":

                match = re.search(
                    r"S(\d{2})E(\d{2})",
                    file.name,
                    re.IGNORECASE
                )

                # Movie subtitles
                if "movies" in path_parts:

                    movie_folder = file.parts[-2]

                    metadata = {
                        "message": f"Subtitle for movie: {movie_folder}"
                    }

                # TV subtitles
                elif match:

                    season = int(match.group(1))
                    episode = int(match.group(2))

                    show_name = file.parts[-3].replace(".", " ").replace("_", " ")

                    subtitle_metadata = fetch_tv_metadata(
                        show_name,
                        season,
                        episode
                    )

                    if subtitle_metadata:
                        metadata = {
                            "message": f'Subtitle for: {subtitle_metadata.get("title", "Unknown Episode")}'
                        }

                    else:
                        metadata = {
                            "message": "Subtitle metadata unavailable"
                        }

                # Random subtitles
                else:
                    metadata = {
                        "message": "Subtitle requires manual review"
                    }

            # TV episode metadata
            elif media_type == "TV Show" and status == "valid":

                match = re.search(
                    r"S(\d{2})E(\d{2})",
                    file.name,
                    re.IGNORECASE
                )

                if match:

                    season = int(match.group(1))
                    episode = int(match.group(2))

                    show_name = file.parts[-3].replace(".", " ").replace("_", " ")

                    metadata = fetch_tv_metadata(
                        show_name,
                        season,
                        episode
                    )

            # Movie metadata
            elif media_type == "Movie" and status == "valid":

                metadata = {
                    "message": "No external movie metadata configured"
                }

            suggested_name = ""

            # Rename suggestions
            if status == "needs_rename":

                suggested_name = generate_rename_suggestion(
                    file,
                    media_type,
                    suggested_tracker
                )

                # Prevent invalid episode renaming
                if suggested_name == "MANUAL_REVIEW_REQUIRED":
                    status = "manual_review"
                    suggested_name = ""

            result = {
                "file": str(file),
                "type": media_type,
                "status": status,
                "suggested_name": suggested_name,
                "metadata": metadata
            }

            results.append(result)

            print(f"[{media_type}] {file} -> {status}")

            log_event(str(file), media_type, status)

    print("\nScan complete.")

    results.sort(key=lambda item: item["file"].lower())

    return results

if __name__ == "__main__":
    scan_media_library()
    