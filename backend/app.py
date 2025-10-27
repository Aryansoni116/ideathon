from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from dataclasses import dataclass, asdict
from typing import List, Dict
import random
import time
import threading
from geopy.distance import geodesic
import folium
from io import BytesIO
import json
import csv
from datetime import datetime

# Configuration
class Config:
    SECRET_KEY = 'ev-charging-location-based'
    CORS_ORIGINS = ["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:5173", "http://localhost:5174", "http://127.0.0.1:5173", "http://127.0.0.1:5174"]
    UPDATE_INTERVAL = 30
    JALANDHAR_COORDINATES = (31.3260, 75.5762)
    PHAGWARA_COORDINATES = (31.2249, 75.7705)

@dataclass
class ChargingStation:
    id: str
    name: str
    latitude: float
    longitude: float
    is_available: bool
    connector_type: str
    power_kw: float
    last_updated: float
    address: str
    price_per_kwh: float
    operator: str
    available_slots: int
    total_slots: int
    timestamp: str

class LocationBasedChargingService:
    def __init__(self):
        self.connector_types = ['Type2', 'CCS', 'CHAdeMO', 'Bharat DC-001']
        self.operators = ['Tata Power', 'BSES', 'Fortum', 'Magenta', 'EVRE']
        self.stations = self._generate_stations()
        
    def _generate_stations(self) -> List[ChargingStation]:
        locations = [
            # Jalandhar stations
            {'name': "Tata Power EV Station - Jalandhar City Center", 'lat': 31.3259, 'lng': 75.5792, 'address': "Near BMC Chowk, Jalandhar City"},
            {'name': "BSES Charging Point - Model Town", 'lat': 31.3387, 'lng': 75.5728, 'address': "Model Town Market, Jalandhar"},
            {'name': "EVRE Highway Charger - Nakodar Road", 'lat': 31.3125, 'lng': 75.5921, 'address': "NH-44, Nakodar Road"},
            {'name': "Fortum Quick Charge - Rama Mandi", 'lat': 31.3045, 'lng': 75.6138, 'address': "Rama Mandi Chowk, GT Road"},
            {'name': "Magenta Power Station - Khurla Kingra", 'lat': 31.2896, 'lng': 75.6382, 'address': "Khurla Kingra Village"},
            {'name': "BSES Express Charger - Bhogpur", 'lat': 31.2743, 'lng': 75.6627, 'address': "Bhogpur Bypass, NH-44"},
            {'name': "Tata Power Highway Hub - Adampur", 'lat': 31.2598, 'lng': 75.6894, 'address': "Adampur Doaba"},
            {'name': "EVRE Fast Charger - Maqsudan", 'lat': 31.2456, 'lng': 75.7128, 'address': "Maqsudan, GT Road"},
            {'name': "Fortum EV Station - Mithapur", 'lat': 31.2345, 'lng': 75.7453, 'address': "Mithapur Chowk"},
            {'name': "Magenta Power Charger - Phagwara Main", 'lat': 31.2249, 'lng': 75.7705, 'address': "Phagwara Bus Stand"}
        ]
        
        stations = []
        for i, loc in enumerate(locations, 1):
            available_slots = random.randint(0, 4)
            stations.append(ChargingStation(
                id=f"PB{i:03d}",
                name=loc['name'],
                latitude=loc['lat'],
                longitude=loc['lng'],
                is_available=available_slots > 0,
                connector_type=random.choice(self.connector_types),
                power_kw=random.choice([7.4, 15, 30, 50, 120]),
                last_updated=time.time(),
                address=loc['address'],
                price_per_kwh=round(random.uniform(12.5, 18.5), 2),
                operator=random.choice(self.operators),
                available_slots=available_slots,
                total_slots=4,
                timestamp=datetime.now().isoformat()
            ))
        return stations
    
    def find_nearest_station(self, user_lat: float, user_lng: float, max_distance_km: float = 20) -> Dict:
        """Find the nearest available charging station to user's location"""
        user_location = (user_lat, user_lng)
        nearest_station = None
        min_distance = float('inf')
        
        for station in self.stations:
            if station.is_available:  # Only consider available stations
                station_location = (station.latitude, station.longitude)
                distance = geodesic(user_location, station_location).kilometers
                
                if distance < min_distance and distance <= max_distance_km:
                    min_distance = distance
                    nearest_station = station
        
        if nearest_station:
            return {
                'success': True,
                'nearest_station': self._format_station_data(nearest_station, min_distance),
                'user_location': {'lat': user_lat, 'lng': user_lng},
                'distance_km': round(min_distance, 2),
                'estimated_drive_time': self._calculate_drive_time(min_distance),
                'google_maps_url': self._generate_google_maps_url(user_lat, user_lng, nearest_station.latitude, nearest_station.longitude)
            }
        else:
            return {
                'success': False,
                'message': 'No available charging stations found within 20km radius',
                'user_location': {'lat': user_lat, 'lng': user_lng},
                'alternative_stations': self._get_alternative_stations(user_lat, user_lng)
            }
    
    def _format_station_data(self, station: ChargingStation, distance: float) -> Dict:
        """Format station data for response"""
        return {
            'id': station.id,
            'name': station.name,
            'latitude': station.latitude,
            'longitude': station.longitude,
            'address': station.address,
            'connector_type': station.connector_type,
            'power_kw': station.power_kw,
            'available_slots': station.available_slots,
            'total_slots': station.total_slots,
            'price_per_kwh': station.price_per_kwh,
            'operator': station.operator,
            'distance_km': round(distance, 2),
            'is_available': station.is_available
        }
    
    def _calculate_drive_time(self, distance_km: float) -> str:
        """Calculate estimated drive time based on distance"""
        avg_speed = 40  # km/h in urban areas
        time_minutes = int((distance_km / avg_speed) * 60)
        return f"{time_minutes} minutes"
    
    def _generate_google_maps_url(self, from_lat: float, from_lng: float, to_lat: float, to_lng: float) -> str:
        """Generate Google Maps navigation URL"""
        return f"https://www.google.com/maps/dir/{from_lat},{from_lng}/{to_lat},{to_lng}"
    
    def _get_alternative_stations(self, user_lat: float, user_lng: float, count: int = 3) -> List[Dict]:
        """Get alternative stations (including unavailable ones) when no available stations found"""
        user_location = (user_lat, user_lng)
        all_stations = []
        
        for station in self.stations:
            station_location = (station.latitude, station.longitude)
            distance = geodesic(user_location, station_location).kilometers
            station_data = self._format_station_data(station, distance)
            all_stations.append(station_data)
        
        # Sort by distance and return top N
        return sorted(all_stations, key=lambda x: x['distance_km'])[:count]
    
    def get_nearby_stations(self, user_lat: float, user_lng: float, radius_km: float = 10) -> List[Dict]:
        """Get all stations within radius (both available and unavailable)"""
        user_location = (user_lat, user_lng)
        nearby_stations = []
        
        for station in self.stations:
            station_location = (station.latitude, station.longitude)
            distance = geodesic(user_location, station_location).kilometers
            
            if distance <= radius_km:
                station_data = self._format_station_data(station, distance)
                station_data['estimated_drive_time'] = self._calculate_drive_time(distance)
                nearby_stations.append(station_data)
        
        return sorted(nearby_stations, key=lambda x: x['distance_km'])
    
    def get_all_stations(self) -> List[ChargingStation]:
        return self.stations
    
    def get_stations_for_ml(self) -> List[Dict]:
        """Get stations data in ML-friendly format"""
        ml_data = []
        for station in self.stations:
            station_dict = asdict(station)
            # Add derived features for ML
            station_dict['utilization_rate'] = 1 - (station.available_slots / station.total_slots)
            station_dict['is_peak_hours'] = self._is_peak_hours()
            station_dict['day_of_week'] = datetime.now().weekday()
            station_dict['hour_of_day'] = datetime.now().hour
            ml_data.append(station_dict)
        return ml_data
    
    def _is_peak_hours(self) -> bool:
        """Check if current time is peak hours (for ML features)"""
        hour = datetime.now().hour
        return (7 <= hour <= 10) or (17 <= hour <= 20)
    
    def simulate_real_time_updates(self):
        """Update station availability in real-time"""
        for station in self.stations:
            if random.random() < 0.3:  # 30% chance of status change
                new_slots = random.randint(0, station.total_slots)
                station.available_slots = new_slots
                station.is_available = new_slots > 0
                station.last_updated = time.time()
                station.timestamp = datetime.now().isoformat()

