import os
from datetime import datetime


def find_and_log_empty_files(start_path, extension, log_name="empty_files_log.txt"):
    if not extension.startswith('.'):
        extension = '.' + extension

    print(f"Scanning: {start_path} for empty {extension} files...")

    found = []
    for root, dirs, files in os.walk(start_path):
        for file in files:
            if file.lower().endswith(extension.lower()):
                full_path = os.path.join(root, file)
                try:
                    if os.path.getsize(full_path) == 0:
                        found.append(full_path)
                        print(f"Found: {file}")
                except OSError:
                    continue

    # Save to log file
    try:
        with open(log_name, "w", encoding="utf-8") as f:
            f.write(f"REPORT DATE: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Scanned folder: {start_path}\n")
            f.write(f"Extension: {extension}\n")
            f.write("-" * 50 + "\n")
            if found:
                for path in found:
                    f.write(path + "\n")
            else:
                f.write("No empty files with this extension were found.\n")

        print(f"\nDone! Results saved to: {os.path.abspath(log_name)}")
    except Exception as e:
        print(f"Error writing log: {e}")


# --- CONFIGURATION ---
folder_to_search = input("Enter the folder path to search: ").strip()
extension_to_find = '.safetensors'

find_and_log_empty_files(folder_to_search, extension_to_find)

