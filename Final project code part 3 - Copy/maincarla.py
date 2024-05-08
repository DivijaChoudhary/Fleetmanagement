import base64
from datetime import datetime
import json
import random
from flask_socketio import SocketIO, emit
import time
from flask import Flask, flash, jsonify, redirect, render_template, request, send_file, session, url_for
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
    response = requests.get(f'http://localhost:5000/vehicle/{vehicle_id}')
    vehicle_info= json.loads(response.text)
    response_sensor = requests.get(f'http://localhost:5000/vehicle/{vehicle_id}/sensors')
    vehicle_sensor_info= json.loads(response_sensor.text)
    
    print("vehicle info", vehicle_sensor_info)
    current_trip= {
                'Trip_id':'Trip_123',
                'source': 'Trip Source 1',
                'destination': 'Trip Destination 1',
                'occupancy': 2,
                'start_time': '2024-04-22 08:00:00',
                'completed': False
            }
    all_trips= [
                {   'Trip_id':'Trip_123',
                    'source': 'Trip Source 2',
                    'destination': 'Trip Destination 2',
                    'occupancy': 3,
                    'start_time': '2024-04-21 10:00:00',
                    'completed': True,
                    'end_time': '2024-04-21 12:00:00'
                }
            ]
    maintenance_records=requests.get(f'http://localhost:5000/vehicle/{vehicle_id}/maintenance')
    vehicle_maintenance_info= json.loads(maintenance_records.text)
    
    print("vehicle info", vehicle_maintenance_info)
    
    return render_template('vehicle_details.html', vehicle=vehicle_info,vehicle_sensor=vehicle_sensor_info,current_trip=current_trip,all_trips=all_trips,vehicle_maintenance_info=vehicle_maintenance_info)
    
# get all driver
@app.route('/getalldriver', methods=['GET'])
def vehicle_driver_all():
    response = requests.get('http://localhost:5000/drivers/details')
    print("resposne",response)
    driver_info= json.loads(response.text)
    
    print("driver info",driver_info )
    
    return render_template('viewalldrivers.html', driver_info=driver_info)
      
# Dummy data for real-time sensor and trip status updates
# when you load first time the realdata 


@app.route('/getRealTimeData/<trip_id>')
def get_real_time_data(trip_id):
    
    print(trip_id)
#     sensor_data = [
#     {"trip_id": "Trip_123", "sensor_id": "1", "timestamp": time.time(), "vehicle_id": "123", 
#      "status": "Healthy", "value": random.randint(1, 100)},
#     {"trip_id": "Trip_123", "sensor_id": "2", "timestamp": time.time(), "vehicle_id": "123", 
#      "status": "Faulty", "value": random.randint(1, 100)},
#     # Add more sensor data as needed
# ]
    

    # trip_status_data = [
    #     {"trip_id": "Trip_123", "timestamp": time.time(), "location_lat": random.uniform(-90, 90), 
    #      "location_lon": random.uniform(-180, 180), "battery_level": random.uniform(0, 100), "speed": random.uniform(0, 120), 
    #     "Moving_status": "Moving", 
    #      "moving_direction": random.uniform(0, 360), 
    #      "isturning": random.choice([True, False]),"Throttle": 0.75,
    #     "Steer": -0.001496124779805541,
    #     "Brake": 0.0,
    #     "Reverse":  random.choice([True, False]),
    #     "Hand_brake":  random.choice([True, False]),
    #     "Manual":  random.choice([True, False]),
    #     "Gear": 1,
    #     "Power": "97.7%" 
    #     },
    #     # Add more trip status data as needed
    # ]
    trip_status_data_api=requests.get(f'http://localhost:5002/getLastStatus/{trip_id}')
    trip_data=json.loads(trip_status_data_api.text)
    trip_status_data=trip_data
    print("tripstatus data",trip_status_data)
