# -*- coding: utf-8 -*-
"""
Created on Fri Dec 24 19:19:13 2021

@author: rince

Ver las conclsuioens del abstract
Que me lod escarge o me aparezca el enlace para descargarlo si me es de utilidad.
Que me ponga antes los que tengas más matches
Que me traduzca automáticamente el abstract.
Que me los agrupe por palabras clave encontradas.
Filtrar por fecha.
Como no puedo descargármelos en mi equipo, puedo ponerlos en un calendar o un doc comaprtido de google para hacerlo en el despacho.
Si es open access, porque me lo puedo bajar en casa.
Que los resultados se guarden directamente en un fcihero.

"""

import requests
import json
from time import time
from bs4 import BeautifulSoup


class Paper():
    
    def __init__(self, title, abstract, kws, date, url = None):
        self._title = title
        self._abstract = abstract
        self._kws = kws
        self._date = date
        self._url = url
      
        

def save_tmp(data, file_name = "tmp.txt"):
    file = open(file_name, "w", encoding="utf-8")
    file.write(data)
    file.close()


def save_pdf(url, file_name = "tmp.pdf"):
    import shutil
    with requests.get(url, stream=True) as r:
        with open(file_name, 'wb') as f:
            shutil.copyfileobj(r.raw, f)


def load_historical(file_accepetd = "h_accepted.txt", f_rejected = "h_rejected.txt"):
    h_accepted = {}
    h_rejected = {}
    file = open(file_accepetd, "r", encoding="utf-8")
    data = file.readline()
    file.close()
    if data.strip() != "":
        h_accepted = eval(data)
    file = open(f_rejected, "r", encoding="utf-8")
    data = file.readline()
    file.close()
    if data.strip() != "":
        h_rejected = eval(data)
    
    print("Accepted size:", len(h_accepted), " / Rejected size:", len(h_rejected))
    return h_accepted, h_rejected
    

def add_historical(historical, link, journal = "", title = "", pub_date = ""):
    data = {"journal": journal, "title": title, "pub_date": pub_date}
    if journal == "":
        historical[link] = ""
    else:
        historical[link] = data
    return historical


def save_historical(h_accepted, h_rejected):
    data = str(h_accepted)
    save_tmp(data, "h_accepted.txt")    
    data = str(h_rejected)
    save_tmp(data, "h_rejected.txt")    
    
    
##

def url_get(url):
    xml_headers = {
            #"User-Agent"    : self.__user_agent,
            "Accept"        : 'text/xml',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
    }
    result = requests.get(url, headers = xml_headers)
    return result


def sciencedirect_papers_link(xml_node):
    import xml.etree.ElementTree as ET
    #print(xml_node)
    root = ET.fromstring(xml_node)
    #print(root)

    links = [l.text for l in root.iter("link")]
    return links[1:]


def sciencedirect_json_data(html_block):
    #print(html_block)
    soup = BeautifulSoup(html_block, 'html.parser')
    json_script = soup.find_all(lambda tag: tag.name == "script" and tag.has_attr("data-iso-key"))
    #print(json_script[0])
    #print(json_script[0].text)
    json_data = json.loads(json_script[0].text)
    return json_data


def json_find_key(json, key):
    #print("Entry", json)
    for j_key, j_val in json.items():
        if j_key == key:
            return j_val
        if type(j_val) == type([]):
            for json_block in j_val:
                result = json_find_key(json_block, key)
                if result is not None:
                    return result
        # Falta si encuentra otro json anidado
    return None


def sc_title(json_data):
    #print(json_data['article']["title"]["content"][-1])
    title = json_find_key(json_data['article']["title"]["content"][-1], '_')
    return title


def sc_date(json_data):
    #print(json_data['article']["title"]["content"][-1])
    article_block = json_data['article']
    #print(article_block)
    title = article_block["dates"]["Publication date"]
    return title


