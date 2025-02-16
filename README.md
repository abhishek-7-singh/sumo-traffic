# 🚦 Smart Traffic Signal Control System

## 📝 Introduction
The **Smart Traffic Signal Control System** is designed to optimize traffic flow by collecting and analyzing vehicle data, including speed and proximity to other vehicles. The system leverages **SUMO (Simulation of Urban Mobility)** for realistic traffic simulations, and all collected data is stored in **Firebase** for real-time processing and monitoring.

## 🚀 Features
- **Real-time Traffic Monitoring** – Tracks vehicle positions, speeds, and congestion levels.
- **Firebase Integration** – Stores vehicle proximity and speed data for further analysis.
- **Traffic Optimization** – Can be extended to dynamically adjust signal timings based on congestion.
- **Simulation with SUMO** – Uses realistic traffic models for better accuracy.
- **Custom Map Integration** – Generate maps using OpenStreetMap (OSM) for different regions.

## 🛠️ Technologies Used
- **SUMO (Simulation of Urban Mobility)** – Traffic simulation tool.
- **Firebase** – Stores real-time vehicle data.
- **Python** – Used for data extraction and processing.
- **OpenStreetMap (OSM)** – Generates custom traffic maps.
- **TraCI (Traffic Control Interface)** – Interfaces SUMO with external controllers.

## 📥 Installation & Setup

### 🔹 Clone the Repository
```sh
git clone https://github.com/abhishek-7-singh/smart-traffic-signal.git
```

### 🔹 Navigate to the Project Folder
```sh
cd smart-traffic-signal
```

### 🔹 Install Dependencies
```sh
pip install sumo-tools firebase-admin
```

### 🔹 Start SUMO Simulation
```sh
sumo-gui -c config.sumocfg
```

## 📌 How It Works
1. SUMO simulates vehicle movement in a predefined traffic network.
2. The system collects real-time data on vehicle speeds and proximity.
3. The data is pushed to **Firebase** for storage and analysis.
4. Insights can be used to optimize traffic flow and reduce congestion.

## 🗺️ Generating Custom Maps with OSM Web Wizard
To create a traffic network from OpenStreetMap:
1. **Visit** [OSM Web Wizard](https://sumo.dlr.de/docs/Tutorials/OSMWebWizard.html)
2. **Select your desired region** on the map.
3. **Export the network** in SUMO format.
4. **Import the generated file** into your SUMO project.
5. Use the exported **.net.xml** file to define your traffic simulation.

## 🤝 Contributing
1. **Fork the repository**
2. **Create a new branch** (`feature-enhancement`)
3. **Commit your changes** (`git commit -m "Added Firebase integration"`)
4. **Push to your branch** (`git push origin feature-enhancement`)
5. **Open a pull request**

## 📜 License
This project is licensed under the **MIT License**.

## 📬 Contact
📧 **Email:** support@yourdomain.com  
🔗 **GitHub:** [Your Repository](https://github.com/abhishek-7-singh/smart-traffic-signal)

