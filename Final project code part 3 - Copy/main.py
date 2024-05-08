import base64
from datetime import datetime
import json
import random
from flask_socketio import SocketIO, emit
import time
from flask import Flask, flash, jsonify, redirect, render_template, request, send_file
import requests
import random
import time
from flask import render_template
from apscheduler.schedulers.background import BackgroundScheduler
# pip install apscheduler
# pip install flask-socketio



app = Flask(__name__)
socketio = SocketIO(app)
app.secret_key = '5765878775'
# @app.route('/')
# def dashboard():
#     # Define your static data here
#     fleet_data = [
#         {"id":"123","make": "Mercedes", "model":"Benz Smart EQ Fortwo","status": "On-trip"},
#         {"id":"456","make": "Porsche","model":" Fortwo" ,"status": "Offline"},
#         {"id":"789","make": "Porsche1","model":" Fortwo1" ,"status": "Online"},
#         # Add more entries as needed...
#     ]
#     # from cookies pass driver id and get vehicle id and vehicle details then for each veg=hicle get current longitute and latitude
#     coordinates = [
#     {"id": "123", "latitude": 37.7749, "longitude": -74.4194},
#     {"id": "456", "latitude": 40.7749, "longitude": -74.4194},
#     {"id": "789", "latitude": 42.7749, "longitude": -74.4194},
#     # Add more coordinates here as needed
# ]

    
#     return render_template('driver_dashboard.html', fleet=fleet_data,coordinates_json=coordinates)

@app.route('/vehicle-details/<vehicle_id>')
def vehicle_details(vehicle_id):
    fleet_data = [
        {
            "id": "123",
            "make": "Mercedes",
            "model": "Benz Smart EQ Fortwo",
            "status": "On-trip",
            "sensors": [
                {'type': 'Temperature', 'status': 'Healthy'},
                {'type': 'Pressure', 'status': 'Faulty'},
                {'type': 'Speed', 'status': 'Healthy'},
            ],
            "current_trip": {
                'Trip_id':'Trip_123',
                'source': 'Trip Source 1',
                'destination': 'Trip Destination 1',
                'occupancy': 2,
                'start_time': '2024-04-22 08:00:00',
                'completed': False
            },
            "all_trips": [
                {   'Trip_id':'Trip_id',
                    'source': 'Trip Source 2',
                    'destination': 'Trip Destination 2',
                    'occupancy': 3,
                    'start_time': '2024-04-21 10:00:00',
                    'completed': True,
                    'end_time': '2024-04-21 12:00:00'
                }
            ],
            "maintenance_records": [
        {
            "service_date": "2024-04-20",
            "tires_rotated": True,
            "air_filter_changed": False,
            "battery_status": "Good",
            "breaks_replaced": True,
            "oil_changed": True,
            "wiper_changed": False,
            "wiper_fluid_changed": True,
            "tires_changed": False
        },
        
    ]

        },
        {
            "id": "456",
            "make": "Porsche",
            "model": "Fortwo",
            "status": "Offline",
            "sensors": [
                {'type': 'Temperature', 'status': 'Faulty'},
                {'type': 'Pressure', 'status': 'Healthy'},
            ],
            "current_trip": None,
            "all_trips": [],
            "maintenance_records": [
        {
            "service_date": "2024-04-20",
            "tires_rotated": True,
            "air_filter_changed": False,
            "battery_status": "Good",
            "breaks_replaced": True,
            "oil_changed": True,
            "wiper_changed": False,
            "wiper_fluid_changed": True,
            "tires_changed": False
        },
        
    ]
        },
        {
            "id": "789",
            "make": "Porsche1",
            "model": "Fortwo1",
            "status": "On-Trip",
            "sensors": [
                {'type': 'Temperature', 'status': 'Healthy'},
                {'type': 'Speed', 'status': 'Faulty'},
            ],
            "current_trip": None,
            "all_trips": [
                {   'Trip_id':'Trip_789',
                    'source': 'Trip Source 3',
                    'destination': 'Trip Destination 3',
                    'occupancy': 4,
                    'start_time': '2024-04-20 09:00:00',
                    'completed': True,
                    'end_time': '2024-04-20 11:00:00'
                }
            ],
            "maintenance_records": [
        {
            "service_date": "2024-04-20",
            "tires_rotated": True,
            "air_filter_changed": False,
            "battery_status": "Good",
            "breaks_replaced": True,
            "oil_changed": True,
            "wiper_changed": False,
            "wiper_fluid_changed": True,
            "tires_changed": False
        },
        
    ]
        },
        
    ]

    vehicle = next((v for v in fleet_data if v['id'] == vehicle_id), None)
    if vehicle:
        return render_template('vehicle_details.html', vehicle=vehicle)
    else:
        return "Vehicle not found", 404
    
