import os
import datetime
import requests
import pandas as pd
from tqdm import tqdm

class EBirdTools:
    def __init__(self, api_key):
        with open(api_key) as f:
            self.headers = {'X-eBirdApiToken': f.read()}

    def get_species(self, lat, lng, back=14, dist=25):
        """
        Get recent sightings of all species by the specified location.
        Per the API, only lists one entry per species.
        @param lat: Latitude to 2 decimal places (-90 to 90)
        @param lng: Longitude to 2 decimal places (-180 to 180)
        @param back: Days back to fetch observations (1 to 30)
        @param dist: Search radius (km) from given position (0 to 50)
        @return: List of species
        """
        # https://api.ebird.org/v2/data/obs/geo/recent
        url = f"https://api.ebird.org/v2/data/obs/geo/recent?lat={lat}&lng={lng}&back={back}&dist={dist}"
        req = requests.request("GET", url, headers=self.headers)
        
        df = pd.read_json(req.text)
        # Throw away the rest of the columns in the df. We only care about the speciesCode.
        output = df['speciesCode'].to_list()
        return output
    
    def get_sightings(self, species, lat, lng, back=14, dist=25, verbose=False):
        """
        Get recent sightings of each of the listed species by the specified location.
        @param species: List of species
        @param lat: Latitude to 2 decimal places (-90 to 90)
        @param lng: Longitude to 2 decimal places (-180 to 180)
        @param back: Days back to fetch observations (1 to 30)
        @param dist: Search radius (km) from given position (0 to 50)
        @param verbose: Whether to silence debug info
        @return: Df of all sightings
        """
        # Get all individual sightings per species.
        df_list = []
        for s in tqdm(species, disable=(not verbose)):
            # https://api.ebird.org/v2/data/obs/geo/recent/{{speciesCode}}
            url = f"https://api.ebird.org/v2/data/obs/geo/recent/{s}?lat={lat}&lng={lng}&back={back}&dist={dist}"
            req = requests.request("GET", url, headers=self.headers)
            
            df = pd.read_json(req.text)
            df_list.append(df)
        
        df = pd.concat(df_list)
        # Replace invalid values for howMany with 1's
        df = df.fillna({'howMany': 1})
        return df

    def get_data(self, lat, lng, back=14, dist=25, verbose=False):
        """
        The main pipeline. Returns df and also saves it to a csv.
        """
        try:
            species = self.get_species(lat, lng, back, dist)
            if verbose:
                print('Species found:', len(species))
            df = self.get_sightings(species, lat, lng, back, dist, verbose)
    
            # Deliberately start filename with "ebd*" so that it gets gitignore'd
            filename = 'ebd_' \
                + datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') \
                + f'_{lat}_{lng}_{back}_{dist}' \
                + '.csv'
            # Save into a subdirectory
            filename = os.path.join('data', filename)
            df.to_csv(filename)
            if verbose:
                print('Data saved to:', filename)
            
            # The original format is better for filesize. Decompress AFTER saving.
            df = EBirdTools.decompress(df)
            return df
        except KeyError:
            print('Query contained no data. Aborting.')

    def decompress(df):
        """
        Static method to decompress a df. Removes the howMany column
        by creating new rows of duplicate entries.
        Does not access the API.
        """
        df = df.copy()
        
        # This helper function returns a list with a length
        # equal to the input number
        _x = lambda x: [None for _ in range(int(x))]
        df['howMany'] = df['howMany'].apply(_x)
        # Explode to make the duplicate entries
        df = df.explode('howMany')
        df = df.drop('howMany', axis=1)
        # Clean up
        df = df.reset_index(drop=True)
        return df
    
    def load_data(filename):
        """
        Static method to load data from a file.
        Does not access the API.
        """
        df = pd.read_csv(filename, index_col=0)
        df = EBirdTools.decompress(df)
        return df