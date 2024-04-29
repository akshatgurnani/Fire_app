import os
from flask import Flask, render_template, request ,Response
import cv2
from werkzeug.utils import secure_filename
import numpy as np
import tensorflow as tf
# from tensorflow import keras
# from keras.applications.resnet import ResNet50 
from PIL import Image
import keras.utils as image
from keras.applications.resnet import preprocess_input, decode_predictions 
import yagmail
from geo import get_current_gps_coordinates
import requests as rq
# import io


app = Flask(__name__)

model = tf.keras.models.load_model('./test_model.h5')

camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

def gen_frames(camera, model):
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            # Convert frame for fire detection
            pil_im = Image.fromarray(frame)
            pil_im = pil_im.resize((224, 224))  # resize for the model
            img_array = image.img_to_array(pil_im)
            img_array = np.expand_dims(img_array, axis=0) / 255

            # Predict fire
            probabilities = model.predict(img_array)[0]
            prediction = np.argmax(probabilities)

            # Annotate frame based on prediction
            font = cv2.FONT_HERSHEY_SIMPLEX
            if prediction == 0:
                text = 'Fire Detected'
                cv2.putText(frame, text, (50, 50), font, 1, (0, 0, 255), 2, cv2.LINE_4)
                
                # Saving the frame as an image temporarily
                img_path = 'detected_fire.jpg'
                cv2.imwrite(img_path, frame)
                
                # Sending email
                user = 'priyankachovatiya10@gmail.com'
                app_password = 'btys zkcw jzpt kdhz'
                to = 'priyankamrjp@gmail.com'
                subject = 'Fire Detection System Alert!'
                contents = ['Fire detected', 'Urgent action required']
                attachments = [img_path]
                with yagmail.SMTP(user, app_password) as yag:
                    yag.send(to, subject, contents,attachments=attachments)
                    print('Sent email successfully')
                    
                #sending sms
                url = "https://www.fast2sms.com/dev/bulkV2"
                coordinates = get_current_gps_coordinates()
                if coordinates is not None:
                    latitude, longitude = coordinates
                    detect_msg = "Fire Detected\nLatitude is: " + str(latitude) + ", Longitude is: " + str(longitude)
                    querystring = {
                        "authorization": "CTMLMlIASVae6kYcaJkMfcvdkYrSyE16KP8TBEMx1NZkHzeQErt9sH78U4mX",
                        "message": [detect_msg],
                        "language": "english",
                        "route": "q",
                        "numbers": "9066436692"
                    }
                    headers = {'cache-control': "no-cache"}
                    response = rq.request("GET", url, headers=headers, params=querystring)
                    print(response.text)
                
            else:
                text = 'Fire Not Detected'
                cv2.putText(frame, text, (50, 50), font, 1, (255, 255, 0), 2, cv2.LINE_4)

            # Encode frame for streaming
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            
    
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/Login")
def Login():
    return render_template("Login.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/Actions")
def Actions():
    return render_template("Actions.html")

@app.route("/video_feed")
def video_feed():
    return Response(gen_frames(camera, model), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/upload", methods=["POST"])
def upload():
    if request.method == "POST":
        file = request.files["file"]
        if file:
            filename = secure_filename(file.filename)
            file.save(filename)
            img = image.load_img(filename, target_size=(224, 224))
            img_array = image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0) / 255
            probabilities = model.predict(img_array)[0]
            prediction = np.argmax(probabilities)
            if prediction == 1:
                results = "Fire Not Detected"
            if prediction == 0:
                results = "Fire Detected"
                
                # Sending email
                user = 'priyankachovatiya10@gmail.com'
                app_password = 'btys zkcw jzpt kdhz'
                to = 'priyankamrjp@gmail.com'
                subject = 'Fire Detection System Alert!'
                contents = ['Fire detected', 'Urgent action required', filename]
                with yagmail.SMTP(user, app_password) as yag:
                    yag.send(to, subject, contents)
                    print('Sent email successfully')
                    
                    # Sending SMS
                url = "https://www.fast2sms.com/dev/bulkV2"
                coordinates = get_current_gps_coordinates()
                if coordinates is not None:
                    latitude, longitude = coordinates
                    detect_msg = "Fire Detected\nLatitude is: " + str(latitude) + ", Longitude is: " + str(longitude)
                    querystring = {
                        "authorization": "CTMLMlIASVae6kYcaJkMfcvdkYrSyE16KP8TBEMx1NZkHzeQErt9sH78U4mX",
                        "message": [detect_msg],
                        "language": "english",
                        "route": "q",
                        "numbers": "9066436692"
                    }
                    headers = {'cache-control': "no-cache"}
                    response = rq.request("GET", url, headers=headers, params=querystring)
                    print(response.text)
            return render_template("results.html", results=results)
    return "Error"


if __name__ == "__main__":
    app.run(debug=True)



