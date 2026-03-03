 ## Smart Predictive Maintenance System

### 📌 Project Overview

The Smart Predictive Maintenance System is a web-based application developed using Flask (Python) and SQLite.

This system enables users to register machines, log operational sensor data, classify risk levels based on predefined thresholds, and visualize system analytics through an interactive dashboard.

The project was developed for academic purposes to demonstrate backend development, database integration, risk modeling, and data visualization techniques.


## 🎯 Objectives
To design and implement a predictive maintenance monitoring system

To develop a threshold-based risk classification algorithm

To integrate a relational database with a web application

To visualize maintenance data using interactive charts

To demonstrate full-stack development concepts in a structured manner


##🏗️ Project Structure

Smart_maintenance_system/
│
├── app.py
├── maintenance.db
├── templates/
│   ├── index.html
│   ├── add_machine.html
│   ├── view_machines.html
│   ├── add_sensor.html
│   ├── view_logs.html
│   └── dashboard.html
│
└── screenshots/
    ├── home.png
    ├── add_machine.png
    ├── view_machines.png
    ├── sensor_logs.png
    └── dashboard.png

## ⚙️ System Features

### 1️⃣ Machine Management
- Add new machines
- View registered machines
- Store machine name and location
- Maintain structured database records

### 2️⃣ Sensor Data Logging
- Record temperature, vibration, and pressure
- Automatically calculate risk levels
- Associate logs with specific machines 

### 3️⃣ Risk Classification Logic

Risk is calculated using a threshold-based scoring system:

| Condition              | Score |
| ---------------------- | ----- |
| Temperature > 90       | +2    |
| Temperature > 80       | +1    |
| Vibration > 50         | +2    |
| Vibration > 40         | +1    |
| Pressure < 20 or > 100 | +1    |


### Risk Levels:
- NORMAL
- MEDIUM RISK
- HIGH RISK

### 4️⃣ 📊 Dashboard Analytics

The dashboard provides:

- Total Machines Count
- Total Sensor Logs Count
- High Risk Logs Count
- Temperature Trend Chart
- Risk Distribution Chart

Charts are generated dynamically using Chart.js.

---

## 🗄️ Database Design

### Machines Table
| Field        | Type                  |
| ------------ | --------------------- |
| machine_id   | INTEGER (Primary Key) |
| machine_name | TEXT                  |
| location     | TEXT                  |


### SensorLogs Table
| Field       | Type                  |
| ----------- | --------------------- |
| log_id      | INTEGER (Primary Key) |
| machine_id  | INTEGER (Foreign Key) |
| temperature | REAL                  |
| vibration   | REAL                  |
| pressure    | REAL                  |
| risk_level  | TEXT                  |

Foreign key constraints are enabled to ensure relational consistency between machines and sensor logs.

💻 Technologies Used

Python

Flask

SQLite

HTML5

CSS3

Chart.js

Jinja2

▶️ How to Run the project

## ▶️ How to Run the Project

### Step 1: Install Dependencies

pip install flask

### Step 2: Run the Application

python app.py

### Step 3: Access the Web Interface with Browser
http://127.0.0.1:5000/

🎓 Academic Relevance

This project demonstrates:

Backend logic implementation

Database schema design

Risk-based decision modeling

Data visualization techniques

Full-stack web application architecture

It is suitable for:

Mini Project Submission

Internship Evaluation

Academic Demonstration

Final Year Project Prototype

📄 License

This project is intended for academic use only.