def sc_abstract(json_data):
    a_block = json_data['abstracts']
    if 'content' not in a_block:
        return "No abstract"
    #print(a_block['content'])
    #return a_block['content'][-1]['$$'][-1]['$$'][0]['_']
    return json_find_key(a_block['content'][-1]['$$'][-1]['$$'][0],'_')


def sc_find_abstract(html_block, json_data):
    soup = BeautifulSoup(html_block, 'html.parser')
    abstract_html = soup.find(lambda b: b.name == 'div' and b.has_attr('class') and 'author' in b['class'])
    if abstract_html is not None:
        return abstract_html.text
    return sc_abstract(json_data)
    

def sc_keywords(json_data):
    keywords = []
    
    #print(json_data)
    if 'content' in json_data['combinedContentItems']:
        first_block = json_data['combinedContentItems']["content"][0]
        #print("fisrt blok:\n", first_block)
        if '$$' not in first_block:
            return ["unkown keywords"]       
        if '$$' not in first_block['$$'][0]:
            return ["unkown keywords"]       

        #print("combinedContentItems:\n", json_data['combinedContentItems']["content"][0])
        keywords_json = first_block['$$'][0]['$$']
        #print("keywords_json:\n", keywords_json)
        for index in range(1, len(keywords_json)):
            #print(keywords_json[index]['$$'][0])
            ks_json = keywords_json[index]['$$'][0]
            if '$$' in ks_json:
                if '_' not in ks_json['$$'][0]:
                    kw = "unkown keyword"
                else:
                    kw = ks_json['$$'][0]['_'].lower()
            else:
                kw = ks_json['_'].lower()
            #keywords.append(keywords_json[index]['$$'][0]['_'].lower())
            keywords.append(kw)
    return keywords


def sc_extract(web_text):
    soup = BeautifulSoup(web_text, 'html.parser')
    json_data = sciencedirect_json_data(web_text)
    
    title = sc_title(json_data)
    abstract = sc_find_abstract(web_text, json_data)
    keywords = sc_keywords(json_data)
    pub_date = sc_date(json_data)
    link_html = soup.find(lambda b: b.name == 'link' and b.has_attr('rel') and 'canonical' in b['rel'])
    #print(link_html['href'])
    paper = Paper(title, abstract, keywords, pub_date, url = link_html['href'])

    return paper    


#def sc_process(paper):
def paper_process(paper):
    title = paper._title
    abstract = paper._abstract
    keywords = paper._kws
    pub_date = paper._date
    link = paper._url

    title_matches = matches_text(all_keywords, title) 
    abstract_matches = matches_text(all_keywords, abstract)    
    kws_matches = matches_list(all_keywords, keywords)
    
    has_matches = any_match(title_matches, abstract_matches, kws_matches)
    #has_matches = True
    if not has_matches:
        return False
   
    print(results_counter, "/", paper_counter, ": Title match", title_matches, " / Abstract match", abstract_matches, "/ Keywords match", kws_matches)
        #print()
    print(pub_date, "/", link)
    print('Title:', title)
    #print('date:', pub_date)
    print("Abstract:", abstract)
    print("Keywords:", keywords)
    print("---------------------")
    
    papers_accepted = []
    if (results_counter % 5) == 0 and len(papers_accepted) > 0:
        # Save incrementally
        pass
    
    return True

##

def ieee_json_data(html_block):
    json_block = ""
    soup = BeautifulSoup(html_block, 'html.parser')
    for script in soup.find_all("script"):
        if 'xplGlobal.document.metadata' in script.text:
            #print(script.text.index('xplGlobal.document.metadata'))
            chars =570 - len(script.text) + len('xplGlobal.document.metadata=')
        #print(chars)
            code_block = script.text[chars:].strip()
        #print(code_block[:-1])
            json_block = json.loads(code_block[:-1])
            break
    return json_block


def ieee_keywords(json_block):
    if "keywords" not in json_block:
        return ["No keywords"]
    kws = []
    for kw_json in json_block["keywords"]:
        for kw in kw_json['kwd']:
            kws.append(kw)
    return kws