#     trip status data [{'_id': {'$oid': '663b0ee7c4f17e247f8e6e16'},
#                         'Count': 4, 
#                         'Server FPS': 92.59259033203125, 'Client FPS': 92.59259033203125, 
#                         'Vehicle': 'Mercedes Sprinter', 
#                         'Map': 'Town10HD_Opt', 
#                         'Unique_id': '4a77d76cab9beed398389f2203e85e0bb852271d9e035cc957e6ab5b9bbd75d1', 
#                         'Speed (km/h)': 26.392090717991017, 'Moving_status': 'Moving', 
#                         'Heading': {'Value': -179.90170288085938, 
#                                     'Direction': 'S'}, 
#                         'Location': {'X': 43.91999053955078, 'Y': -64.40351867675781, 'Z': -0.02229640819132328}, 
#                         'Number of vehicles': 31,                        
# 'Throttle': 0.75, 
# 'Steer': -0.001496124779805541, 
# 'Brake': 0.0, 'Reverse': False, 
# 'Hand brake': False, 
# 'Manual': False, 
# 'Gear': 1, 
# 'Power': '97.7%', 
# 'timestamp': {'$date': '2024-05-07T00:04:26Z'}, 
# 'trip_id': {'$oid': '663b0edfc4f17e247f8e6e12'}, 
# 'expiry_date': {'$date': '2025-05-07T00:04:26Z'}}]
    # coordinates = [
    #     {"id": "123", "latitude": 37.7749, "longitude": -74.4194},
    #     {"id": "456", "latitude": 40.7749, "longitude": -74.4194},
    #     {"id": "789", "latitude": 42.7749, "longitude": -74.4194},
    #     # Add more coordinates here as needed
    # ]
    
    # Filter sensor data and trip status data by trip ID
    # trip_sensor_data = [sensor for sensor in sensor_data if sensor["trip_id"] == trip_id]
    # trip_status_data = [trip for trip in trip_status_data if trip["trip_id"] == trip_id]
    # trip_status_data_jsonify=jsonify({
        
    #     "trip_status_data": trip_status_data
    # })
    # Return the filtered data
    trip_id = trip_status_data[0]['trip_id']['$oid']
    print("trip id",trip_id)
    return render_template('real_time_trip_details_carla.html',
                           trip_status_data=trip_status_data,trip_id=trip_id,trip_status_data_jsonify=trip_status_data)
# when you load 5 sec time the realdata 
@app.route('/getRealTimeDataJSON/<trip_id>')
def get_real_time_data_json(trip_id):
    # trip_status_data= {"trip_id": "Trip_123", "timestamp": time.time(), "location_lat": random.uniform(-90, 90), 
    #     "location_lon": random.uniform(-180, 180), "battery_level": random.uniform(0, 100), "speed": random.uniform(0, 120), 
    #     "Moving_status": "Moving", 
    #     "moving_direction": random.uniform(0, 360), 
    #     "isturning": random.choice([True, False]),
    #     "Throttle": 0.75,
    #     "Steer": -0.001496124779805541,
    #     "Brake": 0.0,
    #     "Reverse":  random.choice([True, False]),
    #     "Hand_brake":  random.choice([True, False]),
    #     "Manual":  random.choice([True, False]),
    #     "Gear": 1,
    #     "Power": "97.7%" 
    #     }
    print("trip id in 2nd",trip_id)
    trip_status_data_api=requests.get(f'http://localhost:5002/getLastStatus/{trip_id}')
    trip_status_data=json.loads(trip_status_data_api.text)
    trip_status_data=trip_status_data
    print("trip status 2nd",trip_status_data)
    return jsonify(trip_status_data)

@app.route('/register')
def registration():
    return render_template('registerAV.html')

@app.route('/registerAV', methods=['GET', 'POST'])
def register():
    
        # Here you retrieve the data from the form
        vehicle={
        "make": request.form['make'],
        
        "model" : request.form['model'],
        "registration_date": request.form['registrationDate'],
        "manufacturer": request.form['manufacturer'],
        "mileage": request.form['mileage'],
        "driver_id": session['driver_id']

        }
        jsonrequest=json.dumps(vehicle)
        response = requests.post('http://localhost:5000/vehicle/register', data=jsonrequest,headers= {'Content-Type': 'application/json'})
        if response.status_code == 201:
            return render_template('registerAV.html', message="Registration Successful!!")
        else:
            return render_template('registerAV.html', message="Registration unsuccessful!!")


