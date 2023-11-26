import os
from functools import lru_cache

catalog_number = {'狮城财经': '147', '家有儿女': '179', '社会百科': '108'}


def split_list(lst, num_workers):
    avg = len(lst) // num_workers
    remainder = len(lst) % num_workers
    result = []

    i = 0
    for _ in range(num_workers):
        if remainder > 0:
            start = i
            end = i + avg + 1
            i = end
            remainder -= 1
        else:
            start = i
            end = i + avg
            i = end

        result.append(lst[start:end])

    return result


def save_html_to_file(html_content, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(html_content)


@lru_cache
def create_folder(folder):
    current_path = os.getcwd()
    folder_path = os.path.join(current_path, folder)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


def save_content(folder_path, page_content, file_name):
    content_path = os.path.join(folder_path, 'content')
    create_folder(content_path)
    with open(os.path.join(content_path, file_name), 'w', encoding='gbk') as file:
        file.write(page_content)
