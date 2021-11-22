from typing import Iterable, Optional, Tuple
from google.cloud import vision
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
import io
from PIL import Image

from pathlib import Path


class ObjectProcessor:

    def __init__(self, client : vision.ImageAnnotatorClient = None) -> None:
        
        self.client = client
        if not self.client:
            self.client = vision.ImageAnnotatorClient()

    
    def process_image(self, path: str) -> Tuple[Optional[str], Iterable]:
        
        with io.open(path, 'rb') as image_file:
            content = image_file.read()

        image = vision.Image(content=content)
        
        response = self.client.object_localization(image=image)

        if response.error.message:
            raise Exception(
                '{}\nFor more info on error messages, check: '
                'https://cloud.google.com/apis/design/errors'.format(
                    response.error.message))

        objects = response.localized_object_annotations
        
        colors = ["yellow", "red", "blue", "green", "cyan", "magenta"]

        data = {}
        plt.figure()
        img = mpimg.imread(path)
        plt.imshow(img)

        width, height = Image.open(path).size

        for idx, object in enumerate(objects):
            if object.name in data:
                color = data[object.name]['color']
            else:
                color = colors[idx % len(colors)]
            data[object.name] = {
                "color": color,
                "confianza": f"{object.score * 100:.2f}%"
            }
            
            coord = [[vertex.x * width, vertex.y * height] for vertex in object.bounding_poly.normalized_vertices]
            coord.append(coord[0]) #repeat the first point to create a 'closed loop'
            xs, ys = zip(*coord) #create lists of x and y values
            plt.plot(xs, ys, color=color)
        
        file_name = os.path.splitext(os.path.basename(path))[0]
        modified_file_path = os.path.join(Path(path).parent.absolute(), file_name + '-altered.png')
        plt.savefig(modified_file_path, format='png')
        
        return modified_file_path, data