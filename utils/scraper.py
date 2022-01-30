from typing import TypedDict
import requests
from bs4 import BeautifulSoup
from algoliasearch.search_client import SearchClient
from datetime import datetime
import json
import io
import time
from datetime import date

Entry = TypedDict('Entry', {'elem_id': str,
                            'title': str,
                            'url': str,
                            'company': str,
                            'address': list,
                            'benefits': str,
                            'salary': str,
                            'description': list,
                            'post_time': str,
                            'crawl_time': str})

Entry2 = TypedDict('Entry2', {'elem_id': str,
                              'title': str,
                              'url': str,
                              'company': str,
                              'address': list,
                              'benefits': str,
                              'minSalary': str,
                              'maxSalary': str,
                              'description': str,
                              'post_time': str})


# simulate a login to get salary range
# get this session from real login, this may expires after a while
# to retrieve the session id from cookie: https://developers.google.com/web/tools/chrome-devtools/storage/cookies
# then copy the string of key "_ITViec_session" at site itviec.com and paste it here
session = 'LFkF0GjprNUDGx8ntpk4A%2BC8Ojp9LtUVc8tqkszBxkYubI0gICNdB5ctAD%2BftUXvuTj7pA%2FfCVp3ZKQTte9nt6BuA8tmmV78OJkjTvhSLrVMSTGUM4%2FcVkvfL2EOFdCJgZ1LAKdrgDQQtDc9C69okaOxhNPfWaXuCSmU03zIhae8c1sKeed2KiLxSdqRY%2Fe9%2FZgv6rFairc9DvkJIsqcM7BbTyjutJEa19gJkwyPYiYb6chM4byb0F8s8bSoXu7u%2FRdFSUlPmETJiGm1SDowXuwDf8y1lHIuaWnn6Jgk%2F7Jwdgy7R8I%2F58Gb%2BXlJO%2B18GQOYyn0EQVXp2%2BUw%2FgmC39bdXVOlzaUt4PMhDYqaGPGldTE%2BLNFjdIgj%2FgfYeJKGjlsf7RaysfAINCh%2FURPePEDSe2CBP%2FB0ZZn1pq8Kh285NAUrX9WcNvk2XbKjFXRHTVUwlfw9Ubt16XaESgRB--ztZwqzSt%2FgjEOaN8--xbxYz8hphGNMCa010tUznA%3D%3D'


def scrap_itviec() -> list[Entry]:
    results: list[Entry] = []

    url1 = f'https://itviec.com/it-jobs/ho-chi-minh-hcm'
    url2 = f'https://itviec.com/it-jobs/ha-noi'
    url3 = f'https://itviec.com/it-jobs/da-nang'
    urls = [url1, url2, url3]
    for url in urls:

        p = requests.get(url, cookies={'_ITViec_session': session})

        soup = BeautifulSoup(p.content, 'html.parser')
        pagination = soup.find(class_='pagination')
        pagenum = int(pagination.find_all('li')[-2].a.string)
        for i in range(pagenum):
            newurl = url + '?page=' + str(i+1)
            page = requests.get(newurl, cookies={'_ITViec_session': session})
            container = soup.find(id='container')
            elems = container.find_all(class_='job')
            print(i)
            for elem in elems:
                id = 0
                data: Entry = dict()
                data['elem_id'] = id  # elem.attrs['id']
                data['title'] = elem.find(class_='title').text.strip()
                data['url'] = elem.attrs['data-search--job-selection-job-url-value']
                data['salary'] = elem.find(
                    class_='svg-icon__text').text.strip()
                data['description'] = []
                data['address'] = []
                if data['url'] is not None:
                    jd_link = f"https://itviec.com/{data['url']}"
                    jd_page = requests.get(jd_link)
                    jd_soup = BeautifulSoup(jd_page.content, 'html.parser')
                    data['company'] = jd_soup.find(
                        class_='job-details__sub-title').text.strip()
                    for addr in jd_soup.find_all(class_='job-details__address-map'):
                        data['address'].append(
                            addr.findPreviousSibling('span').text.strip())
                        # data['address'] += '\n'
                    # data['address'] = jd_soup.find(class_='job-details__address-map').findPreviousSibling('span').text.strip()

                    for ultag in jd_soup.find_all('ul'):
                        for litag in ultag.find_all('li'):
                            data['description'].append(str(litag.text.strip()))
                            # data['description'] += '\n'

                    for x in jd_soup.find_all(class_='svg-icon--blue'):
                        data['post_time'] = x.find(
                            class_='svg-icon__text').text.strip()
                    # data['post_time'] = jd_soup.find(class_='svg-icon--blue').contents[1].contents[1]
                    # data['post_time'] = str(time_div.find(class_='svg-icon__text').text.strip())
                    # data['post_time'] = time_div[-2]
                    now = datetime.now()
                    data['crawl_time'] = now.strftime("%m/%d/%Y, %H:%M:%S")

                benefits = elem.find(class_='benefits')
                if benefits is not None:
                    data['benefits'] = benefits.get_text(
                        strip=True, separator=', ')
                id = id + 1
                results.append(data)
    with io.open('Itviec.txt', 'w', encoding='utf-8') as f:
        f.write(json.dumps(results))
    today = date.today()
    with io.open('data/Itviec_lastUpdate.txt', 'w', encoding='utf-8') as f:
        f.write(today.strftime("%d/%m/%Y"))
    return results


def scrap_vietnamwork() -> list[Entry]:
    # In GG Chrome Network tab, filter by "queries?" call when refresh page to catch api key & app id
    # index = SearchClient.create(
    #     'JF8Q26WWUD', 'ecef10153e66bbd6d54f08ea005b60fc').init_index('vnw_job_v2')
    # search_result = index.search(
    #     '',
    #     request_options={
    #         'attributesToRetrieve': ['jobId', 'company', 'alias', 'objectID', 'jobTitle', 'jobLocations', 'benefits', 'salaryMax', 'salaryMin', "_highlightResult", "timestamp"],
    #         # 'facetFilters': [["locationIds:29"]],  # filter jobs by HCM city
    #         'facetFilters': [["locationIds:24"]],  # filter jobs by Hanoi city
    #         # 'facetFilters': [["locationIds:17"]],  # filter jobs by Danang city
    #         'page': page_num - 1,
    #         'hitsPerPage': limit,
    #     }
    # )['hits']
    # # return search_result
    # res = [*map(lambda r: Entry2(elem_id=r['jobId'],
    #                              title=r['jobTitle'],
    #                              company=r['company'],
    #                              address=r['jobLocations'][0],
    #                              # append '-je' for Vietnamese page
    #                              url='/' + r['alias'] + '-' + \
    #                              r['objectID'] + '-jv',
    #                              benefits=', '.join(
    #     [*map(lambda b: b['benefitName'], r['benefits'])]),
    #     minSalary=str(r['salaryMin']),
    #     maxSalary=str(r['salaryMax']),
    #     description=r['_highlightResult']['jobDescription']['value'],
    #     post_time=r['timestamp']
    # ), search_result)]
    # with io.open('VietnamWork.txt', 'w', encoding='utf-8') as f:
    #     f.write(json.dumps(res, ensure_ascii=False))
    time.sleep(6)
    today = date.today()
    with io.open('data/VietnamWork_lastUpdate.txt', 'w', encoding='utf-8') as f:
        f.write(today.strftime("%d/%m/%Y"))

    return {'result': 'ok'}


scrap_vietnamwork()
