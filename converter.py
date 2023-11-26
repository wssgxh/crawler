import os

htmls_directory = "htmls/179/"

try:
    # 获取指定目录下的所有文件
    html_files = [f for f in os.listdir(htmls_directory) if os.path.isfile(os.path.join(htmls_directory, f))]

    for html_file in html_files:
        file_path = os.path.join(htmls_directory, html_file)
        print(html_file)
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()

        # 转换为GBK格式
        gbk_content = html_content.encode('gbk')

        # 将转换后的内容写入新文件
        gbk_file_path = file_path
        with open(gbk_file_path, 'wb') as gbk_file:
            gbk_file.write(gbk_content)

        print(f"成功将文件 {html_file} 转换为GBK格式并保存到 {gbk_file_path}")

except Exception as e:
    print(f"发生错误：{e}")