def ieee_abstract(json_block):
    if "abstract" in json_block:
        return json_block["abstract"]
    return "No abstract found"


def ieee_extract(web_text):
     json_block = ieee_json_data(web_text)
     #print(json_block)

     title = json_block["formulaStrippedArticleTitle"]
     abstract = ieee_abstract(json_block)
     keywords = ieee_keywords(json_block)
     pub_date = json_block["journalDisplayDateOfPublication"]

     paper = Paper(title, abstract, keywords, pub_date, url = "https://ieeexplore.ieee.org" + json_block["pdfUrl"])
     
     return paper

"""
def ieee_process(paper):
     title = paper._title
     abstract = paper._abstract
     keywords = paper._kws
     pub_date = paper._date
     
     title_matches = matches_text(all_keywords, title)
     abstract_matches = matches_text(all_keywords, abstract)
     kws_matches = matches_list(all_keywords, keywords)
     
     if not any_match(title_matches, abstract_matches, kws_matches):
         return False

     print(results_counter, "/", paper_counter, ": Title match", title_matches, " / Abstract match", abstract_matches, "/ Keywords match", kws_matches)        
     print(title)
     print(abstract)
     print("Keywords: ", keywords)
     print(pub_date, "/ PDF: ", paper._url)
     #print("Is open: ", json_block["isOpenAccess"])
     #print("start page:", json_block["startPage"], " / end page:", json_block["endPage"])
     print("-------------------")
     return True
"""


def oxford_extract(web_text):
    soup = BeautifulSoup(web_text, 'html.parser')

    title_html = soup.find(lambda b: b.name == 'h1' and b.has_attr('class') and 'wi-article-title' in b['class'])
    title = title_html.text.strip()

    abstract_html = soup.find(lambda b: b.name == 'section' and b.has_attr('class') and 'abstract' in b['class'])
    if abstract_html == None:
        abstract = "No abstract."
    else:
        abstract = abstract_html.text

    kw_html = soup.find(lambda b: b.name == 'div' and b.has_attr('class') and 'kwd-group' in b['class'])
    if kw_html == None:
       keywords=["No keywords."]     
    else:
       keywords = []
    date_html = soup.find(lambda b: b.name == 'div' and b.has_attr('class') and 'citation-date' in b['class'])
    pub_date = date_html.text
     #print("-----------------------")

    # <meta property="og:url" content="https://academic.oup.com/jcde/article/8/6/1622/6448508"/>
    url_html = soup.find(lambda b: b.name == 'meta' and b.has_attr('property') and 'og:url' in b['property'])
    url = url_html['content']
    paper = Paper(title, abstract, keywords, pub_date, url = url)
     
    return paper


def search_papers(rss, f_extract, f_process):
    global paper_counter, results_counter, h_r, h_a
    
    for journal, rss_url in rss.items():
        #rss_url = "https://rss.sciencedirect.com/publication/science/14717727"
        print("\n**", journal)
        print()
        result = url_get(rss_url)
        links = sciencedirect_papers_link(result.text) # poner un límite o por fechas
        #print(links)
        
        #links = ["http://ieeexplore.ieee.org/document/9306773",]
        for link in links:
            #print(link)
            paper_counter +=1
            
            if link in h_a or link in h_r:
                #print("already in historical.")
                continue
            
            result = url_get(link)
            
            paper = f_extract(result.text)
            accepted = f_process(paper)
            if not accepted:
                h_r = add_historical(h_r, link)
            else:        
                h_a = add_historical(h_a, link, journal, paper._title, paper._date)
                results_counter += 1
            
            
            """
            json_block = ieee_json_data(result.text)
            #print(json_block)
           
            title = json_block["formulaStrippedArticleTitle"]
            abstract = ieee_abstract(json_block)
            keywords = ieee_keywords(json_block)
            pub_date = json_block["journalDisplayDateOfPublication"]
            
            title_matches = matches_text(all_keywords, title)
            abstract_matches = matches_text(all_keywords, abstract)
            kws_matches = matches_list(all_keywords, keywords)
            
            if not any_match(title_matches, abstract_matches, kws_matches):
                h_r = add_historical(h_r, link)
                continue

            h_a = add_historical(h_a, link, journal, title, pub_date)
            results_counter += 1
            print(results_counter, "/", paper_counter, ": Title match", title_matches, " / Abstract match", abstract_matches, "/ Keywords match", kws_matches)        
            print(title)
            print(abstract)
            print("Keywords: ", keywords)
            print(pub_date, "/ PDF: ", "https://ieeexplore.ieee.org" + json_block["pdfUrl"])
            #print("Is open: ", json_block["isOpenAccess"])
            #print("start page:", json_block["startPage"], " / end page:", json_block["endPage"])
            
        
            if (results_counter % 5) == 0 or (paper_counter % 500) == 0:
                #print("Historizal to save:", historical)
                save_historical(h_a, h_r)
                #pass
            """
            
        save_historical(h_a, h_r)

