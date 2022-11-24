from flask import Flask, render_template
from range_key_dict import RangeKeyDict
import sqlite3
import pdb

app = Flask(__name__)
pause_amp = 2
tsw_to_solar_power_mode_matrix = RangeKeyDict({
    # What about > 800 and less than 100?
    (701, 801): "HIGH",
    (451, 701): "MEDIUM",
    (101, 451): "LOW"
})

soc_to_charging_pace_matrix = {
    "HIGH": RangeKeyDict({
        (76, 101): "FAST",
        (51, 76): "MEDIUM",
        (21, 51): "SLOW",
        (0, 21): "PAUSE"
    }),
    "MEDIUM": RangeKeyDict({
        (86, 101): "FAST",
        (61, 86): "MEDIUM",
        (21, 61): "SLOW",
        (0, 21): "PAUSE"
    }),
    "LOW": RangeKeyDict({
        (90, 101): "FAST",
        (71, 91): "MEDIUM",
        (21, 71): "SLOW",
        (0, 21): "PAUSE"
    })
}

charging_pace_to_optimal_amp_matrix = {
    "FAST": 15,
    "MEDIUM": 11,
    "SLOW": 6,
    "PAUSE": 2
}


@app.route('/dashboard')
def dashboard():
    latest_soc_record = fetch_latest_soc()
    latest_tsw_record = fetch_latest_tsw()
    calculated_optimal_amp = calculate_optimal_amp(round(latest_soc_record[1]), round(latest_tsw_record[1]))
    results = {
        "battery": latest_soc_record,
        "inverter": latest_tsw_record,
        "optimal_amp": calculated_optimal_amp,
    }
    return render_template('dashboard.html', results=results)


def calculate_optimal_amp(latest_soc, latest_tsw):
    solar_power_mode = tsw_to_solar_power_mode_matrix[latest_tsw]
    charge_pace = soc_to_charging_pace_matrix[solar_power_mode][latest_soc]
    optimal_amp = charging_pace_to_optimal_amp_matrix[charge_pace]
    return optimal_amp


def fetch_latest_soc():
    con = sqlite3.connect("solar_powered_kangoo.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM battery_values ORDER BY created_at DESC LIMIT 1;")
    return cur.fetchall()[0]


def fetch_latest_tsw():
    con = sqlite3.connect("solar_powered_kangoo.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM inverter_values ORDER BY created_at DESC LIMIT 1;")
    return cur.fetchall()[0]
