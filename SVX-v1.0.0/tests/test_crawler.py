import pytest
from Crawler import ChampionshipLinks as clist
import sqlalchemy
from sqlalchemy import create_engine, inspect
from sqlalchemy.ext.declarative import declarative_base


from unittest.mock import MagicMock, patch


def test_get_link_prefix():
    cl = clist(sport_name="basketball", country="usa", division="nba")
    expected_url = "https://www.flashscore.com/basketball/usa/nba"
    assert cl.get_link_prefix() == expected_url

def test_retrieve_country_links():
    mock_driver = MagicMock() #stimulates the driver
    mock_temp = MagicMock() #stimulates the menu element
    mock_button = MagicMock() #stimulate the "More" button
    mock_link = MagicMock() # Simulate the menu returning a list of link elements
    
    # Simulate finding elements
    mock_driver.find_element.return_value = mock_temp
    mock_temp.find_element.return_value = mock_button
    mock_temp.find_elements.return_value = [mock_link]
    mock_button.click.return_value = None  # Simulate successful click
    mock_link.find_element.return_value.get_attribute.return_value = "https://www.flashscore.com/basketball/usa/nba"
    
    links = []
    clist.retrieve_country_links(mock_driver, links, "basketball")
    
    assert len(links) == 1
    assert links[0].sport_name == "basketball"
    assert links[0].country == "usa"
    assert links[0].division == "nba"

def test_database_schema():
    engine = create_engine("sqlite:///:memory:")  # Use an in-memory SQLite database for testing
    #Base.metadata.create_all(bind=engine)

    inspector = inspect(engine)
    tables = inspector.get_table_names()
    assert "championship_links" in tables

    columns = [col['name'] for col in inspector.get_columns("championship_links")]
    assert "id" in columns
    assert "url" in columns
    assert "sport" in columns
    assert "country" in columns
    assert "league" in columns

def test_invalid_championship_link():
    cl = clist(sport_name="", country="usa", division="nba")
    expected_url = "https://www.flashscore.com//usa/nba"
    assert cl.get_link_prefix() == expected_url