##

def _matches(all_keywords, search_space):
    result = []
    for keywords in all_keywords:
        for kw in keywords:
            for s_w in search_space:
                if kw in s_w:
                  result.append(kw)  
    return result


def matches_text(all_keywords, title):
    low_title = title.lower()
    result = []
    for keywords in all_keywords:
        for kw in keywords:
            if kw in low_title:
                result.append(kw)  
    return result


def matches_list(all_keywords, words_list):
    low_list = [w.lower() for w in words_list]
    return _matches(all_keywords, low_list)


def any_match(*matches_list):
    for m_list in matches_list:
        if len(m_list) > 0:
            return True
    return False
    
###################

science_direct_rss = {
    "Advances in Engineering Software": "https://rss.sciencedirect.com/publication/science/09659978",
    "Applied Soft Computing": "https://rss.sciencedirect.com/publication/science/15684946",
    "Computers in Human Behavior Reports": "https://rss.sciencedirect.com/publication/science/24519588",
    "Computer Standards & Interfaces": "https://rss.sciencedirect.com/publication/science/09205489",
    "Design Studies": "https://rss.sciencedirect.com/publication/science/0142694X",
    "Entertainment Computing": "https://rss.sciencedirect.com/publication/science/18759521",
    "European Management Journal":"https://rss.sciencedirect.com/publication/science/02632373",
    "Futures": "https://rss.sciencedirect.com/publication/science/00163287",
    "Information & Management": "https://rss.sciencedirect.com/publication/science/03787206",
    "Information and Software Technology": "https://rss.sciencedirect.com/publication/science/09505849",
    "Information Systems": "https://rss.sciencedirect.com/publication/science/03064379",
    "International Journal of Child-Computer Interaction": "https://rss.sciencedirect.com/publication/science/22128689",
    "Information and Organization": "https://rss.sciencedirect.com/publication/science/14717727",
    "Information Processing & Management": "https://rss.sciencedirect.com/publication/science/03064573",
    "Information Sciences": "https://rss.sciencedirect.com/publication/science/00200255",
    "International Journal of Information Management": "https://rss.sciencedirect.com/publication/science/02684012",
    "International Journal of Project Management": "https://rss.sciencedirect.com/publication/science/02637863",
    "Future Generation Computer Systems":"https://rss.sciencedirect.com/publication/science/0167739X",
    "Journal of Business Research": "https://rss.sciencedirect.com/publication/science/01482963",
    "Journal of Engineering and Technology Management": "https://rss.sciencedirect.com/publication/science/09234748",
    "Journal of International Management": "https://rss.sciencedirect.com/publication/science/10754253",
    "Journal of Innovation & Knowledge": "https://rss.sciencedirect.com/publication/science/2444569X",
    "Journal of Manufacturing Processes":"https://rss.sciencedirect.com/publication/science/15266125",
    "Journal of Systems and Software": "https://rss.sciencedirect.com/publication/science/01641212",
    "Organizational Dynamics": "https://rss.sciencedirect.com/publication/science/00902616", 
    "Performance Evaluation": "https://rss.sciencedirect.com/publication/science/01665316",
    "Project Leadership and Society": "https://rss.sciencedirect.com/publication/science/26667215",
    "Research in Organizational Behavior": "https://rss.sciencedirect.com/publication/science/01913085",
    "Scandinavian Journal of Management": "https://rss.sciencedirect.com/publication/science/09565221",
    "SoftwareX": "https://rss.sciencedirect.com/publication/science/23527110",
    "Software Impacts": "https://rss.sciencedirect.com/publication/science/26659638",
    "Technovation":"https://rss.sciencedirect.com/publication/science/01664972",
    "Telematics and Informatics": "https://rss.sciencedirect.com/publication/science/07365853",
    "The International Journal of Management Education": "https://rss.sciencedirect.com/publication/science/14728117",
    "The Journal of Strategic Information Systems": "https://rss.sciencedirect.com/publication/science/09638687",
    "The Leadership Quarterly":"https://rss.sciencedirect.com/publication/science/10489843"
}

