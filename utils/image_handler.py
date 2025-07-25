"""Image processing utilities for handling image uploads from device gallery"""

import discord
import aiohttp
import asyncio
from PIL import Image
import io
import os

class ImageHandler:
    def __init__(self):
        self.max_file_size = 8 * 1024 * 1024  # 8MB limit
        self.supported_formats = ['JPEG', 'PNG', 'GIF', 'WEBP']
        self.max_dimensions = (2048, 2048)
    
    async def process_uploaded_image(self, attachment: discord.Attachment) -> dict:
        """Process an uploaded image from user's device gallery"""
        result = {
            "success": False,
            "url": None,
            "error": None,
            "processed": False
        }
        
        try:
            # Check file size
            if attachment.size > self.max_file_size:
                result["error"] = "Image file too large. Maximum size is 8MB."
                return result
            
            # Check if it's an image
            if not attachment.content_type or not attachment.content_type.startswith('image/'):
                result["error"] = "File is not a valid image."
                return result
            
            # Download the image
            async with aiohttp.ClientSession() as session:
                async with session.get(attachment.url) as response:
                    if response.status != 200:
                        result["error"] = "Failed to download image."
                        return result
                    
                    image_data = await response.read()
            
            # Process the image with PIL
            try:
                image = Image.open(io.BytesIO(image_data))
                
                # Check format
                if image.format not in self.supported_formats:
                    result["error"] = f"Unsupported image format. Supported: {', '.join(self.supported_formats)}"
                    return result
                
                # Resize if too large
                if image.size[0] > self.max_dimensions[0] or image.size[1] > self.max_dimensions[1]:
                    image.thumbnail(self.max_dimensions, Image.Resampling.LANCZOS)
                    result["processed"] = True
                
                # Convert to RGB if necessary (for JPEG compatibility)
                if image.mode not in ('RGB', 'RGBA'):
                    if image.mode == 'P' and 'transparency' in image.info:
                        image = image.convert('RGBA')
                    else:
                        image = image.convert('RGB')
                    result["processed"] = True
                
                # If we processed the image, we would normally save it to a file hosting service
                # For now, we'll just use the original Discord URL
                result["success"] = True
                result["url"] = attachment.url
                
                return result
                
            except Exception as e:
                result["error"] = f"Failed to process image: {str(e)}"
                return result
                
        except Exception as e:
            result["error"] = f"Error handling image: {str(e)}"
            return result
    
    def validate_image_upload(self, attachment: discord.Attachment) -> tuple[bool, str]:
        """Validate an image upload from device gallery"""
        # Check file size
        if attachment.size > self.max_file_size:
            return False, "Image file too large. Maximum size is 8MB."
        
        # Check content type
        if not attachment.content_type or not attachment.content_type.startswith('image/'):
            return False, "Please upload a valid image file from your device gallery."
        
        # Check file extension
        valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
        file_extension = os.path.splitext(attachment.filename.lower())[1]
        
        if file_extension not in valid_extensions:
            return False, f"Unsupported file type. Please use: {', '.join(valid_extensions)}"
        
        return True, "Valid image file."
    
    async def get_image_info(self, attachment: discord.Attachment) -> dict:
        """Get information about an uploaded image"""
        info = {
            "filename": attachment.filename,
            "size": attachment.size,
            "content_type": attachment.content_type,
            "url": attachment.url,
            "dimensions": None,
            "format": None
        }
        
        try:
            # Download and analyze the image
            async with aiohttp.ClientSession() as session:
                async with session.get(attachment.url) as response:
                    if response.status == 200:
                        image_data = await response.read()
                        image = Image.open(io.BytesIO(image_data))
                        
                        info["dimensions"] = image.size
                        info["format"] = image.format
                        
        except Exception as e:
            info["error"] = str(e)
        
        return info

# Global instance
image_handler = ImageHandler()

async def process_image(attachment: discord.Attachment) -> str:
    """Process an image upload and return URL"""
    result = await image_handler.process_uploaded_image(attachment)
    
    if result["success"]:
        return result["url"]
    else:
        raise ValueError(result["error"])

def validate_image(attachment: discord.Attachment) -> tuple[bool, str]:
    """Validate an image upload"""
    return image_handler.validate_image_upload(attachment)

async def get_image_details(attachment: discord.Attachment) -> dict:
    """Get detailed information about an uploaded image"""
    return await image_handler.get_image_info(attachment)
