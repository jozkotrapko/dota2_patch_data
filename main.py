import csv
import requests
from bs4 import BeautifulSoup

url = "https://dltv.org/stats/heroes?period=7.34"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

rows = soup.find_all('div', class_='table__body-row')

# Create and open the CSV file in write mode
with open('data.csv', 'w', newline='') as file:
    writer = csv.writer(file)

    # Write the header row
    writer.writerow(['HERO', 'MAPS PLAYED', 'BANS TOTAL', 'WINRATE', 'AV. DURATION', 'KDA'])

    # Iterate through each table row and write the data to the CSV file
    for row in rows:
        hero = row.find('div', class_='cell__name').text.strip()

        # Check if the required elements exist
        cells = row.find_all('div', class_='cell__text')
        if len(cells) >= 5:
            maps_played = cells[0].text.strip()
            bans_total = cells[1].text.strip()
            winrate = cells[2].text.strip().replace('%', '')  # Remove '%' symbol
            winrate = f"{float(winrate) / 100:.4f}"  # Convert to decimal format with 4 decimal places
            average_duration = cells[3].text.strip().split(':')
            average_duration = (int(average_duration[0]), int(average_duration[1]))  # Convert to tuple of integers

            kda = cells[4].text.strip()

            # Write the data as a row in the CSV file
            writer.writerow([hero, maps_played, bans_total, winrate, average_duration, kda])

print("Data saved to data.csv")