#import pandas as pd
import sys
import os

try:
    import boto3
    print("boto import successful!")
except Exception as e:
    print("UNSUCCESSFUL LOAD OF BOTO LIBRARY")
    print("PLEASE CONSIDER DOWNLOADING THE VIRTUAL ENVIRONMENT PROVIDED IN THE S3 STORAGE ASSOCIATED")
    print(e)

try:
    from flask import Flask, request
    print()
    print("flask library import successful!")
except Exception as f:
    print()
    print("UNSUCCESSFUL LOAD OF FLASK LIBRARY")
    print("PLEASE CONSIDER DOWNLOADING THE VIRTUAL ENVIRONMENT PROVIDED IN THE S3 STORAGE ASSOCIATED")
    print(f)
    print()

try:
    import tensorflow as tf
    print()
    print("tensorflow library import successful!")
except Exception as t:
    print()
    print("UNSUCCESSFUL LOAD OF TENSORFLOW LIBRARY")
    print("PLEASE CONSIDER DOWNLOADING THE VIRTUAL ENVIRONMENT PROVIDED IN THE S3 STORAGE ASSOCIATED")
    print(t)
    print()

try:
    import numpy as np
    from numpy import asarray
    print()
    print("numpy library import successful!")
except Exception as n:
    print()
    print("UNSUCCESSFUL LOAD OF NUMPY LIBRARY")
    print("PLEASE CONSIDER DOWNLOADING THE VIRTUAL ENVIRONMENT PROVIDED IN THE S3 STORAGE ASSOCIATED")
    print(n)
    print()

try:
    import cv2
    print()
    print("cv2 successfully imported!")
    print()
except Exception as e:
    print()
    print("UNSUCCESSFUL LOAD OF CV2 LIBRARY")
    print("PLEASE CONSIDER DOWNLOADING THE VIRTUAL ENVIRONMENT PROVIDED IN THE S3 STORAGE ASSOCIATED")
    print(e)
    print()

s3_resource = boto3.resource('s3')

cwdpath = os.getcwd()
print("Current working directory: " + cwdpath)
print()

newDirectory = "model.model"

newPath = os.path.join(cwdpath, newDirectory)
print("new path: " + newPath)
print("trying to create path")
if not os.path.exists(newPath):
    print("model.model was not found")
    os.mkdir(newPath)
    print('Created: ', newPath)
else:
    print("model.model found")
#os.mkdir(newPath)
print("new path: " + newPath)
print()
print()

#importing the necessary files and weights to build the model
try:
    print()
    print("Getting .pb file from s3")
    newEnding = 'saved_model.pb'
    newestPath = os.path.join(newPath, newEnding)
    s3_resource.Object('capstone-bucket-first', 'modelForAPI/w2smallModelForAPI.model/saved_model.pb').download_file(newestPath)

    print("got .pb file from s3")
    print()
except Exception as A:
    print()
    print("UNSURPRISINGLY DID NOT WORK")
    print(A)
    print()
    sys.exit(1)

try:
    os.chdir('model.model')
    cwdpath = os.getcwd()
    print("Current working directory: " + cwdpath)
    print()
    newDirectory = "variables"
    variablePath = os.path.join(cwdpath, newDirectory)
    print("new variables path: " + variablePath)
    print()
    print("trying to create variables path")
    if not os.path.exists(variablePath):
        print("the path was not found")
        os.mkdir(variablePath)
        print('Created: ', variablePath)
    else:
        print("variables directory found")
    #os.mkdir(newPath)
    print("new path: " + newPath)
    print()
    
except Exception as Y:
    print("unable to make variables folder")
    print(Y)
    print()

try:
    print()
    print("Getting variables.data file from s3")
    newEnding = 'variables/variables.data-00000-of-00001'
    newestPath = os.path.join(newPath, newEnding)
    s3_resource.Object('capstone-bucket-first', 'modelForAPI/w2smallModelForAPI.model/variables/variables.data-00000-of-00001').download_file(newestPath)

    print("got .variables.data file from s3")
    print()
except Exception as A:
    print()
    print("UNSURPRISINGLY DID NOT WORK")
    print(A)
    print()
    sys.exit(1)

try:
    print()
    print("Getting variables.index file")
    newEnding = 'variables/variables.index'
    newestPath = os.path.join(newPath, newEnding)
    s3_resource.Object('capstone-bucket-first', 'modelForAPI/w2smallModelForAPI.model/variables/variables.index').download_file(newestPath)

    print("got .variables.index file from s3")
    print()
except Exception as A:
    print()
    print("UNSURPRISINGLY DID NOT WORK")
    print(A)
    print()
    sys.exit(1)

try:
    print("going back to normal directory")
    os.chdir('../')
    currentDirectory = os.getcwd()
    print("current working directory: " + currentDirectory)
    print()
except Exception as cantChange:
    print("unable to change directories back to botoExample")
    print(cantChange)
    print()

# Initialize the Flask application
app = Flask(__name__)


try:
    model = tf.keras.models.load_model("model.model")
    print()
    print("model load successful!")
    print()
except Exception as uhoh:
    print()
    print("ERROR LOADING MODEL")
    print(uhoh)
    print()


# route http posts to this method
@app.route('/api/predict', methods=['GET'])
def test():
    r = request
    # convert string of image data to uint8
    nparr = np.fromstring(r.data, np.uint8)
    # decode image
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # reshape image
    imArray = asarray(img)
    imArray = imArray / 255
    imReshaped = np.array(imArray).reshape(-1, 512, 512, 1)

    # getting the prediciton from the model
    prediction = model.predict(imReshaped)
    
    # build a response dict to send back to client
    stringHE = prediction[0][0]
    stringHU = prediction[0][1]
    stringR = prediction[0][2]
    stringU = prediction[0][3]
    return "HEPG2: {:.4f}, HUVEC: {:.4f}, RPE: {:.4f}, U2OS: {:.4f}".format(stringHE, stringHU, stringR, stringU)


# start flask app
if __name__ == '__main__':
    app.debug = True
    app.run(port=8080)

