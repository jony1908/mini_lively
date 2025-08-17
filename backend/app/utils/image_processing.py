"""
Image processing utilities for avatar uploads.
Handles image resizing, optimization, and format standardization.
"""

import io
import uuid
from PIL import Image, ImageOps
from typing import Optional, Tuple


class ImageProcessor:
    """Handles image processing for user avatars."""
    
    # Avatar size constants
    AVATAR_SIZE = (256, 256)  # Standard avatar size
    THUMBNAIL_SIZE = (64, 64)  # Thumbnail size
    MAX_FILE_SIZE = 2 * 1024 * 1024  # 2MB max file size
    SUPPORTED_FORMATS = {'JPEG', 'PNG', 'WEBP'}
    
    @classmethod
    def process_avatar(cls, image_data: bytes, filename: str) -> Tuple[bytes, str]:
        """
        Process uploaded avatar image with proper scaling and optimization.
        
        Args:
            image_data: Raw image bytes
            filename: Original filename
            
        Returns:
            Tuple of (processed_image_bytes, new_filename)
            
        Raises:
            ValueError: If image is invalid or too large
        """
        # Validate file size
        if len(image_data) > cls.MAX_FILE_SIZE:
            raise ValueError(f"Image file too large. Maximum size is {cls.MAX_FILE_SIZE // (1024 * 1024)}MB")
        
        try:
            # Open and validate image
            image = Image.open(io.BytesIO(image_data))
            
            # Convert to RGB if necessary (handles RGBA, P mode, etc.)
            if image.mode != 'RGB':
                # Create white background for transparency
                background = Image.new('RGB', image.size, (255, 255, 255))
                if image.mode == 'RGBA':
                    background.paste(image, mask=image.split()[-1])  # Use alpha channel as mask
                else:
                    background.paste(image)
                image = background
            
            # Auto-orient image based on EXIF data
            image = ImageOps.exif_transpose(image)
            
            # Create square crop (center crop)
            image = cls._crop_to_square(image)
            
            # Resize to standard avatar size with high-quality resampling
            image = image.resize(cls.AVATAR_SIZE, Image.Resampling.LANCZOS)
            
            # Generate unique filename
            file_extension = 'jpg'  # Always save as JPEG for consistency
            new_filename = f"avatar_{uuid.uuid4().hex}.{file_extension}"
            
            # Save optimized image
            output_buffer = io.BytesIO()
            image.save(
                output_buffer,
                format='JPEG',
                quality=85,  # Good balance between quality and file size
                optimize=True,
                progressive=True
            )
            
            processed_data = output_buffer.getvalue()
            
            return processed_data, new_filename
            
        except Exception as e:
            raise ValueError(f"Failed to process image: {str(e)}")
    
    @classmethod
    def _crop_to_square(cls, image: Image.Image) -> Image.Image:
        """
        Crop image to square aspect ratio (center crop).
        
        Args:
            image: PIL Image object
            
        Returns:
            Square-cropped PIL Image
        """
        width, height = image.size
        
        # Determine crop box for center square
        if width > height:
            # Landscape - crop sides
            left = (width - height) // 2
            top = 0
            right = left + height
            bottom = height
        else:
            # Portrait or square - crop top/bottom
            left = 0
            top = (height - width) // 2
            right = width
            bottom = top + width
        
        return image.crop((left, top, right, bottom))
    
    @classmethod
    def create_thumbnail(cls, image_data: bytes) -> bytes:
        """
        Create thumbnail version of processed avatar.
        
        Args:
            image_data: Processed avatar image bytes
            
        Returns:
            Thumbnail image bytes
        """
        try:
            image = Image.open(io.BytesIO(image_data))
            image = image.resize(cls.THUMBNAIL_SIZE, Image.Resampling.LANCZOS)
            
            output_buffer = io.BytesIO()
            image.save(
                output_buffer,
                format='JPEG',
                quality=80,
                optimize=True
            )
            
            return output_buffer.getvalue()
            
        except Exception as e:
            raise ValueError(f"Failed to create thumbnail: {str(e)}")
    
    @classmethod
    def validate_image_format(cls, image_data: bytes) -> bool:
        """
        Validate that uploaded file is a supported image format.
        
        Args:
            image_data: Raw image bytes
            
        Returns:
            True if valid image format, False otherwise
        """
        try:
            image = Image.open(io.BytesIO(image_data))
            return image.format in cls.SUPPORTED_FORMATS
        except Exception:
            return False