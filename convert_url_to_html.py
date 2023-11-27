from html_tools import catalog_number
from html_tools import get_and_save_html_content, get_and_save_html_content_v2
import os
def get_url_list(number):
    with open(f'htmls/{number}/links', 'r', encoding='utf-8') as file:
        lines = file.readlines()

    unique_lines = list(set(lines))

    formatted_unique_lines = []
    for item in unique_lines:

        item = item.strip()

        # if 2 urls in the same line
        if len(item) == 104:
            half_length = len(item) // 2
            formatted_unique_lines.append(item[:half_length])
            formatted_unique_lines.append(item[half_length:])
        else:
            formatted_unique_lines.append(item)

    return formatted_unique_lines


if __name__ == "__main__":
    # urls = get_url_list(catalog_number['社会百科'])
    # get_and_save_html_content(urls, catalog_number['狮城财经'], worker=16)


    urls = get_url_list(catalog_number['狮城财经'])
    get_and_save_html_content_v2(urls, catalog_number['狮城财经'], worker=16)
    # os.system("shutdown /s /t 1")

