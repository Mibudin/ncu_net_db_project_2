from urllib.parse import quote_plus
from pyquery import PyQuery
import abc
import re
from dataclasses import dataclass


@dataclass
class DicEntry:
    src: str = ""
    url: str = ""
    title: str = ""
    subtitle: str = ""
    dic: str = ""


class Dic(abc.ABC):
    def __init__(self, host: str, src: str):
        self._src: str = src
        self._host: str = host
        self._protocol: str = 'https' if host.startswith('https') else 'http'

    @classmethod
    @abc.abstractmethod
    def _search_url(cls, text: str) -> str:
        pass

    @abc.abstractmethod
    def search(self, text: str) -> list[DicEntry]:
        pass

    def _handle_dic(self, dic: PyQuery) -> None:
        dic.make_links_absolute(base_url=self._host)
        # for node in dic('a').items():
        #     self._fill_links(node)
        # for node in dic('img').items():
        #     self._fill_links(node)

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
        super().__init__('https://www.weblio.jp', 'weblio 国語辞典')
        self._blacklist = ['百科事典', 'ウィキペディア', '日本の自動車技術240選']

    @classmethod
    def _search_url(cls, text: str) -> str:
        return 'https://www.weblio.jp/content/' + quote_plus(text)

    def search(self, text: str) -> list[DicEntry]:
        url = self._search_url(text)
        doc = PyQuery(url)
        if not doc:
            return []

        titles = [t.html() for t in doc('#cont>.pbarT .pbarTL>a').items()]
        dics = []
        for i, dic in enumerate(doc('#cont>.kijiWrp>.kiji').items()):
            title = titles[i]
            if not title:
                continue
            if title in self._blacklist:
                continue
            dic = dic.clone()
            self._handle_dic(dic)
            dics.append(DicEntry(src=self._src, url=url, title=title, dic=dic.html()))

        return dics


class GogenyuraiDic(Dic):
    def __init__(self):
        super().__init__('https://gogen-yurai.jp', '語源由来辞典')

    @classmethod
    def _search_url(cls, text: str) -> str:
        return 'https://gogen-yurai.jp/?s=' + quote_plus(text)

    def search(self, text: str) -> list[DicEntry]:
        url = self._search_url(text)
        doc = PyQuery(url)
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
            dic('#post_pagination').prev('p').remove()
            dic('#post_pagination').remove()

            pages = [self._full_link(node, 'href')
                     for node in doc2('#post_pagination>a').items()]
            for page in pages:
                doc2 = PyQuery(page)
                if not doc2:
                    continue
                dic.append(doc2('#article>.post_content').clone().html())
                dic('#single_banner_shortcode').remove()
                dic('#post_pagination').prev('p').remove()
                dic('#post_pagination').remove()

            self._handle_dic(dic)
            dics.append(DicEntry(src=self._src, url=url, title=self._src,
                                 subtitle=title, dic=dic.html()))

        return dics


def test():
    weblio = WeblioDic()
    dics = weblio.search('風')
    print(dics[0])


def test2():
    gogen = GogenyuraiDic()
    dics = gogen.search('ほし')
    print(dics[1])
    print(dics[5])


def test3():
    html = '''
    <html>
    <head><title>The Dormouse's story</title></head>
    <body>
        <p class="title"><b>The Dormouse's story</b></p>
            <p class="story">Once upon a time there were three little sisters; and their names were
            <a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
            <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
            <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
            and they lived at the bottom of a well.
        </p>
        <p class="story">...</p>
        <div class="SgkdjImg"> <img src="https://weblio.hs.llnwd.net/e7/img/dict/sgkdj/images/103047.jpg" alt="風の画像"/>
        <div class="SgkdjImgMidaghigo"/> </div>
    </div>'''
    doc = PyQuery(html)
    print(doc.html())


if __name__ == '__main__':
    pass
    # test()
    # test2()
    # test3()
