<img width="790" height="150" alt="SportVisionX__2_-removebg-preview" src="https://github.com/user-attachments/assets/06fa393c-cca7-4904-a757-22b0ede11be4" />

## Basic overview
Advanced sports match crawler and analytics platform designed to track and analyze championships and match results, providing comprehensive statistics about past events.

## Download and installation
You can [download](https://github.com/cristirvn/SVX/archive/refs/heads/uv-migration.zip) and use it right away 

## Project description
- backend folder contains following:
  -  tests folder : testing the crawler and crawl_championship functions functionality
  -  Analyze.py and Analyzer.py: deep analizing of certain matches (avaiable soon)
  - Crawler.py : retrieving all the cahmpionship links for a certain sport using [selenium](https://www.selenium.dev/documentation/) for crawling the data and store them in a database using [sqlalchemy](https://www.sqlalchemy.org/)
  - Crawl_championship: crawling all the matches for a specific championship
  - config.ini: contains the database credentials in order to store the matches data
  - Drive_backup.py: google drive backup for matches.csv file to store it
- frontend folder contains folowing:
    -fastapi_setup folder: [fastapi](https://fastapi.tiangolo.com/#installation) initialization for react application
    -sports-app folder: [react](https://react.dev/learn) application setup

-pyproject.toml: contain dependencies versions, project beeing managed with [uv](https://docs.astral.sh/uv/)
-uv.lock: uv generated lockfile

## How to run the project
1.Download the project as mentioned earlier
2.Install uv if not installed
```bash
pip install uv
```


