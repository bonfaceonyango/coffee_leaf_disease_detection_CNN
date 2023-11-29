import os
import numpy as np

import tensorflow as tf
from django.conf import settings
from django.template.response import TemplateResponse
from django.utils.datastructures import MultiValueDictKeyError
# import the load image from the mobilenet folder file named load.py
from mobile_net_cnn.load import load_image
from django.core.files.storage import FileSystemStorage


class CustomFileSystemStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        self.delete(name)
        return name


def index(request):
    message = ""
    prediction = ""
    probability = ""
    fss = CustomFileSystemStorage()

    try:
        image = request.FILES["image"]
        print("Name", image.file)
        _image = fss.save(image.name, image)
        path = str(settings.MEDIA_ROOT) + "/" + image.name

        # image details
        image_url = fss.url(_image)

        # Load and preprocess the image using the load_image function
        test_image = load_image(path, target_size=(224, 224))

        # Load model
        model = tf.keras.models.load_model(
            os.getcwd() + '/mobile_net_cnn/Mobilenet.h5')

        result = model.predict(test_image)

        # Labels
        # 'Cerscospora' 0
        # 'Healthy' 1
        # 'Leaf_rust' 2
        # 'Miner' 3
        # 'Phoma' 4
        labels = ['Cerscospora', 'Healthy', 'Leaf_rust', 'Miner', 'Phoma']

        predicted_index = np.argmax(result)

        # Get the probability of the predicted class
        probability = (result[0, predicted_index])
        prediction_percentage = probability * 100
        if 0 <= predicted_index < len(labels):
            prediction = labels[predicted_index]

        else:
            prediction = "Unknown"

        return TemplateResponse(
            request,
            "index.html",
            {
                "message": message,
                "image": image,
                "image_url": image_url,
                "prediction": prediction,
                "prediction_percentage": prediction_percentage
            },
        )

    except MultiValueDictKeyError:
        return TemplateResponse(
            request,
            "index.html",
            {"message": "No Image Selected"},
        )
