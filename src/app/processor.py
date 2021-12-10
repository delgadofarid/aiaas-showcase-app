import json
import os
from typing import Iterable
from google.cloud import vision
from app.detect import FaceProcessor, LabelProcessor, LandmarkProcessor, LogoProcessor, ObjectProcessor, OCRProcessor
from pathlib import Path

import whatimage
import pyheif
from PIL import Image


class ProcessedImage:

    def __init__(self, image_description: Iterable, modified_image_path: Path) -> None:
        self.description = image_description
        self.path = modified_image_path

    def __str__(self) -> str:
        return json.dumps({
            "desc": self.description,
            "path": self.path
        }, indent=4)

    def __repr__(self) -> str:
        return self.__str__()


class ImageProcessor:

    def __init__(self) -> None:
        self.client = vision.ImageAnnotatorClient()
        self.processors = {
            "face": FaceProcessor(client=self.client),
            "label": LabelProcessor(client=self.client),
            "text": OCRProcessor(client=self.client),
            "object": ObjectProcessor(client=self.client),
            "logo": LogoProcessor(client=self.client),
            "landmark": LandmarkProcessor(client=self.client)
        }

    def process_image(self, path: Path, type: str) -> ProcessedImage:
        processed_path, details = self.processors[type].process_image(path)
        fmt = self.extract_format(processed_path)
        if fmt in ['heic', 'avif']:
            processed_path = self.parse_heic_avif(processed_path)
        return ProcessedImage(details, processed_path)
    
    def extract_format(self, path: Path) -> str:
        with open(path, "rb") as f:
            bytesIo = f.read()
        fmt = whatimage.identify_image(bytesIo)
        return fmt
    
    def parse_heic_avif(self, path: str) -> Path:
        with open(path, "rb") as f:
            bytesIo = f.read()
        i = pyheif.read_heif(bytesIo)
        pi = Image.frombytes(mode=i.mode, size=i.size, data=i.data)
        _, file_extension = os.path.splitext(path)
        parsed_path = Path(str(path).replace(file_extension, ".jpeg"))
        pi.save(parsed_path, format="jpeg")
        return parsed_path
