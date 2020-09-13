import bs4 as bs 
import re
import pandas as pd
import numpy as np

#Define Default markdown style:

def get_book_details(soup):
    
    '''
    Input: BeautifulSoup object of Kindle notes in HTML format
    Output: Dictionary with book title, author, and citations
    
    '''
    
    book_details = {}
    
    try:
        book_details['title'] = soup.find('div', {'class': 'bookTitle'}).text.strip()
        book_details['authors'] = soup.find('div', {'class': 'authors'}).text.strip()
        book_details['citations']= soup.find('div', {'class': 'citation'}).text.strip()
    except:
        pass
    
    return book_details


def get_page_location(div_soup):
    
    type_pattern = r'(.*)-'
    page_pattern = r'Page (.+) ·'
    location_pattern = r'Location (\d+)'
    
    '''
    Use when div_soup[class] = noteHeading
    Input: BeautifulSoup div that contains data on SectionHeader
    Output: Dictionary on Header Type, Page, & Location
    
    Example: 
        Input Header: "Highlight(orange) - Page xxiv · Location 185"
        Output: {type: Highlight(orange), page: xxiv, location: 185} 
             
    '''
    
    details = {}  
    
    try:
        details['type'] = re.findall(type_pattern, div_soup)[0].strip()
    except:
        details['type'] = -1
    
    try:
        details['page'] = re.findall(page_pattern, div_soup)[0]  
    except:
        details['page'] = -1
        
    try:
        details['location'] = re.findall(location_pattern, div_soup)[0]
    except:
        details['location'] = -1                                 
    
    return details

def soup_to_frame(soup):
    
    '''
    Input: BeautifulSoup Object of Kindle HTML notes
    Output: Pandas DataFrame containing relevant note data
    
    '''
    
    #all_divs: list of all relevant data contained in divs
    all_divs = soup.findAll('div')
    
    #Book notes are divided into sections, use the section VAR to track current section
    section = 0

    #section_headers dictionary {Key = Section #: Value = Section title}
    section_headers = {}
    section_texts = pd.DataFrame()

    current_type = None
    current_page = None
    current_location = None

    for idx,div_tag in enumerate(all_divs):

        #If tag is sectionHeading add to section_headers and increment section by 1
        if div_tag['class'][0] == 'sectionHeading':

            section += 1
            section_headers[section] = div_tag.text.strip()
            continue

        #If tag is noteHeading: use get_page_location"()
        if div_tag['class'][0] == 'noteHeading':
            div_text = div_tag.text.strip() #get text of div
            page_location = get_page_location(div_text) #extract page & location

            current_type = page_location['type']
            current_page = page_location['page']
            current_location = page_location['location']

            #If a note tag, noteHeading will be followed by a noteText
            #If the div is a Bookmark, there will be no noteText.
            #We will need to populate with blank dummy text data to maintain correct indexing:
            if current_type == 'Bookmark':
                text = pd.Series([idx, section, current_type, '', current_page, current_location],
                    index = ['div_index', 'Section', 'Type', 'Text', 'Page', 'Location'])
                section_texts = pd.concat([section_texts, text], axis = 1, sort = True)
                continue


        if div_tag['class'][0] == 'noteText':
            text = pd.Series([idx, section, current_type, div_tag.text.strip(), current_page, current_location],
                            index = ['div_index', 'Section', 'Type', 'Text', 'Page', 'Location'])
            section_texts = pd.concat([section_texts, text], axis = 1, sort = True)
            continue
            
    return section_headers, section_texts.T


def frame_to_markdown(book_details, headers, text, style):
    '''
    Input: 
        book_details = output of get_book_details()
        headers = 1st output of soup_to_frame()
        text = 2nd output of soup_to_frame()
        styling_dict = Dictionary that determines markdown formatting of sections
            Must have Keys: 'title', 'author', 'section', 'location', 'note'
                    Values: MarkDown notation (ie. #, > for each attribute)
            
    Output:
        .txt file of Kindle HTML output in Markdown format 
    
    '''
    
    title = book_details['title']
    author = book_details['authors']
    
    file_friendly = re.sub(r'[^\w\s]','',title)
    file_name = file_friendly + ' Markdown Notes.txt'


    file_content = "\n{} {} \n{} {} \n \n --- \n".format(style['title'], title, style['author'], author)

    #section_num tracks current chapter 
    section_num = 1
    
    for _, row in text.iterrows():

        if row['Section'] == section_num:
            
            file_content = file_content + "{} {} \n".format(style['section'], headers[section_num])
            
            section_num += 1

        # write text
        if row["Type"] != 'Bookmark':
            
            file_content = file_content + "{} {}  -- {}Location: {}  Page: {}{})\n\n".format(style['note'], 
            row['Text'],style['location'], row['Location'], row['Page'], style['location'])

    return file_content
    
    

def html_to_markdown(html_file, style):
    
    #Read HTML file and convert to BeautifulSoup object:
    #f1 = open(html_file, 'r', encoding="utf-8").read()
    soup = bs.BeautifulSoup(html_file, features='html.parser') 
    
    book_details = get_book_details(soup)
    shead, stext = soup_to_frame(soup)
    
    tmp = frame_to_markdown(book_details, shead, stext, style)
    return tmp



def get_md(text):
    
    p = re.compile(r'(.*) \(')
    tmp = re.findall(p, text)
    return tmp[0]

    
    
    