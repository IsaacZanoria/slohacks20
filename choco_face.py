# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 22:17:21 2020

@author: rjsta
"""
import os
import numpy as np
import cv2

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=r"C:\Users\rjsta\OneDrive\Documents\slohacks2020\skilled-creek-269711-1d85d6c7c548.json"



def detect_faces(path):
    #"""Detects faces in an image."""
    from google.cloud import vision
    import io
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.face_detection(image=image)
    faces = response.face_annotations
    

    # Names of likelihood from google.cloud.vision.enums
    #likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                       #'LIKELY', 'VERY_LIKELY')
    print('Faces:')
    
    faces_bounds = []
    
    for face in faces:
        
        #print('anger: {}'.format(likelihood_name[face.anger_likelihood]))
        #print('joy: {}'.format(likelihood_name[face.joy_likelihood]))
        #print('surprise: {}'.format(likelihood_name[face.surprise_likelihood]))

        vertices = ([(vertex.x, vertex.y)
                    for vertex in face.bounding_poly.vertices])
        
        print(vertices)
        print(face.landmarking_confidence)
        faces_bounds.append([vertices, face.landmarking_confidence])
        
    
    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
    
    return faces_bounds
        
faces_path = r"C:\Users\rjsta\OneDrive\Documents\slohacks2020\faces.png"

bounding_boxes = detect_faces(faces_path)

image = cv2.imread(faces_path)

#color = 0
for box in bounding_boxes:
    if box[1] > .4:
        cv2.rectangle(image, box[0][0], box[0][2], (0, 20, 200), 5)

cv2.imshow('Caffeine', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
