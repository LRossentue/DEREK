#!/usr/bin/env python3
"""
Normalize ASCII face heights to 45 lines.

- Trimming: removes lines from TOP only
- Padding: adds blank lines equally to top and bottom (starting at bottom if odd)
- Excludes: derek_sassy_3_60.txt (kept as funny outlier)

Usage:
    python normalize_faces.py
"""

from pathlib import Path


TARGET_HEIGHT = 45
EXCLUDE_FILES = ["derek_sassy_3_60.txt"]


def normalize_face(face_file: Path, target_height: int) -> None:
    """Normalize a face file to target height.

    Args:
        face_file: Path to face file
        target_height: Target number of lines (45)
    """
    with open(face_file, 'r', encoding='utf-8') as f:
        lines = f.read().splitlines()

    current_height = len(lines)
    filename = face_file.name

    if current_height == target_height:
        print(f"✓ {filename:30s} - already {current_height} lines")
        return

    if current_height > target_height:
        # TRIM from TOP
        lines_to_remove = current_height - target_height
        trimmed_lines = lines[lines_to_remove:]

        with open(face_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(trimmed_lines) + '\n')

        print(f"✂ {filename:30s} - trimmed {lines_to_remove} from top: {current_height} → {target_height}")

    else:
        # PAD equally top and bottom (starting at bottom)
        lines_to_add = target_height - current_height
        bottom_padding = (lines_to_add + 1) // 2  # Extra line goes to bottom if odd
        top_padding = lines_to_add - bottom_padding

        padded_lines = ([''] * top_padding) + lines + ([''] * bottom_padding)

        with open(face_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(padded_lines) + '\n')

        print(f"+ {filename:30s} - padded top:{top_padding} bottom:{bottom_padding}: {current_height} → {target_height}")


def main():
    # Get faces directory
    faces_dir = Path(__file__).parent.parent / 'faces'

    if not faces_dir.exists():
        print(f"ERROR: Faces directory not found: {faces_dir}")
        return 1

    print("=" * 70)
    print(f"Normalizing faces to {TARGET_HEIGHT} lines")
    print(f"Excluding: {', '.join(EXCLUDE_FILES)}")
    print("=" * 70)
    print()

    # Process all face files except excluded ones
    face_files = sorted(faces_dir.glob("derek_*.txt"))
    processed = 0

    for face_file in face_files:
        if face_file.name in EXCLUDE_FILES:
            print(f"⊗ {face_file.name:30s} - skipped (outlier)")
            continue

        normalize_face(face_file, TARGET_HEIGHT)
        processed += 1

    print()
    print("=" * 70)
    print(f"COMPLETE - Processed {processed} faces (target: {TARGET_HEIGHT} lines)")
    print("=" * 70)

    return 0


if __name__ == '__main__':
    exit(main())
