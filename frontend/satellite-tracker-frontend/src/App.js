import React, { useState, useEffect } from 'react'; // React hooks for state and lifecycle
import axios from 'axios'; // For making HTTP requests to the backend
import './App.css'; // Import CSS for styling

function App() {
  // State variables to manage satellite data, loading status, and errors
  const [satelliteData, setSatelliteData] = useState(null); // Holds satellite position data
  const [loading, setLoading] = useState(true); // Tracks if data is being fetched
  const [error, setError] = useState(null); // Stores error messages

  // useEffect hook to fetch data when component mounts and on interval
  useEffect(() => {
    // Function to fetch satellite data from backend
    const fetchSatelliteData = async () => {
      try {
        // Make GET request to Flask backend for ISS (NORAD ID: 25544)
        const response = await axios.get('http://localhost:5000/api/satellite/25544');
        setSatelliteData(response.data); // Update state with fetched data
        setLoading(false); // Set loading to false once data is received
      } catch (err) {
        setError('Failed to fetch satellite data'); // Set error message
        setLoading(false); // Stop loading
      }
    };

    fetchSatelliteData(); // Initial fetch
    const interval = setInterval(fetchSatelliteData, 5000); // Fetch every 5 seconds

    // Cleanup function to clear interval when component unmounts
    return () => clearInterval(interval);
  }, []); // Empty dependency array means this runs once on mount

  // Display loading message while fetching data
  if (loading) return <div>Loading...</div>;
  // Display error message if fetch fails
  if (error) return <div>{error}</div>;

  // Render satellite data once loaded
  return (
    <div className="App">
      <h1>Satellite Tracker</h1> {/* App title */}
      {satelliteData && ( // Check if satelliteData exists before rendering
        <div>
          <h2>{satelliteData.name}</h2> {/* Satellite name */}
          <p>Latitude: {satelliteData.latitude.toFixed(4)}°</p> {/* Latitude, 4 decimals */}
          <p>Longitude: {satelliteData.longitude.toFixed(4)}°</p> {/* Longitude, 4 decimals */}
          <p>Altitude: {satelliteData.altitude.toFixed(2)} km</p> {/* Altitude, 2 decimals */}
          {/* Convert UNIX timestamp to readable date */}
          <p>Timestamp: {new Date(satelliteData.timestamp * 1000).toLocaleString()}</p>
        </div>
      )}
    </div>
  );
}

export default App; // Export the App component