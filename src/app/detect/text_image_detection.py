from typing import Iterable, Optional, Tuple
from google.cloud import vision
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
import io

from pathlib import Path


class OCRProcessor:

    def __init__(self, client : vision.ImageAnnotatorClient = None) -> None:
        
        self.client = client
        if not self.client:
            self.client = vision.ImageAnnotatorClient()

    
    def process_image(self, path: str) -> Tuple[Optional[str], Iterable]:
        
        with io.open(path, 'rb') as image_file:
            content = image_file.read()

        image = vision.Image(content=content)
        
        response = self.client.text_detection(image=image)

        if response.error.message:
            raise Exception(
                '{}\nFor more info on error messages, check: '
                'https://cloud.google.com/apis/design/errors'.format(
                    response.error.message))

        texts = response.text_annotations
        
        color = "cyan"

        data = list()
        dataset = set()
        plt.figure()
        img = mpimg.imread(path)
        plt.imshow(img)

        for text in texts:
            if "locale" in text:
                continue
            
            dataset.add(text.description)
            
            coord = [[vertex.x, vertex.y] for vertex in text.bounding_poly.vertices]
            coord.append(coord[0]) #repeat the first point to create a 'closed loop'
            xs, ys = zip(*coord) #create lists of x and y values
            plt.plot(xs, ys, color=color)
        
        data.append(", ".join(dataset))
        
        file_name = os.path.splitext(os.path.basename(path))[0]
        modified_file_path = os.path.join(Path(path).parent.absolute(), file_name + '-altered.png')
        plt.savefig(modified_file_path, format='png')
        
        return modified_file_path, data