@app.route('/add-maintenance-record/<vehicle_id>', methods=['GET'])
def add_maintenance_record(vehicle_id):
    # Pass the vehicle_id to the template
    return render_template('add_maintenance_record.html', vehicle_id=vehicle_id)
@app.route('/add-insurance/<vehicle_id>', methods=['GET'])
def add_insurance_record(vehicle_id):
    # Pass the vehicle_id to the template
    return render_template('add_insurance.html', vehicle_id=vehicle_id)

@app.route('/submit-maintenance-record/<vehicle_id>', methods=['POST'])
def submit_maintenance_record(vehicle_id):
    # Extract form data from request.form and save the record
    vehicle={
    "service_date" : request.form['serviceDate'],
    "tires_rotated": 'tiresRotated' in request.form,
    'air_filter_changed':'air_filter_changed' in request.form,
    'battery_status':'battery' in request.form,
    'brakes_replaced':'brakes' in request.form,
    'oil_changed':'OilChanged' in request.form,
    'wipers_changed':'WiperChanged' in request.form,
    'wiper_fluid_refilled':'WiperFuildRefilled' in request.form,
    'tires_changed':'tireschanged' in request.form,
    # 'maintenance_id': record.record_id,
    #     'wiper_fluid_refilled': record.wiper_fluid_refilled,
    #     'wipers_changed': record.wipers_changed,
    #     'oil_changed': record.oil_changed,
    #     'service_date': record.service_date.strftime('%Y-%m-%d'),  # Format date as string
    #     'battery_status': record.battery_status,
    #     'air_filter_changed': record.air_filter_changed,
    #     'tires_changed': record.tires_changed,
    #     'tires_rotated': record.tires_rotated,
    #     'brakes_replaced': record.brakes_replaced,
    
    }
    print(vehicle)

    # Save the data to the database or wherever it needs to go
    jsonrequest=json.dumps(vehicle)
    response = requests.post(f'http://localhost:5000/vehicle/{vehicle_id}/maintenance', data=jsonrequest,headers= {'Content-Type': 'application/json'})
    if response.status_code == 201:
            return render_template('add_maintenance_record.html', vehicle_id=vehicle_id, message="Record Added Successfully!!")
    else:
            return render_template('add_maintenance_record.html', message="Unsuccessful!!")
@app.route('/submit-insurance/<vehicle_id>', methods=['POST'])
def submit_insurance_record(vehicle_id):
    # Extract form data from request.form and save the record
    vehicle={
    "insured_by" : request.form['insuredBy'],
    "expiration_date":request.form['expirationDate'],

    "policy_no":request.form['policyNumber'],
    "vehicle_id":vehicle_id
    # 'maintenance_id': record.record_id,
    #     'wiper_fluid_refilled': record.wiper_fluid_refilled,
    #     'wipers_changed': record.wipers_changed,
    #     'oil_changed': record.oil_changed,
    #     'service_date': record.service_date.strftime('%Y-%m-%d'),  # Format date as string
    #     'battery_status': record.battery_status,
    #     'air_filter_changed': record.air_filter_changed,
    #     'tires_changed': record.tires_changed,
    #     'tires_rotated': record.tires_rotated,
    #     'brakes_replaced': record.brakes_replaced,
    
    }
    print(vehicle)

    # Save the data to the database or wherever it needs to go
    jsonrequest=json.dumps(vehicle)
    response = requests.post(f'http://localhost:5000/insurance/register', data=jsonrequest,headers= {'Content-Type': 'application/json'})
    if response.status_code == 201:
            return render_template('add_insurance.html', vehicle_id=vehicle_id, message="Record Added Successfully!!")
    else:
            return render_template('add_insurance.html', vehicle_id=vehicle_id,message="Unsuccessful!!")
    

@app.route('/add-sensor/<vehicle_id>')
def add_sensor(vehicle_id):

    # You would have logic here to ensure the vehicle exists, etc.
    return render_template('add_sensor.html', vehicle_id=vehicle_id)
