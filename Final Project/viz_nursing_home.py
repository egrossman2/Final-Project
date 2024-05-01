import sqlite3
import matplotlib.pyplot as plt

conn = sqlite3.connect('nursing_home_data.db')

conn.row_factory = sqlite3.Row  # Access columns by name
cur = conn.cursor()
cur.execute('''SELECT AVG(residents_weekly_confirmed_covid_19) AS avg_weekly_confirmed
               FROM NursingHomeData''')
avg_weekly_confirmed = cur.fetchone()['avg_weekly_confirmed']

cur.execute('''SELECT AVG(residents_weekly_covid_19_deaths) AS avg_weekly_deaths
               FROM NursingHomeData''')
avg_weekly_deaths = cur.fetchone()['avg_weekly_deaths']

averages = [avg_weekly_confirmed, avg_weekly_deaths]
categories = ['Weekly Confirmed Cases', 'Weekly Deaths']

plt.figure(figsize=(10, 5))
plt.bar(categories, averages, color=['blue', 'red'])
plt.title('Average Weekly COVID-19 Statistics per Nursing Home')
plt.ylabel('Average Number')
plt.show()

plt.figure(figsize=(10, 5))
plt.pie(averages, labels=categories, colors=['green', 'orange'], autopct='%1.1f%%', startangle=140)
plt.title('Proportion of Average Weekly COVID-19 Statistics per Nursing Home')
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.show()

conn = sqlite3.connect('nursing_home_data.db')
cursor = conn.cursor()
cursor.execute('''
        SELECT NHD.id,
               AVG(NHD.residents_weekly_confirmed_covid_19) AS avg_cases,
               AVG(NHD.residents_weekly_covid_19_deaths) AS avg_deaths
        FROM NursingHomeData NHD
        JOIN NursingHomeExtended NHE ON NHD.id = NHE.home_id
        GROUP BY NHD.id
    ''')
data = cursor.fetchall()
conn.close()

ids, avg_cases, avg_deaths = zip(*data)
plt.figure()
plt.plot(ids, avg_cases, label="Average Cases", color="blue")
plt.plot(ids, avg_deaths, label="Average Deaths", color="red")
plt.xlabel("Nursing Home ID")
plt.ylabel("Average per Week")
plt.legend()
plt.title("Average Weekly COVID-19 Cases and Deaths in Nursing Homes")
plt.savefig("avg_cases_deaths_nh.png")
plt.close()