# Dummy data for real-time sensor and trip status updates
# when you load first time the realdata 

@app.route('/getRealTimeData/<trip_id>')
def get_real_time_data(trip_id):
    print(trip_id)
    sensor_data = [
    {"trip_id": "Trip_123", "sensor_id": "1", "timestamp": time.time(), "vehicle_id": "123", 
     "status": "Healthy", "value": random.randint(1, 100)},
    {"trip_id": "Trip_123", "sensor_id": "2", "timestamp": time.time(), "vehicle_id": "123", 
     "status": "Faulty", "value": random.randint(1, 100)},
    # Add more sensor data as needed
]
    

    trip_status_data = [
        {"trip_id": "Trip_123", "timestamp": time.time(), "location_lat": random.uniform(-90, 90), 
         "location_lon": random.uniform(-180, 180), "battery_level": random.uniform(0, 100), "speed": random.uniform(0, 120), 
        "acceleration": random.uniform(-10, 10), "engine_temp": random.uniform(60, 120), 
        "engine_rpm": random.randint(1000, 5000), "ismoving": random.choice([True, False]), 
        "iscrashed": random.choice([True, False]), "moving_direction": random.uniform(0, 360), 
        "distance_completed": random.uniform(0, 1000), "isturning": random.choice([True, False]), 
        "angle_turn": random.uniform(-180, 180), "left_turn_signal": random.choice([True, False]), 
        "right_turn_signal": random.choice([True, False])},
        # Add more trip status data as needed
    ]
    coordinates = [
        {"id": "123", "latitude": 37.7749, "longitude": -74.4194},
        {"id": "456", "latitude": 40.7749, "longitude": -74.4194},
        {"id": "789", "latitude": 42.7749, "longitude": -74.4194},
        # Add more coordinates here as needed
    ]
    trip_details = [{"id": "133"}]
    trip_details_json = json.dumps(trip_details)
    # Filter sensor data and trip status data by trip ID
    trip_sensor_data = [sensor for sensor in sensor_data if sensor["trip_id"] == trip_id]
    trip_status_data = [trip for trip in trip_status_data if trip["trip_id"] == trip_id]
    trip_status_data_jsonify=jsonify({
        "sensor_data": sensor_data,
        "trip_status_data": trip_status_data
    })
    # Return the filtered data
    return render_template('real_trip_details_trial3.html', sensor_data=trip_sensor_data, 
                           trip_status_data=trip_status_data,coordinates_json=coordinates,trip_id=trip_id,trip_status_data_jsonify=trip_status_data_jsonify)
# when you load 5 sec time the realdata 
@app.route('/getRealTimeDataJSON/<trip_id>')
def get_real_time_data_json(trip_id):
    trip_status_data={"trip_id": "Trip_123", "timestamp": time.time(), "location_lat": random.uniform(-90, 90), 
         "location_lon": random.uniform(-180, 180), "battery_level": random.uniform(0, 100), "speed": random.uniform(0, 120), 
        "acceleration": random.uniform(-10, 10), "engine_temp": random.uniform(60, 120), 
        "engine_rpm": random.randint(1000, 5000), "ismoving": random.choice([True, False]), 
        "iscrashed": random.choice([True, False]), "moving_direction": random.uniform(0, 360), 
        "distance_completed": random.uniform(0, 1000), "isturning": random.choice([True, False]), 
        "angle_turn": random.uniform(-180, 180), "left_turn_signal": random.choice([True, False]), 
        "right_turn_signal": random.choice([True, False])}
    return jsonify(trip_status_data)

@app.route('/register')
def registration():
    return render_template('registerAV.html')

