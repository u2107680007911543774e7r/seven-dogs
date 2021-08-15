import os
import time

import pywebio
from pywebio.input import input, TEXT
from pywebio.output import put_text, put_markdown, put_table, put_grid, put_link
import csv

from pywebio.session import set_env

import main


def seven_dogs():
    set_env(title='Danny\'s App')
    keyword = input("Input your keyword：", type=TEXT)
    put_markdown(f'# **Search results \"{keyword}\":**')
    start = time.time()
    put_table(generate_table_content(keyword), header=['Title', 'Price (USD)', 'Shop', 'Link']).style(
        'width: 200%; margin-left:-50%; '
        'margin-right: 20%;')
    end = time.time()
    put_text(f'Runtime: {end - start} secs')


def generate_table_content(keyword):
    list2x = main.search_3(keyword)
    # with open('results.csv', 'r') as f:
    #     reader = csv.reader(f)
    #     for row in reader:
    #         list2x.append(row)
    #     f.close()
    res = []
    for item in list2x:
        res.append([put_text(item[0]), put_text(item[1]), put_text(item[2]), put_link(url=item[3], name=item[3])])
    return res


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    pywebio.start_server(seven_dogs, port=port)
