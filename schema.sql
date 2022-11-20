CREATE TABLE battery_values(
        id INTEGER PRIMARY KEY NOT NULL,
        soc REAL NOT NULL,
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    );

CREATE TABLE inverter_values(
        id INTEGER PRIMARY KEY NOT NULL,
        total_solar_watt REAL,
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    );

CREATE TABLE amp_set_log(
        id INTEGER PRIMARY KEY  NOT NULL,
        amp REAL NOT NULL,
        current_soc REAL,
        current_tsw REAL,
        set_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    );