@app.route('/registerAV', methods=['GET', 'POST'])
def register():
    
        # Here you retrieve the data from the form
        make = request.form['make']
        print(make)
        model = request.form['model']
        registrationDate = request.form['registrationDate']
        manufacturer = request.form['manufacturer']
        vin = request.form['vin']

        # Perform your validation and data storage here
        # ...

        # If everything is ok, flash a success message
        flash('Vehicle Registration Successful!!')

        fleet_data = [
        {"id":"123","make": "Mercedes", "model":"Benz Smart EQ Fortwo","status": "On-trip"},
        {"id":"456","make": "Porsche","model":" Fortwo" ,"status": "Offline"},
        {"id":"789","make": "Porsche1","model":" Fortwo1" ,"status": "Online"},
        # Add more entries as needed...
                    ]
        # from cookies pass driver id and get vehicle id and vehicle details then for each veg=hicle get current longitute and latitude
        coordinates = [
            {"id": "123", "latitude": 37.7749, "longitude": -74.4194},
            {"id": "456", "latitude": 40.7749, "longitude": -74.4194},
            {"id": "789", "latitude": 42.7749, "longitude": -74.4194},
            # Add more coordinates here as needed
        ]


    # If it's a GET request, just render the registration form
        return render_template('registerAV.html', message="Registration Successful!!")
@app.route('/add-maintenance-record/<vehicle_id>', methods=['GET'])
def add_maintenance_record(vehicle_id):
    # Pass the vehicle_id to the template
    return render_template('add_maintenance_record.html', vehicle_id=vehicle_id)

@app.route('/submit-maintenance-record/<vehicle_id>', methods=['POST'])
def submit_maintenance_record(vehicle_id):
    # Extract form data from request.form and save the record
    service_date = request.form['serviceDate']
    tires_rotated = 'tiresRotated' in request.form
    # Save the data to the database or wherever it needs to go

    # Redirect to the vehicle details page or display success message
    flash('Maintenance record added successfully!')
    return render_template('add_maintenance_record.html', message="Successfully Maintenance Record is Added")

@app.route('/add-sensor/<vehicle_id>')
def add_sensor(vehicle_id):
    # You would have logic here to ensure the vehicle exists, etc.
    return render_template('add_sensor.html', vehicle_id=vehicle_id)
@app.route('/submit-sensor/<vehicle_id>', methods=['POST'])
def submit_sensor_record(vehicle_id):
   
    #
    return render_template('add_sensor.html', message="Successfully Sensor Record is Added")
# ################### Admin dashboard ################################
@app.route('/')
def dashboard():
#     # Define your static data here
#     fleet_data = [
#         {"id":"123","make": "Mercedes", "model":"Benz Smart EQ Fortwo","status": "On-trip"},   
#         {"id":"456","make": "Porsche","model":" Fortwo" ,"status": "Offline"},
#         {"id":"789","make": "Porsche1","model":" Fortwo1" ,"status": "Online"},
#         {"id":"1011","make": "Porsche2","model":" Fortwo2" ,"status": "On-trip"},
#         {"id":"1213","make": "Porsche3","model":" Fortwo3" ,"status": "On-trip"},
#         {"id":"1415","make": "Mercedes1", "model":"Benz Smart EQ Fortwo","status": "On-trip"},
#         # Add more entries as needed...
#     ]
#     # from cookies pass driver id and get vehicle id and vehicle details then for each veg=hicle get current longitute and latitude
#     coordinates = [
#     {"id": "123", "latitude": 37.7749, "longitude": -74.4194},
#     {"id": "456", "latitude": 40.7749, "longitude": -74.4194},
#     {"id": "789", "latitude": 42.7749, "longitude": -74.4194},
#     {"id": "1011", "latitude": 45.7749, "longitude": -74.4194},
#     {"id": "1213", "latitude": 41.7749, "longitude": -74.4194},
#     {"id": "1415", "latitude": 60.7749, "longitude": -74.4194},
#     # Add more coordinates here as needed
# ]

    
#     return render_template('admin_dashboard.html', fleet=fleet_data,coordinates_json=coordinates)
    return render_template('login.html')

