container = soup.find(id='container')
    #     elems = container.find_all(class_='job', limit=limit)
    #     for elem in elems:
    #         id = 0
    #         print(elem)
    #         data: Entry = dict()
    #         data['elem_id'] = id  # elem.attrs['id']
    #         data['title'] = elem.find(class_='title').text.strip()
    #         data['url'] = elem.attrs['data-search--job-selection-job-url-value']
    #         data['salary'] = elem.find(class_='svg-icon__text').text.strip()
    #         data['description'] = []
    #         data['address'] = []
    #         if data['url'] is not None:
    #             jd_link = f"https://itviec.com/{data['url']}"
    #             jd_page = requests.get(jd_link)
    #             jd_soup = BeautifulSoup(jd_page.content, 'html.parser')
    #             data['company'] = jd_soup.find(
    #                 class_='job-details__sub-title').text.strip()
    #             for addr in jd_soup.find_all(class_='job-details__address-map'):
    #                 data['address'].append(
    #                     addr.findPreviousSibling('span').text.strip())
    #                 #data['address'] += '\n'
    #             #data['address'] = jd_soup.find(class_='job-details__address-map').findPreviousSibling('span').text.strip()

    #             for ultag in jd_soup.find_all('ul'):
    #                 for litag in ultag.find_all('li'):
    #                     data['description'].append(str(litag.text.strip()))
    #                     #data['description'] += '\n'

    #             for x in jd_soup.find_all(class_='svg-icon--blue'):
    #                 data['post_time'] = x.find(
    #                     class_='svg-icon__text').text.strip()
    #             #data['post_time'] = jd_soup.find(class_='svg-icon--blue').contents[1].contents[1]
    #             #data['post_time'] = str(time_div.find(class_='svg-icon__text').text.strip())
    #             #data['post_time'] = time_div[-2]
    #             now = datetime.now()
    #             data['crawl_time'] = now.strftime("%m/%d/%Y, %H:%M:%S")

    #         benefits = elem.find(class_='benefits')
    #         if benefits is not None:
    #             data['benefits'] = benefits.get_text(
    #                 strip=True, separator=', ')
    #         id = id + 1
    #         results.append(data)
    # with io.open('Itviec.txt', 'w', encoding='utf-8') as f:
    #     f.write(json.dumps(results, ensure_ascii=False))
    # return results