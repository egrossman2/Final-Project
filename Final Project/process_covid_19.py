import sqlite3

DB_NAME = 'covid19_india_data.db'
OUTPUT_FILE = 'calculated_data.txt'

# Connect to the database and perform calculations
conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

# Total confirmed COVID-19 cases
cursor.execute("SELECT SUM(confirmed) FROM StateData")
total_confirmed = cursor.fetchone()[0]

# Average confirmed COVID-19 cases per state
cursor.execute("SELECT AVG(confirmed) FROM StateData")
average_confirmed_per_state = cursor.fetchone()[0]

conn.close()

# Write the calculated data to a text file
with open(OUTPUT_FILE, 'w') as file:
    file.write(f"Total confirmed cases in India: {total_confirmed}\n")
    file.write(f"Average confirmed cases per state in India: {average_confirmed_per_state}\n")