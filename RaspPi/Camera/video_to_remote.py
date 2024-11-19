import os
import firebase_admin
from firebase_admin import credentials, storage, db

# key for firebase(cloud) adress
cred = credentials.Certificate('/home/peworo/Downloads/homesecurity-c8d2c-firebase-adminsdk-lnqdw-9a879c8769.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': 'homesecurity-c8d2c.appspot.com',
    'databaseURL': 'https://homesecurity-c8d2c-default-rtdb.firebaseio.com'
})
bucket = storage.bucket()

# uploading video to cloud function
def upload_to_firebase(file_path):
    try:
        blob = bucket.blob(os.path.basename(file_path))
        blob.upload_from_filename(file_path)
        blob.make_public()
        video_url = blob.public_url

    
        ref = db.reference('videos')
        new_video_ref = ref.push()
        new_video_ref.set({
            'url': video_url,
            'description': 'Raspberry Pi video upload'
        })

        print(f"UPLOADED: {video_url}")

    except Exception as e:
        print("Failed to upload video to Firebase:", e)