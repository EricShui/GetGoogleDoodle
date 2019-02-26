import requests, time, re
from multiprocessing import Pool

header = {
    'Referer': 'https://www.google.com/doodles?hl=zh-CN',
    'Host': 'www.google.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
}


def build_url_get_page(year, moth):
    base_url = 'https://www.google.com/doodles/json/{years}/{moths}?hl=zh_CN'.format(years=year, moths=moth)
    try:
        print(year, ' ', moth)
        response = requests.get(base_url, headers=header)
        if response.status_code == 200:
            return response.json()
        # print(response.json())
    except Exception as e:
        print('ERROR' + '_' * 50 + '\n', e.args)


def parse_page(json):
    if json:
        try:
            # print(json)
            for content in json:
                allUrl = content.get('url')
                date = content.get('run_date_array')
                title = content.get('title')
                yield {
                    'imgUrl': allUrl,
                    'date': date,
                    'title': title
                }
        except:
            pass


def save_image(result):
    out = requests.get(str('https:' + result.get('imgUrl')))
    if result.get('imgUrl')[-3:] == 'png':
        path = 'PNG'
    elif result.get('imgUrl')[-3:] == 'gif':
        path = 'GIF'
    else:
        path = 'JPG'
    try:
        name = result.get('title')
        fileName = re.sub('/', '&', name)
        with open(
                './' + path + '/' + str(result.get('date')[0]) + '.' + str(result.get('date')[1]) + '.' + str(
                    result.get('date')[2]) + '.' + fileName + '.' + path, 'wb') as f:
            print(str(result.get('date')[0]) + '.' + str(result.get('date')[1]) + '.' + str(
                result.get('date')[2]) + '.' + fileName + '.' + path + str('https:' + result.get('imgUrl')))
            f.write(out.content)
    except Exception as e:
        time.sleep(3)
        print('error' + '--' * 30 + '\n', e)




if __name__ == '__main__':
    pool = Pool()
    years = ([x for x in range(2018, 1995, -1)])
    moths = ([y for y in range(12, 0, -1)])
    page = pool.map(build_url_get_page, years, moths)