@app.route('/submit-sensor/<vehicle_id>', methods=['POST'])
def submit_sensor_record(vehicle_id):
        sensor={
            "sensor_type": request.form['sensorType'],
            
            "sensor_status" : request.form['sensorStatus'],
            
            "vehicle_id": vehicle_id

            }
        jsonrequest=json.dumps(sensor)
        response = requests.post('http://localhost:5000/sensor/register', data=jsonrequest,headers= {'Content-Type': 'application/json'})
        if response.status_code == 201:
            return render_template('add_sensor.html', message="Sensor Registration Successful!!",vehicle_id=vehicle_id)
        else:
            return render_template('add_sensor.html', message="Sensor Registration unsuccessful!!",vehicle_id=vehicle_id)
   
    
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
    
    response = requests.get(f'http://localhost:5000/vehicle/{vehicle_id}')
    vehicle_info= json.loads(response.text)
    response_sensor = requests.get(f'http://localhost:5000/vehicle/{vehicle_id}/sensors')
    vehicle_sensor_info= json.loads(response_sensor.text)
    response_insurance = requests.get(f'http://localhost:5000/vehicle/{vehicle_id}/insurance')
    vehicle_insurance_info= json.loads(response_insurance.text)
    if 'message' in vehicle_insurance_info:  # Assuming no records found
        vehicle_insurance_info = []
   

    print("vehicle info", vehicle_insurance_info)
    # current_trip= {
    #             'Trip_id':'Trip_123',
    #             'source': 'Trip Source 1',
    #             'destination': 'Trip Destination 1',
    #             'occupancy': 2,
    #             'start_time': '2024-04-22 08:00:00',
    #             'completed': False
    #         }
    current_trip_api=requests.get(f'http://localhost:5002/getCurrentTrip/{vehicle_id}')
    currenttrip=json.loads(current_trip_api.text)
    print("current trip",currenttrip)
    if 'message' in currenttrip:
        currenttrip = []
    # current trip [{'_id': {'$oid': '663a93e6cc88ec78693c63fe'}, 
    #                'vehicle_id': '1', 
    #                'source': {'type': 'Point', 'coordinates': [12.1222, 42.4222]},
    #                  'destination': {'type': 'Point', 'coordinates': [56.877, 98.655]}, 
    #                  'occupancy': 4, 'completed': True, 'start_time': {'$date': '2024-04-22T13:25:00Z'}, 
    #                  'end_time': {'$date': '2024-04-22T13:55:00Z'}, 'expiry_date': {'$date': '2025-04-22T13:25:00Z'}}]
    # print("currnet trip souce",currenttrip[0].source)
    all_trip_api=requests.get(f'http://localhost:5002/getAllTrips/{vehicle_id}')
    alltrip=json.loads(all_trip_api.text)
    if 'message' in alltrip:
        alltrip = []
    print("all trip",alltrip)
    # all_trips= [
    #             {   'Trip_id':'Trip_123',
    #                 'source': 'Trip Source 2',
    #                 'destination': 'Trip Destination 2',
    #                 'occupancy': 3,
    #                 'start_time': '2024-04-21 10:00:00',
    #                 'completed': True,
    #                 'end_time': '2024-04-21 12:00:00'
    #             }
    #         ]
    maintenance_records=requests.get(f'http://localhost:5000/vehicle/{vehicle_id}/maintenance')
    vehicle_maintenance_info= json.loads(maintenance_records.text)
    
    print("vehicle info", vehicle_maintenance_info)
    
    return render_template('vehicle_details.html', vehicle=vehicle_info,vehicle_sensor=vehicle_sensor_info,current_trip=currenttrip,all_trips=alltrip,
                           vehicle_maintenance_info=vehicle_maintenance_info,vehicle_insurance_info=vehicle_insurance_info)
    

