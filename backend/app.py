# Import necessary libraries
from flask import Flask, jsonify  # Flask for web server, jsonify for JSON responses
import requests  # For making HTTP requests to the N2YO API
from flask_cors import CORS  # To allow cross-origin requests from React
from dotenv import load_dotenv  # To load environment variables from .env file
import os  # For accessing environment variables

# Initialize Flask application
app = Flask(__name__)
CORS(app)  # Enable CORS to allow frontend (React) to communicate with backend

# Load environment variables from .env file
load_dotenv()
API_KEY = os.getenv('N2YO_API_KEY')  # Get the N2YO API key from .env
BASE_URL = "https://api.n2yo.com/rest/v1/satellite"  # Base URL for N2YO API

# Example NORAD ID for the International Space Station (ISS)
ISS_NORAD_ID = 25544

# Define a route to get satellite position data
@app.route('/api/satellite/<int:norad_id>', methods=['GET'])
def get_satellite_position(norad_id):
    """
    Fetch satellite position data for a given NORAD ID.
    Args:
        norad_id (int): The NORAD ID of the satellite (e.g., 25544 for ISS)
    Returns:
        JSON response with satellite data or an error message
    """
    try:
        # Define observer location (example: New York coordinates)
        lat = 40.7128  # Latitude
        lon = -74.0060  # Longitude
        alt = 0  # Altitude in kilometers
        
        # Construct the API URL with observer location and API key
        url = f"{BASE_URL}/positions/{norad_id}/{lat}/{lon}/{alt}/1/&apiKey={API_KEY}"
        
        # Make the HTTP GET request to the N2YO API
        response = requests.get(url)
        data = response.json()  # Parse the JSON response
        
        # Check if position data exists in the response
        if 'positions' in data:
            position = data['positions'][0]  # Get the first position object
            # Return satellite data as JSON
            return jsonify({
                'name': data['info']['satname'],  # Satellite name
                'latitude': position['satlatitude'],  # Current latitude
                'longitude': position['satlongitude'],  # Current longitude
                'altitude': position['sataltitude'],  # Altitude in kilometers
                'timestamp': position['timestamp']  # UNIX timestamp
            })
        else:
            # Return error if satellite data is not found
            return jsonify({'error': 'Satellite not found'}), 404
            
    except Exception as e:
        # Handle any errors (e.g., network issues, invalid API key)
        return jsonify({'error': str(e)}), 500

# Run the Flask app if this file is executed directly
if __name__ == '__main__':
    app.run(debug=True, port=5000)  # Debug mode on port 5000