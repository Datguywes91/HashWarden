# HashWarden
HashWarden is a lightweight, pure-Python File Integrity Monitor (FIM) designed to detect unauthorized changes to critical files and directories. Whether you are auditing server configurations, monitoring a homelab environment, or exploring the mechanics of cryptographic hashing, this tool provides a simple and effective early-warning system for file tampering.

At its core, the script scans a target directory and calculates the SHA-256 checksum for every file, establishing a known-good baseline. During active monitoring, it continually recalculates the hashes and compares them against this baseline. Because SHA-256 is highly sensitive, altering even a single byte of data completely changes the resulting hash. The script instantly identifies these deviations, alerting you to newly added, modified, or maliciously deleted files.

Built entirely with Python's standard library, the tool requires no external dependencies and is ready to run right out of the box. It is designed to be memory-efficient—processing large files in chunks to prevent crashes—and features an optional continuous monitoring loop. This project is perfect for security enthusiasts, system administrators, and anyone looking to maintain strict visibility over their file systems.


## Features
* **SHA-256 Hashing:** Uses secure cryptographic hashing to detect even single-byte alterations.
* **Memory Efficient:** Reads files in 64KB chunks, allowing it to safely hash massive files (like ISOs or log archives) without crashing.
* **Continuous Monitoring:** Includes an optional interval mode to run silently in the background and check for changes periodically.
* **Zero Dependencies:** Built entirely with Python's standard library. No `pip install` required.

## Installation

Since the script uses only native Python libraries, setup is incredibly simple. Just clone the repository and run it.

```bash
git clone [https://github.com/Datguywes91/file-integrity-monitor.git](https://github.com/YOUR-USERNAME/file-integrity-monitor.git)
cd file-integrity-monitor

Usage Guide

The tool operates in two primary modes: update (to create the baseline) and check (to verify against it).
1. Establish the Baseline

Before you can monitor files, you need to calculate their known-good hashes. Point the script at your target directory using --mode update.
Bash

python integrity_checker.py /path/to/target/directory --mode update

This creates a baseline.json file in your current working directory containing the file paths and their SHA-256 hashes.
2. Run an Integrity Check (One-off)

To verify your files haven't been tampered with, run the script in check mode.
Bash

python integrity_checker.py /path/to/target/directory --mode check

3. Continuous Monitoring

To leave the script running as an active monitor, add the --interval flag followed by the number of seconds between checks.
Bash

# Checks the directory every 5 minutes (300 seconds)
python integrity_checker.py /path/to/target/directory --mode check --interval 300

Example Output

When a modification is detected, the script outputs a clear, timestamped alert to the console:
Plaintext

[2026-08-16 14:30:00] [!] ALERT: Modifications detected!
  New files:
    - /target/directory/suspicious_script.sh
  Modified files:
    - /target/directory/config.yaml
  Deleted files:
    - /target/directory/old_logs.txt
--------------------------------------------------
