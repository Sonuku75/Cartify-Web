"""
File upload security foundation for Cartify.
Provides validation, safe filename generation, and MIME/magic-byte verification
for future media/product image uploads.
"""
import os
import re
import uuid
from typing import Optional, Set
from django.core.exceptions import ValidationError
from django.conf import settings

# Upload Constraints
MAX_IMAGE_FILE_SIZE = getattr(settings, 'MAX_IMAGE_FILE_SIZE', 5 * 1024 * 1024)  # 5 MB
ALLOWED_IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp'}
ALLOWED_IMAGE_MIME_TYPES = {'image/jpeg', 'image/png', 'image/webp'}

# Magic byte signatures for verified image formats
# JPEG starts with FF D8 FF
# PNG starts with 89 50 4E 47 0D 0A 1A 0A
# WebP starts with RIFF (bytes 0-3) and WEBP (bytes 8-11)
MAGIC_BYTE_SIGNATURES = {
    'image/jpeg': [b'\xff\xd8\xff'],
    'image/png': [b'\x89PNG\r\n\x1a\n'],
}


def sanitize_filename(filename: str) -> str:
    """
    Sanitizes raw user filename by removing path traversal characters,
    null bytes, control characters, and reserved system characters.
    """
    if not filename:
        return ""

    # Strip directory components (both Unix and Windows)
    basename = os.path.basename(filename.replace('\\', '/'))

    # Remove null bytes and control characters
    cleaned = re.sub(r'[\x00-\x1f\x7f]', '', basename)

    # Normalize whitespace and strip traversal symbols
    cleaned = cleaned.replace('..', '')

    return cleaned.strip()


def generate_secure_filename(original_filename: str) -> str:
    """
    Generates a cryptographically random, collision-free filename.
    Preserves sanitized extension and discards the original user filename
    to avoid path traversal, encoding exploits, or sensitive name leakage.
    """
    sanitized = sanitize_filename(original_filename)
    _, ext = os.path.splitext(sanitized)
    ext = ext.lower()

    if ext not in ALLOWED_IMAGE_EXTENSIONS:
        ext = '.jpg'  # Default safe extension if unknown

    return f"{uuid.uuid4().hex}{ext}"


def detect_mime_from_magic_bytes(header: bytes) -> Optional[str]:
    """
    Inspects raw file header bytes to reliably identify the true file type,
    preventing executable script injection masquerading as images.
    """
    if not header:
        return None

    # Check JPEG
    if header.startswith(b'\xff\xd8\xff'):
        return 'image/jpeg'

    # Check PNG
    if header.startswith(b'\x89PNG\r\n\x1a\n'):
        return 'image/png'

    # Check WebP (RIFF .... WEBP)
    if len(header) >= 12 and header.startswith(b'RIFF') and header[8:12] == b'WEBP':
        return 'image/webp'

    return None


def validate_image_file(
    file_obj,
    max_size: int = MAX_IMAGE_FILE_SIZE,
    allowed_extensions: Optional[Set[str]] = None,
    allowed_mime_types: Optional[Set[str]] = None,
) -> None:
    """
    Performs comprehensive security validation on an uploaded file object.
    
    Checks:
    1. Maximum file size
    2. Allowed file extension
    3. Content verification via binary magic bytes
    
    Raises:
        ValidationError if any security check fails.
    """
    if allowed_extensions is None:
        allowed_extensions = ALLOWED_IMAGE_EXTENSIONS
    if allowed_mime_types is None:
        allowed_mime_types = ALLOWED_IMAGE_MIME_TYPES

    # 1. File Size Verification
    file_size = getattr(file_obj, 'size', None)
    if file_size is None:
        pos = file_obj.tell()
        file_obj.seek(0, os.SEEK_END)
        file_size = file_obj.tell()
        file_obj.seek(pos)

    if file_size > max_size:
        max_mb = max_size / (1024 * 1024)
        raise ValidationError(
            f"File size exceeds the maximum allowed limit of {max_mb:.1f} MB."
        )

    if file_size == 0:
        raise ValidationError("Uploaded file is empty.")

    # 2. Extension Verification
    filename = getattr(file_obj, 'name', '')
    sanitized = sanitize_filename(filename)
    _, ext = os.path.splitext(sanitized)
    ext = ext.lower()

    if ext not in allowed_extensions:
        allowed_list = ", ".join(sorted(allowed_extensions))
        raise ValidationError(
            f"File extension '{ext}' is not allowed. Allowed types: {allowed_list}"
        )

    # 3. Magic Byte Binary Content Verification
    pos = file_obj.tell()
    try:
        header = file_obj.read(32)
    finally:
        file_obj.seek(pos)

    detected_mime = detect_mime_from_magic_bytes(header)
    if not detected_mime or detected_mime not in allowed_mime_types:
        raise ValidationError(
            "File content does not match a valid, permitted image format."
        )
