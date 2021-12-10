import os
import pathlib

def detect_safe_search(path: pathlib.Path):
    """Detects unsafe features in the file."""
    from google.cloud import vision
    import io
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.safe_search_detection(image=image)
    safe = response.safe_search_annotation

    # Names of likelihood from google.cloud.vision.enums
    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                       'LIKELY', 'VERY_LIKELY')
    print('Safe search:')

    print('adult: {}'.format(likelihood_name[safe.adult]))
    print('medical: {}'.format(likelihood_name[safe.medical]))
    print('spoofed: {}'.format(likelihood_name[safe.spoof]))
    print('violence: {}'.format(likelihood_name[safe.violence]))
    print('racy: {}'.format(likelihood_name[safe.racy]))

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

BASE_REPO = "/Users/u6104617/Desktop/misc/Simon Bolivar/Especializacion Dirección Marketing/lab/ai-showcase-app"
print(BASE_REPO)
print(BASE_REPO + '/creds/studied-theater-332018-c486e62fa0c9.json')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = BASE_REPO + '/creds/studied-theater-332018-c486e62fa0c9.json'

def main():
    detect_safe_search(BASE_REPO + '/ai_showcase_app/img/explicit/spoofed_04.jpeg')

if __name__ == "__main__":
    main()