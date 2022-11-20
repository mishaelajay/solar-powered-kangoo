from flask import Flask, render_template
import sqlite3

app = Flask(__name__)


@app.route('/dashboard')
def dashboard():
    battery_values = {}  # run the battery script and fetch values from db
    inverter_values = {}  # run the inverter script and fetch values from db
    return render_template('dashboard.html')


conn = sqlite3.connect('solar-powered.db')
print("Opened successfully")
