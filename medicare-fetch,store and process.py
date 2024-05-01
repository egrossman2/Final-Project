import requests
import sqlite3

# Constants
DB_NAME = 'FinalData.db'
API_URL = "https://data.cms.gov/data-api/v1/dataset/2457ea29-fc82-48b0-86ec-3b0755de7515/data"

# Database Setup
def setup_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Providers (
            NPI TEXT PRIMARY KEY,
            PROVIDER_TYPE_CD TEXT,
            PROVIDER_TYPE_DESC TEXT,
            STATE_CD TEXT,
            FIRST_NAME TEXT,
            MDL_NAME TEXT,
            LAST_NAME TEXT,
            ORG_NAME TEXT,
            GNDR_SW TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ProviderDetails (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ENRLMT_ID TEXT,
            PECOS_ASCT_CNTL_ID TEXT,
            NPI TEXT,
            FOREIGN KEY (NPI) REFERENCES Providers (NPI)
        )
    ''')
    conn.commit()
    conn.close()

setup_database()

def fetch_data():
    response = requests.get(API_URL)
    if response.status_code == 200:
        records = response.json()[:25]
        return records
    else:
        print(f"Error fetching data: Status Code {response.status_code}")

# Store data into the database
def store_data(records):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    for record in records:
        cursor.execute('''
            INSERT OR IGNORE INTO Providers (NPI, PROVIDER_TYPE_CD, PROVIDER_TYPE_DESC, STATE_CD, FIRST_NAME,
                                   MDL_NAME, LAST_NAME, ORG_NAME, GNDR_SW)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            record['NPI'],
            record['PROVIDER_TYPE_CD'],
            record['PROVIDER_TYPE_DESC'],
            record['STATE_CD'],
            record['FIRST_NAME'],
            record['MDL_NAME'],
            record['LAST_NAME'],
            record['ORG_NAME'],
            record['GNDR_SW']
        ))
        cursor.execute('''
            INSERT OR IGNORE INTO ProviderDetails (ENRLMT_ID, PECOS_ASCT_CNTL_ID, NPI)
            VALUES (?, ?, ?)
        ''', (
            record['ENRLMT_ID'],
            record['PECOS_ASCT_CNTL_ID'],
            record['NPI']
        ))

    conn.commit()
    conn.close()
    
def process_data():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()

        cursor.execute('''
            SELECT Pr.PROVIDER_TYPE_DESC, COUNT(*)
            FROM Providers Pr
            JOIN ProviderDetails Pd ON Pr.NPI = Pd.NPI
            GROUP BY Pr.PROVIDER_TYPE_DESC
        ''')
        results = cursor.fetchall()

        with open('Medicare-caculated.txt', 'w') as f:
            for provider_type, count in results:
                f.write(f"Provider Type: {provider_type}, Number of Providers: {count}\n")



    conn.commit()
    conn.close()
for _ in range(4):
    batch_records = fetch_data()
    if batch_records:
        store_data(batch_records)