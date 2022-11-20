from flask import Flask, render_template
import sqlite3

app = Flask(__name__)


@app.route('/dashboard')
def dashboard():
    results = {
        "battery": fetch_latest_soc(),
        "inverter": fetch_latest_tsw()
    }
    return render_template('dashboard.html', results=results)

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