@app.route('/registerAVbyadmin', methods=['GET', 'POST'])
def registerbyadmin():
    
         # Here you retrieve the data from the form
        vehicle={
        "make": request.form['make'],
        
        "model" : request.form['model'],
        "registration_date": request.form['registrationDate'],
        "manufacturer": request.form['manufacturer'],
        "mileage": request.form['mileage'],
        "driver_id":request.form['owner']

        }
        jsonrequest=json.dumps(vehicle)
        response = requests.post('http://localhost:5000/vehicle/register', data=jsonrequest,headers= {'Content-Type': 'application/json'})
        r1 = requests.get('http://localhost:5000/drivers')
        driver_data=json.loads(r1.text)
        if response.status_code == 201:
            return render_template('registerAvbyadmin.html', message="Registration Successful!!",driver_data=driver_data)
        else:
            return render_template('registerAvbyadmin.html', message="Registration unsuccessful!!",driver_data=driver_data)
@app.route('/registerbyadmin')
def registrationbyadmin():
    r1 = requests.get('http://localhost:5000/drivers')
    driver_data=json.loads(r1.text)

    
    return render_template('registerAvbyadmin.html',driver_data=driver_data)   

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
    "labels": ["1", "2"],
    "trips": [2, 4]
}

@app.route('/analytics')
def index():
    # r=requests.get('http://localhost:5002/tripsCountsPerVehicle')
    # rjson=json.loads(r.text)
    # print("rjson",rjson)
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
    account_id=session['account_id']
    r=requests.get(f'http://localhost:5000/account/{account_id}')
    profile=json.loads(r.text)
    print(profile)
    # driver_id=session['driver_id']
    # r1=requests.get(f'http://localhost:5000/driver/{driver_id}')
    # profile_driver=json.loads(r1.text)
    # print("profile",profile)
    # print("profile driver",profile_driver)
    
    return render_template('profile.html',profile=profile)
@app.route('/updateprofile',methods=['post'])
def updateprofile():
     users = {
        "email" : request.form['email'],
        "password" : request.form['password'],
        "zipcode" : request.form['zipcode'],
        "state" : request.form['state'],
        "city" : request.form['city'],
        "street_addr" : request.form['address'],

            }
     print("accountid",session['account_id'])
     
     account_id=session['account_id']
     jsonrequest = json.dumps(users)
            # print(jsonrequest)
            # r = requests.post(f'http://{global_ip}/signin', data=jsonrequest, headers= {'Content-Type': 'application/json'})
            # Make a POST request to the /register/driver API
     r = requests.put(f'http://localhost:5000/account/update/{account_id}', data=jsonrequest,headers= {'Content-Type': 'application/json'})
     if r.status_code == 200:
        r1=requests.get(f'http://localhost:5000/account/{account_id}')
        profile=json.loads(r1.text)
        print(profile)
        # driver_id=session['driver_id']
        # r1=requests.get(f'http://localhost:5000/driver/{driver_id}')
        # profile_driver=json.loads(r1.text)
        # print("profile",profile)
        # print("profile driver",profile_driver)
        
        return render_template('profile.html',profile=profile,message="Profile Updated")
     else:
        r1=requests.get(f'http://localhost:5000/account/{account_id}')
        profile=json.loads(r1.text)
        print(profile)
        # driver_id=session['driver_id']
        # r1=requests.get(f'http://localhost:5000/driver/{driver_id}')
        # profile_driver=json.loads(r1.text)
        # print("profile",profile)
        # print("profile driver",profile_driver)
        
        return render_template('profile.html',profile=profile,message="Profile not Updated")
          
     
@app.route('/logout')
def logout():
    # Clear the entire session
    session.clear()
    return render_template('login.html')
