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


def detect_subtitle_language(filename):
    """
    Detects subtitle language from filename tags.
    """

    name = filename.lower()

    language_map = {
        ".en.": "English",
        ".eng.": "English",
        ".english.": "English",
        ".pt.": "Portuguese",
        ".por.": "Portuguese",
        ".portuguese.": "Portuguese",
        ".es.": "Spanish",
        ".spa.": "Spanish",
        ".spanish.": "Spanish"
    }

    for code, language in language_map.items():
        if code in name:
            return language

    return "Unknown"


def check_naming(file_name, media_type):
    """
    Checks if file follows basic Plex naming rules.
    """

    if media_type == "Subtitle":
        if re.search(r"S\d{2}E\d{2}", file_name, re.IGNORECASE):
            return "subtitle_matched"
        return "manual_review"

    if media_type == "TV Show":
        if re.search(r"S\d{2}E\d{2}", file_name, re.IGNORECASE):
            return "valid"
        return "needs_rename"

    if media_type == "Movie":
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
        "total_gb": round(total / (1024 ** 3), 2),
        "used_gb": round(used / (1024 ** 3), 2),
        "free_gb": round(free / (1024 ** 3), 2),
        "usage_percent": round((used / total) * 100, 1)
    }


def fetch_tv_metadata(show_name, season, episode):
    """
    Fetches TV episode metadata from TVMaze API using show name,
    season number, and episode number.
    """

    try:
        search_url = f"https://api.tvmaze.com/singlesearch/shows?q={show_name}"
        search_response = requests.get(search_url, timeout=5)

        if search_response.status_code != 200:
            return None

        show_data = search_response.json()
        show_id = show_data["id"]

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
    """

    if media_type == "Movie":
        try:
            movie_folder = file_path.parts[-2]
            extension = file_path.suffix
            suggested_name = movie_folder.replace(" ", ".") + extension

            if suggested_name.lower() == file_path.name.lower():
                return ""

            return suggested_name

        except IndexError:
            return ""

    if media_type == "Subtitle":
        return ""

    if media_type != "TV Show":
        return ""

    try:
        show_name = file_path.parts[-3]
        season_folder = file_path.parts[-2]
        extension = file_path.suffix

        season_match = re.search(r"\d+", season_folder)

        if not season_match:
            return ""

        season = int(season_match.group())

        current_match = re.search(
            r"S(\d{2})E(\d{2})",
            file_path.name,
            re.IGNORECASE
        )

        if current_match:
            current_episode = int(current_match.group(2))

            existing_episode_check = fetch_tv_metadata(
                show_name,
                season,
                current_episode
            )

            if not existing_episode_check:
                return "MANUAL_REVIEW_REQUIRED"

            return ""

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
                    highest_episode = max(highest_episode, episode_num)

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

        if suggested_name.lower() == file_path.name.lower():
            return ""

        return suggested_name

    except IndexError:
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
            old_path = Path(item["real_file"])
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

            # Subtitle files: detect language and avoid automatic renaming
            if media_type == "Subtitle":
                subtitle_language = detect_subtitle_language(file.name)
                manual_review = subtitle_language == "Unknown"

                if "movies" in path_parts:
                    movie_folder = file.parts[-2]

                    metadata = {
                        "message": f"Subtitle for movie: {movie_folder}",
                        "subtitle_language": subtitle_language,
                        "manual_review": manual_review
                    }

                    status = "subtitle_matched"

                    if manual_review:
                        metadata["message"] = (
                            "Language not detected - manual review required"
                        )
                        status = "subtitle_language_unknown"

                else:
                    match = re.search(
                        r"S(\d{2})E(\d{2})",
                        file.name,
                        re.IGNORECASE
                    )

                    if match:
                        season = int(match.group(1))
                        episode = int(match.group(2))

                        show_name = (
                            file.parts[-3]
                            .replace(".", " ")
                            .replace("_", " ")
                        )

                        subtitle_metadata = fetch_tv_metadata(
                            show_name,
                            season,
                            episode
                        )

                        if subtitle_metadata:
                            episode_title = subtitle_metadata.get(
                                "title",
                                f"S{season:02d}E{episode:02d}"
                            )

                            metadata = {
                                "message": f"Subtitle for: {episode_title}",
                                "subtitle_language": subtitle_language,
                                "manual_review": manual_review,
                                "episode_title": episode_title,
                                "season": season,
                                "episode": episode
                            }

                        else:
                            metadata = {
                                "message": "Subtitle metadata unavailable",
                                "subtitle_language": subtitle_language,
                                "manual_review": manual_review,
                                "season": season,
                                "episode": episode
                            }

                        status = "subtitle_matched"

                        if manual_review:
                            metadata["message"] = (
                                "Language not detected - manual review required"
                            )
                            status = "subtitle_language_unknown"

                    else:
                        metadata = {
                            "message": (
                                "Language not detected - manual review required"
                            ),
                            "subtitle_language": subtitle_language,
                            "manual_review": True
                        }

                        status = "subtitle_language_unknown"

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

                    show_name = (
                        file.parts[-3]
                        .replace(".", " ")
                        .replace("_", " ")
                    )

                    metadata = fetch_tv_metadata(
                        show_name,
                        season,
                        episode
                    )

                    # If metadata does not exist,
                    # the episode likely exceeds the official episode count.
                    if metadata is None:
                        status = "manual_review"

            # Movie metadata
            elif media_type == "Movie" and status == "valid":

                movie_folder = file.parts[-2]

                metadata = {
                    "message": movie_folder
                }

            suggested_name = ""

            # Rename suggestions are only generated for TV/movie media files.
            # Subtitle files are checked for language/manual review only.
            if media_type != "Subtitle" and status in [
                "needs_rename",
                "manual_review"
            ]:
                suggested_name = generate_rename_suggestion(
                    file,
                    media_type,
                    suggested_tracker
                )

                # Prevent unsafe rename suggestions
                if suggested_name == "MANUAL_REVIEW_REQUIRED":
                    status = "manual_review"
                    suggested_name = ""

            result = {
                "file": str(file).replace("test_media", ""),
                "real_file": str(file),
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
    