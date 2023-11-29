import os
import numpy as np
from keras.preprocessing import image
import matplotlib.pyplot as plt

# Enum for Labels


class PlantLabels:
    CERSCOSOPORA = 0
    HEALTHY = 1
    LEAF_RUST = 2
    MINER = 3
    PHOMA = 4

# Function for Image Loading and Preprocessing


def load_and_preprocess_images(category_path, label, target_size=(50, 50)):
    data = []
    labels = []

    for filename in os.listdir(category_path):
        # print(filename)
        file_path = os.path.join(category_path, filename)

        # Check if the file is an image
        if file_path.endswith(('.jpg', '.jpeg', '.png')):
            img = image.load_img(file_path, target_size=target_size)
            img_array = image.img_to_array(img)
            data.append(img_array)
            labels.append(label)

    return data, labels


cnn_directory = os.path.dirname(os.path.abspath(__file__))

# Define paths for each category relative to the cnn directory
categories = {
    PlantLabels.CERSCOSOPORA: os.path.join(cnn_directory, "data/Cerscospora/"),
    PlantLabels.HEALTHY: os.path.join(cnn_directory, "data/Healthy/"),
    PlantLabels.LEAF_RUST: os.path.join(cnn_directory, "data/Leaf_rust/"),
    PlantLabels.MINER: os.path.join(cnn_directory, "data/Miner/"),
    PlantLabels.PHOMA: os.path.join(cnn_directory, "data/Phoma/"),
}

# Load and preprocess images for each category
all_data = []
all_labels = []

for label, path in categories.items():
    category_data, category_labels = load_and_preprocess_images(path, label)
    all_data.extend(category_data)
    all_labels.extend(category_labels)

# Convert to NumPy arrays
plants = np.array(all_data)
labels = np.array(all_labels)

# Save the data
np.save("plants", plants)
np.save("labels", labels)

# Function for Loading Test Image


def load_image(img_path, target_size=(224, 224), show=False):
    img = image.load_img(img_path, target_size=target_size)
    img_array = image.img_to_array(img)
    img_tensor = np.expand_dims(img_array, axis=0)
    img_tensor /= 255.0  # Normalize to [0, 1]

    if show:
        plt.imshow(img_tensor[0])
        plt.axis('off')
        plt.show()

    return img_tensor


# # Example of loading a test image
# test_img_path = "path/to/your/test/image.jpg"
# loaded_test_img = load_image(test_img_path, show=True)
