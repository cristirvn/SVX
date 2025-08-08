<img width="790" height="150" alt="SportVisionX__2_-removebg-preview" src="https://github.com/user-attachments/assets/06fa393c-cca7-4904-a757-22b0ede11be4" />

## Basic overview
Advanced sports match crawler and analytics platform designed to track and analyze championships and match results, providing comprehensive statistics about past events.

## Download and installation
You can [download](https://github.com/cristirvn/SVX/archive/refs/heads/uv-migration.zip) and use it right away 

## Usage
- backend folder contains following:
  -  tests folder : testing the crawler and crawl_championship functions functionality
  -  ❗temporary unusable due to unfinished❗️ Analyze.py and Analyzer.py
      deep analizing of certain matches (avaiable soon)
  - Crawler.py : retrieving all the cahmpionship links for a certain sport using [selenium](https://www.selenium.dev/documentation/) for crawling the data and store them in a database using [sqlalchemy](https://www.sqlalchemy.org/)
      ❗️in the first version of project, the only sport that works is basketball❗️
  - Crawl_championship
