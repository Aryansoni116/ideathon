import { VscHome, VscArchive, VscAccount, VscSettingsGear } from 'react-icons/vsc';
import Hyperspeed from '../components/MenuBackground';
import StarBorder from '../components/ui/StarBorder'; 
import Dock from '../components/ui/Dock';
import './Menu.css';

const Menu = () => {
  const items = [
    { icon: <VscHome size={24} />, label: 'Home', onClick: () => window.location.href = '/' },
    { icon: <VscArchive size={24} />, label: 'Menu', onClick: () => window.location.href = '/menu' },
    { icon: <VscAccount size={24} />, label: 'Profile', onClick: () => alert('Profile!') },
    { icon: <VscSettingsGear size={24} />, label: 'Settings', onClick: () => alert('Settings!') },
  ];

  const handleFindNearestStation = async () => {
    // Check if geolocation is supported
    if (!navigator.geolocation) {
      alert('Geolocation is not supported by your browser. Please use a modern browser.');
      return;
    }

    // Show loading message
    alert('📍 Finding your location... Please allow location access.');

    // Get user's current location
    navigator.geolocation.getCurrentPosition(
      async (position) => {
        const userLat = position.coords.latitude;
        const userLng = position.coords.longitude;
        
        try {
          // Show loading message
          alert('🔍 Searching for nearest charging station...');
          
          // Call backend API to find nearest station
          const response = await fetch('http://localhost:5000/api/find-nearest', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              latitude: userLat,
              longitude: userLng
            })
          });

          const result = await response.json();

          if (result.success) {
            // Success - show station details and open map
            const station = result.nearest_station;
            const userConfirmed = confirm(
              `📍 Nearest Station Found!\n\n` +
              `🏪 **${station.name}**\n` +
              `📏 **Distance:** ${result.distance_km} km\n` +
              `⏱️ **Drive Time:** ${result.estimated_drive_time}\n` +
              `🔌 **Available Slots:** ${station.available_slots}/${station.total_slots}\n` +
              `⚡ **Power:** ${station.power_kw} kW\n` +
              `💰 **Price:** ₹${station.price_per_kwh}/kWh\n\n` +
              `Open navigation map and get directions?`
            );

            if (userConfirmed) {
              // Open interactive navigation map
              window.open(
                `http://localhost:5000/api/navigation-map?lat=${userLat}&lng=${userLng}`,
                '_blank'
              );
              
              // Also open Google Maps for directions
              setTimeout(() => {
                window.open(result.google_maps_url, '_blank');
              }, 1000);
            }

          } else {
            // No available stations found
            const userConfirmed = confirm(
              `❌ No available charging stations found within 20km.\n\n` +
              `But we found ${result.alternative_stations?.length || 0} stations nearby.\n\n` +
              `Would you like to view all nearby stations on the map?`
            );

            if (userConfirmed) {
              window.open(
                `http://localhost:5000/api/navigation-map?lat=${userLat}&lng=${userLng}`,
                '_blank'
              );
            }
          }

        } catch (error) {
          console.error('Backend error:', error);
          alert(
            '🚨 Unable to connect to charging station service.\n\n' +
            'Please make sure:\n' +
            '1. The backend server is running (python app.py)\n' +
            '2. You are on http://localhost:5173\n' +
            '3. The backend is running on port 5000\n\n' +
            'Error: ' + error.message
          );
        }
      },
      (error) => {
        // Handle location errors
        let errorMessage = 'Unable to access your location. ';
        
        switch (error.code) {
          case error.PERMISSION_DENIED:
            errorMessage += 'Please allow location access in your browser settings to find nearby charging stations.';
            break;
          case error.POSITION_UNAVAILABLE:
            errorMessage += 'Location information is unavailable. Please check your device location services.';
            break;
          case error.TIMEOUT:
            errorMessage += 'Location request timed out. Please try again.';
            break;
          default:
            errorMessage += 'An unknown error occurred. Please try again.';
        }
        
        alert(errorMessage);
      },
      {
        enableHighAccuracy: true,
        timeout: 15000,
        maximumAge: 0
      }
    );
  };

  const handleViewAllStations = () => {
    // Directly open the comprehensive map without location
    window.open('http://localhost:5000/api/map/comprehensive', '_blank');
  };

  const handleDownloadData = () => {
    // Open ML data download
    window.open('http://localhost:5000/api/ml/data', '_blank');
  };

return (
  <div className="page">
    <Hyperspeed />
    
    <Dock 
      items={items}
      panelHeight={68}
      baseItemSize={50}
      magnification={70}
    />
    
    {/* Choose the level of transparency you prefer: */}
    
    {/* Option 1: Very subtle transparency */}
    <div className="subtle-transparent-container">
      <div className="star-border-container">
        <div className="description-text">
          Never run out of charge - find stations instantly
        </div>
        
        <StarBorder
          as="button"
          className="menu-button"
          color="cyan"
          speed="5s"
          onClick={handleFindNearestStation}
        >
          🔍 Find Nearest Station
        </StarBorder>

        <StarBorder
          as="button"
          className="menu-button"
          color="magenta"
          speed="5s"
          onClick={handleViewAllStations}
        >
          🗺️ View All Stations
        </StarBorder>

        <StarBorder
          as="button"
          className="menu-button"
          color="yellow"
          speed="5s"
          onClick={handleDownloadData}
        >
          📊 Download Data
        </StarBorder>
      </div>
    </div>
  </div>
);
};

export default Menu;