@app.route('/vehicle-details-admin/<vehicle_id>')
def vehicle_details_admin(vehicle_id):
    fleet_data = [
        {
            "id": "123",
            "make": "Mercedes",
            "model": "Benz Smart EQ Fortwo",
            "status": "On-trip",
            "sensors": [
                {'type': 'Temperature', 'status': 'Healthy'},
                {'type': 'Pressure', 'status': 'Faulty'},
                {'type': 'Speed', 'status': 'Healthy'},
            ],
            "current_trip": {
                'Trip_id':'Trip_123',
                'source': 'Trip Source 1',
                'destination': 'Trip Destination 1',
                'occupancy': 2,
                'start_time': '2024-04-22 08:00:00',
                'completed': False
            },
            "all_trips": [
                {   'Trip_id':'Trip_id',
                    'source': 'Trip Source 2',
                    'destination': 'Trip Destination 2',
                    'occupancy': 3,
                    'start_time': '2024-04-21 10:00:00',
                    'completed': True,
                    'end_time': '2024-04-21 12:00:00'
                }
            ],
            "maintenance_records": [
        {
            "service_date": "2024-04-20",
            "tires_rotated": True,
            "air_filter_changed": False,
            "battery_status": "Good",
            "breaks_replaced": True,
            "oil_changed": True,
            "wiper_changed": False,
            "wiper_fluid_changed": True,
            "tires_changed": False
        },
        
    ]

        },
        {
            "id": "456",
            "make": "Porsche",
            "model": "Fortwo",
            "status": "Offline",
            "sensors": [
                {'type': 'Temperature', 'status': 'Faulty'},
                {'type': 'Pressure', 'status': 'Healthy'},
            ],
            "current_trip": None,
            "all_trips": [],
            "maintenance_records": [
        {
            "service_date": "2024-04-20",
            "tires_rotated": True,
            "air_filter_changed": False,
            "battery_status": "Good",
            "breaks_replaced": True,
            "oil_changed": True,
            "wiper_changed": False,
            "wiper_fluid_changed": True,
            "tires_changed": False
        },
        
    ]
        },
        {
            "id": "789",
            "make": "Porsche1",
            "model": "Fortwo1",
            "status": "Online",
            "sensors": [
                {'type': 'Temperature', 'status': 'Healthy'},
                {'type': 'Speed', 'status': 'Faulty'},
            ],
            "current_trip": None,
            "all_trips": [
                {   'Trip_id':'Trip_789',
                    'source': 'Trip Source 3',
                    'destination': 'Trip Destination 3',
                    'occupancy': 4,
                    'start_time': '2024-04-20 09:00:00',
                    'completed': True,
                    'end_time': '2024-04-20 11:00:00'
                }
            ],
            "maintenance_records": [
        {
            "service_date": "2024-04-20",
            "tires_rotated": True,
            "air_filter_changed": False,
            "battery_status": "Good",
            "breaks_replaced": True,
            "oil_changed": True,
            "wiper_changed": False,
            "wiper_fluid_changed": True,
            "tires_changed": False
        },
        
    ]
        },
        {"id":"1011",
         "make": "Porsche2",
         "model":" Fortwo2" ,
         "status": "On-trip",
         "sensors": [
                {'type': 'Temperature', 'status': 'Healthy'},
                {'type': 'Pressure', 'status': 'Faulty'},
                {'type': 'Speed', 'status': 'Healthy'},
            ],
            "current_trip": {
                'Trip_id':'Trip_123',
                'source': 'Trip Source 1',
                'destination': 'Trip Destination 1',
                'occupancy': 2,
                'start_time': '2024-04-22 08:00:00',
                'completed': False
            },
            "all_trips": [
                {   'Trip_id':'Trip_id',
                    'source': 'Trip Source 2',
                    'destination': 'Trip Destination 2',
                    'occupancy': 3,
                    'start_time': '2024-04-21 10:00:00',
                    'completed': True,
                    'end_time': '2024-04-21 12:00:00'
                }
            ],
            "maintenance_records": [
        {
            "service_date": "2024-04-20",
            "tires_rotated": True,
            "air_filter_changed": False,
            "battery_status": "Good",
            "breaks_replaced": True,
            "oil_changed": True,
            "wiper_changed": False,
            "wiper_fluid_changed": True,
            "tires_changed": False
        },
            ]
         
        },

        {"id":"1213","make": "Porsche3","model":" Fortwo3" ,"status": "On-trip",
         "sensors": [
                {'type': 'Temperature', 'status': 'Healthy'},
                {'type': 'Pressure', 'status': 'Faulty'},
                {'type': 'Speed', 'status': 'Healthy'},
            ],
            "current_trip": {
                'Trip_id':'Trip_1213',
                'source': 'Trip Source 1',
                'destination': 'Trip Destination 1',
                'occupancy': 2,
                'start_time': '2024-04-22 08:00:00',
                'completed': False
            },
            "all_trips": [
                {   'Trip_id':'Trip_id',
                    'source': 'Trip Source 2',
                    'destination': 'Trip Destination 2',
                    'occupancy': 3,
                    'start_time': '2024-04-21 10:00:00',
                    'completed': True,
                    'end_time': '2024-04-21 12:00:00'
                }
            ],
            "maintenance_records": [
        {
            "service_date": "2024-04-20",
            "tires_rotated": True,
            "air_filter_changed": False,
            "battery_status": "Good",
            "breaks_replaced": True,
            "oil_changed": True,
            "wiper_changed": False,
            "wiper_fluid_changed": True,
            "tires_changed": False
        },]
        },

        {"id":"1415","make": "Mercedes1", "model":"Benz Smart EQ Fortwo","status": "On-trip",
         "sensors": [
                {'type': 'Temperature', 'status': 'Healthy'},
                {'type': 'Pressure', 'status': 'Faulty'},
                {'type': 'Speed', 'status': 'Healthy'},
            ],
            "current_trip": {
                'Trip_id':'Trip_1214',
                'source': 'Trip Source 1',
                'destination': 'Trip Destination 1',
                'occupancy': 2,
                'start_time': '2024-04-22 08:00:00',
                'completed': False
            },
            "all_trips": [
                {   'Trip_id':'Trip_id',
                    'source': 'Trip Source 2',
                    'destination': 'Trip Destination 2',
                    'occupancy': 3,
                    'start_time': '2024-04-21 10:00:00',
                    'completed': True,
                    'end_time': '2024-04-21 12:00:00'
                }
            ],
            "maintenance_records": [
        {
            "service_date": "2024-04-20",
            "tires_rotated": True,
            "air_filter_changed": False,
            "battery_status": "Good",
            "breaks_replaced": True,
            "oil_changed": True,
            "wiper_changed": False,
            "wiper_fluid_changed": True,
            "tires_changed": False
        },]
        },
        
    ]

    vehicle = next((v for v in fleet_data if v['id'] == vehicle_id), None)
    if vehicle:
        return render_template('vehicle_details.html', vehicle=vehicle)
    else:
        return "Vehicle not found", 404

