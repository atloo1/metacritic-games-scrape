# python -m metacritic_games_scrape.post_scrape.table_2

import pandas as pd

from ..constants import (
    CLEAN_JSON_FILEPATH,
    CRIT_SCORE_K,
    ESRB_K,
    DATE_K,
    DEV_K,
    PUB_K,
    USER_SCORE_K,
)
from .load_scrape_data import get_clean_data_df

df = get_clean_data_df()

# has both critiques
crit_score_mask = pd.notna(df[CRIT_SCORE_K])
user_score_mask = pd.notna(df[USER_SCORE_K])
crit_and_user_score_mask = crit_score_mask & user_score_mask
num_both_critiques = len(df.loc[crit_and_user_score_mask])  
print(f'num_both_critiques: {num_both_critiques}')

# has any criticism
crit_or_user_score_mask = crit_score_mask | user_score_mask
num_any_criticism = len(df.loc[crit_or_user_score_mask])
print(f'num_any_criticism: {num_any_criticism}')

# has dev & pub
has_dev_mask = pd.notna(df[DEV_K])
has_pub_mask = pd.notna(df[PUB_K])
has_dev_and_pub_mask = has_dev_mask & has_pub_mask
num_dev_and_pub = len(df.loc[has_dev_and_pub_mask])
print(f'num_dev_and_pub: {num_dev_and_pub}')

# has esrb
has_esrb_mask = pd.notna(df[ESRB_K])
num_esrb = len(df.loc[has_esrb_mask])
print(f'num_esrb: {num_esrb}')

# has date
has_date_mask = pd.notna(df[DATE_K])
num_dates = len(df.loc[has_date_mask])
print(f'num_dates: {num_dates}')
