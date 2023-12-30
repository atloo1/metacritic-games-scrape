from pathlib import Path

# START_URL = 'https://www.metacritic.com/browse/game/?page=1'    # metascored
START_URL = 'https://www.metacritic.com/browse/game/all/all/all-time/new/?page=1'   # existing


HERE_FILEPATH = Path(__file__).resolve()
PROJ_ROOT_PATH = HERE_FILEPATH.parent
POST_SCRAPE_PATH = PROJ_ROOT_PATH / 'post_scrape'
CLEAN_JSON_FILEPATH = POST_SCRAPE_PATH / 'data_cleaned.json'
SCRAPE_JSON_FILEPATH = POST_SCRAPE_PATH / 'data.json'

# xpath & corresponding data fields
CRIT_SCORE_K = 'critics_score'     # critics' AKA metascore
CRIT_SCORE_XPATH = '/html/body/div[1]/div/div/div[2]/div[1]/div[4]/div/div[2]/div/div[1]/div[2]/div/div[1]/div/div/a//span/text()'
DATE_K = 'date'     # initial release date
DATE_XPATH = '/html/body/div[1]/div/div/div[2]/div[1]/div[6]/div/div/div[2]/div[2]/div[1]//div [@class="c-gameDetails_ReleaseDate u-flexbox u-flexbox-row"]/span[2]/text()'
DESC_K = 'description'   # promotional summary of the game
DESC_XPATH = '/html/head/meta[28]/@content'
DEV_K = 'developer'
DEV_XPATH = '/html/body/div[1]/div/div/div[2]/div[1]/div[6]/div/div/div[2]/div[2]/div[2]/div [@class="c-gameDetails_Developer u-flexbox u-flexbox-row"]//li/text()'
ESRB_K = 'esrb'     # ESRB content rating
ESRB_XPATH = '/html/body/div[1]/div/div/div[2]/div[1]/div[6]/div/div/div[2]/div[1]/div//div [@class="c-productionDetailsGame_esrb_title u-inline-block g-outer-spacing-left-medium-fluid"]/span[1]/text()'
GAME_PAGE_URLS_XPATH = '/html/body/div[1]/div/div/div[2]/div[1]/main/section/div[3]//div [@class="c-finderProductCard c-finderProductCard-game"]/a/@href'
GENRE_K = 'genre'
GENRES_K = 'genres'
GENRES_XPATH = '/html/body/div[1]/div/div/div[2]/div[1]/div[6]/div/div//li [@class="c-genreList_item"]/div/a/span/text()'
NEXT_PAGE_XPATH = '/html/body/div[1]/div/div/div[2]/div[1]/main/section/div[4]/span[3]'
NUM_CRIT_MIX_REVS_K = 'num_critic_mixed_reviews'
NUM_CRIT_MIX_REVS_XPATH = '/html/body/div[1]/div/div/div[2]/div[1]/div[4]/div/div[2]/div/div[1]/div[2]/div/div[2]//div [@class="c-reviewsStats_neutralStats"]/span[2]/text()'
NUM_CRIT_NEG_REVS_K = 'num_critic_negative_reviews'
NUM_CRIT_NEG_REVS_XPATH = '/html/body/div[1]/div/div/div[2]/div[1]/div[4]/div/div[2]/div/div[1]/div[2]/div/div[2]//div [@class="c-reviewsStats_negativeStats"]/span[2]/text()'
NUM_CRIT_POS_REVS_K = 'num_critic_positive_reviews'
NUM_CRIT_POS_REVS_XPATH = '/html/body/div[1]/div/div/div[2]/div[1]/div[4]/div/div[2]/div/div[1]/div[2]/div/div[2]//div [@class="c-reviewsStats_positiveStats"]/span[2]/text()'
NUM_CRIT_REVS_K = 'num_critic_reviews'
NUM_USER_MIX_REVS_K = 'num_user_mixed_reviews'
NUM_USER_MIX_REVS_XPATH = '/html/body/div[1]/div/div/div[2]/div[1]/div[4]/div/div[4]/div/div[1]/div[2]/div/div[2]//div [@class="c-reviewsStats_neutralStats"]/span[2]/text()'
NUM_USER_NEG_REVS_K = 'num_user_negative_reviews'
NUM_USER_NEG_REVS_XPATH = '/html/body/div[1]/div/div/div[2]/div[1]/div[4]/div/div[4]/div/div[1]/div[2]/div/div[2]//div [@class="c-reviewsStats_negativeStats"]/span[2]/text()'
NUM_USER_POS_REVS_K = 'num_user_positive_reviews'
NUM_USER_POS_REVS_XPATH = '/html/body/div[1]/div/div/div[2]/div[1]/div[4]/div/div[4]/div/div[1]/div[2]/div/div[2]//div [@class="c-reviewsStats_positiveStats"]/span[2]/text()'
NUM_USER_REVS_K = 'num_user_reviews'
PLATS_K = 'platforms'
PLATS_XPATH = '/html/body/div[1]/div/div/div[2]/div[1]/div[6]/div/div/div[2]/div[2]/div[1]/div [@class="c-gameDetails_Platforms u-flexbox u-flexbox-row"]//li/text()'
PUB_K = 'publisher'
PUB_XPATH = '/html/body/div[1]/div/div/div[2]/div[1]/div[6]/div/div/div[2]/div[2]/div[2]/ div [@class="c-gameDetails_Distributor u-flexbox u-flexbox-row"]/span[2]/text()'
USER_SCORE_K = 'users_score'
USER_SCORE_XPATH = '/html/body/div[1]/div/div/div[2]/div[1]/div[4]/div/div[4]/div/div[1]/div[2]/div/div[1]/div/div/a//span/text()'
TITLE_K = 'title'
TITLE_XPATH = '/html/body/div[1]/div/div/div[2]/div[1]/div[1]/div/div/div[2]/div[3]/div[1]/div/text()'
URL_K = 'url'

