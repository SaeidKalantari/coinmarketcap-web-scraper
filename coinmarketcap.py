# Written by SAEID KALANTARI

import json
from requests_html import HTMLSession

root_address = 'https://coinmarketcap.com'
session = HTMLSession()

def scrape_coins(data):
    print('Scraping coins...')
    pages = []
    for page_number in range(1, 101):
        pages.append(root_address + '/?page=' + str(page_number))

    for page in pages:
        print("Scrapping... page: " + str(page))

        r = session.get(page)
        r.html.render(scrolldown=16, sleep=0.1)

        rows = r.html.find('tbody tr')

        for row in rows:
            d = dict()
            columns = row.find('td')
            if columns[1].find('p', first=True) is not None:
                d['rank'] = columns[1].find('p', first=True).text.strip()
                name_and_sym = columns[2].find('p')
                d['name'] = name_and_sym[0].text.strip()
                d['symbol'] = name_and_sym[1].text.strip()
                price_col = columns[3].find('span')
                d['price'] = price_col[0].text.strip()

                hourly_p = columns[4].find('span')
                hourly_span_neg = columns[4].find('.icon-Caret-down')
                hourly_span_pos = columns[4].find('.icon-Caret-up')
                if hourly_span_neg:
                    hourly_span_sym = '-'
                elif hourly_span_pos:
                    hourly_span_sym = '+'
                if columns[4].text.strip() != '--':
                    d['h1'] = hourly_span_sym + hourly_p[0].text.strip()
                else:
                    d['h1'] = '-'

                daily_p = columns[5].find('span')
                daily_span_neg = columns[5].find('.icon-Caret-down')
                daily_span_pos = columns[5].find('.icon-Caret-up')
                if daily_span_neg:
                    daily_span_sym = '-'
                elif daily_span_pos:
                    daily_span_sym = '+'
                if columns[5].text.strip() != '--':
                    d['h24'] = daily_span_sym + daily_p[0].text.strip()
                else:
                    d['h24'] = '-'

                weekly_p = columns[6].find('span')
                weekly_span_neg = columns[6].find('.icon-Caret-down')
                weekly_span_pos = columns[6].find('.icon-Caret-up')
                if weekly_span_neg:
                    weekly_span_sym = '-'
                elif weekly_span_pos:
                    weekly_span_sym = '+'
                if columns[6].text.strip() != '--':
                    d['h7'] = weekly_span_sym + weekly_p[0].text.strip()
                else:
                    d['h7'] = '-'

                if columns[7].text.strip() != '--':
                    market_cap_col = columns[7].find('span')[1]
                    d['market_cap'] = market_cap_col.text.strip()
                else:
                    d['market_cap'] = '-'

                volume_daily_col = columns[8].find('p')
                if columns[8].text.strip() != '--':
                    d['Volume_24h_dollar'] = volume_daily_col[0].text.strip()
                    d['Volume_24h_sym'] = volume_daily_col[1].text.strip()
                else:
                    d['Volume_24h_dollar'] = '-'
                    d['Volume_24h_sym'] = '-'

                circulating_supply_col = columns[9].find('p')
                if columns[9].text.strip() != '--':
                    d['circulating_supply'] = circulating_supply_col[0].text.strip()
                else:
                    d['circulating_supply'] = '-'
            data.append(d)

    return data


def save_json(data):
    with open('coins.json', 'w') as f:
        json.dump(data, f)


def open_json():
    with open('coins.json', 'r') as f:
        return json.load(f)


def main():
    data = []
    data = scrape_coins(data)
    save_json(data)

    print('Done.')


if __name__ == '__main__':
    main()