ieee_rss = {
    "Computer": "https://ieeexplore.ieee.org/rss/TOC2.XML",
    "IBM Journal of Research and Development": "https://ieeexplore.ieee.org/rss/TOC5288520.XML",
    "IEEE Access": "https://ieeexplore.ieee.org/rss/TOC6287639.XML",
    "IEEE BITS the Information Theory Magazine": "https://ieeexplore.ieee.org/rss/TOC9393008.XML",
    "IEEE Design & Test": "https://ieeexplore.ieee.org/rss/TOC6221038.XML",
    "IEEE Pulse": "https://ieeexplore.ieee.org/rss/TOC5454060.XML",
    "IEEE Internet Computing": "https://ieeexplore.ieee.org/rss/TOC4236.XML",
    "IEEE Software": "https://ieeexplore.ieee.org/rss/TOC52.XML",
    "IEEE Transactions on Affective Computing": "https://ieeexplore.ieee.org/rss/TOC5165369.XML",
    "IEEE Transactions on Computational Social Systems": "https://ieeexplore.ieee.org/rss/TOC6570650.XML",
    "IEEE Transactions on Computers": "https://ieeexplore.ieee.org/rss/TOC12.XML",
    "IEEE Transactions on Cybernetics":"https://ieeexplore.ieee.org/rss/TOC6221036.XML",
    "IEEE Transactions on Emerging Topics in Computing": "https://ieeexplore.ieee.org/rss/TOC6245516.XML",
    "IEEE Transactions on Human-Machine Systems": "https://ieeexplore.ieee.org/rss/TOC6221037.XML",
    "IEEE Transactions on Information Theory": "https://ieeexplore.ieee.org/rss/TOC18.XML",
    "IEEE Transactions on Games": "https://ieeexplore.ieee.org/rss/TOC7782673.XML",
    "IEEE Transactions on Software Engineering": "https://ieeexplore.ieee.org/rss/TOC32.XML",
    "Interacting with Computers":"https://ieeexplore.ieee.org/rss/TOC8016801.XML",
    "IT Professional": "https://ieeexplore.ieee.org/rss/TOC6294.XML",
    "Journal of Social Computing": "https://ieeexplore.ieee.org/rss/TOC8964404.XML",
    "The Computer Journal": "https://ieeexplore.ieee.org/rss/TOC8016794.XML"
}

