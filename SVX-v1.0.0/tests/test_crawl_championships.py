from Crawl_Championship import add_date, get_urls, Match, insert_match
from unittest.mock import MagicMock, patch
from Drive_backup import upload_to_gdrive_by_key

def test_get_urls():
    mock_driver = MagicMock()
    mock_element = MagicMock()
    mock_element.find_element.return_value.get_attribute.return_value = "http://example.com"
    mock_driver.find_elements.return_value = [mock_element, mock_element]

    urls = get_urls(mock_driver)
    assert urls == ["http://example.com", "http://example.com"]


def test_insert_match():
    mock_cursor = MagicMock()
    match = Match(
        sport="Soccer", date="2024-12-17", ROUND="Final", 
        home="Team A", away="Team B", home_score=3, away_score=2,
        home_score_by_period=[1, 1, 1], away_score_by_period=[1, 1, 0],
        url="http://example.com", country="Country", division="Division", season="2024-2025"
    )
    insert_match(mock_cursor, match)
    mock_cursor.execute.assert_called_once()

'''
@patch("Drive_backup.upload_to_gdrive_by_key")
def test_upload_to_drive(mock_upload):
    upload_to_gdrive_by_key("test.csv")
    mock_upload.assert_called_once_with("test.csv")
'''