class InteractiveMapGenerator:
    @staticmethod
    def create_location_based_map(user_lat: float, user_lng: float, nearest_station: Dict, all_nearby_stations: List[Dict]) -> folium.Map:
        """Create an interactive map showing user location and nearest station"""
        m = folium.Map(
            location=[user_lat, user_lng],
            zoom_start=13,
            tiles='OpenStreetMap'
        )
        
        # Add user location marker
        folium.Marker(
            [user_lat, user_lng],
            popup=folium.Popup(f"""
                <div style="width: 200px;">
                    <h4>📍 Your Location</h4>
                    <p>Lat: {user_lat:.4f}</p>
                    <p>Lng: {user_lng:.4f}</p>
                </div>
            """, max_width=250),
            icon=folium.Icon(color='blue', icon='user', prefix='fa'),
            tooltip="You are here"
        ).add_to(m)
        
        # Add nearest station marker
        if nearest_station:
            folium.Marker(
                [nearest_station['latitude'], nearest_station['longitude']],
                popup=folium.Popup(f"""
                    <div style="width: 250px;">
                        <h4>⚡ {nearest_station['name']}</h4>
                        <hr>
                        <p><b>Distance:</b> {nearest_station['distance_km']} km</p>
                        <p><b>Drive Time:</b> {nearest_station.get('estimated_drive_time', 'N/A')}</p>
                        <p><b>Slots:</b> {nearest_station['available_slots']}/{nearest_station['total_slots']}</p>
                        <p><b>Power:</b> {nearest_station['power_kw']} kW</p>
                        <p><b>Price:</b> ₹{nearest_station['price_per_kwh']}/kWh</p>
                        <p><b>Operator:</b> {nearest_station['operator']}</p>
                        <button onclick="window.open('{nearest_station.get('google_maps_url', '#')}', '_blank')" 
                                style="background: #4285f4; color: white; border: none; padding: 8px 16px; border-radius: 4px; cursor: pointer;">
                            🗺️ Get Directions
                        </button>
                    </div>
                """, max_width=300),
                icon=folium.Icon(color='green', icon='bolt', prefix='fa'),
                tooltip=f"Nearest Station - {nearest_station['distance_km']} km"
            ).add_to(m)
            
            # Add line from user to nearest station
            folium.PolyLine(
                [[user_lat, user_lng], [nearest_station['latitude'], nearest_station['longitude']]],
                color='green',
                weight=4,
                opacity=0.8,
                popup=f"Route to nearest station - {nearest_station['distance_km']} km"
            ).add_to(m)
        
        # Add other nearby stations
        for station in all_nearby_stations:
            if nearest_station and station['id'] != nearest_station.get('id'):
                color = 'orange' if station['is_available'] else 'red'
                icon = 'bolt' if station['is_available'] else 'times'
                
                folium.Marker(
                    [station['latitude'], station['longitude']],
                    popup=folium.Popup(f"""
                        <div style="width: 220px;">
                            <h5>{station['name']}</h5>
                            <p><b>Distance:</b> {station['distance_km']} km</p>
                            <p><b>Status:</b> {'🟢 Available' if station['is_available'] else '🔴 Occupied'}</p>
                            <p><b>Slots:</b> {station['available_slots']}/{station['total_slots']}</p>
                        </div>
                    """, max_width=250),
                    icon=folium.Icon(color=color, icon=icon, prefix='fa'),
                    tooltip=f"{station['name']} - {station['distance_km']} km"
                ).add_to(m)
        
        # Add info panel
        info_html = f"""
        <div style="position: fixed; top: 10px; left: 10px; z-index: 1000; background: white; padding: 10px; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.2); max-width: 300px;">
            <h4>🚗 EV Charging Navigator</h4>
            <p><b>Your Location:</b><br>Lat: {user_lat:.4f}<br>Lng: {user_lng:.4f}</p>
            {f'<p><b>Nearest Station:</b><br>{nearest_station["name"]}<br>Distance: {nearest_station["distance_km"]} km</p>' if nearest_station else '<p><b>No available stations nearby</b></p>'}
            <p><b>Nearby Stations:</b> {len(all_nearby_stations)} found</p>
        </div>
        """
        m.get_root().html.add_child(folium.Element(info_html))
        
        return m

    @staticmethod
    def create_comprehensive_map(stations: List[ChargingStation]) -> folium.Map:
        """Create a detailed Folium map with all stations"""
        center_lat = (Config.JALANDHAR_COORDINATES[0] + Config.PHAGWARA_COORDINATES[0]) / 2
        center_lng = (Config.JALANDHAR_COORDINATES[1] + Config.PHAGWARA_COORDINATES[1]) / 2
        
        m = folium.Map(
            location=[center_lat, center_lng],
            zoom_start=12,
            tiles='OpenStreetMap'
        )
        
        # Add route
        folium.PolyLine(
            [Config.JALANDHAR_COORDINATES, Config.PHAGWARA_COORDINATES],
            color='blue',
            weight=5,
            opacity=0.7,
            popup="Jalandhar-Phagwara Highway Route"
        ).add_to(m)
        
        # Add stations with detailed information
        for station in stations:
            color = 'green' if station.is_available else 'red'
            icon = 'bolt' if station.is_available else 'times'
            
            popup_html = f"""
            <div style="width: 280px;">
                <h4>{station.name}</h4>
                <hr>
                <p><b>Status:</b> <span style="color: {'green' if station.is_available else 'red'}">
                    {'🟢 Available' if station.is_available else '🔴 Occupied'}
                </span></p>
                <p><b>Slots:</b> {station.available_slots}/{station.total_slots}</p>
                <p><b>Utilization:</b> {(1 - station.available_slots/station.total_slots)*100:.1f}%</p>
                <p><b>Connector:</b> {station.connector_type}</p>
                <p><b>Power:</b> {station.power_kw} kW</p>
                <p><b>Price:</b> ₹{station.price_per_kwh}/kWh</p>
                <p><b>Operator:</b> {station.operator}</p>
                <p><b>Last Updated:</b> {datetime.fromtimestamp(station.last_updated).strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
            """
            
            folium.Marker(
                [station.latitude, station.longitude],
                popup=folium.Popup(popup_html, max_width=300),
                tooltip=f"{station.name} - {station.available_slots}/{station.total_slots} slots",
                icon=folium.Icon(color=color, icon=icon, prefix='fa')
            ).add_to(m)
        
        return m

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Fix CORS - Allow all origins during development
CORS(app)

