import sqlite3

DB_NAME = 'FinalData.db'
OUTPUT_FILE = 'average_cases.txt'

def calculate_average_cases(db_name):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    cur.execute('''
    SELECT AVG(NHD.residents_weekly_confirmed_covid_19) as avg_confirmed_cases
    FROM NursingHomeData NHD
    JOIN NursingHomeExtended NHE ON NHD.id = NHE.home_id
    ''')
    result = cur.fetchone()[0]

    conn.close()

    return result

def write_to_file(filename, data):
    with open(filename, 'w') as file:
        file.write(str(data))

def main():
    avg_cases = calculate_average_cases(DB_NAME)
    write_to_file(OUTPUT_FILE, f"The average number of weekly confirmed COVID-19 cases per nursing home is: {avg_cases}")
    print(f"Calculation complete. Check the {OUTPUT_FILE} file for the result.")

if __name__ == '__main__':
    main()