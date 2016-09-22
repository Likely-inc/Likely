"""
This is the recognition part of the Likely web app. It recognizes photo features in given photos.
"""

import argparse
import base64
import httplib2

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

DISCOVERY_URL = 'https://{api}.googleapis.com/$discovery/rest?version={apiVersion}'

def getImageFeatures(photo_file):
    """
    Get the features of the given photo file.
    :param photo_file:
    :return: dictionary of the features:
    """

    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('vision', 'v1', credentials=credentials,
                              discoveryServiceUrl=DISCOVERY_URL)

    with open(photo_file.split("?")[0], 'rb') as image:
        image_content = base64.b64encode(image.read())
        service_request = service.images().annotate(body={
            'requests': [{
                'image': {
                    'content': image_content.decode('UTF-8')
                },
                'features': [{
                    'type': 'LABEL_DETECTION',
                    'maxResults': 500
                },
                    {
                        'type': 'FACE_DETECTION',
                        'maxResults': 500
                    },
                    {
                        'type': 'IMAGE_PROPERTIES',
                        'maxResults': 500
                    },
                    {
                        'type': 'LANDMARK_DETECTION',
                        'maxResults': 500
                    },
                    {
                        'type': 'LOGO_DETECTION',
                        'maxResults': 500
                    }]
            }]
        })

        labels = ['noLabels']
        landmarks = ['noLandmarks']
        faces = ['noFaces']
        logos = ['noLogos']

        result = {'landmarks': landmarks, 'labels': labels, 'faces': faces,'colors': {'blueMean': 0, 'redMean': 0}, "logos": logos}

        response = service_request.execute()

        properties = ['noProperties']

        if 'landmarkAnnotations' in response['responses'][0]:
            landmarks = response['responses'][0]['landmarkAnnotations']
            result['landmarks'] = landmarks['locations']

        if 'labelAnnotations' in response['responses'][0]:
            labels = response['responses'][0]['labelAnnotations']
            numOfLabels = len(labels)
            for i in range(numOfLabels):
                result['labels'].append(labels[i]['description'])

        if 'faceAnnotations' in response['responses'][0]:
            faces = response['responses'][0]['faceAnnotations']
            if 'joyLikelihood' in faces:
                result['faces'].append({'joyLikelihood': faces['joyLikelihood']}) #todo fix
            if 'sorrowLikelihood' in faces:
                result['faces'].append({'sorrowLikelihood': faces['sorrowLikelihood']})
            if 'angerLikelihood' in faces:
                result['faces'].append({'angerLikelihood': faces['angerLikelihood']})
            if 'surpriseLikelihood' in faces:
                result['faces'].append({'surpriseLikelihood': faces['surpriseLikelihood']})

        if 'imagePropertiesAnnotation' in response['responses'][0]:
            properties = response['responses'][0]['imagePropertiesAnnotation']
            numOfColors = len(properties['dominantColors']['colors'])

            # calculate the mean value of BLUE color in the photo
            blueSum = 0
            for i in range(numOfColors):
                blueSum += properties['dominantColors']['colors'][i]['color']['blue'] * properties['dominantColors']['colors'][i]['pixelFraction']
            blueMean = blueSum / 256
            result['colors']['blueMean'] = blueMean

            # calculate the mean value of RED color in the photo
            redSum = 0
            for i in range(numOfColors):
                redSum += properties['dominantColors']['colors'][i]['color']['blue'] * properties['dominantColors']['colors'][i]['pixelFraction']
            redMean = redSum / 256
            result['colors']['redMean'] = redMean

        if 'logoAnnotations' in response['responses'][0]:
            logos = response['responses'][0]['logoAnnotations']
            result['logos'] = logos

        # debug prints, todo remove
        print(labels)
        print(faces)
        print(properties)
        print(landmarks)
        print(logos)
        print()
        print(result)

        return result


def main(photo_file):
    getImageFeatures(photo_file)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('image_file', help='The image you\'d like to label.')
    args = parser.parse_args()
    main(args.image_file)
