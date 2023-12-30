# metacritic-games-scrape

### setup (assumes [poetry](python-poetry.com) prerequisite)
```
poetry install --only scrape  # if scraping yourself
poetry install --only analyze  # if using pre-existing data
poetry install --without dev     # everything above
poetry install  # if developing
```

### [reproduce data](https://drive.google.com/drive/folders/1cbFvyNQ35JMsCnaBpy-t3rCZphIQwMFY?usp=sharing)
```
cd <project-root>
scrapy crawl metacritic_games -L DEBUG -O post_scrape/data.json --logfile post_scrape/logs.txt
python post_scrape/clean_json.py    # process scrape data per write-up procedure
```
`data.json.gz`: scrape results used in write-up

`logs.json.gz`: logs underlying `data.json.gz`

`http_cache.tar.gz` (available upon request): scrapy HTTP cache underlying `data.json.gz`; use via `tar -xzf http_cache.tar.gz -C <project-root>/.scrapy/httpcache/`

### reproduce findings
`clean_data_validation.ipynb`: manually inspect scrape output per write-up procedure

`table_2.py`: reproduce underlying data for table 2

`fig_1.ipynb`: reproduce figure 1

`fig_2.ipynb`: reproduce figure 2

`fig_3.ipynb`: reproduce figure 3

`fig_4.ipynb`: reproduce figure 4

`tables_3_4_fig_5.ipynb`: reproduce underlying data for tables 3 & 4 + figure 5

`tables_2_3_4_fig_5_pretty.ipynb`: reproduce tables 2, 3, & 4 + figure 5 as seen in write-up

### reading materials ([available upon request](https://drive.google.com/drive/folders/1m8wfo5qNFt-TyoxRlzkI1yu7kGcgnSNV?usp=sharing))
`supplement_citations.pdf`: textual citations as seen in write-up

`supplement_figures.pdf`: enlarged figures from write-up

`supplement_table_1.pdf`: table 1 as alluded to in write-up

`supplement_table_3.pdf`: complete table 3 as alluded to in write-up

`write-up.pdf`: a research-style paper presenting the work of this repository

### utils
`load_scrape_data.py`: instantiate DataFrame of cleaned scrape data

`nlp_utils.py`: text normalization, topic modeling, & cross validation pipeline

### bash helpers
```
cd <project-root>

# scrape progress; 1 line = 1 page
wc -l metacritic_games_scrape/data.json

# find a page in HTTP cache; next scrape will re-download it if deleted
query_url="https://www.metacritic.com/game/halo-2/"  # set me
query_str="{'url': '${query_url}'"
find metacritic_games_scrape/.scrapy/httpcache/metacritic_games/ -type f -name "meta" -exec bash -c '[[ "$(head -n 1 "$0")" == "$1"* ]] && echo "File $0 starts with query_str"' {} "$query_str" \;
```