oxford_rss = {
    "Children & Schools - LI": "https://academic.oup.com/rss/site_5441/3302.xml",
    "Children & Schools - AA": "https://academic.oup.com/rss/site_5441/advanceAccess_3302.xml",
    "Communication Theory - LI": "https://academic.oup.com/rss/site_6090/3964.xml",
    "Communication Theory - AA": "https://academic.oup.com/rss/site_6090/advanceAccess_3964.xml",
    "Interacting with Computers - LI": "https://academic.oup.com/rss/site_5295/3161.xml",
    "Interacting with Computers - AA": "https://academic.oup.com/rss/site_5295/advanceAccess_3161.xml",
    "Journal of Computational Design and Engineering - Latest Issues": "https://academic.oup.com/rss/site_6272/4058.xml",
    "Journal of Computational Design and Engineering - Advance Articles": "https://academic.oup.com/rss/site_6272/advanceAccess_4058.xml",
    "Journal of Computer-Mediated Communication - LI": "https://academic.oup.com/rss/site_6096/3967.xml",
    "Journal of Computer-Mediated Communication - AA": "https://academic.oup.com/rss/site_6096/advanceAccess_3967.xml",
    "The Computer Journal - LI": "https://academic.oup.com/rss/site_5271/3137.xml",
    "The Computer Journal - AA": "https://academic.oup.com/rss/site_5271/advanceAccess_3137.xml",
    }

agile_keywords = (
    "scrum",
    "extreme programming",
    "software value",
    "value of software",
    "manifesto",
    "agile",
    "agility",
    "agile contract",
    "devops",
    "devsecops",
    "horizontal slicing",
    "capability",
    "capabilities",
    "okr",
    "object-key",
    "user story",
    "user stories",
    "vertical slicing"
    )

management_keywords = (
    "cell structure",
    "cell organization",
    "dao",
    "decentralized autonomous organization",
    "lean management",
    "lean software",
    "kanban",
    "sense and respond",
    "sense & respond",
    "team",
    "fearless",
    "psychological safety",
    "sychological safety",
    "beyond budgeting",
    "open space",
    "betacodex",
    "beta codex"
    )

programming_kws = (
    "python",
    "tdd",
    "test-driven",
    "bdd",
    "behaviour driven",
    "behaviur driven",
    "pandas",
    "refactoring",
    "web3",
    "web 3"
    )

education_kws = (
    'student project',
    )

all_keywords = (agile_keywords, management_keywords, programming_kws, education_kws)

# 41 keywords


ts = time()
paper_counter = 0
h_a, h_r = load_historical()
results_counter = len(h_a)

print("Oxford", len(oxford_rss), "RSS")
print()
search_papers(science_direct_rss, oxford_extract, paper_process)
print("Final count:", paper_counter, "Results:", results_counter, "Time:", (time()-ts))


"""
#results_counter = len(h_a)
for journal, rss_url in oxford_rss.items():
    continue
    print("\n**", journal, rss_url)
    result = url_get(rss_url)
    links = sciencedirect_papers_link(result.text)
    #links = []
    
    for link in links:
        print(link)
        result = url_get(link)
#save_tmp(result.text)
        soup = BeautifulSoup(result.text, 'html.parser')

        title_html = soup.find(lambda b: b.name == 'h1' and b.has_attr('class') and 'wi-article-title' in b['class'])
        print(title_html.text.strip())

        abstract_html = soup.find(lambda b: b.name == 'section' and b.has_attr('class') and 'abstract' in b['class'])
        if abstract_html == None:
            print("No abstract.")
        else:
            print(abstract_html.text)

        kw_html = soup.find(lambda b: b.name == 'div' and b.has_attr('class') and 'kwd-group' in b['class'])
        if kw_html == None:
            print("No keywords.")
        else:
            print("KW:", kw_html.text)

        date_html = soup.find(lambda b: b.name == 'div' and b.has_attr('class') and 'citation-date' in b['class'])
        print("date:", date_html.text)
        print("-----------------------")

"""


print("Science direct", len(science_direct_rss), "RSS")
print()
search_papers(science_direct_rss, sc_extract, paper_process)
print("Final count:", paper_counter, "Results:", results_counter, "Time:", (time()-ts))


print("IEEE", len(ieee_rss), "RSS")
print()
search_papers(ieee_rss, ieee_extract, paper_process)
print("Final count:", paper_counter, "Results:", results_counter, "Time:", (time()-ts))

exit();


# El código de abajo ya nos e usa porque está en los métodos de arriba.

