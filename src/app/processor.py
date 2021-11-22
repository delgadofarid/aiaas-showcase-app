from typing import Iterable
from google.cloud import vision
from app.detect import FaceProcessor, LabelProcessor, LandmarkProcessor, LogoProcessor, ObjectProcessor, OCRProcessor
import json


class ProcessedImage:

    def __init__(self, image_description: Iterable, modified_image_path: str) -> None:
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

    def process_image(self, path: str, type: str) -> ProcessedImage:
        processed_path, details = self.processors[type].process_image(path)
        return ProcessedImage(details, processed_path)
