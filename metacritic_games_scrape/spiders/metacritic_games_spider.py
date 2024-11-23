import html

from scrapy import Spider
from scrapy.selector import Selector

from constants import (
    DATE_K,
    DESC_K,
    GAME_META_COLL_PARSE_D,
    GAME_META_PARSE_D,
    GAME_PAGE_URLS_XPATH,
    NEXT_PAGE_DISABLED_STR,
    NEXT_PAGE_ENABLED_STR,
    NEXT_PAGE_XPATH,
    REVS_PARSE_D,
    SKIP_URLS,
    START_URL,
    URL_K,
    USER_SCORE_K,
)


class MainSpider(Spider):
    name = 'metacritic_games'
    start_urls = [
        START_URL,
    ]
    # galleries_d = dict()    # debug duplicate URLs more granularly than DUPEFILTER_DEBUG

    def parse_game_page(self, response):
        url = response.url
        game_d = {URL_K: url}

        # add metadata str values to dict
        for k, xpath in GAME_META_PARSE_D.items():
            v = Selector(text=response.body).xpath(xpath).get()
            # self.logger.debug(f'{url} {k}: {v}')
            if v is not None:
                v = html.unescape(v).strip()

                # avoid 'Feb NaN, 2000' -> '2000-02-01' & fabricating resolution
                if k == DATE_K and 'NaN' in v:
                    # self.logger.debug(f'{url} {k}: {v} overwritten to None')
                    v = None

                # false positives, e.g. https://www.metacritic.com/game/pimania/
                elif k == DESC_K and v == 'loaded':
                    # self.logger.debug(f'{url} {k}: {v} overwritten to None')
                    v = None

            # else:
            #     self.logger.debug(f'{url} {k} is None')

            # self.logger.debug(f'{url} {k}: {v}')
            game_d[k] = v

        # add Collection values to dict
        for k, xpath in GAME_META_COLL_PARSE_D.items():
            vs = Selector(text=response.body).xpath(xpath).getall()
            # self.logger.debug(f'{url} {k}: {vs}')
            vs = sorted(html.unescape(v).strip() for v in vs)  # sort for convenient comparison
            # self.logger.debug(f'{url} {k}: {vs}')
            game_d[k] = vs

        # add int values to dict
        for k, xpath in REVS_PARSE_D.items():
            v = Selector(text=response.body).xpath(xpath).get()
            # self.logger.debug(f'{url} {k}: {v}')
            if v is not None:
                v = v.split(' ')[0]
                if k == USER_SCORE_K:
                    v = v.replace('.', '')  # '1.2' -> '12' for CRIT_SCORE_K
                v = None if v == 'tbd' else int(v)
                # self.logger.debug(f'{url} {k}: {v}')

            # else:
            # self.logger.debug(f'{url} {k} is None')

            # self.logger.debug(f'{url} {k}: {v}')
            game_d[k] = v

        yield game_d

    def parse(self, response):
        # get game page URLs from this gallery page & parse them
        # url = response.url
        game_page_urls = Selector(text=response.body).xpath(GAME_PAGE_URLS_XPATH).getall()
        # self.logger.debug(f'{url} game_page_urls: {game_page_urls}')
        # self.galleries_d[url] = game_page_urls
        for game_page_url in game_page_urls:
            if game_page_url not in SKIP_URLS:
                yield response.follow(game_page_url, self.parse_game_page)

        # paginate gallery for new game page URLs
        next_page_arrow_selector = Selector(text=response.body).xpath(NEXT_PAGE_XPATH).get()
        next_page_enabled = next_page_arrow_selector.startswith(NEXT_PAGE_ENABLED_STR)
        next_page_disabled = next_page_arrow_selector.startswith(NEXT_PAGE_DISABLED_STR)
        next_page_statuses = (next_page_enabled, next_page_disabled)

        if all(next_page_statuses) or not any(next_page_statuses):
            raise ValueError(f'next_page_enabled: {next_page_enabled} & next_page_disabled: {next_page_disabled}')

        if next_page_enabled:
            this_gallery_page_url = response.url
            gallery_page_url, this_page_num = this_gallery_page_url.rsplit('=', 1)
            next_page_num = int(this_page_num) + 1
            next_gallery_page_url = f'{gallery_page_url}={next_page_num}'
            yield response.follow(next_gallery_page_url, self.parse)

        # else:
        #     self.logger.debug(f'galleries_d: {self.galleries_d}')