# the content @ NEXT_PAGE_XPATH showing if pagination is allowed
NEXT_PAGE_ENABLED_STR = '<span class="c-navigationPagination_item c-navigationPagination_item--next enabled">'
NEXT_PAGE_DISABLED_STR = '<span class="c-navigationPagination_item c-navigationPagination_item--next disabled">'

ESRB_D = {      # text label to numerical age
    'Rated AO': '18+',
    'Rated E': '6+',
    'Rated E +10': '10+',
    'Rated eC': '3+',
    'Rated M': '17+',
    'Rated T': '13+',
    'Rated RP': '?',
}
GAME_META_COLL_PARSE_D = {  # parsing dict for game metadata of type Collection 
    GENRES_K: GENRES_XPATH,
    PLATS_K: PLATS_XPATH,
}
GAME_META_PARSE_D = {   # game metadata parsing dict
    ESRB_K: ESRB_XPATH,
    DESC_K: DESC_XPATH,
    DEV_K: DEV_XPATH,
    PUB_K: PUB_XPATH,
    DATE_K: DATE_XPATH,
    TITLE_K: TITLE_XPATH,
}
DESCRIPTIVE_KS = [    # most readable subset of fields
    DATE_K,
    DESC_K,
    DEV_K,
    ESRB_K,
    GENRE_K,
    PUB_K,
    TITLE_K,
]
NON_NEG_KS = {  # these have values ≥ 0
    CRIT_SCORE_K,
    NUM_CRIT_MIX_REVS_K,
    NUM_CRIT_NEG_REVS_K,
    NUM_CRIT_POS_REVS_K,
    NUM_USER_MIX_REVS_K,
    NUM_USER_NEG_REVS_K,
    NUM_USER_POS_REVS_K,
    USER_SCORE_K,
    }
NUM_CRIT_REVS_KS = {    # grouped under number of critic reviews
    NUM_CRIT_MIX_REVS_K,
    NUM_CRIT_NEG_REVS_K,
    NUM_CRIT_POS_REVS_K,
}
NUM_USER_REVS_KS = {    # grouped under number of user reviews
    NUM_USER_MIX_REVS_K,
    NUM_USER_NEG_REVS_K,
    NUM_USER_POS_REVS_K,
}
PLATS_D = {  # pythonic names for platforms 
    '3DS': '3ds',
    'Dreamcast': 'dreamcast',
    'DS': 'ds',
    'Game Boy Advance': 'gba',
    'GameCube': 'gc',
    'iOS (iPhone/iPad)': 'ios',
    'Nintendo 64': 'n64',
    'Nintendo Switch': 'switch',
    'PC': 'pc',
    'PlayStation 2': 'ps2',
    'PlayStation 3': 'ps3',
    'PlayStation 4': 'ps4',
    'PlayStation 5': 'ps5',
    'PlayStation Vita': 'ps_vita',
    'PlayStation': 'ps1',
    'PSP': 'psp',
    'Wii U': 'wii_u',
    'Wii': 'wii',
    'Xbox 360': 'xbox_360',
    'Xbox One': 'xbox_1',
    'Xbox Series X': 'xbox_x',
    'Xbox': 'xbox',
}
REVS_PARSE_D = {    # reviews parsing dict
    CRIT_SCORE_K: CRIT_SCORE_XPATH,
    NUM_CRIT_MIX_REVS_K: NUM_CRIT_MIX_REVS_XPATH,
    NUM_CRIT_NEG_REVS_K: NUM_CRIT_NEG_REVS_XPATH,
    NUM_CRIT_POS_REVS_K: NUM_CRIT_POS_REVS_XPATH,
    NUM_USER_MIX_REVS_K: NUM_USER_MIX_REVS_XPATH,
    NUM_USER_NEG_REVS_K: NUM_USER_NEG_REVS_XPATH,
    NUM_USER_POS_REVS_K: NUM_USER_POS_REVS_XPATH,
    USER_SCORE_K: USER_SCORE_XPATH,
}
SCORE_KS = {  # these have 0 ≤ values ≤ 100
    CRIT_SCORE_K,
    USER_SCORE_K,
}
SKIP_URLS = {   # relative URLs to skip
    # not games
    '/',  # https://www.metacritic.com/
    '/game/nintendo-ds/',
    '/game/nintendo-switch/',
    '/game/nintendo-wii/',
    '/game/playstation-3/',
    '/game/playstation-4/',
    '/game/playstation-5/',
    '/game/playstation-portable/',
    '/game/playstation-vita/',
    '/game/wii-u/',
    '/game/xbox-360/',
    '/game/xbox-series-x/',
    # malformed pages w/ identity crisis
    '/game/ginka/',
    '/game/the-awakener-forgotten-oath/',
}

CRIT_KS = {CRIT_SCORE_K} | NUM_CRIT_REVS_KS
USER_KS = {USER_SCORE_K} | NUM_USER_REVS_KS
CRITICISM_KS = CRIT_KS | USER_KS
