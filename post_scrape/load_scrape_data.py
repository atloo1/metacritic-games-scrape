import json

import pandas as pd

from metacritic_games_scrape.constants import (     # TODO relative imports
    CLEAN_JSON_FILEPATH,
    DATE_K
)

def get_clean_data_df():
    with open(CLEAN_JSON_FILEPATH) as f:
        games_d = json.load(f)
    
    df = pd.DataFrame(games_d).T
    df[DATE_K] = pd.to_datetime(df[DATE_K])
    return df