@app.route('/registerAVbyadmin', methods=['GET', 'POST'])
def registerbyadmin():
    
        # Here you retrieve the data from the form
        make = request.form['make']
        print(make)
        model = request.form['model']
        registrationDate = request.form['registrationDate']
        manufacturer = request.form['manufacturer']
        vin = request.form['vin']

        # Perform your validation and data storage here
        # ...

        # If everything is ok, flash a success message
        flash('Vehicle Registration Successful!!')

        # fleet_data = [
        # {"id":"123","make": "Mercedes", "model":"Benz Smart EQ Fortwo","status": "On-trip"},
        # {"id":"456","make": "Porsche","model":" Fortwo" ,"status": "Offline"},
        # {"id":"789","make": "Porsche1","model":" Fortwo1" ,"status": "Online"},
        # # Add more entries as needed...
        #             ]
        # # from cookies pass driver id and get vehicle id and vehicle details then for each veg=hicle get current longitute and latitude
        # coordinates = [
        #     {"id": "123", "latitude": 37.7749, "longitude": -74.4194},
        #     {"id": "456", "latitude": 40.7749, "longitude": -74.4194},
        #     {"id": "789", "latitude": 42.7749, "longitude": -74.4194},
        #     # Add more coordinates here as needed
        # ]


    # If it's a GET request, just render the registration form
        return render_template('registerAVbyadmin.html', message="Registration Successful!!")
@app.route('/registerbyadmin')
def registrationbyadmin():
    return render_template('registerAvbyadmin.html')   

