import traci
import time
import traci.constants as tc
import pytz
import datetime
import numpy as np
import pandas as pd
from random import randrange
from tensorflow.keras.models import load_model
from firebase_admin import credentials, initialize_app, db
   
# Load pre-trained traffic 
# density prediction model
model = load_model(r'C:\Users\abhi1\Downloads\sumo-example-main\sumo-example-main\traffic_density_model\traffic_density_model.h5')

# Initialize Firebase
cred = credentials.Certificate #( Update this path to your Firebase JSON credentials file)  
initialize_app(cred, {
    'databaseURL': '# Replace with your actual Firebase DB URL'  
})

# Helper function to get formatted date and time
def getdatetime():
    utc_now = pytz.utc.localize(datetime.datetime.utcnow())
    currentDT = utc_now.astimezone(pytz.timezone("Asia/Singapore"))
    return currentDT.strftime("%Y-%m-%d %H:%M:%S")

# Flatten 2D list for easier data formatting
def flatten_list(_2d_list):
    flat_list = []
    for element in _2d_list:
        if isinstance(element, list):
            flat_list.extend(element)
        else:
            flat_list.append(element)
    return flat_list

# Predict traffic density based on real-time vehicle data
def predict_traffic_density(veh_data):
    data = np.array([veh_data])  # Prepare data in model input format
    prediction = model.predict(data)
    return prediction[0]

# Start SUMO with GUI
sumoCmd = ["sumo-gui", "-c", "osm.sumocfg"]
traci.start(sumoCmd)

# Set target vehicle to track
target_vehicle = 'veh0'

# Main simulation loop
while traci.simulation.getMinExpectedNumber() > 0:
    traci.simulationStep()

    # Retrieve vehicle and traffic light data
    vehicles = traci.vehicle.getIDList()
    trafficlights = traci.trafficlight.getIDList()

    # Check if target vehicle (veh0) is in the simulation
    if target_vehicle in vehicles:
        # Gather data for target vehicle
        x, y = traci.vehicle.getPosition(target_vehicle)
        lon, lat = traci.simulation.convertGeo(x, y)
        spd = round(traci.vehicle.getSpeed(target_vehicle) * 3.6, 2)  # Speed in km/h
        edge = traci.vehicle.getRoadID(target_vehicle)
        surrounding_tls = traci.vehicle.getNextTLS(target_vehicle)  # Traffic lights near target_vehicle

        # Format data for Firebase
        veh_data = {
            "vehicle_id": target_vehicle,
            "location": {"lon": lon, "lat": lat},
            "speed": spd,
            "edge": edge,
            "nearby_traffic_lights": surrounding_tls,
            "timestamp": getdatetime()
        }
        
        # Push target vehicle data to Firebase
        db.reference(f"vehicles/{target_vehicle}").set(veh_data)

        # Gather data for nearby vehicles
        nearby_vehicles = []
        for veh in vehicles:
            if veh != target_vehicle:
                other_x, other_y = traci.vehicle.getPosition(veh)
                other_lon, other_lat = traci.simulation.convertGeo(other_x, other_y)
                other_spd = round(traci.vehicle.getSpeed(veh) * 3.6, 2)
                
                # Add nearby vehicle data
                nearby_vehicles.append({
                    "vehicle_id": veh,
                    "location": {"lon": other_lon, "lat": other_lat},
                    "speed": other_spd
                })
        
        # Push nearby vehicles data to Firebase
        db.reference(f"vehicles/{target_vehicle}/nearby_vehicles").set(nearby_vehicles)

        print(f"Updated Firebase with data for {target_vehicle} and surroundings")

        # Control Traffic Lights based on density prediction
        veh_data_features = [spd, len(vehicles), 0]  # Replace 0 with an appropriate feature if available
        density_prediction = predict_traffic_density(veh_data_features)
        threshold = 0.6  # Congestion threshold
        for tls_id in trafficlights:
            if density_prediction > threshold:
                traci.trafficlight.setPhaseDuration(tls_id, 40)  # Example green light duration in seconds
            else:
                traci.trafficlight.setPhaseDuration(tls_id, 20)

traci.close()

print("Simulation complete. Data is available in Firebase.")
