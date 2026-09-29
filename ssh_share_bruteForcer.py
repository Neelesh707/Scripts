#!/usr/bin/env python3

import subprocess
import os

# Define target and wordlist location
TARGET = "target"
WORDLIST = "/root/Desktop/wordlists/shares.txt"

# Check if wordlist exists
if not os.path.isfile(WORDLIST):
    print(f"Wordlist not found: {WORDLIST}")
    exit(1)

# Open wordlist and test each share
with open(WORDLIST, "r") as file:
    for share in file:
        share = share.strip()

        if not share:
            continue

        print(f"Testing share: {share}")

        command = [
            "smbclient",
            f"//{TARGET}/{share}",
            "-N",
            "-c",
            "ls"
        ]

        result = subprocess.run(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        if result.returncode == 0:
            print(f"[+] Anonymous access allowed for: {share}")
        else:
            print(f"[-] Access denied for: {share}")
