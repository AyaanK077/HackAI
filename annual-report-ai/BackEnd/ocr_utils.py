import pytesseract
from pdf2image import convert_from_path, convert_from_bytes
from typing import Union, List
import io
import logging
from PIL import Image

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OCRProcessor:
    def __init__(self, tesseract_path: str = None):
        if tesseract_path:
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
        self._verify_tesseract()

    def _verify_tesseract(self):
        try:
            pytesseract.get_tesseract_version()
        except EnvironmentError:
            logger.error("Tesseract not found. Please install it or provide path.")
            raise

    def extract_text_from_image(self, image: Union[str, Image.Image, bytes]) -> str:
        try:
            if isinstance(image, bytes):
                image = Image.open(io.BytesIO(image))
            elif isinstance(image, str):
                image = Image.open(image)
            image = self._preprocess_image(image)
            return pytesseract.image_to_string(image)
        except Exception as e:
            logger.error(f"Image processing failed: {str(e)}")
            raise

    def extract_text_from_pdf(self, pdf_source: Union[str, bytes], dpi: int = 300) -> str:
        try:
            images = self._convert_pdf_to_images(pdf_source, dpi)
            full_text = []
            for i, image in enumerate(images):
                page_text = self.extract_text_from_image(image)
                full_text.append(f"--- PAGE {i+1} ---\n{page_text}")
                logger.info(f"Processed page {i+1}")
            return "\n\n".join(full_text)
        except Exception as e:
            logger.error(f"PDF processing failed: {str(e)}")
            raise

    def _convert_pdf_to_images(self, pdf_source: Union[str, bytes], dpi: int) -> List[Image.Image]:
        if isinstance(pdf_source, bytes):
            return convert_from_bytes(pdf_source, dpi=dpi)
        return convert_from_path(pdf_source, dpi=dpi)

    def _preprocess_image(self, image: Image.Image) -> Image.Image:
        image = image.convert('L')
        return image

def extract_text_from_pdf(pdf_path: str, tesseract_path: str = None) -> str:
    processor = OCRProcessor(tesseract_path)
    return processor.extract_text_from_pdf(pdf_path)