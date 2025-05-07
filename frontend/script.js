document.getElementById("upload-form").addEventListener("submit", function(event) {
    event.preventDefault();

    let fileInput = document.getElementById("file-input").files[0];
    if (!fileInput) {
        alert("Please upload an image or video file.");
        return;
    }

    let formData = new FormData();
    formData.append("file", fileInput);

    fetch("/detect", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("result").innerHTML = `<h3>Result: ${data.message}</h3>`;
    })
    .catch(error => console.error("Error:", error));
});
