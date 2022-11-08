import requests
from bs4 import BeautifulSoup
from ebooklib import epub

# Global
currentBookTitle = ""
currentBookNumber = 0
book, extras = None, None
spine = ["nav"]
book1, book2, book3, book4, book5, book6, book7 = [], [], [], [], [], [], [] # Table of Contents subsections
x = 0

def initializeEpubMetadata():
    global book
    book = epub.EpubBook()
    book.set_title("A Practical Guide To Evil")
    book.set_cover(content="APGTE_front.png", file_name="APGTE_front.png")
    book.add_author("ErraticErrata")

def main():
    # Load text file containing the extra chapter titles
    global extras
    extras_file = open("Extra Chapters.txt", 'r')
    data = extras_file.read()
    extras = data.split("\n")

    print("Press ENTER to begin book scraping of A Practical Guide To Evil.", end=" ")
    input()

    global book, currentBookTitle, currentBookNumber
    initializeEpubMetadata()
    # Access Table of Contents
    URLTableOfContents = "https://practicalguidetoevil.wordpress.com/table-of-contents/"
    page = requests.get(URLTableOfContents)

    soup = BeautifulSoup(page.content, "html.parser") # Table of Contents
    
    entryResults = soup.find("div", class_="entry-content")

    for child in entryResults.find_all(recursive=False):
        if child.name == 'h2': # Book Number
            currentBookNumber += 1
            currentBookTitle = child.text + " — "
        elif child.name == 'ul': # Get all chapters of a Book Number, then extract content each
            iterateChapters(child)
    
    generateBook()
    print("Epub file has been generated!")
    
"""
    On a given book number, get information about each chapters.
"""
def iterateChapters(chapters):
    chaptersSoup = BeautifulSoup(str(chapters), "html.parser") # Contains a list (not the Python kind of list) of chapters of a given book number

    for chapter in chaptersSoup.find_all("li"):
        if (not chapter.string): # Book 2 has an extra empty CSS tag as the first list element, filter it out
            continue
        chapterSoup = BeautifulSoup(str(chapter), "html.parser")
        currentChapterTitle = currentBookTitle + chapterSoup.find('a').text # Get Chapter Title
        url = chapterSoup.find('a')['href'] # Get URL of Chapter
        extractChapter(url, currentChapterTitle) # Extract content
        
def extractChapter(url, currentChapterTitle):
    global book, extras
    chapterPage = requests.get(url) # Visit the Chapter page
    chapterSoup = BeautifulSoup(chapterPage.content, "html.parser") # Chapter page HTML content

    # Get information on the succeeding chapter to identify an 'Extra' chapter
    nextChapterInfo = chapterSoup.find("div", class_="nav-next").findChild("a", recursive=True)
    nextChapterText = next(nextChapterInfo.stripped_strings)
    nextChapterLink = nextChapterInfo['href']

    # Proceed to extract the text of the chapter
    content = chapterSoup.find("div", class_="entry-content") # Chapter main text body
    for s in chapterSoup.select("div", id="jp-post-flair") : s.extract() # Remove footer buttons
    appendChapterToBook(content, currentChapterTitle)

    # Determine if an Extra chapter succeeds the current chapter
    if nextChapterText in extras:
        print("Extra chapter detected. Appending extra chapter...")
        extractChapter(nextChapterLink, nextChapterText) # Fancy recursive XD

def appendChapterToBook(content, currentChapterTitle):
    global x
    global book, spine, book1, book2, book3, book4, book5, currentBookNumber
    epubChapter = epub.EpubHtml(title=currentChapterTitle, file_name=str(x) + ".xhtml", lang='hr')
    epubChapter.content = "<h2>" + currentChapterTitle + "</h2>" + str(content).replace('<div class="entry-content">\n', "").replace('\n </div>', "")

    book.add_item(epubChapter)
    spine.append(epubChapter)
    if currentBookNumber == 1 : book1.append(epubChapter)
    elif currentBookNumber == 2 : book2.append(epubChapter)
    elif currentBookNumber == 3 : book3.append(epubChapter)
    elif currentBookNumber == 4 : book4.append(epubChapter)
    elif currentBookNumber == 5 : book5.append(epubChapter)
    elif currentBookNumber == 6 : book6.append(epubChapter)
    else : book7.append(epubChapter)

    x += 1
    print(currentChapterTitle + " OK!")

def generateBook():
    global book, spine, book1, book2, book3, book4, book5
    print("Generating EPUB file...")
    book.spine = spine
    book.toc = (
             (epub.Section('Book 1'),
             book1),
             (epub.Section('Book 2'),
             book2),
             (epub.Section('Book 3'),
             book3),
             (epub.Section('Book 4'),
             book4),
             (epub.Section('Book 5'),
             book5),
             (epub.Section('Book 6'),
             book6),
             (epub.Section('Book 7'),
             book7)
            )

    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    epub.write_epub('A Practical Guide To Evil.epub', book, {})

if __name__ == "__main__": 
    main()