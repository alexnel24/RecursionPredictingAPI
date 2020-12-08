# RecursionPredictingAPI
This repository contains a python script to locally load a tensorflow CNN model and run an API to produce predictions on images of cells based off of the Recursion Pharma company public dataset rxrx1. 

THIS PROJECT WAS DONE DURING ALEX NELSON'S CAPSTONE PROJECT WHILE COMPLETING A MASTER OF SOFTWARE DEVELOPMENT FROM THE UNIVERSITY OF UTAH IN 2020.

<br>
<br>
This python script loads the model from aws s3 storage. To receive restricted user access to this s3 location, please e-mail Alex at alexander.nelson24@gmail.com with this request.

<br>
<br>
Here are a list of needed libraries:
<br>
1.	sys and os
<br>
2.	boto3
<br>
3.	Flask and request from flask
<br>
4.	tensorflow
<br>
5.	numpy
<br>
6.	cv2 from opencv-python

<br>
<br>
A virtual environment is also available with these 6 libraries at the same s3 location
