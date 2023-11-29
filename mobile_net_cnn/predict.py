import os
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from keras.models import load_model
from keras.preprocessing import image
from load import load_image
# load model
model = tf.keras.models.load_model(os.getcwd() + '/Mobilenet.h5')


def make_prediction(image_path_input):
    try:
        new_image = load_image(image_path_input)
        if new_image.dtype != np.float32:
            new_image = new_image.astype(np.float32)
    except Exception as e:
        print(f"Error loading image: {e}")
        return None

    pred_probs = model.predict(new_image)

    # Get the predicted class index with the highest probability
    predicted_class_index = np.argmax(pred_probs)
    classes = ['Cerscospora', 'Healthy', 'Leaf_rust', 'Miner', 'Phoma']

    # Get the corresponding class label
    predicted_class = classes[predicted_class_index]

    # Extract the ground truth class from the image path
    true_class = os.path.basename(os.path.dirname(image_path_input))

    # Check if the prediction is correct
    is_correct = predicted_class == true_class

    # Get the probability of the predicted class
    predicted_probability = pred_probs[0, predicted_class_index]

    # Plot the image
    img = image.load_img(image_path_input, target_size=(224, 224))
    plt.subplot(1, 3, 1)
    plt.imshow(img)
    plt.axis("off")

    # Set text color based on correctness
    text_color = 'green' if is_correct else 'red'

    # Display the predicted class and probability
    plt.title(
        f"Predicted: {predicted_class} ({predicted_probability:.2f})", color=text_color)

    # Return the predicted class, probability, and correctness
    return predicted_class, predicted_probability, true_class, is_correct


# Example of making a prediction
# Replace with the actual path to your test image
test_image_path = "/home/bonface/Desktop/coffee_leaf_disease_detection_CNN/mobile_net_cnn/data/Phoma/6 (3).jpg"
make_prediction(test_image_path)
plt.show()
