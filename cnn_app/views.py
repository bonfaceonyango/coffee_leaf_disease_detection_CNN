import os
import numpy as np
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError

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
            print(request)

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

        # Set prediction to unknown if probability is less than 50%
        if probability < 50:
            prediction = "unknown"

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

def index(request):
    message = ""
    prediction = ""
    probability = ""
    image_url = None
    data = {}
    print(request)

    # if request.method == 'POST':
    #     try:
    #         # Get the uploaded image from the form
    #         image = request.FILES.get("image")
    #         print("image")
    #         print(image)

    #         # Check if the image is not None
    #         if image:
    #             # # Save the image using CustomFileSystemStorage
    #             # fss = CustomFileSystemStorage()
    #             # _image = fss.save(image.name, image)
    #             # image_url = fss.url(_image)

    #             # Call the upload_image API
    #             upload_response = upload_image(request, image_url)

    #             # If image is successfully uploaded, call the predict_image API
    #             if upload_response.get("message") == "Image saved successfully":
    #                 pass
    #                 # predict_image(request, image_url)
    #                 # prediction = data.get("prediction", "")
    #                 # probability = data.get("probability", "")

    #                 # image_url=data.get("image_url")
    #             else:
    #                 raise ValidationError("Error uploading image.")

    #         else:
    #             raise ValidationError("No image selected.")

    #     except ValidationError as ve:
    #         message = str(ve)
    #     except Exception as e:
    #         print(f"An error occurred while processing image: {e}")
    #         message = "An error occurred while processing image"

    return TemplateResponse(
        request,
        "index.html",
        {
            "message": message,
            "image_url": image_url,
            "prediction": prediction,
            "probability": probability,
            "description": data.get("Description", ""),
            "cause": data.get("Cause", ""),
            "signs": data.get("Symptoms", ""),
            "treatment": data.get("Treatment", "")
        },
    )
