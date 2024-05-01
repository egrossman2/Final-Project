import sqlite3

def setup_database(db_name):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    cur.execute('''
    CREATE TABLE IF NOT EXISTS StateData (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        state_code TEXT UNIQUE NOT NULL,
        last_updated TEXT,
        population INTEGER,
        confirmed INTEGER,
        deceased INTEGER,
        recovered INTEGER,
        tested INTEGER,
        vaccinated INTEGER
    )
    ''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS DistrictData (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        state_id INTEGER NOT NULL,
        district_name TEXT NOT NULL,
        population INTEGER,
        confirmed INTEGER,
        deceased INTEGER,
        recovered INTEGER,
        tested INTEGER,
        vaccinated INTEGER,
        FOREIGN KEY (state_id) REFERENCES StateData (id)
    )
    ''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    setup_database('FinalData.db')