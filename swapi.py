import requests
import sqlite3
import matplotlib.pyplot as plt

SWAPI_BASE_URL = "https://swapi.dev/api"
DB_NAME = 'FinalData.db'

def setup_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS People (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        height INTEGER,
                        mass INTEGER,
                        homeworld TEXT
                    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS Planets (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        population INTEGER,
                        url TEXT
                    )''')
    conn.commit()
    conn.close()

def fetch_data(api_url, endpoint):
    url = f"{api_url}/{endpoint}"
    response = requests.get(url, verify=False)
    return response.json()['results']

def store_data():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    people = fetch_data(SWAPI_BASE_URL, 'people')
    planets = fetch_data(SWAPI_BASE_URL, 'planets')
    for person in people[:25]:
        cursor.execute('INSERT INTO People (name, height, mass, homeworld) VALUES (?, ?, ?, ?)',
                       (person['name'], person['height'], person['mass'], person['homeworld']))
    for planet in planets[:25]:
        cursor.execute('INSERT INTO Planets (name, population, url) VALUES (?, ?, ?)',
                       (planet['name'], planet['population'], planet['url']))
    conn.commit()
    conn.close()

setup_database()
store_data()

def process_and_join_data():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT AVG(p.height) AS avg_height, SUM(pl.population) AS total_population
        FROM People p
        JOIN Planets pl ON p.homeworld = pl.url
    ''')
    result = cursor.fetchone()
    avg_height = result[0]
    total_population = result[1]

    with open('output.txt', 'w') as file:
        file.write(f"Average Height: {avg_height}\n")
        file.write(f"Total Homeworld Population: {total_population}\n")

    cursor.execute('SELECT pl.name, COUNT(*) FROM People p JOIN Planets pl ON p.homeworld = pl.url GROUP BY pl.name')
    homeworld_counts = cursor.fetchall()
    conn.close()
    return homeworld_counts, avg_height

homeworld_counts, avg_height = process_and_join_data()

plt.figure(figsize=(12, 6))
homeworlds, counts = zip(*homeworld_counts)
plt.bar(homeworlds, counts, color='skyblue')
plt.xlabel('Homeworld')
plt.ylabel('Number of Characters')
plt.title('Number of Characters per Homeworld')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('characters_per_homeworld.png')
plt.show()

plt.figure(figsize=(12, 6))
plt.axhline(y=avg_height, color='red', linestyle='-')
plt.text(0.5, avg_height, f'Average height = {avg_height}', fontsize=12, va='center', ha='center', backgroundcolor='w')
plt.title('Average Height of Characters')
plt.xlabel('Homeworld')
plt.ylabel('Average Height')
plt.xticks([])
plt.tight_layout()
plt.savefig('avg_height.png')
plt.show()

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()
cursor.execute('SELECT height, mass FROM People WHERE height <> "unknown" AND mass <> "unknown"')
scatter_data = cursor.fetchall()
conn.close()
heights, masses = zip(*[(h, m) for h, m in scatter_data if h is not None and m is not None])

plt.figure(figsize=(12, 6))
plt.scatter(heights, masses, alpha=0.5, color='green')
plt.xlabel('Height (cm)')
plt.ylabel('Mass (kg)')
plt.title('Height and Mass of Characters')
plt.tight_layout()
plt.savefig('height_vs_mass.png')
plt.show()