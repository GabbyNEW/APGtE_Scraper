# IGNORE THIS SCRIPT !!

import requests
from bs4 import BeautifulSoup
from ebooklib import epub


if __name__ == '__main__':
    book = epub.EpubBook()

    # add metadata
    book.set_identifier('sample123456')
    book.set_title('Sample book')
    book.set_language('en')

    book.add_author('Aleksandar Erkalovic')

    URLTableOfContents = "https://practicalguidetoevil.wordpress.com/2015/03/25/prologue/"
    page = requests.get(URLTableOfContents)
    soup = BeautifulSoup(page.content, "html.parser") # Table of Contents
    content = soup.find("div", class_="entry-content") # Chapter main text body
    for s in soup.select("div", id="jp-post-flair") : s.extract() # Remove footer buttons


    # intro chapter
    c1 = epub.EpubHtml(title='Introduction', file_name='intro.xhtml', lang='en')
    c1.content=str(content)

    URLTableOfContents = "https://practicalguidetoevil.wordpress.com/2015/04/01/chapter-1-knife/"
    page = requests.get(URLTableOfContents)
    soup = BeautifulSoup(page.content, "html.parser") # Table of Contents
    content = soup.find("div", class_="entry-content") # Chapter main text body
    for s in soup.select("div", id="jp-post-flair") : s.extract() # Remove footer buttons

    # about chapter
    c2 = epub.EpubHtml(title='About this book', file_name='about.xhtml')
    c2.content=str(content)

    # about chapter
    c3 = epub.EpubHtml(title='About this book', file_name='about2.xhtml')
    c3.content='<h1>AAAA</h1><p>TEST ETSTSTTTS mine.</p>'

    # add chapters to the book
    book.add_item(c1)
    book.add_item(c2)
    book.add_item(c3)
    
    # create table of contents
    # - add section
    # - add auto created links to chapters

    book.toc = (epub.Link('intro.xhtml', 'Introduction', 'intro'), # Introduction section, shows on top of the Table of Contents
                 (epub.Section('Languages'), # Section
                 set([c1, c2])),    # Subsections
                (epub.Section('Languages'),
                 set([c1, c2]))
                )

    # add navigation files
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    # define css style
    style = '''
@namespace epub "http://www.idpf.org/2007/ops";
body {
    font-family: Cambria, Liberation Serif, Bitstream Vera Serif, Georgia, Times, Times New Roman, serif;
}
h2 {
     text-align: left;
     text-transform: uppercase;
     font-weight: 200;     
}
ol {
        list-style-type: none;
}
ol > li:first-child {
        margin-top: 0.3em;
}
nav[epub|type~='toc'] > ol > li > ol  {
    list-style-type:square;
}
nav[epub|type~='toc'] > ol > li > ol > li {
        margin-top: 0.3em;
}
'''

    # add css file
    nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)
    book.add_item(nav_css)

    # create spine
    book.spine = ['nav', c1, c2, c3] # The book must know the start of each section. We do this by specifying chapters

    # create epub file
    epub.write_epub('test.epub', book, {})