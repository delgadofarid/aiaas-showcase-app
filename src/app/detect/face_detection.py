from typing import Iterable, Optional, Tuple
from google.cloud import vision
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
import io

from pathlib import Path


class FaceProcessor:

    def __init__(self, client : vision.ImageAnnotatorClient = None) -> None:
        
        self.client = client
        if not self.client:
            self.client = vision.ImageAnnotatorClient()

    
    def process_image(self, path: str) -> Tuple[Optional[str], Iterable]:
        
        with io.open(path, 'rb') as image_file:
            content = image_file.read()

        image = vision.Image(content=content)
        
        # print(image)
        # print(path)
        response = self.client.face_detection(image=image)

        if response.error.message:
            raise Exception(
                '{}\nFor more info on error messages, check: '
                'https://cloud.google.com/apis/design/errors'.format(
                    response.error.message))

        faces = response.face_annotations

        likelihood_name = ('DESCONOCIDO', 
                           'MUY IMPROBABLE', 
                           'IMPROBABLE', 
                           'POSIBLE', 
                           'PROBABLE', 
                           'MUY PROBABLE')
        
        colors = ["yellow", "red", "blue", "green", "cyan", "magenta"]

        data = {}
        plt.figure()
        img = mpimg.imread(path)
        plt.imshow(img)

        for idx, face in enumerate(faces):
            color = colors[idx % len(colors)]
            data[f"Rostro {idx + 1}"] = {
                "color": color,
                "confianza": f"{face.detection_confidence * 100:.2f}%",
                "emoción.alegría": likelihood_name[face.anger_likelihood],
                "emoción.tristeza": likelihood_name[face.sorrow_likelihood],
                "emoción.enfado": likelihood_name[face.joy_likelihood],
                "emoción.sorpresa": likelihood_name[face.surprise_likelihood],
                "imgprop.underexposed": likelihood_name[face.under_exposed_likelihood],
                "imgprop.blurred": likelihood_name[face.blurred_likelihood],
                "imgprop.headwear": likelihood_name[face.headwear_likelihood]
            }
            
            coord = [[vertex.x, vertex.y] for vertex in face.bounding_poly.vertices]
            coord.append(coord[0]) #repeat the first point to create a 'closed loop'
            xs, ys = zip(*coord) #create lists of x and y values
            plt.plot(xs, ys, color=color)
        
        file_name = os.path.splitext(os.path.basename(path))[0]
        modified_file_path = os.path.join(Path(path).parent.absolute(), file_name + '-altered.png')
        plt.savefig(modified_file_path, format='png')
        
        return modified_file_path, data
