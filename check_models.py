import os
import sys

# Provide the path for mian folder - will check only sub-folders not the whole tree ─────────────────────────────────────────────────────────────────────────────

RED    = "\033[91m"
YELLOW = "\033[93m"
GREEN  = "\033[92m"
RESET  = "\033[0m"

def check_folder(folder_path: str):
    """Returns: file not found, empty file, OK."""
    try:
        entries = os.listdir(folder_path)
    except PermissionError:
        return "error", [], "File error - Can't access"

    safetensors = [
        f for f in entries
        if f.lower().endswith(".safetensors")
    ]

    if not safetensors:
        return "missing", [], None

    results = []
    has_empty = False
    for fname in safetensors:
        fpath = os.path.join(folder_path, fname)
        size = os.path.getsize(fpath)
        results.append((fname, size))
        if size == 0:
            has_empty = True

    status = "empty" if has_empty else "ok"
    return status, results, None


def main():
    print("Provide main folder to check sub-folders:")
    SEARCH_DIR = input(">>> ").strip().strip('"').strip("'")
    if not SEARCH_DIR:
        print(f"{RED}Error: no path provided.{RESET}")
        sys.exit(1)
    if not os.path.isdir(SEARCH_DIR):
        print(f"{RED}Error: invalid path: {SEARCH_DIR}{RESET}")
        sys.exit(1)

    subfolders = sorted([
        f for f in os.scandir(SEARCH_DIR)
        if f.is_dir()
    ], key=lambda e: e.name.lower())

    if not subfolders:
        print("No sub-folders to check.")
        return

    missing = []
    empty   = []
    ok      = []
    errors  = []

    for entry in subfolders:
        status, files, err = check_folder(entry.path)
        if status == "missing":
            missing.append(entry.name)
        elif status == "empty":
            empty.append((entry.name, files))
        elif status == "ok":
            ok.append((entry.name, files))
        elif status == "error":
            errors.append((entry.name, err))

    # ── Raport ───────────────────────────────────────────────────────────────
    total = len(subfolders)
    print(f"\n{'='*60}")
    print(f"  Checked sub-folders: {total}")
    print(f"  {GREEN}OK (file present > 0B):{RESET}        {len(ok)}")
    print(f"  {YELLOW}No .safetensors file found:{RESET}   {len(missing)}")
    print(f"  {RED}Empty file (0 bytes):{RESET}      {len(empty)}")
    if errors:
        print(f"  {RED}Access Error:{RESET}             {len(errors)}")
    print(f"{'='*60}\n")

    if missing:
        print(f"{YELLOW}── MISSING .safetensors ─────────────────────────────{RESET}")
        for name in missing:
            print(f"  {YELLOW}[BRAK]{RESET} {name}")
        print()

    if empty:
        print(f"{RED}── EMPTY FILE (0 bytes) ────────────────────────────────{RESET}")
        for name, files in empty:
            print(f"  {RED}[EMPTY]{RESET} {name}")
            for fname, size in files:
                marker = f"{RED}0 B{RESET}" if size == 0 else f"{size:,} B"
                print(f"         └─ {fname}  ({marker})")
        print()

    if errors:
        print(f"{RED}── ACCESS ERROR ────────────────────────────────────────{RESET}")
        for name, err in errors:
            print(f"  {RED}[ACCESS ERROR]{RESET} {name}: {err}")
        print()

    if not missing and not empty:
        print(f"{GREEN}ALL OK — every sub-folder has .safetensors > 0 bytes.{RESET}\n")
    else:
        problem_count = len(missing) + len(empty)
        print(f"{RED}Found {problem_count} sub-folders with Errors.{RESET}\n")
        print("You should try downloading those model ID's again.\n")


if __name__ == "__main__":
    main()