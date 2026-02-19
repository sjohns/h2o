#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to process and compare ZIP and HTML files in a directory.

The script compares ZIP files against a reference ZIP file (`packing_slips_correct.zip`) and HTML files against a reference HTML file (`packing_slips_correct.html`). If all ZIP files match the reference, the script terminates. Non-matching ZIP files are processed further, and the remaining HTML files are then processed using BeautifulSoup.
"""

from pathlib import Path
import os
import pandas as pd
from bs4 import BeautifulSoup
import zipfile
import hashlib
import sys

# Default to the script directory so the tool runs from this repository.
# Optional override: H2O_BASE_DIR=/path/to/H2O
directory = Path(os.environ.get('H2O_BASE_DIR', Path(__file__).resolve().parent))

# Initialize lists to hold file names for HTML and ZIP files
files_html = []
files_zip = []

# Collect HTML and ZIP files, excluding the reference files
for file_path in directory.iterdir():
    if file_path.is_file() and file_path.name.startswith('packing_slip'):
        if file_path.suffix == '.html' and file_path.name != 'packing_slips_correct.html':
            files_html.append(file_path.name)
        elif file_path.suffix == '.zip' and file_path.name != 'packing_slips_correct.zip':
            files_zip.append(file_path.name)

# Display the collected files
print("HTML Files to be processed (excluding 'packing_slips_correct.html'):")
print(files_html)
print("ZIP Files to be processed (excluding 'packing_slips_correct.zip'):")
print(files_zip)

# Reference files to compare against
correct_zip_file = 'packing_slips_correct.zip'
correct_html_file = 'packing_slips_correct.html'

def get_zip_file_details(zip_file_path):
    """
    Extracts details from a ZIP file.

    Args:
        zip_file_path (Path): Path to the ZIP file.

    Returns:
        dict: A dictionary containing the ZIP file name, size, list of contained files, and SHA-256 hash.
    """
    zip_file_name = zip_file_path.name
    zip_file_size = zip_file_path.stat().st_size  # Get the size of the ZIP file
    contained_files = []
    hasher = hashlib.sha256()
    
    with zipfile.ZipFile(zip_file_path, 'r') as zip_file:
        for info in zip_file.infolist():
            contained_files.append(info.filename)
            with zip_file.open(info.filename) as f:
                while chunk := f.read(8192):
                    hasher.update(chunk)
    
    return {
        'zip_file_name': zip_file_name,
        'zip_file_size': zip_file_size,
        'contained_files': contained_files,
        'hash': hasher.hexdigest()
    }

# Gather details for the reference ZIP file
correct_zip_path = directory / correct_zip_file
correct_zip_details = get_zip_file_details(correct_zip_path)

# Display reference ZIP file details
print(f"Details for the reference ZIP file: {correct_zip_details['zip_file_name']}")
print(f"File size: {correct_zip_details['zip_file_size']} bytes")
print(f"Contained files: {correct_zip_details['contained_files']}")
print(f"Hash: {correct_zip_details['hash']}\n")

# Collect and store details for each ZIP file, excluding the reference file
zip_files_details = []
for file_path in directory.iterdir():
    if file_path.is_file() and file_path.suffix == '.zip' and file_path.name != correct_zip_file:
        zip_file_details = get_zip_file_details(file_path)
        zip_files_details.append(zip_file_details)

# Compare each ZIP file's hash with the reference ZIP file's hash
filtered_zip_files_details = []
for zip_details in zip_files_details:
    if zip_details['hash'] != correct_zip_details['hash']:
        filtered_zip_files_details.append(zip_details)

# Check if all ZIP files match the reference and either exit or proceed
if not filtered_zip_files_details:
    print("All ZIP files match the reference ZIP file.")
    sys.exit()  # Exit the script if all ZIP files match
else:
    print("Some ZIP files do not match the reference ZIP file:")
    for zip_details in filtered_zip_files_details:
        print(f"Non-matching ZIP file: {zip_details['zip_file_name']}")
        print(f"Hash: {zip_details['hash']}\n")

# Function to get file size and hash for an HTML file
def get_file_size_and_hash(file_path):
    """
    Calculates the size and SHA-256 hash of a file.

    Args:
        file_path (Path): Path to the file.

    Returns:
        tuple: A tuple containing the file size and SHA-256 hash.
    """
    file_size = file_path.stat().st_size
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    file_hash = hasher.hexdigest()
    return file_size, file_hash

# Gather details for the reference HTML file
correct_html_path = directory / correct_html_file
correct_html_size, correct_html_hash = get_file_size_and_hash(correct_html_path)

# Compare each HTML file's hash with the reference HTML file's hash
filtered_files_html = []
for html_file in files_html:
    html_file_path = directory / html_file
    html_size, html_hash = get_file_size_and_hash(html_file_path)
    
    if html_hash != correct_html_hash:
        filtered_files_html.append(html_file)  # Keep only non-matching files

# Display the remaining HTML files after filtering
print("Remaining HTML files after filtering:")
print(filtered_files_html)

def process_html_file(html_file_path):
    """
    Processes an HTML file using BeautifulSoup.

    Args:
        html_file_path (Path): Path to the HTML file.

    Returns:
        list: A list of extracted headers from the HTML file.
    """
    with open(html_file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
        headers = [header.get_text(strip=True) for header in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])]
        print(f"Extracted headers from {html_file_path.name}: {headers}")
        return headers

# Process each remaining non-matching HTML file
for html_file in filtered_files_html:
    html_file_path = directory / html_file
    process_html_file(html_file_path)
