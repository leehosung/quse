import datetime

TEMPLATE_DIR = 'templates'
OUTPUT_DIR = '/Users/tyson/git/leehosung.github.io/_drafts'
contents = file('{}/{}'.format(TEMPLATE_DIR, 'weekly.md')).read()

def get_next_sunday():
    today = datetime.date.today()
    sunday = today + datetime.timedelta((6 - today.weekday()) % 7)
    return sunday

sunday = get_next_sunday()

file_name = sunday.strftime('%Y-%m-%d-%Y-W%W.md')
file_path = '{}/{}'.format(OUTPUT_DIR, file_name)
open(file_path, 'w').write(contents.format(sunday.year, sunday.strftime('%W'), sunday))