# Initialize services
charging_service = LocationBasedChargingService()
map_generator = InteractiveMapGenerator()

# API Routes
@app.route('/')
def home():
    return jsonify({
        'message': 'EV Charging Station Location-Based Service',
        'endpoints': {
            '/': 'API information',
            '/api/stations': 'Get all stations data',
            '/api/stations/ml': 'Get ML-ready station data',
            '/api/find-nearest': 'Find nearest charging station (POST with lat/lng)',
            '/api/nearby-stations': 'Get all nearby stations (GET with lat/lng)',
            '/api/navigation-map': 'Get interactive navigation map',
            '/api/map/comprehensive': 'Get comprehensive station map',
            '/api/ml/data': 'Download ML dataset',
            '/api/directions': 'Get Google Maps directions'
        }
    })

@app.route('/api/stations', methods=['GET'])
def get_all_stations():
    """Get all stations data"""
    stations = charging_service.get_all_stations()
    return jsonify([asdict(station) for station in stations])

@app.route('/api/stations/ml', methods=['GET'])
def get_ml_stations():
    """Get stations data in ML-ready format"""
    ml_data = charging_service.get_stations_for_ml()
    return jsonify(ml_data)

@app.route('/api/find-nearest', methods=['POST'])
def find_nearest_station():
    """Find the nearest available charging station to user's location"""
    try:
        data = request.get_json()
        
        if not data or 'latitude' not in data or 'longitude' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing location data',
                'message': 'Please provide latitude and longitude in the request body'
            }), 400
        
        user_lat = float(data['latitude'])
        user_lng = float(data['longitude'])
        
        # Validate coordinates
        if not (-90 <= user_lat <= 90) or not (-180 <= user_lng <= 180):
            return jsonify({
                'success': False,
                'error': 'Invalid coordinates',
                'message': 'Please provide valid latitude (-90 to 90) and longitude (-180 to 180)'
            }), 400
        
        # Find nearest station
        result = charging_service.find_nearest_station(user_lat, user_lng)
        
        return jsonify(result)
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': 'Invalid data format',
            'message': 'Please provide valid numeric coordinates'
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Server error',
            'message': str(e)
        }), 500

