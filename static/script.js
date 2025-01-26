document.getElementById('uploadForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const formData = new FormData();
    const fileInput = document.getElementById('imageInput');
    formData.append('image', fileInput.files[0]);
    
    fetch('/detect_mood', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        const resultDiv = document.getElementById('result');
        if (data.emotion) {
            resultDiv.innerHTML = `Detected Mood: ${data.emotion}`;
        } else {
            resultDiv.innerHTML = `Error: ${data.error}`;
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