import matplotlib.pyplot as plt
import io



# Sample data for the bar chart
dates = ['2024-04-20', '2024-04-21', '2024-04-22']
utilization = [8, 6, 7]  # Sample utilization values for each day

# Sample data for demonstration
vehicle_status_data = {
    "offline": 10,
    "on_trip": 20,
    "online": 30
}

utilization_data = {
    "labels": ["Day 1", "Day 2", "Day 3", "Day 4", "Day 5"],
    "utilization": [5, 8, 7, 9, 6]
}

distance_data = {
    "labels": ["Day 1", "Day 2", "Day 3", "Day 4", "Day 5"],
    "distance": [50, 70, 60, 80, 65]
}

@app.route('/analytics')
def index():
    return render_template('analytics.html')
@app.route('/alerts')
def alerts():
    return render_template('alerts.html')

@app.route('/vehicle-status-distribution')
def vehicle_status_distribution():
    return jsonify(vehicle_status_data)

@app.route('/average-utilization')
def average_utilization():
    return jsonify(utilization_data)

@app.route('/distance-travelled')
def distance_travelled():
    return jsonify(distance_data)

@app.route('/viewalldrivers')
def viewdrivers():
    return render_template('viewalldrivers.html')
@app.route('/registeruser')
def registerusers():
    return render_template('userregister.html')
@app.route('/viewprofile')
def viewprofile():
    return render_template('profile.html')
@app.route('/submit-login',methods=['GET', 'POST'])
def login():
    users = {
    "admin_user": {"username": "admin_user", "password": "adminpass", "role": "admin"},
    "driver_user": {"username": "driver_user", "password": "driverpass", "role": "driver"}
}
    username = request.form['username']
    password = request.form['password']

    # Check if user exists and password is correct
    user = users.get(username)
    if user and user['password'] == password:
        # Redirect based on role
        if user['role'] == 'admin':
            return redirect('/admin-dashboard')
        elif user['role'] == 'driver':
            return redirect('/driver-dashboard')
    else:
        return "Invalid credentials", 401
    return render_template('profile.html')

@app.route('/submit-registration', methods=['POST','GET'])
def registrations():
    return render_template('login.html')

@app.route('/admin-dashboard')
def admin_dashboard():
    # Define your static data here
    fleet_data = [
        {"id":"123","make": "Mercedes", "model":"Benz Smart EQ Fortwo","status": "On-trip"},   
        {"id":"456","make": "Porsche","model":" Fortwo" ,"status": "Offline"},
        {"id":"789","make": "Porsche1","model":" Fortwo1" ,"status": "Online"},
        {"id":"1011","make": "Porsche2","model":" Fortwo2" ,"status": "On-trip"},
        {"id":"1213","make": "Porsche3","model":" Fortwo3" ,"status": "On-trip"},
        {"id":"1415","make": "Mercedes1", "model":"Benz Smart EQ Fortwo","status": "On-trip"},
        # Add more entries as needed...
    ]
    # from cookies pass driver id and get vehicle id and vehicle details then for each veg=hicle get current longitute and latitude
    coordinates = [
    {"id": "123", "latitude": 37.7749, "longitude": -74.4194},
    {"id": "456", "latitude": 40.7749, "longitude": -74.4194},
    {"id": "789", "latitude": 42.7749, "longitude": -74.4194},
    {"id": "1011", "latitude": 45.7749, "longitude": -74.4194},
    {"id": "1213", "latitude": 41.7749, "longitude": -74.4194},
    {"id": "1415", "latitude": 60.7749, "longitude": -74.4194},
    # Add more coordinates here as needed
]

    
    return render_template('admin_dashboard.html', fleet=fleet_data,coordinates_json=coordinates)
   

@app.route('/driver-dashboard')
def driver_dashboard():
    fleet_data = [
        {"id":"123","make": "Mercedes", "model":"Benz Smart EQ Fortwo","status": "On-trip"},
        {"id":"456","make": "Porsche","model":" Fortwo" ,"status": "Offline"},
        {"id":"789","make": "Porsche1","model":" Fortwo1" ,"status": "On-trip"},
        # Add more entries as needed...
    ]
    # from cookies pass driver id and get vehicle id and vehicle details then for each veg=hicle get current longitute and latitude
    coordinates = [
    {"id": "123", "latitude": 37.7749, "longitude": -74.4194},
    {"id": "456", "latitude": 40.7749, "longitude": -74.4194},
    {"id": "789", "latitude": 42.7749, "longitude": -74.4194},
    # Add more coordinates here as needed
]

    
    return render_template('driver_dashboard.html', fleet=fleet_data,coordinates_json=coordinates)

