import requests
import sqlite3
from sqlite3 import IntegrityError

API_URL = "https://data.covid19india.org/v4/min/data.min.json"

def get_api_data():
    response = requests.get(API_URL)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

def insert_data_into_db(db_name, api_data):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    inserted_rows = 0

    for state_code, state_info in api_data.items():
        if inserted_rows >= 25:
            break

        state_meta = state_info.get('meta', {})
        state_total = state_info.get('total', {})
        cur.execute('''
            INSERT OR IGNORE INTO StateData (state_code, last_updated, population, confirmed, deceased, recovered, tested, vaccinated)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
            (
                state_code,
                state_meta.get('last_updated', ''),
                state_meta.get('population', 0),
                state_total.get('confirmed', 0),
                state_total.get('deceased', 0),
                state_total.get('recovered', 0),
                state_total.get('tested', 0),
                state_total.get('vaccinated', 0)
            )
        )
        inserted_rows += 1

        state_id = cur.lastrowid

        districts = state_info.get('districts', {})
        for district_name, district_info in districts.items():
            if inserted_rows >= 25:
                break

            district_meta = district_info.get('meta', {})
            district_total = district_info.get('total', {})
            cur.execute('''
                INSERT OR IGNORE INTO DistrictData (state_id, district_name, population, confirmed, deceased, recovered, tested, vaccinated)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                (
                    state_id,
                    district_name,
                    district_meta.get('population', 0),
                    district_total.get('confirmed', 0),
                    district_total.get('deceased', 0),
                    district_total.get('recovered', 0),
                    district_total.get('tested', 0),
                    district_total.get('vaccinated', 0),
                )
            )
            inserted_rows += 1

        if inserted_rows >= 25:
            break

    conn.commit()
    conn.close()

if __name__ == '__main__':
    api_data = get_api_data()
    insert_data_into_db('FinalData.db', api_data)