for journal, rss_url in ieee_rss.items():
    print("\n**", journal)
    print()
    result = url_get(rss_url)
    links = sciencedirect_papers_link(result.text) # poner un límite o por fechas
    #print(links)
    
    #links = ["http://ieeexplore.ieee.org/document/9306773",]
    for link in links:
        #print(link)
        paper_counter +=1
        
        if link in h_a or link in h_r:
            #print("already in historical.")
            continue
        
        result = url_get(link)
        
        paper = ieee_extract(result.text)
        accepted = paper_process(paper)
        if not accepted:
            h_r = add_historical(h_r, link)
        else:        
            h_a = add_historical(h_a, link, journal, paper._title, paper._date)
            results_counter += 1
        
        
        """
        json_block = ieee_json_data(result.text)
        #print(json_block)
       
        title = json_block["formulaStrippedArticleTitle"]
        abstract = ieee_abstract(json_block)
        keywords = ieee_keywords(json_block)
        pub_date = json_block["journalDisplayDateOfPublication"]
        
        title_matches = matches_text(all_keywords, title)
        abstract_matches = matches_text(all_keywords, abstract)
        kws_matches = matches_list(all_keywords, keywords)
        
        if not any_match(title_matches, abstract_matches, kws_matches):
            h_r = add_historical(h_r, link)
            continue

        h_a = add_historical(h_a, link, journal, title, pub_date)
        results_counter += 1
        print(results_counter, "/", paper_counter, ": Title match", title_matches, " / Abstract match", abstract_matches, "/ Keywords match", kws_matches)        
        print(title)
        print(abstract)
        print("Keywords: ", keywords)
        print(pub_date, "/ PDF: ", "https://ieeexplore.ieee.org" + json_block["pdfUrl"])
        #print("Is open: ", json_block["isOpenAccess"])
        #print("start page:", json_block["startPage"], " / end page:", json_block["endPage"])
        """
    
        if (results_counter % 5) == 0 or (paper_counter % 500) == 0:
            #print("Historizal to save:", historical)
            save_historical(h_a, h_r)
            #pass
            
#save_pdf("https://ieeexplore.ieee.org" + json_block["pdfUrl"])
        
print("Final count:", paper_counter, "Results:", results_counter)


exit();
print()
print("Science direct", len(science_direct_rss), "RSS")
print()
#paper_counter = 0
#results_counter = 0
for journal, rss_url in science_direct_rss.items():
    print("\n**", journal)
    print()
    #rss_url = "https://rss.sciencedirect.com/publication/science/03064379"
    result = url_get(rss_url)

    links = sciencedirect_papers_link(result.text) # poner un límite o por fechas
    for link in links:
        paper_counter +=1

        if link in h_a or link in h_r:
            #print("already in historical.")
            continue
        
        #  print(link)
        result = url_get(link)
        json_data = sciencedirect_json_data(result.text)
        
        title = sc_title(json_data)
        title_matches = matches_text(all_keywords, title)
        
        abstract = sc_find_abstract(result.text, json_data)
        abstract_matches = matches_text(all_keywords, abstract)
        
        keywords = sc_keywords(json_data)
        kws_matches = matches_list(all_keywords, keywords)
        
        pub_date = sc_date(json_data)
        
        has_matches = any_match(title_matches, abstract_matches, kws_matches)
        #has_matches = True
        if not has_matches:
            h_r = add_historical(h_r, link)
            continue
       
            #add_historical(historical, link, journal, title, pub_date)

        h_a = add_historical(h_a, link, journal, title, pub_date)
        results_counter += 1
        print(results_counter, "/", paper_counter, ": Title match", title_matches, " / Abstract match", abstract_matches, "/ Keywords match", kws_matches)
            #print()
        print(pub_date, "/", link)
        print('Title:', title)
        #print('date:', pub_date)
        print("Abstract:", abstract)
        print("Keywords:", keywords)
        print("---------------------")
  
print("Final count:", paper_counter, "Results:", results_counter)
    