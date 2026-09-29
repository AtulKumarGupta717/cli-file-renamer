#!/usr/bin/env python3
"""
Smart Batch File Renamer
A robust CLI tool for batch renaming files safely with complete error handling.
"""

import argparse
import sys
from pathlib import Path


def format_error(message: str) -> str:
    """Formats standard error outputs."""
    return f"Error: {message}"


def batch_rename(directory_path: str, prefix: str, extension: str = None, dry_run: bool = False) -> None:
    dir_path = Path(directory_path)

    # 1. Validation: Directory exists
    if not dir_path.exists():
        print(format_error(f"The directory '{directory_path}' does not exist."), file=sys.stderr)
        sys.exit(1)

    # 2. Validation: Path is indeed a folder
    if not dir_path.is_dir():
        print(format_error(f"'{directory_path}' is not a valid directory."), file=sys.stderr)
        sys.exit(1)

    try:
        # Get files only
        files = [f for f in dir_path.iterdir() if f.is_file()]

        # Filter by extension if specified
        if extension:
            clean_ext = extension if extension.startswith('.') else f".{extension}"
            files = [f for f in files if f.suffix.lower() == clean_ext.lower()]

        if not files:
            print(f"No matching files found in '{directory_path}'.")
            sys.exit(0)

        print(f"Found {len(files)} matching file(s) in '{directory_path}'.")
        if dry_run:
            print("--- [DRY RUN MODE ENABLED: No files will be changed] ---\n")

        renamed_count = 0
        skipped_count = 0

        for idx, file_path in enumerate(sorted(files), start=1):
            new_filename = f"{prefix}_{idx:03d}{file_path.suffix}"
            new_path = dir_path / new_filename

            # Skip target collision
            if new_path.exists() and new_path != file_path:
                print(f"Skipped: '{file_path.name}' -> Target '{new_filename}' already exists.", file=sys.stderr)
                skipped_count += 1
                continue

            try:
                if dry_run:
                    print(f"[Would Rename] {file_path.name} -> {new_filename}")
                else:
                    file_path.rename(new_path)
                    print(f"Renamed: {file_path.name} -> {new_filename}")
                renamed_count += 1
            except PermissionError:
                print(format_error(f"Permission denied for '{file_path.name}'."), file=sys.stderr)
                skipped_count += 1
            except Exception as e:
                print(format_error(f"Failed to rename '{file_path.name}': {e}"), file=sys.stderr)
                skipped_count += 1

        action_word = "Would rename" if dry_run else "Successfully renamed"
        print(f"\nSummary: {action_word} {renamed_count} file(s). Skipped: {skipped_count}.")
        sys.exit(0)

    except PermissionError:
        print(format_error(f"Permission denied to access folder '{directory_path}'."), file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(format_error(f"An unexpected error occurred: {e}"), file=sys.stderr)
        sys.exit(1)


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="file-renamer",
        description="Smart Batch File Renamer — Safely rename multiple files in a folder.",
        epilog="Example: python renamer.py ./my_photos vacation -e jpg --dry-run"
    )

    parser.add_argument("directory", help="Path to the directory containing files")
    parser.add_argument("prefix", help="Prefix for new filenames (e.g., 'photo' -> 'photo_001.jpg')")
    parser.add_argument("-e", "--extension", help="Filter by file extension (e.g., 'png', 'txt')", default=None)
    parser.add_argument("--dry-run", action="store_true", help="Simulate renaming without modifying files")

    args = parser.parse_args()

    # Graceful handling of Ctrl + C (KeyboardInterrupt)
    try:
        batch_rename(args.directory, args.prefix, args.extension, args.dry_run)
    except KeyboardInterrupt:
        print("\n\nProcess interrupted cleanly by user (Ctrl+C). Exiting.", file=sys.stderr)
        sys.exit(130)


if __name__ == "__main__":
    main()