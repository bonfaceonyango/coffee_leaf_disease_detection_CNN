console.log("ACADEMY OMEN IS COOL");

// get elements by id
const message = document.getElementById("message");
const button = document.getElementById("submitBtn");
const fileInput = document.getElementById("file");
const description = document.getElementById("description");

// if button is clicked, check the file input
button.addEventListener("click", function () {
  if (fileInput.files.length === 0) {
    message.innerHTML = "No File selected, Please select a file!";
  } else {
    console.log("fileInput");
    console.log(fileInput);
    message.innerHTML = "Processing Image....";

    // Create a FormData object to send the file
    const formData = new FormData();
    formData.append("image", fileInput.files[0]);
    console.log("formData");
    console.log(formData);

    // Make a POST request to upload the image
    fetch("http://localhost:8000/api/upload/", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        const saved_image = data.image_url.split("/");
        const image_new = saved_image[saved_image.length - 1];
        console.log("saved_image");
        console.log(image_new);

        // After uploading the image, update the DOM with the uploaded image
        document.getElementById("uploadedImage").src = data.image_url;
        document.getElementById("imageName").innerText = data.image_name;
        // Make a GET request for prediction
        return fetch(`http://localhost:8000/api/predict/${image_new}/`);
      })
      .then((predictionResponse) => predictionResponse.json())
      .then((predictionData) => {
        // description.innerHTML = predictionData.description;
        console.log(predictionData);
        // Update the DOM with prediction details . the ids are accesed in html file
        message.innerHTML = "Image processed";
        document.getElementById("prediction").innerText =
          predictionData.prediction;
        document.getElementById("predictionPercentage").innerText =
          predictionData.probability.toFixed(2) + "%";
        document.getElementById("imageName").innerText =
          predictionData.image_url;
        const descriptionElement = document.getElementById("description");
        const causeElement = document.getElementById("cause");
        const signsElement = document.getElementById("signs");
        const treatmentElement = document.getElementById("treatment");
        if (descriptionElement) {
          descriptionElement.innerText = predictionData.description;
        }
        if (causeElement) {
          causeElement.innerText = predictionData.cause;
        }
        if (signsElement) {
          signsElement.innerText = predictionData.signs;
        }
        if (treatmentElement) {
          treatmentElement.innerText = predictionData.treatment;
        }
        message.innerHTML = "Image processed";
      })
      .catch((error) => {
        console.error(error);
        message.innerHTML = "Error in the process.";
      });
  }
});