@app.route('/api/nearby-stations', methods=['GET'])
def get_nearby_stations():
    """Get all stations near user's location"""
    try:
        user_lat = float(request.args.get('lat', Config.JALANDHAR_COORDINATES[0]))
        user_lng = float(request.args.get('lng', Config.JALANDHAR_COORDINATES[1]))
        radius = float(request.args.get('radius', 15))
        
        stations = charging_service.get_nearby_stations(user_lat, user_lng, radius)
        
        return jsonify({
            'success': True,
            'user_location': {'lat': user_lat, 'lng': user_lng},
            'radius_km': radius,
            'stations': stations,
            'total_stations': len(stations),
            'available_stations': len([s for s in stations if s['is_available']])
        })
        
    except ValueError:
        return jsonify({'success': False, 'error': 'Invalid coordinates'}), 400

@app.route('/api/navigation-map', methods=['GET'])
def get_navigation_map():
    """Get interactive map with user location and nearest station"""
    try:
        user_lat = float(request.args.get('lat', Config.JALANDHAR_COORDINATES[0]))
        user_lng = float(request.args.get('lng', Config.JALANDHAR_COORDINATES[1]))
        
        # Find nearest station
        nearest_result = charging_service.find_nearest_station(user_lat, user_lng)
        nearest_station = nearest_result.get('nearest_station')
        nearby_stations = charging_service.get_nearby_stations(user_lat, user_lng, 15)
        
        # Create map
        m = map_generator.create_location_based_map(user_lat, user_lng, nearest_station, nearby_stations)
        
        map_bytes = BytesIO()
        m.save(map_bytes, close_file=False)
        map_bytes.seek(0)
        
        return send_file(
            map_bytes, 
            mimetype='text/html', 
            download_name='ev_charging_navigation_map.html'
        )
        
    except ValueError:
        return jsonify({'success': False, 'error': 'Invalid coordinates'}), 400

