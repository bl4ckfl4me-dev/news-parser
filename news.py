from datetime import datetime
from bs4 import BeautifulSoup
import hashlib
import logging
import requests


class NewsScrapper:
    def __init__(self, url: str, html_tag: str, html_attrs: dict):
        self.url = url
        self.html_tag = html_tag
        self.html_attrs = html_attrs
        self.__parsed_content = self._get_news_content()
        self.__hashed_content = self._get_hashed_url_content(' '.join(self.__parsed_content).encode())

    def _get_hashed_url_content(self, content: bytes) -> str:
        try:
            return hashlib.sha224(content).hexdigest()
        except TypeError:
            logging.error(f'{datetime.now()}: {self.url} - content is not defined')

    def _get_news_content(self) -> set[str] | None:
        try:
            news_page_content = requests.get(self.url, timeout=5).content
            soup = BeautifulSoup(news_page_content, 'html.parser')
            parsed_news = soup.find_all(self.html_tag, self.html_attrs)
            return set(news.text.strip() for news in parsed_news)
        except requests.RequestException:
            logging.error(f'{datetime.now()}: {self.url} - timeout error')

    def is_news_changed(self) -> bool:
        latest_content = self._get_news_content()
        try:
            latest_hashed_content = self._get_hashed_url_content(' '.join(latest_content).encode())
        except TypeError:
            logging.error(f'{datetime.now()}:{self.url} - cant reach content')
            return False
        if self.__hashed_content != latest_hashed_content:
            self.__hashed_content = latest_hashed_content
            return True
        return False

    def fetch_all_new_news(self) -> set[str]:
        latest_news = self._get_news_content()
        new_news = set(content for content in latest_news if content not in self.__parsed_content)
        self.__parsed_content = latest_news
        return new_news

