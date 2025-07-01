import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
import json
from import_asyncio import BlueskyApiScraper

# filepath: c:\Users\nerea\Desktop\Bases de datos TFM\test_import_asyncio.py


class TestBlueskyApiScraper(unittest.TestCase):
    @patch('import_asyncio.httpx.post')
    def test_create_session(self, mock_post):
        # Simular respuesta de la API
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'didDoc': {'service': [{'serviceEndpoint': 'https://mock.endpoint'}]},
            'accessJwt': 'mock_access_token'
        }
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response

        scraper = BlueskyApiScraper()
        scraper.create_session()

        self.assertEqual(scraper.service_endpoint, 'https://mock.endpoint')
        self.assertEqual(scraper.access_token, 'mock_access_token')

    @patch('import_asyncio.httpx.get')
    def test_fetch_posts(self, mock_get):
        # Simular respuesta de la API
        mock_response = MagicMock()
        mock_response.json.return_value = {'posts': [{'record': {'createdAt': '2025-04-30T12:00:00Z'}}]}
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        scraper = BlueskyApiScraper()
        scraper.service_endpoint = 'https://mock.endpoint'
        scraper.access_token = 'mock_access_token'

        posts = scraper.fetch_posts('@mock_handle')
        self.assertIn('posts', posts)

    def test_filter_posts(self):
        scraper = BlueskyApiScraper()
        posts = {
            'posts': [
                {'record': {'createdAt': '2025-04-30T12:00:00Z', 'text': 'Test post'},
                 'uri': 'mock_uri', 'author': {'handle': '@mock_handle'}}
            ]
        }
        filtered_posts = scraper.filter_posts(posts)
        self.assertEqual(len(filtered_posts), 1)
        self.assertEqual(filtered_posts[0]['text'], 'Test post')

    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    def test_save_posts(self, mock_open):
        scraper = BlueskyApiScraper()
        posts = [{'text': 'Test post'}]
        scraper.save_posts(posts, 'mock_file.json')

        mock_open.assert_called_once_with('mock_file.json', 'w', encoding='utf-8')
        mock_open().write.assert_called_once_with(json.dumps(posts, indent=4, ensure_ascii=False))

    @patch('import_asyncio.BlueskyApiScraper.fetch_posts')
    @patch('import_asyncio.BlueskyApiScraper.save_posts')
    def test_scrape(self, mock_save_posts, mock_fetch_posts):
        mock_fetch_posts.return_value = {
            'posts': [{'record': {'createdAt': '2025-04-30T12:00:00Z', 'text': 'Test post'},
                       'uri': 'mock_uri', 'author': {'handle': '@mock_handle'}}]
        }

        scraper = BlueskyApiScraper()
        scraper.service_endpoint = 'https://mock.endpoint'
        scraper.access_token = 'mock_access_token'

        handles = ['@mock_handle']
        all_posts = scraper.scrape(handles)

        self.assertIn('@mock_handle', all_posts)
        self.assertEqual(len(all_posts['@mock_handle']), 1)
        mock_save_posts.assert_called_once()

if __name__ == '__main__':
    unittest.main()