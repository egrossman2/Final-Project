import requests
import sqlite3
from sqlite3 import IntegrityError

API_URL = "https://data.cms.gov/data-api/v1/dataset/137f90cb-ac53-4b3d-8358-e65cf64e03d3/data"

def get_api_data():
    response = requests.get(API_URL)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

def insert_data_into_db(db_name, api_data):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    for count, record in enumerate(api_data):
        if count >= 25:
            break
        try:
            cur.execute('''
                INSERT INTO NursingHomeData (week_ending, provider_name, provider_address, provider_city, provider_state, provider_zip_code, provider_phone_number, county, staff_weekly_confirmed_covid_19, residents_weekly_confirmed_covid_19, residents_total_confirmed_covid_19, staff_total_confirmed_covid_19, residents_weekly_all_deaths, residents_weekly_covid_19_deaths, number_of_all_beds, total_number_of_occupied_beds) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (
                    record['week_ending'],
                    record['provider_name'],
                    record['provider_address'],
                    record['provider_city'],
                    record['provider_state'],
                    record['provider_zip_code'],
                    record['provider_phone_number'],
                    record['county'],
                    record['staff_weekly_confirmed_covid_19'],
                    record['residents_weekly_confirmed_covid_19'],
                    record['residents_total_confirmed_covid_19'],
                    record['staff_total_confirmed_covid_19'],
                    record['residents_weekly_all_deaths'],
                    record['residents_weekly_covid_19_deaths'],
                    record['number_of_all_beds'],
                    record['total_number_of_occupied_beds']
                )
            )
            home_id = cur.lastrowid
            cur.execute('''
                INSERT INTO NursingHomeExtended (home_id, passed_quality_assurance_check, submitted_data) 
                VALUES (?, ?, ?)''',
                (
                    home_id,
                    record['passed_quality_assurance_check'],
                    record['submitted_data']
                )
            )
        except IntegrityError:
            continue

    conn.commit()
    conn.close()

if __name__ == '__main__':
    api_data = get_api_data()
    insert_data_into_db('FinalData.db', api_data)