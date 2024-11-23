# metacritic-games-scrape

[![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/atloo1/metacritic-games-scrape/ci.yaml)](https://github.com/atloo1/metacritic-games-scrape/actions/workflows/ci.yaml?query=branch%3Amain)
[![Dynamic TOML Badge](https://img.shields.io/badge/dynamic/toml?url=https%3A%2F%2Fraw.githubusercontent.com%2Fatloo1%2Fmetacritic-games-scrape%2Frefs%2Fheads%2Fmain%2Fpyproject.toml&query=%24.tool.poetry.dependencies.python&label=python)](https://github.com/atloo1/metacritic-games-scrape/blob/main/pyproject.toml)
[![Dynamic TOML Badge](https://img.shields.io/badge/dynamic/toml?url=https%3A%2F%2Fraw.githubusercontent.com%2Fatloo1%2Fmetacritic-games-scrape%2Frefs%2Fheads%2Fmain%2Fpyproject.toml&query=%24.tool.poetry.version&label=version)](https://github.com/atloo1/metacritic-games-scrape/blob/main/pyproject.toml)
[![GitHub License](https://img.shields.io/github/license/atloo1/metacritic-games-scrape)](https://github.com/atloo1/metacritic-games-scrape/blob/main/LICENSE)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/atloo1/metacritic-games-scrape)

[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)
[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Renovate enabled](https://img.shields.io/badge/renovate-enabled-brightgreen.svg)](https://renovatebot.com/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

scrape games on metacritic.com

## prerequisites

- [poetry](https://python-poetry.org/docs/#installing-with-pipx)

```
git clone https://github.com/atloo1/metacritic-games-scrape.git
cd metacritic-games-scrape/
```

## run

### scrape

```
poetry install --only scrape
poetry run scrapy crawl metacritic_games -L DEBUG -O post_scrape/data.json --logfile post_scrape/logs.txt
poetry run python -m post_scrape.clean_json
```

#### artifacts available upon request:

- `http_cache.tar.gz`: HTTP cache of the scrape underlying `write-up.pdf`
  - use with `tar -xzf http_cache.tar.gz -C <project-root>/.scrapy/httpcache/`

### analyze

```
poetry install --only analyze
poetry run jupyter notebook ./post_scrape/
# or do as you please with data_cleaned.json
```

#### artifacts available upon request:

- `data_cleaned.json.gz`: the dataset for all analyses & starting point if not scraping for yourself
- `data.json.gz`: `scrapy crawl` output
- `logs.json.gz`: `scrapy crawl` logs

## file descriptions

### reading materials [available upon request](https://drive.google.com/drive/folders/1m8wfo5qNFt-TyoxRlzkI1yu7kGcgnSNV?usp=sharing):

- `supplement_citations.pdf`: textual citations; an alternative of write-up's hyperlinks
- `supplement_figures.pdf`: enlarged figures from write-up
- `supplement_table_1.pdf`: table 1 as alluded to in write-up
- `supplement_table_3.pdf`: complete table 3 as alluded to in write-up
- `write-up.pdf`: a research-style paper presenting this repository's work

### `./post_scrape/*`:

- `clean_data_validation.ipynb`: `data_cleaned.json` inspection
- `clean_json.py`: `data.json` → `data_cleaned.json`
- `fig_1.ipynb`: reproduce figure 1
- `fig_2.ipynb`: reproduce figure 2
- `fig_3.ipynb`: reproduce figure 3
- `fig_4.ipynb`: reproduce figure 4
- `load_scrape_data.py`: `data_cleaned.json` → DataFrame
- `nlp_utils.py`: text normalization, topic modeling, & cross validation pipeline
- `table_2.py`: reproduce underlying data for table 2
- `tables_3_4_fig_5.ipynb`: reproduce underlying data for tables 3 & 4 + figure 5
- `tables_2_3_4_fig_5_pretty.ipynb`: reproduce tables 2, 3, & 4 + figure 5 as seen in write-up

## develop

### prerequisites

- [pyenv](https://github.com/pyenv/pyenv?tab=readme-ov-file#installation)

### 1st time setup

```
pyenv install 3.9 --skip-existing   # or your choice
pyenv local 3.9   # or your choice
poetry install
poetry run pre-commit install
```

### helpful Bash

#### monitor scrape progress: 1 line = 1 web page

```
wc -l post_scrape/data.json
```

#### find a page in HTTP cache; next scrape will re-download it if deleted

```
query_url="https://www.metacritic.com/game/halo-2/"  # set me
query_str="{'url': '${query_url}'"
find .scrapy/httpcache/metacritic_games/ -type f -name "meta" -exec bash -c '[[ "$(head -n 1 "$0")" == "$1"* ]] && echo "$0 starts with query_str"' {} "$query_str" \;
```
