from typing import Iterable, Optional, Tuple
from google.cloud import vision
import io

from pathlib import Path


class LabelProcessor:

    def __init__(self, client : vision.ImageAnnotatorClient = None) -> None:
        
        self.client = client
        if not self.client:
            self.client = vision.ImageAnnotatorClient()

    
    def process_image(self, path: Path) -> Tuple[Optional[Path], Iterable]:
        
        with io.open(path, 'rb') as image_file:
            content = image_file.read()

        image = vision.Image(content=content)
        
        # print(image)
        # print(path)
        response = self.client.label_detection(image=image)

        if response.error.message:
            raise Exception(
                '{}\nFor more info on error messages, check: '
                'https://cloud.google.com/apis/design/errors'.format(
                    response.error.message))

        labels = response.label_annotations

        data = []
        for idx, label in enumerate(labels):
            data.append(f"{idx + 1}. {label.description} ({label.score * 100:.2f}%)")
        
        return path, data