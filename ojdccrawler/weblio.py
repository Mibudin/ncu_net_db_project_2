from urllib.parse import quote
from pyquery import PyQuery


def main():
    # dom = PyQuery('https://www.weblio.jp/content/%E3%81%BB%E3%81%97')
    # https://github.com/crimx/ext-saladict/blob/dev/src/components/dictionaries/weblio/engine.ts
    print('https://www.weblio.jp/content/' + quote('ほし'))
    doc = PyQuery('https://www.weblio.jp/content/' + quote('ほし'))
    print(doc('#cont'))


if __name__ == '__main__':
    main()
