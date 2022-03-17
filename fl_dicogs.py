from bs4 import BeautifulSoup
import requests
import time

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 OPR/78.0.4093.186 (Edition Yx GX)',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
}
strings_list = []


def get_data_discogs(url):
    try:
        sess = requests.Session()

        r = sess.get(url=url, headers=HEADERS)
        time.sleep(0.5)
        soup = BeautifulSoup(r.text, 'lxml')
        items = soup.find_all("tr")
        for i, item in enumerate(items, 1):

            if i > 3:

                # Имя артиста

                artist = item.find('td', class_='artist').text

                # Имя релиза

                release = (item.find('td', class_='title')).find('a').text

                # Ссылка на релиз

                link_release = 'https://www.discogs.com' + (item.find('td', class_='title')).find('a').get("href")

                # Номер релиза по каталогу

                number = item.find('td', class_='catno has_header').text

                # Год выпуска

                year = item.find('td', class_='year has_header').text

                # Результат

                result_string = f"{number} - {artist} - {release} - {year} - {link_release}"
                print(result_string)
                strings_list.append(result_string)

            else:
                continue

    except Exception as ex:
        print("[INFO] Error in search items!", ex)

    with open("discogs.txt", "w", encoding="utf-8") as f:
        for line in strings_list:
            f.write(f"{line}\n")


def get_number_of_pages(url):
    sess = requests.Session()

    r = sess.get(url=url, headers=HEADERS)
    soup = BeautifulSoup(r.text, 'lxml')
    pages = len(soup.find_all('li', class_='hide_mobile'))
    return pages//2


def main():
    url = input("URL для DISCOGS.COM (Пример ссылки = https://www.discogs.com/label/5376-Bonzai-Classics?page=1)= ")
    number_of_pages = get_number_of_pages(url=url)
    try:
        for i in range(1, number_of_pages+1):
            url = url[0:-1] + str(i)
            get_data_discogs(url=url)
            print(f"[INFO] {i} страница обработана")
            time.sleep(2)

    except Exception as ex:
        print("[INFO] Error!", ex)



# Пример ссылки = https://www.discogs.com/label/5376-Bonzai-Classics?page=1
if __name__ == '__main__':
    main()