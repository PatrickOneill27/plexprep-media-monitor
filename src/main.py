# This script scans the simulated media library folders, detects media files, and outputs their names.
from pathlib import Path  # Used for handling folder paths and scanning directories

# Define the root folder containing the simulated media library
media_folder = Path("test_media")

# Display startup message
print("Scanning media library...\n")

# Recursively scan all files inside the media folder
for file in media_folder.rglob("*"):
    # Check if the current path is a file
    if file.is_file():
         # Determine media type based on folder path
        if "movies" in file.parts:
            media_type = "Movie"
        elif "tv" in file.parts:
            media_type = "TV Show"
        else:
            media_type = "Unknown"
        # Output the detected file name
        print(f"Detected file: {file.name}")

# Display completion message
print("\nScan complete.")
