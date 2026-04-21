import requests
import logging
import pandas as pd

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class LaLigaScraper:
    def __init__(self):
        self.seasons = []  # List to store seasons
        # Add any initialization required

    def download_data(self, season):
        try:
            url = f'https://api.laliga.com/data/{season}'  # Example URL
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for bad responses
            logging.info(f'Successfully downloaded data for season: {season}')
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            logging.error(f'HTTP error occurred: {http_err}')
        except Exception as err:
            logging.error(f'An error occurred: {err}')
        return None

    def process_data(self, data):
        try:
            # Process the data, extract referee information and events
            # Return structured data (e.g., DataFrame)
            # This is a placeholder for actual data processing logic
            return pd.DataFrame(data)
        except Exception as err:
            logging.error(f'Error processing data: {err}')
            return None

    def save_to_csv(self, data, filename):
        try:
            data.to_csv(filename, index=False)
            logging.info(f'Data saved to {filename}')
        except Exception as err:
            logging.error(f'Error saving data to CSV: {err}')

def main():
    scraper = LaLigaScraper()
    seasons = ['2021', '2022', '2023']  # Specify the seasons you want to download
    for season in seasons:
        data = scraper.download_data(season)
        if data:
            processed_data = scraper.process_data(data)
            if processed_data is not None:
                scraper.save_to_csv(processed_data, f'laliga_events_{season}.csv')

if __name__ == '__main__':
    main()