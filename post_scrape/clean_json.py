# python -m post_scrape.clean_json
import json
from datetime import datetime
from constants import (
    CLEAN_JSON_FILEPATH,
    DATE_K,
    ESRB_D,
    ESRB_K,
    GENRE_K,
    GENRES_K,
    NON_NEG_KS,
    NUM_CRIT_REVS_K,
    NUM_CRIT_REVS_KS,
    NUM_USER_REVS_K,
    NUM_USER_REVS_KS,
    PLATS_D,
    PLATS_K,
    SCORE_KS,
    SCRAPE_JSON_FILEPATH,
    URL_K,
)

with open(SCRAPE_JSON_FILEPATH) as f:
    game_dicts = json.load(f)

# list of dicts -> dict
games_dict = dict()

# map, type, & derive certain fields
for game_dict in game_dicts:
    # get key
    url = game_dict.pop(URL_K)

    # ensure non-negative fields
    for non_neg_k in NON_NEG_KS:
        v = game_dict[non_neg_k]
        if v is not None and v < 0:
            raise ValueError(f'{url} has < 0 key {non_neg_k} = {v}')

    # ensure bounded fields
    for score_k in SCORE_KS:
        v = game_dict[score_k]
        if v is not None:
            if v < 0 or v > 100:
                raise ValueError(f'{url} has < 0 | > 100 key {score_k} = {v}')

    # ensure datetime
    date = game_dict[DATE_K]
    if date is not None:
        try:
            datetime.strptime(date, '%b %d, %Y').date()
        except ValueError:
            raise ValueError(f'{url} date {date} not castable to datetime')

    # map 'Rated E' -> '≥6' years old, etc.
    esrb = game_dict.pop(ESRB_K)
    esrb = ESRB_D[esrb] if esrb is not None else esrb
    game_dict[ESRB_K] = esrb
    
    # genres -> genre b/c ≤ 1 genre per game
    genres = game_dict.pop(GENRES_K)
    if not genres:
        game_dict[GENRE_K] = None
    elif len(genres) > 1:
        raise ValueError(f'pipeline assumes ≤ 1 genre per game; {url} violates this')
    else:
        genre = genres[0]
        game_dict[GENRE_K] = genre

    # compute summary stats
    for num_rev_ks in [NUM_CRIT_REVS_KS, NUM_USER_REVS_KS]:
        num_rev_k = next(iter(num_rev_ks))
        
        if '_critic_' in num_rev_k:
            sum_k = NUM_CRIT_REVS_K
        elif '_user_' in num_rev_k:
            sum_k = NUM_USER_REVS_K
        else:
            raise ValueError(f'unhandled key {num_rev_k}')
        
        nums_revs = [
            game_dict[num_rev_k] if game_dict[num_rev_k] is not None else 0
            for num_rev_k in num_rev_ks
        ]
        game_dict[sum_k] = sum(nums_revs)

    # 1 hot encoded 'available on platform' field
    platforms_on = {PLATS_D[platform] for platform in game_dict.pop(PLATS_K)}
    for platform in PLATS_D.values():
        on_platform = True if platform in platforms_on else False
        platform_k = f'on_{platform}'
        game_dict[platform_k] = on_platform

    # build single dict
    games_dict[url] = game_dict

# dump & print status
incomplete = True

with open(CLEAN_JSON_FILEPATH, 'w') as f:
    json.dump(games_dict, f)
    incomplete = False
    
if incomplete:
    print('FAILURE: no clean JSON made')
else:
    print(f'SUCCESS: made {CLEAN_JSON_FILEPATH} of length {len(games_dict)}')
