import json
from jinja2 import Environment, FileSystemLoader
from livereload import Server
import markdown
import glob
import os


def get_md_list():
    return glob.glob('./articles/*/*.md')


def convert_md2html(path):
    with open(path, 'r', encoding='utf-8') as md_data:
        extension_param = 'markdown.extensions.codehilite'
        html_data = markdown.markdown(md_data.read(),
                                      extensions=[extension_param])
    file_name, file_extension = os.path.splitext(path)
    with open('{}.html'.format(file_name), 'w', encoding="utf8") as out_file:
        out_file.write(html_data)


def load_data():
    with open('config.json', encoding="utf8") as config_file:
        context = json.load(config_file)
    return context


def load_templates():
    env = Environment(loader=FileSystemLoader('templates'))
    index_template = env.get_template('index.html')
    page_template = env.get_template('page.html')
    return index_template, page_template


def make_site():
    index_template, page_template = load_templates()
    context_data = load_data()
    context_data.update({'core_css': './css/bootstrap.min.css'})
    context_data.update({'custom_css': './css/starter-template.css'})
    context_data.update({'core_js': './js/bootstrap.min.js'})
    context_data.update({'icon': './favicon.ico'})
    print(context_data['articles'])
    with open('index.html', 'w', encoding="utf8") as out_file:
        out_file.write(index_template.render(context_data))
    for md_file in get_md_list():
        convert_md2html(md_file)
    list_html_files = glob.glob('./articles/*/*.html')
    for html_file in list_html_files:
        with open(html_file, 'r', encoding="utf8") as in_file:
            context_data = {'context': in_file.read()}
            context_data.update({'core_css': './../../css/bootstrap.min.css'})
            context_data.\
                update({'custom_css': './../../css/starter-template.css'})
            context_data.update({'core_js': './../../js/bootstrap.min.js'})
            context_data.update({'icon': './../../favicon.ico'})
            context_data.update({'index': './../../index.html'})
        with open(html_file, 'w', encoding="utf8") as out_file:
            out_file.write(page_template.render(context_data))


if __name__ == '__main__':
    make_site()
    server = Server()
    server.watch('templates/*.html', make_site)
    server.serve(root='site/')
