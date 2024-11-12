import paho.mqtt.client as mqtt
from picamera2 import Picamera2
import cv2
import time
import os
import firebase_admin 
from firebase_admin import credentials, storage, db
from RaspPi.Camera.store_video import Camera


# Parameters
THRESHOLD = 1500  # Light intensity threshold
BROKER = 'localhost'  
PORT = 1883           
TOPIC = 'sensor/light'

#Firebase settings and key

cred = credentials.Certificate('/home/peworo/Downloads/homesecurity-c8d2c-firebase-adminsdk-lnqdw-9a879c8769.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': 'homesecurity-c8d2c.appspot.com',   # Firebase Storage bucket ID
    'databaseURL': 'https://homesecurity-c8d2c-default-rtdb.firebaseio.com'
})

bucket = storage.bucket()

#Upload file to firebase(cloud)
def upload_to_firebase(file_path):
    try:
        blob = bucket.blob(os.path.basename(file_path)) #video name from file
        blob.upload_from_filename(file_path) #upload video to firebase from file
        blob.make_public()
        video_url = blob.public_url

        # save URL in database
        ref = db.reference('videos')
        new_video_ref = ref.push()
        new_video_ref.set({
            'url': video_url,
            'description': 'Raspberry Pi video upload'
        })

        print(f"Video uploaded to Firebase Storage and URL saved to Realtime Database: {video_url}")

    except Exception as e:
        print("Failed to upload video to Firebase:", e)



