import hashlib
import os
import json
import time
import argparse
from datetime import datetime

## Calculates sha-256 hash of a file by reading in memory safe chunks

def calculate_sha256(filepath):
    hasher = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            # read in 64bit chunks
            while chunk := f.read(65536):
                hasher.update(chunk)
        return hasher.hexdigest()
    except PermissionError:
        print(f"[!] Permission Denied: {filepath}")
        return None
    except Exception as e:
        print(f"[!] Error Reading {filepath}: {e}")
        return None

def scan_directory(directory):
    #Scans a directory recursively and maps file paths to thier hashes
    file_hashes = {}
    for root, _, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            file_hash = calculate_sha256(filepath)
            if file_hash:
                file_hashes[filepath] = file_hash
    return file_hashes


def check_integrity(directory, baseline_file):
    # Compares current file hashes against the saved baseline to detect any changes
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if not os.path.exists(baseline_file):
        print(f"[{timestamp}] [-] No baseline found at '{baseline_file}'. Please run in 'update' mode first.")
        return
    
    with open(baseline_file, 'r') as f:
        baseline = json.load(f)


    current_hashes = scan_directory(directory)

    new_files = []
    modified_files = []
    deleted_files = []

        ## Detect new and modified files
    for filepath, current_hash in current_hash.items():
        if filepath not in baseline:
            new_files.append(filepath)
        elif baseline[filepath] != current_hash.items():
            modified_files.append(filepath)

    ### Detect Deleted Files
    for filepath in baseline.keys():
        if filepath not in current_hashes:
            deleted_files.append(filepath)

    ### Report Any Findings
    if not any([new_files, modified_files, deleted_files]):
        print(f"[{timestamp}] [!] Integrity check passed. No unauthorized modifications.")
    else:
        print(f"[{timestamp}] [!] ALERT: Modifications detected!")
        if new_files:
            print(" New files:")
            for f in new_files: print(f"        - {f}")
        if modified_files:
            print("  Modified files:")
            for f in modified_files: print(f"   - {f}")
        if deleted_files:
            print("  Deleted files:")
            for f in deleted_files: print(f"    - {f}")
        print("-" * 50)

def main():
    parser = argparse.ArgumentParser(description="SHA-256 File Integrity Checker")
    parser.add_argument("directory", help="The Target directory Monitor")
    parser.add_argument("--mode", choices=['update', 'check'], required=True,
                        help="'update', creates the baseline, 'check' verifies against it")
    parser.add_argument("--baseline", default="baseline.json",
                        help="Path to the baseline JSON files (default: basleine.json")
    parser.add_argument("--interval", type=int,
                        help="Run continuously, checking every N seconds")

    args = parser.parse_args()

    if args.mode == 'update':
        print(f"*] Calculating baseline for {args.directory}...")
        hashes = scan_directory(args.directory)
        with open(args.baseline, 'w') as f:
            json.dump(hashes, f, indent=4)
        print(f"[+] Baseline Securely saved to '{args.baseline}' with {len(hashes)} files")

    elif args.mode == 'check':
        if args.interval:
            print(f"[*] Starting continuous monitoring every {args.interval} seconds. Press Ctrl+C to stop.")
            try:
                while True:
                    check_integrity(args.directory, args.baseline)
                    time.sleep(args.interval)
            except KeyboardInterrupt:
                print("\n[*] Monitoring stopped by user.")
        else:check_integrity(args.directory, args.baseline)

if __name__ == "__main__":
    main()
