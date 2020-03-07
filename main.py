from flask import Flask, request, render_template

import base64
from datetime import datetime
from os import scandir
from PIL import Image

from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.models import load_model

import keras.backend.tensorflow_backend as tb
tb._SYMBOLIC_SCOPE.value = True

app = Flask(__name__)


@app.route('/')
def hello():
    data = {'count': len([iq for iq in scandir('resize_imgs')])}
    return render_template("index.html",data=data)


@app.route('/canvasData', methods=['POST', "GET"])
def canvasData(**kwrgs):
    data_url = request.values['data']
    content = data_url.split(';')[1]
    image_encoded = content.split(',')[1]
    file_name = datetime.now().strftime('%Y%m%d%H%M%S')+'.png'
    with open("resize_imgs/"+file_name, "wb") as fh:
        fh.write(base64.decodebytes(image_encoded.encode('utf-8')))

    # img = Image.open('imageToSave.png')
    # img.thumbnail((28,28), Image.ANTIALIAS)
    # file_name = datetime.now().strftime('%Y%m%d%H%M%S')+'.png'
    # img.save("resize_imgs/"+file_name,)

    
    #Prediction code
    #load the image
    img = load_img("resize_imgs/"+file_name, color_mode = "grayscale", 
                   target_size=(28, 28))

    img = img_to_array(img)
    # reshape into a single sample with 1 channel
    img = img.reshape(1, 28, 28, 1)
    # prepare pixel data
    img = img.astype('float32')
    img = img / 255.0

    model = load_model('final_model.h5')
    # predict the class
    digit = model.predict_classes(img)

    count = len([iq for iq in scandir('resize_imgs')])
    # digit = [1]
    return {'digit': str(digit[0]), 'count':count}

@app.route('/project_description')
def project_description():
    return render_template("project_description.html",)


if __name__ == '__main__':
    app.run(debug=False, threaded=False)
