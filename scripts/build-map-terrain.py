#!/usr/bin/env python3
"""Create small Web Mercator terrain backdrops from Natural Earth I."""

from __future__ import annotations

import argparse
import math
from pathlib import Path

import numpy as np
from PIL import Image


REGIONS = {
    "asia-natural-earth.jpg": {"bounds": (0, 60, 70, 180), "width": 3000},
    "oceania-natural-earth.jpg": {"bounds": (-60, 90, 10, 180), "width": 2000},
    "europe-natural-earth.jpg": {"bounds": (30, -15, 72, 45), "width": 1500},
}


def mercator_y(latitude: float) -> float:
    latitude = max(-85.051129, min(85.051129, latitude))
    radians = math.radians(latitude)
    return math.log(math.tan(math.pi / 4 + radians / 2))


def inverse_mercator_y(value: float) -> float:
    return math.degrees(2 * math.atan(math.exp(value)) - math.pi / 2)


def build_region(source: Image.Image, output: Path, bounds: tuple[float, ...], width: int) -> None:
    south, west, north, east = bounds
    north_y = mercator_y(north)
    south_y = mercator_y(south)
    longitude_span = math.radians(east - west)
    height = round(width * (north_y - south_y) / longitude_span)
    source_left = math.floor((west + 180) / 360 * source.width)
    source_right = math.ceil((east + 180) / 360 * source.width)
    source_top = math.floor((90 - north) / 180 * source.height)
    source_bottom = math.ceil((90 - south) / 180 * source.height)
    cropped = source.crop((source_left, source_top, source_right, source_bottom)).convert("RGB")
    cropped = cropped.resize((width, cropped.height), Image.Resampling.LANCZOS)
    pixels = np.asarray(cropped, dtype=np.float32)

    fractions = (np.arange(height, dtype=np.float64) + 0.5) / height
    projected_y = north_y - fractions * (north_y - south_y)
    latitudes = np.degrees(2 * np.arctan(np.exp(projected_y)) - np.pi / 2)
    source_rows = (90 - latitudes) / 180 * source.height - source_top
    upper = np.floor(source_rows).astype(np.int32)
    upper = np.clip(upper, 0, pixels.shape[0] - 1)
    lower = np.clip(upper + 1, 0, pixels.shape[0] - 1)
    weight = np.clip(source_rows - upper, 0, 1).astype(np.float32)[:, None, None]
    rendered_pixels = pixels[upper] * (1 - weight) + pixels[lower] * weight
    rendered = Image.fromarray(np.uint8(np.clip(rendered_pixels, 0, 255)), "RGB")
    rendered.save(output, "JPEG", quality=82, optimize=True, progressive=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path, help="Natural Earth I shaded-relief TIFF")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("assets/map/terrain"),
        help="Output directory",
    )
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    Image.MAX_IMAGE_PIXELS = None
    with Image.open(args.source) as source:
        for filename, settings in REGIONS.items():
            build_region(source, args.output / filename, **settings)


if __name__ == "__main__":
    main()
