# Smart Batch File Renamer (CLI Tool)

A production-ready command-line Python utility to safely rename files in bulk. Built with robust error handling, input validation, and dry-run preview capabilities.

## Features
- **Clean Error Handling:** User-friendly error messages without raw python tracebacks.
- **Dry-Run Mode:** Preview changes safely before applying them using `--dry-run`.
- **Extension Filtering:** Target only specific file extensions (e.g., `.jpg`, `.pdf`).
- **Conflict Prevention:** Avoids overwriting existing files automatically.
- **Graceful Termination:** Standardized exit codes (`0` for success, `1` for error, `130` for user cancellation via `Ctrl+C`).

## Installation & Requirements
- Python 3.7+ (No external third-party libraries required).

## Usage

```bash
python renamer.py <directory_path> <prefix> [options]