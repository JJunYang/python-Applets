import os
import requests
from bs4 import BeautifulSoup
import time
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED

download_path = './douban'
if not os.path.exists(download_path):
    os.makedirs(download_path)


def download_pic(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    content = soup.find('div', class_='article')
    images = content.find_all('img')
    pic_link_list = [image['src'] for image in images]
    pic_name_list = [image['alt'] for image in images]
    for name, link in zip(pic_name_list, pic_link_list):
        html = requests.get(link)
        with open(f'{download_path}/{name}.jpg', 'wb') as f:
            f.write(html.content)
    print(f'{url} download finished')


def main():
    start_urls = ['https://movie.douban.com/top250']

    for i in range(1, 10):
        start_urls.append(
            f'https://movie.douban.com/top250?start={25 * i}&filter=')

    start_time = time.time()

    # for url in start_urls:
    #     download_pic(url)

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        for url in start_urls:
            future = executor.submit(download_pic, url)
            futures.append(future)
    wait(futures, return_when=ALL_COMPLETED)

    end_time = time.time()
    print('='*50)
    print(f'total runtime:{end_time-start_time}')


if __name__ == "__main__":
    main()
