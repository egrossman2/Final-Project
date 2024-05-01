import sqlite3

def setup_database(db_name):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    cur.execute('''
    CREATE TABLE IF NOT EXISTS NursingHomeData (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        week_ending DATE,
        provider_name TEXT,
        provider_address TEXT,
        provider_city TEXT,
        provider_state TEXT,
        provider_zip_code TEXT,
        provider_phone_number TEXT,
        county TEXT,
        staff_weekly_confirmed_covid_19 NUMERIC,
        residents_weekly_confirmed_covid_19 NUMERIC,
        residents_total_confirmed_covid_19 NUMERIC,
        staff_total_confirmed_covid_19 NUMERIC,
        residents_weekly_all_deaths NUMERIC,
        residents_weekly_covid_19_deaths NUMERIC,
        number_of_all_beds NUMERIC,
        total_number_of_occupied_beds NUMERIC
    )
    ''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS NursingHomeExtended (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        home_id INTEGER,
        passed_quality_assurance_check TEXT,
        submitted_data TEXT,
        FOREIGN KEY(home_id) REFERENCES NursingHomeData(id)
    )
    ''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    setup_database('nursing_home_data.db')