@app.route('/api/map/comprehensive', methods=['GET'])
def get_comprehensive_map():
    """Get detailed Folium map with all stations"""
    stations = charging_service.get_all_stations()
    m = map_generator.create_comprehensive_map(stations)
    
    map_bytes = BytesIO()
    m.save(map_bytes, close_file=False)
    map_bytes.seek(0)
    
    return send_file(map_bytes, mimetype='text/html', download_name='ev_charging_comprehensive_map.html')

@app.route('/api/ml/data', methods=['GET'])
def download_ml_data():
    """Download complete ML dataset as CSV"""
    ml_data = charging_service.get_stations_for_ml()
    
    # Create CSV manually without pandas
    if not ml_data:
        return jsonify({'error': 'No data available'}), 400
    
    # Create CSV in memory
    output = BytesIO()
    writer = csv.writer(output)
    
    # Write header
    if ml_data:
        writer.writerow(ml_data[0].keys())
    
    # Write data rows
    for row in ml_data:
        writer.writerow(row.values())
    
    output.seek(0)
    
    return send_file(
        output,
        mimetype='text/csv',
        download_name=f'ev_charging_ml_data_{datetime.now().strftime("%Y%m%d_%H%M")}.csv',
        as_attachment=True
    )

@app.route('/api/directions', methods=['GET'])
def get_directions():
    """Generate Google Maps directions URL"""
    try:
        from_lat = float(request.args.get('from_lat'))
        from_lng = float(request.args.get('from_lng'))
        to_lat = float(request.args.get('to_lat'))
        to_lng = float(request.args.get('to_lng'))
        
        maps_url = f"https://www.google.com/maps/dir/{from_lat},{from_lng}/{to_lat},{to_lng}"
        
        return jsonify({
            'success': True,
            'navigation_url': maps_url,
            'from': {'lat': from_lat, 'lng': from_lng},
            'to': {'lat': to_lat, 'lng': to_lng},
            'message': 'Open this URL in Google Maps for turn-by-turn directions'
        })
        
    except (ValueError, TypeError):
        return jsonify({'success': False, 'error': 'Invalid coordinates for directions'}), 400

# Background updates
def background_updates():
    while True:
        time.sleep(Config.UPDATE_INTERVAL)
        charging_service.simulate_real_time_updates()

# Start background thread
update_thread = threading.Thread(target=background_updates, daemon=True)
update_thread.start()

# Production configuration
class ProductionConfig:
    SECRET_KEY = 'your-production-secret-key-change-this'
    CORS_ORIGINS = [
        "http://localhost:3000",
        "http://localhost:5173", 
        "https://aryansoni116.github.io"  # Your GitHub Pages frontend
    ]

# Use production config in production
if __name__ == '__main__':
    import os
    if os.environ.get('RENDER'):
        app.config.from_object(ProductionConfig)
        print("🚀 Running in production mode on Render")
    else:
        app.config.from_object(Config)
        print("🔧 Running in development mode")
    
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
