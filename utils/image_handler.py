import fitz
import io
from PIL import Image
from utils.error_handler import PDFError

class ImageHandler:
    def __init__(self, page):
        self.page = page
        
    def extract_images(self):
        """Extract images from PDF page"""
        image_list = []
        for img_index, img in enumerate(self.page.get_images()):
            try:
                xref = img[0]
                base_image = self.page.parent.extract_image(xref)
                image_bytes = base_image["image"]
                
                # Convert to PIL Image for manipulation
                image = Image.open(io.BytesIO(image_bytes))
                image_list.append({
                    'index': img_index,
                    'image': image,
                    'bbox': img[1],  # Image rectangle
                    'transform': img[2]  # Transform matrix
                })
            except Exception as e:
                raise PDFError(f"Failed to extract image: {str(e)}")
        
        return image_list
