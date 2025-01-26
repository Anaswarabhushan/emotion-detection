from flask import Flask, request, jsonify, render_template
from deepface import DeepFace
import os

app = Flask(__name__)

# Directory to store uploaded images
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    return render_template('upload.html')

@app.route('/detect_mood', methods=['POST'])
def detect_mood():
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    image = request.files['image']
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)

    # Save the uploaded image
    image.save(image_path)

    try:
        # Analyze the uploaded image using DeepFace for multiple faces
        analysis = DeepFace.analyze(img_path=image_path, actions=['emotion'], enforce_detection=False)

        # Prepare the response with detected emotions for each face
        detected_emotions = []
        if isinstance(analysis, list):  # Multiple faces detected
            for idx, face in enumerate(analysis):
                emotion = face['dominant_emotion']
                if emotion in ['happy', 'sad']:
                    detected_emotions.append({
                        "face": idx + 1,
                        "mood": emotion
                    })
        else:  # Single face detected
            emotion = analysis['dominant_emotion']
            if emotion in ['happy', 'sad']:
                detected_emotions.append({
                    "face": 1,
                    "mood": emotion
                })

        # Cleanup the uploaded image after analysis
        if os.path.exists(image_path):
            os.remove(image_path)

        return jsonify({"emotions": detected_emotions})

    except Exception as e:
        if os.path.exists(image_path):
            os.remove(image_path)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__': 
    # Create the uploads folder if it doesn't exist
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    app.run(debug=True)
