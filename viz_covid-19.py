import matplotlib.pyplot as plt
import sqlite3

DB_NAME = 'FinalData.db'

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

# Fetch total confirmed cases by the state
cursor.execute("SELECT state_code, confirmed FROM StateData")
data_confirmed = cursor.fetchall()

states, confirmed_cases = zip(*data_confirmed)

# Bar Plot: Total Confirmed Cases by State
plt.figure()
plt.bar(states, confirmed_cases, color='blue')
plt.xlabel('State Code')
plt.ylabel('Total Confirmed Cases')
plt.title('Total COVID-19 Confirmed Cases by State in India')
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig('total_confirmed_cases_by_state.png')
plt.show()

# Fetch recovered cases by the state
cursor.execute("SELECT state_code, recovered FROM StateData")
data_recovered = cursor.fetchall()

states, recovered_cases = zip(*data_recovered)

# Bar Plot: Total Recovered Cases by State
plt.figure()
plt.bar(states, recovered_cases, color='green')
plt.xlabel('State Code')
plt.ylabel('Total Recovered Cases')
plt.title('Total COVID-19 Recovered Cases by State in India')
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig('total_recovered_cases_by_state.png')
plt.show()

conn.close()