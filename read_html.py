import os
import glob
import re
from html_tools import read_sub_page_html
from tools import save_content
from collections import defaultdict


def read_html_files(folder_path):
    file_list = os.listdir(folder_path)
    grouped_files = defaultdict(list)

    len_grouped_files = len(grouped_files)

    for file_name in file_list:

        match = re.match(r'(\d+)_\d+\.html', file_name)
        if match:
            group_number = match.group(1)
            grouped_files[group_number].append(file_name)

    for index, file_group in enumerate(grouped_files):
        print(file_group)
        page_content = ''
        for index, file_name in enumerate(grouped_files[file_group]):
            file_path = os.path.join(folder_path, file_name)
            page_content += read_sub_page_html(file_path, index)

        content_file_name = file_group + '.text'
        save_content(folder_path, page_content, content_file_name)
        # print(f"Processed file {index + 1} out of {len_grouped_files}")


if __name__ == "__main__":
    read_html_files(folder_path='htmls/147')
