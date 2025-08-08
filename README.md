<img width="790" height="150" alt="SportVisionX__2_-removebg-preview" src="https://github.com/user-attachments/assets/06fa393c-cca7-4904-a757-22b0ede11be4" />

## Basic overview
Advanced sports match crawler and analytics platform designed to track and analyze championships and match results, providing comprehensive statistics about past events.

## Download and installation
You can [download](https://github.com/cristirvn/SVX/archive/refs/heads/uv-migration.zip) and use it right away 

## Project description
- backend directory contains following:
  -  tests directory : testing the crawler and crawl_championship functions functionality
  -  Analyze.py and Analyzer.py: deep analizing of certain matches (avaiable soon)
  - Crawler.py : retrieving all the championship links for a certain sport using [selenium](https://www.selenium.dev/documentation/) for crawling the data and store them in a database using [sqlalchemy](https://www.sqlalchemy.org/)
  - Crawl_championship: crawling all the matches for a specific championship
  - config.ini: contains the database credentials in order to store the matches data
  - Drive_backup.py: google drive backup for matches.csv file to store it
- frontend directory contains folowing:
    -fastapi_setup directory: [fastapi](https://fastapi.tiangolo.com/#installation) initialization for react application
    -sports-app directory: [react](https://react.dev/learn) application setup
- pyproject.toml: contain dependencies versions, project beeing managed with [uv](https://docs.astral.sh/uv/)
- uv.lock: uv generated lockfile

## How to run the project
1.Download the project as mentioned earlier

2.Install uv if not installed
```bash
pip install uv
```
3.Setup the uv venv and sync the dependencies from the .toml file
```bash
uv venv
.venv\Scripts\activate
uv sync
```
4.Add your personal database crrdentials in the config.ini

5.Run the Crawler.py to crawl the championships and store in the database
```bash
uv run Crawler.py
```
6.Run fastapi (from its directory)
```bash
uvicorn main:app --reload
```
7.Start the react application (from its directory)
```bash
npm start
```
8.Fetch the leagues in the react interface by inputing the sport and the country

## Version
v0.1.0
Future updates incoming with more functionalities








