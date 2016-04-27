import argparse
import base64
import httplib2
import pygame
import time
import os
import pygame.camera
from apiclient.discovery import build
from oauth2client.client import GoogleCredentials


def main(photo_file):
    '''Run a label request on a single image'''

    API_DISCOVERY_FILE = \
        'https://vision.googleapis.com/$discovery/rest?version=v1'
    http = httplib2.Http()

    credentials = GoogleCredentials.get_application_default().create_scoped(
        ['https://www.googleapis.com/auth/cloud-platform'])
    credentials.authorize(http)

    service = build(
        'vision', 'v1', http, discoveryServiceUrl=API_DISCOVERY_FILE)

    with open(photo_file, 'rb') as image:
        image_content = base64.b64encode(image.read())
        service_request = service.images().annotate(
            body={
                'requests': [{
                    'image': {
                        'content': image_content
                    },
                    'features': [{
                        'type': 'LABEL_DETECTION',
                        'maxResults': 10,
                    }]
                }]
            })
        response = service_request.execute()
        for x in response['responses'][0]['labelAnnotations']:
            print x['description'] + ' '
        return 0

if __name__ == '__main__':
    name = raw_input("What would you like to name your photo?  ") + ".jpeg";
    pygame.camera.init()
    cam = pygame.camera.Camera(pygame.camera.list_cameras()[0])
    cam.start()
    time.sleep(3)
    img = cam.get_image()

    import pygame.image
    pygame.image.save(img, name)
    #print(os.path.abspath(name))
    pygame.camera.quit()
    main(name)
    
