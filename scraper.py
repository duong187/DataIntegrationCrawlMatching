from typing import TypedDict
import requests
from bs4 import BeautifulSoup
from algoliasearch.search_client import SearchClient
from datetime import datetime

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
session = '5Rr5Rw%2FiqbR2uGw6krXBDXs4kbejWuaNe8H0L5k3GEWYjTl63gGuNSoyEnxxaIWY1uVz15phuCvyD5f4Fax25kStB0nRslRWF1gSmBcrh9ASAIt0OD7pXG1UsUJ2FEJLK45jn%2BQCSH67fcXo%2FwWJwYqtnwfLJCFMddzWRpFMZprJSR9bMviZsEkwCGTKwaUyfh538jwiKbZ1M1oymLQfEP7o2BvmlnhWUHV7gbRW9G%2BguoxPbYORFWVK9ugtQU4IMccJ%2BcIwdaYM6RIhRRXEWXYe0vBo5JaEdjIAb%2Fbv6InJnfPd2eCQ%2BdzHLaB5sSNrx%2BuLqGgO%2BVB06jqG%2Bhk%2BMq%2Bn8zEmBnuqCSOYeqF%2Fx3w3k9GyUY2TIqOhzCnG0ghOtyXLts7oBx%2BtM3bBDquI2RVZo4lu%2Ft22R4Lhuw7BDMKQZlBdKfwPsxzg96IsX0D4VGHM6w%2FJY5dApE1%2FB%2B6skXxFtT29IPBubzjykEZhZJG0Nq9kndjLaYjiGA1ndBfUYIRnzQU5hPXIKvGEnp7fWof4oA5FXdsJuewATyI5hNmuy%2F4dcOfZUYJ3ze0SyiYfN2hkIXrgRJ2ZarXXgiZc7OnGEmdy%2Fb9B2TyvpDqby%2BtOmJvuunLUvKZVeL3PpUc%3D--HLWPRzVwiIIJuOD%2F--VvpcGWSPX0JFSCazW9JT3A%3D%3D'

def scrap_itviec(page_num: int, limit: int) -> list[Entry]:
    results: list[Entry] = []

    #url = f'https://itviec.com/it-jobs/ho-chi-minh-hcm?page={page_num}'
    url = f'https://itviec.com/it-jobs/ha-noi?page={page_num}'
    #url = f'https://itviec.com/it-jobs/da-nang?page={page_num}'
    page = requests.get(url, cookies={'_ITViec_session': session})

    soup = BeautifulSoup(page.content, 'html.parser')

    container = soup.find(id='container')
    elems = container.find_all(class_='job', limit=limit)

    for elem in elems:
        data: Entry = dict()

        data['elem_id'] = elem.attrs['id']
        data['title'] = elem.find(class_='title').text.strip()
        data['url'] = elem.attrs['data-search--job-selection-job-url']
        data['salary'] = elem.find(class_='svg-icon__text').text.strip()
        data['description'] = []
        data['address'] = []
        if data['url'] is not None:
            jd_link = f"https://itviec.com/{data['url']}"
            jd_page = requests.get(jd_link)
            jd_soup = BeautifulSoup(jd_page.content, 'html.parser')
            data['company'] = jd_soup.find(class_='job-details__sub-title').text.strip()
            for addr in jd_soup.find_all(class_='job-details__address-map'):
                data['address'].append(addr.findPreviousSibling('span').text.strip())
                #data['address'] += '\n'
            #data['address'] = jd_soup.find(class_='job-details__address-map').findPreviousSibling('span').text.strip()

            for ultag in jd_soup.find_all('ul'):
                for litag in ultag.find_all('li'):
                    data['description'].append(str(litag.text.strip()))
                    #data['description'] += '\n'

            for x in jd_soup.find_all(class_='svg-icon--blue'):
                data['post_time'] = x.find(class_='svg-icon__text').text.strip()
            #data['post_time'] = jd_soup.find(class_='svg-icon--blue').contents[1].contents[1]
            #data['post_time'] = str(time_div.find(class_='svg-icon__text').text.strip())
            #data['post_time'] = time_div[-2]
            now = datetime.now()
            data['crawl_time'] = now.strftime("%m/%d/%Y, %H:%M:%S")
            

        benefits = elem.find(class_='benefits')
        if benefits is not None:
            data['benefits'] = benefits.get_text(strip=True, separator=', ')

        results.append(data)

    return results


def scrap_vietnamwork(page_num: int, limit: int) -> list[Entry]:
    # In GG Chrome Network tab, filter by "queries?" call when refresh page to catch api key & app id
    index = SearchClient.create('JF8Q26WWUD', 'ecef10153e66bbd6d54f08ea005b60fc').init_index('vnw_job_v2')
    search_result = index.search(
        '',
        request_options={
            'attributesToRetrieve': ['jobId', 'company', 'alias', 'objectID', 'jobTitle', 'jobLocations', 'benefits', 'salaryMax', 'salaryMin', "_highlightResult", "timestamp"],
            #'facetFilters': [["locationIds:29"]],  # filter jobs by HCM city
            'facetFilters': [["locationIds:24"]],  # filter jobs by Hanoi city
            #'facetFilters': [["locationIds:17"]],  # filter jobs by Danang city
            'page': page_num - 1,
            'hitsPerPage': limit,
        }
    )['hits']
    #return search_result
    return [*map(lambda r: Entry2(elem_id=r['jobId'],
                                 title=r['jobTitle'],
                                 company=r['company'],
                                 address=r['jobLocations'][0],
                                 url='/' + r['alias'] + '-' + r['objectID'] + '-jv',  # append '-je' for Vietnamese page
                                 benefits=', '.join([*map(lambda b: b['benefitName'], r['benefits'])]),
                                 minSalary= str(r['salaryMin']),
                                 maxSalary= str(r['salaryMax']),
                                 description= r['_highlightResult']['jobDescription']['value'],
                                 post_time = r['timestamp']
                                ), search_result)]
    
