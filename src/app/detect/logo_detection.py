from typing import Iterable, Optional, Tuple
from google.cloud import vision
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
import io

from pathlib import Path


class LogoProcessor:

    def __init__(self, client : vision.ImageAnnotatorClient = None) -> None:
        
        self.client = client
        if not self.client:
            self.client = vision.ImageAnnotatorClient()

    
    def process_image(self, path: str) -> Tuple[Optional[str], Iterable]:
        
        with io.open(path, 'rb') as image_file:
            content = image_file.read()

        image = vision.Image(content=content)
        
        response = self.client.logo_detection(image=image)

        if response.error.message:
            raise Exception(
                '{}\nFor more info on error messages, check: '
                'https://cloud.google.com/apis/design/errors'.format(
                    response.error.message))

        logos = response.logo_annotations
        
        colors = ["yellow", "red", "blue", "green", "cyan", "magenta"]

        data = {}
        plt.figure()
        img = mpimg.imread(path)
        plt.imshow(img)

        for idx, logo in enumerate(logos):
            if logo.description in data:
                color = data[logo.description]['color']
            else:
                color = colors[idx % len(colors)]
            data[logo.description] = {
                "color": color,
                "confianza": f"{logo.score * 100:.2f}%"
            }
            
            coord = [[vertex.x, vertex.y] for vertex in logo.bounding_poly.vertices]
            coord.append(coord[0]) #repeat the first point to create a 'closed loop'
            xs, ys = zip(*coord) #create lists of x and y values
            plt.plot(xs, ys, color=color)
        
        file_name = os.path.splitext(os.path.basename(path))[0]
        modified_file_path = os.path.join(Path(path).parent.absolute(), file_name + '-altered.png')
        plt.savefig(modified_file_path, format='png')
        
        return modified_file_path, data
