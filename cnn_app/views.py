import os
import numpy as np
from django.views.decorators.csrf import csrf_exempt

import tensorflow as tf
from django.conf import settings
from django.http import JsonResponse
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder

from django.template.response import TemplateResponse
from django.utils.datastructures import MultiValueDictKeyError
# import the load image from the mobilenet folder file named load.py
from mobile_net_cnn.load import load_image
from django.core.files.storage import FileSystemStorage
import pandas as pd

class CustomFileSystemStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        self.delete(name)
        return name
# get base directory
# Get the current script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Navigate up multiple levels to reach the base path of the app folder
app_dir = os.path.abspath(os.path.join(script_dir, '..'))
# cnn_directory = os.path.dirname(os.path.abspath(__file__))

def description(label):
    # print(f'label:{label}')
    path_data=os.path.join(app_dir, "assets/condition.csv")
    df=pd.read_csv(path_data)
    print(df)
    predicted=df.groupby("Condition").get_group(label)
    return predicted
    # # with open(path_data, 'r') as csv_file:
    # #     csv_reader = csv.DictReader(csv_file)
    # #     data = list(csv_reader)
    
    # return data
@csrf_exempt
def upload_image(request):
    try:
        if request.method == 'POST' and request.FILES.get('image'):
            # Get the uploaded image from the form
            image = request.FILES["image"]

            # Save the image using CustomFileSystemStorage
            fss = CustomFileSystemStorage()
            _image = fss.save(image.name, image)
            image_url = fss.url(_image)

            return JsonResponse({"message": "Image saved successfully", "image_url": image_url})
        else:
            return JsonResponse({"error": "Invalid request. Please use a POST request with an image."}, status=400)

    except MultiValueDictKeyError:
        return JsonResponse({"error": "No Image Selected"}, status=400)
    except Exception as e:
        print(f"An error occurred while saving image: {e}")
        return JsonResponse({"error": "An error occurred while saving image"}, status=500)

# Predict image API
def predict_image(request, image_url):
    try:
        # Construct the path to the saved image
        path = os.path.join(settings.MEDIA_ROOT, image_url)

        # Load and preprocess the image using the load_image function
        test_image = load_image(path, target_size=(224, 224))

        # Load the pre-trained model
        model = tf.keras.models.load_model(
            os.path.join(os.getcwd(), 'mobile_net_cnn', 'Mobilenet.h5')
        )

        # Make predictions on the image
        result = model.predict(test_image)
        labels = ['Cerscospora', 'Healthy', 'Leaf_rust', 'Miner', 'Phoma']
        predicted_index = np.argmax(result)
        probability = result[0, predicted_index] * 100
        prediction = labels[predicted_index]

        # Read CSV file
        data = description(prediction.replace("_", " "))
        data = data.to_dict(orient='records')

        # Construct the API response
        data_res = {
            "image_url": image_url,
            "prediction": prediction,
            "probability": probability,
            "description": data[0].get("Description"),
            "cause": data[0].get("Cause"),
            "signs": data[0].get("Symptoms"),
            "treatment": data[0].get("Treatment")
        }

        return JsonResponse(data_res)

    except Exception as e:
        print(f"An error occurred: {e}")
        return JsonResponse({"error": "An error occurred"})



def function_api(request):
    # print(request)
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
        # Read CSV file
        data = description(prediction.replace("_"," "))
        data=data.to_dict(orient='records')

                # image details
        image_url = fss.url(_image)

        data_res = {
            "message": message,
            "image_url": image_url,
            "prediction": prediction,
            "prediction_percentage": prediction_percentage,
            "description": data[0].get("Description"),
            "cause": data[0].get("Cause"),
            "signs": data[0].get("Symptoms"),
            "treatment": data[0].get("Treatment")
        }

        # Serialize the data_res to JSON using DjangoJSONEncoder
        json_response = JsonResponse(data_res, encoder=DjangoJSONEncoder)
        return json_response
        

    except MultiValueDictKeyError:
        return JsonResponse({"error": "No Image Selected"})
    except Exception as e:
        # Log the exception for debugging purposes
        print(f"An error occurred: {e}")
        return JsonResponse({"error": "An error occurred"})

   

def index(request):
    print(request.FILES["image"])
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
        # Read CSV file
        data = description(prediction.replace("_"," "))
        data=data.to_dict(orient='records')

        return TemplateResponse(
            request,
            "index.html",
            {
                "message": message,
                "image": image,
                "image_url": image_url,
                "prediction": prediction,
                "prediction_percentage": prediction_percentage,
                "description":data[0].get("Description"),
                "cause":data[0].get("Cause"),
                "signs":data[0].get("Symptoms"),
                "treatment":data[0].get("Treatment")


            },
        )

    except MultiValueDictKeyError:
        return TemplateResponse(
            request,
            "index.html",
            {"message": "No Image Selected"},
        )
