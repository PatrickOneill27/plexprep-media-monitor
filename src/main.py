from pathlib import Path

media_folder = Path("test_media")

print("Scanning media library...\n")

for file in media_folder.rglob("*"):
    if file.is_file():
        print(f"Detected file: {file.name}")

print("\nScan complete.")