@app.route('/submit-login',methods=['GET', 'POST'])
def login():
    users = {
        "username" : request.form['username'],
        "password" : request.form['password']
            }
    jsonrequest = json.dumps(users)
            # print(jsonrequest)
            # r = requests.post(f'http://{global_ip}/signin', data=jsonrequest, headers= {'Content-Type': 'application/json'})
            # Make a POST request to the /register/driver API
    r = requests.post('http://localhost:5000/login', data=jsonrequest,headers= {'Content-Type': 'application/json'})
    response = json.loads(r.text)
    print("response of login",response)
    if r.status_code == 200:
            session['email']=response['email']
            session['account_id']=response['account_id']
            session['city']=response['city']
            session['role']=response['role']
            session['state']=response['state']
            session['street_addr']=response['street_addr']
            session['zipcode']=response['zipcode']
            
            # session['ispremium']=response[0]['ispremium']
            # session['userid']=response[0]['userid']
            # session['rewardpoints']=response[0]['rewardpoints']
            # print(response[0]['userrole'])
            if session['role'] == 'admin':
                session['staff_id']=response['staff_id']
                return redirect('/admin-dashboard')
            elif session['role'] == 'driver':
                 session['driver_id']=response['driver_id']
                 return redirect('/driver-dashboard')
            

    else:
            #show error message, maybe send a variable here to display in html with jinja
            print("not succcess")
    return render_template('login.html',message="Incorrect details, Please re-enter!!")
    

    # # Check if user exists and password is correct
    # user = users.get(username)
    # if user and user['password'] == password:
    #     # Redirect based on role
    #     if user['role'] == 'admin':
    #         return redirect('/admin-dashboard')
    #     elif user['role'] == 'driver':
    #         return redirect('/driver-dashboard')
    # else:
    #     return "Invalid credentials", 401
    return render_template('profile.html')

@app.route('/submit-registration', methods=['POST','GET'])
def registrations():
       
            role=request.form['role']
            if role == 'admin':
                    payload = {
                    "email": request.form['username'],  # Assuming email is same as username
                    "password": request.form['password'],
                    "zipcode": request.form['zipcode'],
                    "state": request.form['state'],
                    "city": request.form['city'],
                    "street_addr": request.form['street_address'],
                    "first_name": request.form['firstname'],
                    "last_name": request.form['lastname'],
                   
                    "role":request.form['role']
                }
                    print(payload)
                    jsonrequest = json.dumps(payload)
                    # print(jsonrequest)
                    # r = requests.post(f'http://{global_ip}/signin', data=jsonrequest, headers= {'Content-Type': 'application/json'})
                    # Make a POST request to the /register/driver API
                    response = requests.post('http://localhost:5000/register', data=jsonrequest,headers= {'Content-Type': 'application/json'})
                    print("repsosne",response)
                    
                    if response.status_code == 201:
                        # Redirect to the login page on successful registration
                        return render_template('login.html')
                    else:
                        # Return an error message if something went wrong
                        return "Registration failed", 400
        
                 
            else:
                    payload = {
                    "email": request.form['username'],  # Assuming email is same as username
                    "password": request.form['password'],
                    "zipcode": request.form['zipcode'],
                    "state": request.form['state'],
                    "city": request.form['city'],
                    "street_addr": request.form['street_address'],
                    "first_name": request.form['firstname'],
                    "last_name": request.form['lastname'],
                    "license_no": request.form['licenseNumber'],
                    "dob": request.form['dob'],
                   
                    "role":request.form['role']
                }
                    print(payload)
                    jsonrequest = json.dumps(payload)
                    # print(jsonrequest)
                    # r = requests.post(f'http://{global_ip}/signin', data=jsonrequest, headers= {'Content-Type': 'application/json'})
                    # Make a POST request to the /register/driver API
                    response = requests.post('http://localhost:5000/register', data=jsonrequest,headers= {'Content-Type': 'application/json'})
                    print("repsosne",response)
                    
                    if response.status_code == 201:
                        # Redirect to the login page on successful registration
                        return render_template('login.html')
                    else:
                        # Return an error message if something went wrong
                        return "Registration failed", 400
                 

        # Construct the payload from the form data
            # payload = {
            #     "email": request.form['username'],  # Assuming email is same as username
            #     "password": request.form['password'],
            #     "zipcode": request.form['zipcode'],
            #     "state": request.form['state'],
            #     "city": request.form['city'],
            #     "street_addr": request.form['street_address'],
            #     "first_name": request.form['firstname'],
            #     "last_name": request.form['lastname'],
            #     "license_no": request.form['licencenumber'],
            #     "dob": request.form['dob'],
            #     "role":request.form['role']
            # }
            # print(payload)
            # jsonrequest = json.dumps(payload)
            # # print(jsonrequest)
            # # r = requests.post(f'http://{global_ip}/signin', data=jsonrequest, headers= {'Content-Type': 'application/json'})
            # # Make a POST request to the /register/driver API
            # response = requests.post('http://localhost:5000/register', data=jsonrequest,headers= {'Content-Type': 'application/json'})
            # print("repsosne",response)
            
            # if response.status_code == 201:
            #     # Redirect to the login page on successful registration
            #     return render_template('login.html')
            # else:
            #     # Return an error message if something went wrong
            #     return "Registration failed", 400
        
        
    

