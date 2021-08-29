import os
import time
import pywebio
from pywebio.input import input, TEXT
from pywebio.output import put_text, put_markdown, put_table, put_grid, put_link, put_buttons, put_code, put_loading
from pywebio.platform.flask import webio_view
from flask import Flask, render_template, redirect, request, url_for
from pywebio.session import set_env
from flask_bootstrap import Bootstrap
import main


def seven_dogs(keyword):
    set_env(title='FBASearch')

    with put_loading(shape='grow', color='dark').style('margin-left: 50%; width:4rem; height:4rem'):
        content = generate_table_content(keyword)
        put_markdown(f'# **Search results \"{keyword}\":**')
        put_table(content, header=['Title', 'Price', 'Shop', 'Link'])
        # .style(
        #         'width: 200%; margin-left:-50%; '
        #         'margin-right: 20%;')
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
    app = Flask(__name__, template_folder='templates')
    results = []
    Bootstrap(app)


    @app.route('/', methods=['GET', 'POST'])
    @app.route('/index.html', methods=['GET', 'POST'])
    def home():
        if request.method == 'GET':
            return render_template('index.html')
        else:
            text = request.form['search']
            r = main.search_3(text)
            for i in r:
                results.append(i)
            return redirect('search.html')

    @app.route('/faq.html', methods=['GET'])
    def faq():
        return render_template('faq.html')

    @app.route('/contact.html', methods=['GET'])
    def contact():
        return render_template('contact.html')

    @app.route('/search.html')
    def search():
        return render_template('search.html', results=results)

    # app.add_url_rule('/tool', 'webio_view', webio_view(seven_dogs('test')),
    #                   methods=['GET', 'POST', 'OPTIONS'])  # need GET,POST and OPTIONS methods

    app.run(host='localhost', port=port)  # port=port /5000
