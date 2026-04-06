#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 10:41:25 2026

@author: daniel
"""

import os
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime
from PIL import Image


BASE_URL = "http://jsoc.stanford.edu/data/farside/AR_Maps_JPEG/2015/"
DOWNLOAD_DIR = "AR_Maps_JPEG_2015"
GIF_NAME = "farside_2015.gif"

# Duración por frame en milisegundos
FRAME_DURATION = 300


def get_png_links(folder_url: str) -> list[str]:
    """
    Parse the directory listing and return all PNG file links.
    """
    response = requests.get(folder_url, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    links = []

    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.lower().endswith(".png"):
            full_url = urljoin(folder_url, href)
            links.append(full_url)

    return links


def extract_datetime_from_filename(filename: str) -> datetime:
    """
    Extract datetime from filenames like:
    AR_MAP_2015.01.13_00:00:00.png
    """
    pattern = r"AR_MAP_(\d{4}\.\d{2}\.\d{2})_(\d{2}:\d{2}:\d{2})\.png"
    match = re.search(pattern, filename)

    if not match:
        raise ValueError(f"Could not parse datetime from filename: {filename}")

    date_part, time_part = match.groups()
    return datetime.strptime(f"{date_part}_{time_part}", "%Y.%m.%d_%H:%M:%S")


def download_file(url: str, output_path: str) -> None:
    """
    Download a file from URL to output_path.
    """
    response = requests.get(url, stream=True, timeout=60)
    response.raise_for_status()

    with open(output_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)


def download_all_pngs(folder_url: str, download_dir: str) -> list[str]:
    """
    Download all PNG files from the folder URL.
    Returns a list of local file paths.
    """
    os.makedirs(download_dir, exist_ok=True)

    png_links = get_png_links(folder_url)
    if not png_links:
        raise RuntimeError("No PNG files were found in the folder listing.")

    local_files = []

    for url in png_links:
        filename = os.path.basename(url)
        local_path = os.path.join(download_dir, filename)

        if not os.path.exists(local_path):
            print(f"Downloading: {filename}")
            download_file(url, local_path)
        else:
            print(f"Already exists, skipping: {filename}")

        local_files.append(local_path)

    return local_files


def sort_files_chronologically(filepaths: list[str]) -> list[str]:
    """
    Sort local PNG files by the datetime encoded in the filename.
    """
    return sorted(filepaths, key=lambda p: extract_datetime_from_filename(os.path.basename(p)))


def create_gif(image_paths: list[str], gif_path: str, duration_ms: int = 300) -> None:
    """
    Create a GIF from a list of image paths.
    """
    frames = []

    for path in image_paths:
        img = Image.open(path).convert("RGBA")
        frames.append(img)

    if not frames:
        raise RuntimeError("No frames available to create GIF.")

    first_frame, *other_frames = frames
    first_frame.save(
        gif_path,
        save_all=True,
        append_images=other_frames,
        duration=duration_ms,
        loop=0,
        optimize=False,
    )


def main():
    print("Finding and downloading PNG files...")
    local_files = download_all_pngs(BASE_URL, DOWNLOAD_DIR)

    print("Sorting images chronologically...")
    sorted_files = sort_files_chronologically(local_files)

    print("Creating GIF...")
    gif_path = os.path.join(DOWNLOAD_DIR, GIF_NAME)
    create_gif(sorted_files, gif_path, duration_ms=FRAME_DURATION)

    print(f"Done. GIF saved at: {gif_path}")


if __name__ == "__main__":
    main()