@app.route('/admin-dashboard',methods=['GET'])
def admin_dashboard():
    # Define your static data here
    # fleet_data = [
    #     {"id":"123","make": "Mercedes", "model":"Benz Smart EQ Fortwo","status": "On-trip"},   
    #     {"id":"456","make": "Porsche","model":" Fortwo" ,"status": "Offline"},
    #     {"id":"789","make": "Porsche1","model":" Fortwo1" ,"status": "Online"},
    #     {"id":"1011","make": "Porsche2","model":" Fortwo2" ,"status": "On-trip"},
    #     {"id":"1213","make": "Porsche3","model":" Fortwo3" ,"status": "On-trip"},
    #     {"id":"1415","make": "Mercedes1", "model":"Benz Smart EQ Fortwo","status": "On-trip"},
    #     # Add more entries as needed...
    # ]
    
    r1 = requests.get('http://localhost:5000/vehicles')
    fleet_data=json.loads(r1.text)

    print(r1.text)
    # fleet_data=json.loads(r1.text)
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
    coordinatesbyapi=requests.get('http://localhost:5002/getRecentTripInfo')
    print(coordinatesbyapi)
    coordinates=json.loads(coordinatesbyapi.text)
    print("coordinated by api ",coordinates)
    # coordinated by api  
    # [{'vehicle_id': '1', 
    #   'recent_status': {'_id': {'$oid': '663b2e08290d6cafe303c900'}, 
                        
    #     'location_lat': 52.503875732421875, 'location_long': -114.30424499511719}}
    #     ]

    
    return render_template('admin_dashboard.html', fleet=fleet_data,coordinates_json=coordinates)
   

@app.route('/driver-dashboard')
def driver_dashboard():
    driver_id=session['driver_id']
    jsonrequest={"driver_id":driver_id }
    r1 = requests.post('http://localhost:5000/vehiclebydriverid', data=json.dumps(jsonrequest), headers= {'Content-Type': 'application/json'})
    print(r1.text)
    # fleet_data = [
    #     {"id":"123","make": "Mercedes", "model":"Benz Smart EQ Fortwo","status": "On-trip"},
    #     {"id":"456","make": "Porsche","model":" Fortwo" ,"status": "Offline"},
    #     {"id":"789","make": "Porsche1","model":" Fortwo1" ,"status": "On-trip"},
    #     # Add more entries as needed...
    # ]
    fleet_data=json.loads(r1.text)
    # from cookies pass driver id and get vehicle id and vehicle details then for each veg=hicle get current longitute and latitude
    coordinates = [
    {"id": "123", "latitude": 37.7749, "longitude": -74.4194},
    {"id": "456", "latitude": 40.7749, "longitude": -74.4194},
    {"id": "789", "latitude": 42.7749, "longitude": -74.4194},
    # Add more coordinates here as needed
]

    
    return render_template('driver_dashboard.html',fleet=fleet_data,coordinates_json=coordinates)

# @app.route('/create-trip')
# def create_trip():
#     return render_template('createtrip.html')
# @app.route('/submit-trip', methods=['POST','GET'])
# def submit_trip():
#     # Here you would handle saving the trip data to your database or backend system
    
#     # Add logic to save the trip details
#     return render_template('createtrip.html',message="Trip Created Successfully")

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
     app.run(host='127.0.0.1',port=5001,debug=True)

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