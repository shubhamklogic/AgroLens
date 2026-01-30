from flask import Flask        # Import the Flask class

# Initialize the Flask application
app = Flask(__name__)

# Define a route for the home page
@app.route("/")
def home():
    # This message appears in your browser
    return "AgroLens Backend is working! 🌾"

# Start the server
if __name__ == "__main__":
    # debug=True allows auto-reload on code change
    app.run(debug=True)