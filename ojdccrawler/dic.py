from urllib.parse import quote
from pyquery import PyQuery
import abc
import re


class Dic(abc.ABC):
    def __init__(self, host: str):
        self._host: str = host
        self._protocol: str = 'https' if host.startswith('https') else 'http'

    @classmethod
    @abc.abstractmethod
    def _search_url(cls, text: str) -> str:
        pass

    # TODO: Different types for different dictionary
    @abc.abstractmethod
    def search(self, text: str) -> list[tuple[str, str]]:
        pass

    def _handle_dic(self, dic: PyQuery) -> None:
        for node in dic('a').items():
            self._fill_links(node)
        for node in dic('img').items():
            self._fill_links(node)

    def _fill_links(self, doc: PyQuery) -> None:
        if doc.attr('href'):
            doc.attr['href'] = self._full_link(doc, 'href')
        if doc.attr('src'):
            doc.attr['src'] = self._full_link(doc, 'src')
        if doc.attr('srcset'):
            doc.attr['srcset'] = self._full_link(doc, 'srcset')

    def _full_link(self, doc: PyQuery, attr: str) -> str:
        link: str = doc.attr(attr)
        if not link:
            return ''

        if re.search('^[a-zA-Z0-9]+:', link):
            return link

        if link.startswith('//'):
            return self._protocol + ':' + link

        if re.search('^.?/+', link):
            return self._host + '/' + re.sub('^.?/+', '', link)

        return self._host + '/' + link


class WeblioDic(Dic):
    def __init__(self):
        super().__init__('https://www.weblio.jp')

    @classmethod
    def _search_url(cls, text: str) -> str:
        return 'https://www.weblio.jp/content/' + quote(text)

    def search(self, text: str) -> list[tuple[str, str]]:
        doc = PyQuery(self._search_url(text))
        if not doc:
            return []

        titles = [t.html() for t in doc('#cont>.pbarT .pbarTL>a').items()]
        dics = []
        for i, dic in enumerate(doc('#cont>.kijiWrp>.kiji').items()):
            title = titles[i]
            if not title:
                continue
            if title == '百科事典':
                continue
            dic = dic.clone()
            self._handle_dic(dic)
            dics.append((title, dic.html()))

        return dics


class GogenyuraiDic(Dic):
    def __init__(self):
        super().__init__('https://gogen-yurai.jp')

    @classmethod
    def _search_url(cls, text: str) -> str:
        return 'https://gogen-yurai.jp/?s=' + quote(text)

    def search(self, text: str) -> list[tuple[str, str]]:
        doc = PyQuery(self._search_url(text))
        if not doc:
            return []

        links = [self._full_link(node, 'href')
                 for node in doc('#main_col article>a').items()]
        if not links:
            return []

        dics = []
        for link in links:
            doc2 = PyQuery(link)
            if not doc2:
                continue
            title = doc2('#post_title>h1').html()
            dic = doc2('#article>.post_content').clone()
            dic('#single_banner_shortcode').remove()
            dic('#post_pagination').remove()

            pages = [self._full_link(node, 'href')
                     for node in doc2('#post_pagination>a').items()]
            for page in pages:
                doc2 = PyQuery(page)
                if not doc2:
                    continue
                dic.append(doc2('#article>.post_content').clone().html())
                dic('#single_banner_shortcode').remove()
                dic('#post_pagination').remove()

            self._handle_dic(dic)
            dics.append((title, dic.html()))

        return dics


def test():
    weblio = WeblioDic()
    dics = weblio.search('ほし')
    print(dics[3])


def test2():
    gogen = GogenyuraiDic()
    dics = gogen.search('ほし')
    print(dics[1])
    print(dics[5])


if __name__ == '__main__':
    # test()
    test2()
