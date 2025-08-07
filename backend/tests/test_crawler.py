import pytest
from Crawler import ChampionshipLinks as clist
from Crawler import retrieve_country_links
import sqlalchemy
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import declarative_base
from unittest.mock import MagicMock, patch
import configparser


def test_get_link_prefix():
    cl = clist(sport_name="basketball", country="usa", division="nba")
    expected_url = "https://www.flashscore.com/basketball/usa/nba"
    assert cl.get_link_prefix() == expected_url

def test_retrieve_country_links():
    # Mock driver and its methods
    mock_driver = MagicMock()

    # Mock the menu element
    mock_temp = MagicMock()
    mock_driver.find_element.return_value = mock_temp

    # Mock the "More" button
    mock_button = MagicMock()
    mock_temp.find_element.return_value = mock_button

    # Simulate clicking the "More" button
    mock_button.click.return_value = None

    # Mock country links
    mock_link = MagicMock()
    mock_temp.find_elements.return_value = [mock_link]

    # Mock league elements
    mock_league = MagicMock()
    mock_driver.find_elements.return_value = [mock_league]

    # Mock nested elements and their attributes
    mock_a_tag = MagicMock()
    mock_league.find_element.return_value = mock_a_tag
    mock_a_tag.get_attribute.return_value = "https://www.flashscore.com/basketball/usa/nba"

    # List to store results
    links = []

    # Call the function
    retrieve_country_links(mock_driver, links, "basketball")

    # Assertions
    assert len(links) == 1
    assert links[0].sport_name == "basketball"
    assert links[0].country == "usa"
    assert links[0].division == "nba"

    
def test_invalid_championship_link():
    cl = clist(sport_name="", country="usa", division="nba")
    expected_url = "https://www.flashscore.com//usa/nba"
    assert cl.get_link_prefix() == expected_url


def test_database_schema():

    Base = declarative_base()
    config = configparser.ConfigParser()
    config.read("config.ini")

    db_user = config["database"]["user"]
    db_password = config["database"]["password"]
    db_host = config["database"]["host"]
    db_port = config["database"]["port"]
    db_name = config["database"]["dbname"]
    databasse_url = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

    engine = create_engine(databasse_url, echo = True)
    
    # Create the schema
    Base.metadata.create_all(bind=engine)

    # Inspect the schema
    inspector = inspect(engine)

    # Check that the championship_links table exists
    tables = inspector.get_table_names()
    assert "championship_links" in tables, "Table 'championship_links' does not exist"

    # Check that all required columns exist in the table
    columns = {col['name']: col['type'] for col in inspector.get_columns("championship_links")}
    assert "id" in columns, "Column 'id' does not exist"
    assert "url" in columns, "Column 'url' does not exist"
    assert "sport" in columns, "Column 'sport' does not exist"
    assert "country" in columns, "Column 'country' does not exist"
    assert "league" in columns, "Column 'league' does not exist"


