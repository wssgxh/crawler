import os
import chardet

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException

from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
from functools import lru_cache

from tools import split_list, create_folder

catalog_number = {'狮城财经': '147', '家有儿女': '179', '社会百科': '108'}


@lru_cache
def get_sub_url(page_number):
    return f'http://bbs.huasing.net/sForum/bbs.php?B={page_number}'


def get_availabe_links(web_page_sub_selection_path, html_content=False, file_path=False, page_number='147'):
    pre_fix = get_sub_url(page_number)

    if file_path:
        soup = read_file_return_soup(file_path)
    elif html_content:
        soup = BeautifulSoup(html_content, 'html.parser')

    linkers = []
    title_div = soup.find_all('div', id=lambda x: x and x.startswith('subject-'))
    for item in title_div:
        page_id = item['id'].split('-')[1]
        linkers.append(f'{pre_fix}_{page_id}')

    next_page_button = soup.find('input', {'type': 'button', 'value': '下一页 >'})

    if next_page_button:
        onclick_value = next_page_button.get('onclick', '')
        start_index = onclick_value.find('bbs.php?A=') + len('bbs.php?A=')
        end_index = onclick_value.find("'", start_index)
        next_page_value = onclick_value[start_index:end_index]
    else:
        next_page_value = False
    linkers_str = '\n'.join(map(str, linkers))
    with open(os.path.join(web_page_sub_selection_path, 'linkers'), 'a') as file:
        file.write(linkers_str)

    return linkers, next_page_value


def run(driver, url):
    driver.get(url)
    driver.implicitly_wait(1)  # You can adjust the wait time as needed
    html_content = driver.page_source

    return html_content


def read_file_return_soup(file_path):
    # Detect the encoding of the HTML file
    with open(file_path, 'rb') as rawdata:
        result = chardet.detect(rawdata.read())
        encoding = result['encoding']

    # Read the content of the HTML file with detected encoding
    with open(file_path, 'r', encoding='gbk') as file:
        html_content = file.read()

    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    return soup


def read_sub_page_html(file_path, index):
    soup = read_file_return_soup(file_path)
    page_text = ''
    # Find all divs with class 'subject' and id starting with 'subj-'
    title_div = soup.find('div', class_='title')

    if index == 0:
        page_text += (f'topic: {title_div.text}\n')

    subject_divs = soup.find_all('div', class_='subject', id=lambda x: x and x.startswith('subj-'))

    # Find all divs with class 'mediate' and id starting with 'fullc-'
    content_divs = soup.find_all('div', class_='mediate', id=lambda x: x and x.startswith('fullc-'))

    # Iterate over each pair of subject and content
    for subject_div, content_div in zip(subject_divs, content_divs):
        subject = subject_div.get_text(strip=True)
        content = content_div.get_text(strip=True)

        page_text += f'Subject: {subject}\n'
        page_text += f'Content: {content}\n'
        page_text += f'\n'

    return page_text




def get_html_content_with_js_click(url, web_page_sub_selection):
    html_folder = 'htmls'

    create_folder(html_folder)
    web_page_sub_selection_path = os.path.join(html_folder, web_page_sub_selection)
    create_folder(web_page_sub_selection_path)

    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run Chrome in headless mode (no GUI)

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    iteration_count = 0

    try:
        while (True):
            WebDriverWait(driver, 10).until(
                ec.presence_of_element_located((By.XPATH, "//input[@value='下一页 >']"))
            )

            link, next_page_value = get_availabe_links(web_page_sub_selection_path, html_content=driver.page_source,
                                                       page_number=web_page_sub_selection, )
            # Find and click the "下一页" button
            next_page_button = driver.find_element(By.XPATH, "//input[@value='下一页 >']")
            next_page_button.click()
            iteration_count += 1
            print(f"Iteration {iteration_count}: Link: {link}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()


def fetch_and_save_html(url_chunk, web_page_sub_selection, overwrite, web_page_sub_selection_path, index):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    page_number = 1
    next_page_button = True

    with webdriver.Chrome(options=chrome_options) as driver:

        for url in url_chunk:
            file_name = url.split(f'{web_page_sub_selection}_')[1] + f'_{page_number:02}' + '.html'
            file_path = os.path.join(web_page_sub_selection_path, file_name)

            if not overwrite and os.path.exists(file_path):
                print(f'{file_name} skipped')
                continue

            driver.get(url)

            while (next_page_button):
                html_content = driver.page_source

                with open(file_path, 'w', encoding='gbk') as file:
                    file.write(html_content)

                wait = WebDriverWait(driver, 5)
                try:
                    next_page_button = wait.until(ec.presence_of_element_located((By.XPATH, "//a[@class='next' and contains(text(), '下一页')]")))
                except TimeoutException:
                    # can't find the button
                    break

                next_page_button.click()
                page_number += 1
                file_name = url.split(f'{web_page_sub_selection}_')[1] + f'_{page_number:02}' + '.html'
                file_path = os.path.join(web_page_sub_selection_path, file_name)

            print(f'Successfully fetched and saved {page_number:02} HTML for {url}')


def get_and_save_html_content(urls, web_page_sub_selection, overwrite=False, worker=1):
    html_folder = 'htmls'
    create_folder(html_folder)
    web_page_sub_selection_path = os.path.join(html_folder, web_page_sub_selection)
    create_folder(web_page_sub_selection_path)

    urls_split = split_list(urls, worker)
    for item in urls_split:
        print(f'total worker {worker}, each worker has {len(item)} task')
        break

    with ThreadPoolExecutor(max_workers=worker) as executor:
        futures = []
        for index, url_chunk in enumerate(urls_split):
            future = executor.submit(fetch_and_save_html, url_chunk, web_page_sub_selection, overwrite,
                                     web_page_sub_selection_path, index)
            futures.append(future)

        # Wait for all tasks to complete
        for future in futures:
            future.result()
