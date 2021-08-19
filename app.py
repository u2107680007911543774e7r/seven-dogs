import os
import time

import pywebio
from pywebio.input import input, TEXT
from pywebio.output import put_text, put_markdown, put_table, put_grid, put_link, put_buttons, put_code, put_loading
import csv

from pywebio.session import set_env

import main


def seven_dogs():
    set_env(title='FBASearch')
    keyword = input("Input your keyword：", type=TEXT)

    start = time.time()
    with put_loading(shape='grow', color='dark'):
        content = generate_table_content(keyword)
        put_markdown(f'# **Search results \"{keyword}\":**')
        put_table(content, header=['Title', 'Price', 'Shop', 'Link'])
    # .style(
    #         'width: 200%; margin-left:-50%; '
    #         'margin-right: 20%;')
        end = time.time()
        put_code(f'Runtime: {end - start} secs')
        put_buttons([dict(label='Back', value='dark', color='dark')], onclick=put_text('In progress...'))


def generate_table_content(keyword):
    list2x = main.search_3(keyword)
    # with open('results.csv', 'r') as f:
    #     reader = csv.reader(f)
    #     for row in reader:
    #         list2x.append(row)
    #     f.close()
    res = []
    for item in list2x:
        if item[3] != '':
            res.append([put_text(item[0]), put_text(item[1]), put_text(item[2]),
                        put_link(url=item[3], name='Visit Link', new_window=True)])
        else:
            res.append([put_text(item[0]), put_text(item[1]), put_text(item[2]),
                        put_text(item[3])])
    return res


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    pywebio.start_server(seven_dogs, port=port)
