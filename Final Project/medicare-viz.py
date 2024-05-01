import matplotlib.pyplot as plt
import sqlite3

# Open a connection to the SQLite database
conn = sqlite3.connect('cms_medicare.db')

# Query for getting the number of providers per provider type for the bar chart
cursor = conn.cursor()
cursor.execute('''
    SELECT Pr.PROVIDER_TYPE_DESC, COUNT(*)
    FROM Providers Pr
    JOIN ProviderDetails Pd ON Pr.NPI = Pd.NPI
    GROUP BY Pr.PROVIDER_TYPE_DESC
''')
provider_type_counts = cursor.fetchall()
provider_types, counts = zip(*provider_type_counts)

# Bar Chart - Number of Providers per Provider Type
plt.figure(figsize=(12, 6))
plt.bar(provider_types, counts, color='cornflowerblue')
plt.xlabel('Provider Type')
plt.ylabel('Number of Providers')
plt.title('Number of Providers per Provider Type')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('provider_types_counts.png')
plt.show()

# Pie Chart - Distribution of Providers Among Provider Types
plt.figure(figsize=(12, 6))
plt.pie(counts, labels=provider_types, autopct='%1.1f%%', startangle=140)
plt.axis('equal')
plt.title('Distribution of Providers Among Provider Types')
plt.tight_layout()
plt.savefig('provider_types_distribution.png')
plt.show()

# Histogram - Distribution of Provider Counts
plt.figure(figsize=(12, 6))
plt.hist(counts, bins=10, color='lightseagreen', alpha=0.7)
plt.xlabel('Number of Providers')
plt.ylabel('Frequency')
plt.title('Distribution of Provider Counts Among Provider Types')
plt.tight_layout()
plt.savefig('provider_counts_distribution.png')
plt.show()

# Close the database connection
conn.close()