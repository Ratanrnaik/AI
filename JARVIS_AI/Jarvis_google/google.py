import cv2
import base64
import requests
from googlesearch import search

# Function to perform face recognition and Google search
def recognize_and_search():
    # Load a pre-trained face detection model
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Create a video capture object for the default camera (0)
    cap = cv2.VideoCapture(0)

    while True:
        # Read a frame from the webcam
        ret, frame = cap.read()

        # Convert the frame to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the frame
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        # Draw rectangles around the detected faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

            # Extract the face region
            face_roi = frame[y:y+h, x:x+w]

            # Perform face recognition (replace this with your face recognition logic)
            # You may use a face recognition library like face_recognition

            # Encode the face image to base64 for Google search
            _, img_encoded = cv2.imencode(".png", face_roi)
            face_base64 = base64.b64encode(img_encoded).decode("utf-8")

            # Use Google Custom Search JSON API to perform a search
            query = "person in the webcam"
            search_url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={google_api_key}&cx={google_cx}"

            payload = {
                "requests": [
                    {
                        "image": {
                            "content": face_base64
                        },
                        "features": [
                            {
                                "type": "IMAGE_SEARCH_FEATURE_TYPE_UNSPECIFIED"
                            }
                        ],
                    }
                ]
            }

            try:
                # Send the API request
                response = requests.post(search_url, json=payload)
                results = response.json().get("responses", [])[0].get("webDetection", {}).get("webEntities", [])

                # Display the search results
                if results:
                    for i, result in enumerate(results):
                        print(f"Result {i + 1}: {result['description']} ({result['score']:.2f})")
                else:
                    print("No results found.")
            except Exception as e:
                print(f"Error: {e}")

        # Display the frame
        cv2.imshow("Webcam Feed", frame)

        # Break the loop when the 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture object and close the OpenCV window
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Replace with your Google Custom Search API key and CX (Custom Search Engine ID)q
    google_api_key = "AIzaSyAmkhtePf9Z3nCiNfxXgWR2rIqtvHr3hc4"
    google_cx = "544132fdebfe747d3"

    # Start face recognition and Google search
    recognize_and_search()
