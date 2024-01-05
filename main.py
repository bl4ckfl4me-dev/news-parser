from news import NewsScrapper
import time
from datetime import datetime


if __name__ == '__main__':
    news = [
        NewsScrapper(
            'https://news.rambler.ru/',
            'div',
            {
                'class': '_2C1Rd',
            }
        ),
        NewsScrapper(
            'https://www.interfax.ru/moscow/',
            'h3',
            {
                'class': ''
            }
        ),
        NewsScrapper(
            'https://tass.ru/moskva',
            'div',
            {
                'class': 'tass_pkg_title_wrapper-i0jgn',
            }
        ),
        NewsScrapper(
            'https://ria.ru/location_Moskva/',
            'a',
            {
                'class': 'list-item__title color-font-hover-only',
            }
        ),
        NewsScrapper(
            'https://www.rbc.ru/gorod',
            'span',
            {
                'class': 'item js-rm-central-column-item item_image-mob js-special-project-page-item',
            }
        ),
    ]

    while True:
        for n in news:
            if n.is_news_changed():
                new_news = n.fetch_all_new_news()
                if new_news:
                    print(f'{datetime.now().replace(microsecond=0)}:{n.url} - {new_news}')
        time.sleep(10)