@app.route('/create-trip')
def create_trip():
    return render_template('createtrip.html')
@app.route('/submit-trip', methods=['POST','GET'])
def submit_trip():
    # Here you would handle saving the trip data to your database or backend system
    
    # Add logic to save the trip details
    return render_template('createtrip.html',message="Trip Created Successfully")

alerts = []
THRESHOLD_SPEED = 1000000
THRESHOLD_BATTERY = 20000000

# Fetch trip information via API
def fetch_real_time_trip_info():
    # Static data for multiple trips of one driver
    driver_id = "Driver_1"
    trips = []
    for trip_num in range(1, 6):  # Assume 5 trips for demonstration
        trip = {
            "driver_id": driver_id,
            "trip_id": f"Trip_{trip_num}",
            "timestamp": time.time(),
            "location_lat": random.uniform(-90, 90),
            "location_lon": random.uniform(-180, 180),
            "battery_level": random.uniform(0, 10),
            "speed": random.uniform(0, 120),
            "acceleration": random.uniform(-10, 10),
            "engine_temp": random.uniform(60, 120),
            "engine_rpm": random.randint(1000, 5000),
            "ismoving": random.choice([True, False]),
            "iscrashed": random.choice([True, False]),
            "moving_direction": random.uniform(0, 360),
            "distance_completed": random.uniform(0, 1000),
            "isturning": random.choice([True, False]),
            "angle_turn": random.uniform(-180, 180),
            "left_turn_signal": random.choice([True, False]),
            "right_turn_signal": random.choice([True, False])
        }
        trips.append(trip)

    # Check for threshold crossings
    for trip in trips:
        if trip['speed'] > THRESHOLD_SPEED:
            alerts.append(f"High speed detected for {driver_id} on Trip {trip['trip_id']}")
            emit_alert(f"High speed detected for {driver_id} on Trip {trip['trip_id']}")
        if trip['battery_level'] > THRESHOLD_BATTERY:
            alerts.append(f"Low battery level for {driver_id} on Trip {trip['trip_id']}")
            # print(alerts)
            emit_alert(f"High speed detected for {driver_id} on Trip {trip['trip_id']}")
def emit_alert(alert):
   
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    socketio.emit('new_alert', {'alert': alert, 'timestamp': timestamp})
# Initialize scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(fetch_real_time_trip_info, 'interval', seconds=5)
scheduler.start()

if __name__ == '__main__':
    app.run(debug=True)
# ******************for alerts******************
# from flask import Flask, render_template
# from apscheduler.schedulers.background import BackgroundScheduler
# import requests

# app = Flask(__name__)

# # Sample threshold values
# THRESHOLD_SPEED = 80  # Example: Speed threshold in km/h
# THRESHOLD_BATTERY = 20  # Example: Battery level threshold in percent

# alerts = []

# def fetch_real_time_trip_info():
#     # Fetch trip information via API
#     # Replace 'YOUR_API_ENDPOINT' with the actual endpoint
#     response = requests.get('YOUR_API_ENDPOINT')
#     trip_info = response.json()

#     # Check for threshold crossings
#     for trip in trip_info:
#         if trip['speed'] > THRESHOLD_SPEED:
#             alerts.append(f"High speed detected for Driver {trip['driver_id']}")
#         if trip['battery_level'] < THRESHOLD_BATTERY:
#             alerts.append(f"Low battery level for Driver {trip['driver_id']}")

# @app.route('/dashboard')
# def dashboard():
#     return render_template('dashboard.html', alerts=alerts)

# # Initialize scheduler
# scheduler = BackgroundScheduler()
# scheduler.add_job(fetch_real_time_trip_info, 'interval', minutes=5)
# scheduler.start()

# if __name__ == "__main__":
#     app.run(debug=True)