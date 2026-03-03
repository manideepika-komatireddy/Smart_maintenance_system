from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# -------------------- DATABASE CONNECTION --------------------
def get_db_connection():
    conn = sqlite3.connect('maintenance.db')
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


# -------------------- CREATE TABLES --------------------
def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Machines (
            machine_id INTEGER PRIMARY KEY AUTOINCREMENT,
            machine_name TEXT NOT NULL,
            location TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS SensorLogs (
            log_id INTEGER PRIMARY KEY AUTOINCREMENT,
            machine_id INTEGER,
            temperature REAL,
            vibration REAL,
            pressure REAL,
            risk_level TEXT,
            FOREIGN KEY(machine_id) 
                REFERENCES Machines(machine_id) 
                ON DELETE CASCADE
        )
    ''')

    conn.commit()
    conn.close()


create_tables()


# -------------------- HOME PAGE --------------------
@app.route('/')
def home():
    conn = get_db_connection()
    machines = conn.execute('SELECT * FROM Machines').fetchall()
    conn.close()
    return render_template("index.html", machines=machines)


# -------------------- ADD MACHINE --------------------
@app.route('/add_machine', methods=['GET', 'POST'])
def add_machine():
    if request.method == 'POST':
        name = request.form['machine_name']
        location = request.form['location']

        conn = get_db_connection()
        conn.execute(
            "INSERT INTO Machines (machine_name, location) VALUES (?, ?)",
            (name, location)
        )
        conn.commit()
        conn.close()

        return redirect('/')

    return render_template('add_machine.html')


# -------------------- VIEW MACHINES --------------------
@app.route('/view_machines')
def view_machines():
    conn = get_db_connection()
    machines = conn.execute('SELECT * FROM Machines').fetchall()
    conn.close()
    return render_template('view_machines.html', machines=machines)


# -------------------- RISK CALCULATION --------------------
def calculate_risk(temperature, vibration, pressure):
    risk_score = 0

    if temperature > 90:
        risk_score += 2
    elif temperature > 80:
        risk_score += 1

    if vibration > 50:
        risk_score += 2
    elif vibration > 40:
        risk_score += 1

    if pressure < 20 or pressure > 100:
        risk_score += 1

    if risk_score >= 4:
        return "HIGH RISK"
    elif risk_score >= 2:
        return "MEDIUM RISK"
    else:
        return "NORMAL"


# -------------------- ADD SENSOR DATA --------------------
@app.route('/add_sensor/<int:machine_id>', methods=['GET', 'POST'])
def add_sensor(machine_id):
    if request.method == 'POST':
        try:
            temperature = float(request.form['temperature'])
            vibration = float(request.form['vibration'])
            pressure = float(request.form['pressure'])
        except ValueError:
            return "Invalid input. Please enter numeric values."

        risk_level = calculate_risk(temperature, vibration, pressure)

        conn = get_db_connection()
        conn.execute("""
            INSERT INTO SensorLogs 
            (machine_id, temperature, vibration, pressure, risk_level)
            VALUES (?, ?, ?, ?, ?)
        """, (machine_id, temperature, vibration, pressure, risk_level))

        conn.commit()
        conn.close()

        return redirect('/view_machines')

    return render_template('add_sensor.html', machine_id=machine_id)


# -------------------- VIEW LOGS --------------------
@app.route('/view_logs/<int:machine_id>')
def view_logs(machine_id):
    conn = get_db_connection()
    logs = conn.execute(
        'SELECT * FROM SensorLogs WHERE machine_id = ?',
        (machine_id,)
    ).fetchall()
    conn.close()

    return render_template('view_logs.html', logs=logs, machine_id=machine_id)


# -------------------- DASHBOARD --------------------
@app.route('/dashboard')
def dashboard():
    conn = get_db_connection()

    total_machines = conn.execute(
        "SELECT COUNT(*) FROM Machines"
    ).fetchone()[0]

    total_logs = conn.execute(
        "SELECT COUNT(*) FROM SensorLogs"
    ).fetchone()[0]

    high_count = conn.execute(
        "SELECT COUNT(*) FROM SensorLogs WHERE risk_level = 'HIGH RISK'"
    ).fetchone()[0]

    medium_count = conn.execute(
        "SELECT COUNT(*) FROM SensorLogs WHERE risk_level = 'MEDIUM RISK'"
    ).fetchone()[0]

    low_count = conn.execute(
        "SELECT COUNT(*) FROM SensorLogs WHERE risk_level = 'NORMAL'"
    ).fetchone()[0]

    temp_data = conn.execute(
        "SELECT temperature FROM SensorLogs ORDER BY log_id ASC"
    ).fetchall()

    conn.close()

    temp_values = [row["temperature"] for row in temp_data]
    temp_labels = list(range(1, len(temp_values) + 1))

    risk_counts = [low_count, medium_count, high_count]

    return render_template(
        "dashboard.html",
        total_machines=total_machines,
        total_logs=total_logs,
        high_count=high_count,
        medium_count=medium_count,
        low_count=low_count,
        temp_labels=temp_labels,
        temp_values=temp_values,
        risk_counts=risk_counts
    )


# -------------------- RUN APP --------------------
if __name__ == '__main__':
    app.run(debug=True)