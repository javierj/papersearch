# -*- coding: utf-8 -*-
"""
Created on Tue Dec 21 14:53:49 2021

@author: rince
"""


from urllib.parse import quote_plus as url_encode
import json, pathlib
import requests, time


def save_tmp(data):
    file = open("tmp.txt", "w", encoding="utf-8")
    file.write(data)
    file.close()
    

my_key = '1ff1345f7b2e66316522ec31ab816511'

headers = {
            "X-ELS-APIKey"  : my_key,
            #"User-Agent"    : self.__user_agent,
            "Accept"        : 'application/json'
            }

xml_headers = {
            "X-ELS-APIKey"  : my_key,
            #"User-Agent"    : self.__user_agent,
            "Accept"        : 'text/xml',
            'User-Agent': 'Mozilla/5.0'
            }

""" - No me funciona por tema de IP
URL =  "https://api.elsevier.com/content/search/sciencedirect?query=Scrum&apiKey=" + my_key
print(URL)
r = requests.get(URL, headers = headers)
print(r.json())
"""        



URL =  "https://api.elsevier.com/content/search/scopus?query=scrum&apiKey=" + my_key
r = requests.get(URL, headers = headers)
print(r.json())
# Esta funciona.

search_data = r.json()

print("---")
print(search_data['search-results']['opensearch:Query']) #{'@role': 'request', '@searchTerms': 'scrum', '@startPage': '0'}
paper = search_data['search-results']['entry'][0]
print(paper)

for entry in search_data['search-results']['entry']:
    print(entry['dc:title'])


"""
Ejemplo de respuesta.

'search-results': {'opensearch:totalResults': '12658', 
                   'opensearch:startIndex': '0', 
                   'opensearch:itemsPerPage': '25', 
                   'opensearch:Query': {'@role': 'request', '@searchTerms': 'scrum', '@startPage': '0'}, 
                   'link': [{'@_fa': 'true', '@ref': 'self', '
                                 @href': 'https://api.elsevier.com/content/search/scopus?start=0&count=25&query=scrum&apiKey=1ff1345f7b2e66316522ec31ab816511', 
                                 '@type': 'application/json'}, 
                                {'@_fa': 'true', '@ref': 'first', '@href': 'https://api.elsevier.com/content/search/scopus?start=0&count=25&query=scrum&apiKey=1ff1345f7b2e66316522ec31ab816511', '@type': 'application/json'}, 
                                {'@_fa': 'true', '@ref': 'next', '@href': 'https://api.elsevier.com/content/search/scopus?start=25&count=25&query=scrum&apiKey=1ff1345f7b2e66316522ec31ab816511', '@type': 'application/json'}, 
                                {'@_fa': 'true', '@ref': 'last', '@href': 'https://api.elsevier.com/content/search/scopus?start=4975&count=25&query=scrum&apiKey=1ff1345f7b2e66316522ec31ab816511', '@type': 'application/json'}
                                ], 
                    'entry': [{'@_fa': 'true', 'link': [{'@_fa': 'true', '@ref': 'self', '@href': 'https://api.elsevier.com/content/abstract/scopus_id/85115445759'}, 
                                                           {'@_fa': 'true', '@ref': 'author-affiliation', '@href': 'https://api.elsevier.com/content/abstract/scopus_id/85115445759?field=author,affiliation'}, 
                                                           {'@_fa': 'true', '@ref': 'scopus', '@href': 'https://www.scopus.com/inward/record.uri?partnerID=HzOxMe3b&scp=85115445759&origin=inward'}, 
                                                           {'@_fa': 'true', '@ref': 'scopus-citedby', '@href': 'https://www.scopus.com/inward/citedby.uri?partnerID=HzOxMe3b&scp=85115445759&origin=inward'}],
                                  prism:url': 'https://api.elsevier.com/content/abstract/scopus_id/85115445759', 
                                  'dc:identifier': 'SCOPUS_ID:85115445759',
                                  'eid': '2-s2.0-85115445759', 
                                  'dc:title': 'A Comprehensive Review and a Taxonomy Proposal of Team Formation Problems',
                                  'dc:creator': 'Juárez J.', 
                                  'prism:publicationName': 'ACM Computing Surveys', 
                                  'prism:issn': '03600300', 'prism:eIssn': '15577341', '
                                  prism:volume': '54', 'prism:issueIdentifier': '7', 
                                  'prism:pageRange': None, 'prism:coverDate': '2022-09-01', 
                                  'prism:coverDisplayDate': 'September 2022', 'prism:doi': '10.1145/3465399', 
                                  'citedby-count': '0', 
                                  'affiliation': [{'@_fa': 'true', 'affilname': 'Centro de Investigacion Cientifica y de Educacion Superior de Ensenada', 'affiliation-city': 'Ensenada', 'affiliation-country': 'Mexico'}], 
                                  'prism:aggregationType': 'Journal', 'subtype': 're', 'subtypeDescription': 'Review', 'article-number': '153', 
                                  'source-id': '23038', 'openaccess': '0', 'openaccessFlag': False}, 
                                 {'@_fa': 'true', 'link': [{'@_fa': 'true', '@ref': 'self', '@href': 'https://api.elsevier.com/content/abstract/scopus_id/85120696494'}, 
                                                           {'@_fa': 'true', '@ref': 'author-affiliation', '@href': 'https://api.elsevier.com/content/abstract/scopus_id/85120696494?field=author,affiliation'}, 
                                                           {'@_fa': 'true', '@ref': 'scopus', '@href': 'https://www.scopus.com/inward/record.uri?partnerID=HzOxMe3b&scp=85120696494&origin=inward'}, 
                                                           {'@_fa': 'true', '@ref': 'scopu
"""


"""

Un entry completo:
    
{'@_fa': 'true', 'link': [{'@_fa': 'true', '@ref': 'self', '@href': 'https://api.elsevier.com/content/abstract/scopus_id/85115445759'}, 
                          {'@_fa': 'true', '@ref': 'author-affiliation', '@href': 'https://api.elsevier.com/content/abstract/scopus_id/85115445759?field=author,affiliation'}, 
                          {'@_fa': 'true', '@ref': 'scopus', '@href': 'https://www.scopus.com/inward/record.uri?partnerID=HzOxMe3b&scp=85115445759&origin=inward'}, 
                          {'@_fa': 'true', '@ref': 'scopus-citedby', '@href': 'https://www.scopus.com/inward/citedby.uri?partnerID=HzOxMe3b&scp=85115445759&origin=inward'}], 
 'prism:url': 'https://api.elsevier.com/content/abstract/scopus_id/85115445759', 
 'dc:identifier': 'SCOPUS_ID:85115445759', 'eid': '2-s2.0-85115445759', 
 'dc:title': 'A Comprehensive Review and a Taxonomy Proposal of Team Formation Problems', 'dc:creator': 'Juárez J.', 
 'prism:publicationName': 'ACM Computing Surveys', 'prism:issn': '03600300', 'prism:eIssn': '15577341', 'prism:volume': '54', 
 'prism:issueIdentifier': '7', 'prism:pageRange': None, 'prism:coverDate': '2022-09-01', 'prism:coverDisplayDate': 'September 2022', 
 'prism:doi': '10.1145/3465399', 'citedby-count': '0', 
 'affiliation': [{'@_fa': 'true', 'affilname': 'Centro de Investigacion Cientifica y de Educacion Superior de Ensenada', 'affiliation-city': 'Ensenada', 'affiliation-country': 'Mexico'}], 
 'prism:aggregationType': 'Journal', 'subtype': 're', 'subtypeDescription': 'Review', 'article-number': '153', 'source-id': '23038', 'openaccess': '0', 
 'openaccessFlag': False}
    
"""

print("Recuperar el abstract")
#https://api.elsevier.com/content/abstract/scopus_id/{scopus_id}
abstract_url = paper['prism:url']
r = requests.get(abstract_url, headers = xml_headers)
print(r.text)

"""
Abstract

{'abstracts-retrieval-response': {
    'affiliation': [{'affiliation-city': 'Ensenada', 'affilname': 'Centro de Investigacion Cientifica y de Educacion Superior de Ensenada', 'affiliation-country': 'Mexico'}, 
                    {'affiliation-city': 'Beaverton', 'affilname': 'Gurobi Optimization', 'affiliation-country': 'United States'}], 
    'coredata': {'srctype': 'j', 'prism:issueIdentifier': '7', 'eid': '2-s2.0-85115445759', 'prism:coverDate': '2022-09-01', 'prism:aggregationType': 'Journal', 'prism:url': 'https://api.elsevier.com/content/abstract/scopus_id/85115445759', 'subtypeDescription': 'Review', 
                 'dc:creator': {'author': [{'ce:given-name': 'Julio', 'preferred-name': {'ce:given-name': 'Julio', 'ce:initials': 'J.', 'ce:surname': 'Juárez', 'ce:indexed-name': 'Juárez J.'}, '@seq': '1', 'ce:initials': 'J.', '@_fa': 'true', 'affiliation': {'@id': '60032563', '@href': 'https://api.elsevier.com/content/affiliation/affiliation_id/60032563'}, 'ce:surname': 'Juárez', '@auid': '56504878800', 'author-url': 'https://api.elsevier.com/content/author/author_id/56504878800', 'ce:indexed-name': 'Juarez J.'}]}, 'link': [{'@_fa': 'true', '@rel': 'self', '@href': 'https://api.elsevier.com/content/abstract/scopus_id/85115445759'}, {'@_fa': 'true', '@rel': 'scopus', '@href': 'https://www.scopus.com/inward/record.uri?partnerID=HzOxMe3b&scp=85115445759&origin=inward'}, {'@_fa': 'true', '@rel': 'scopus-citedby', '@href': 'https://www.scopus.com/inward/citedby.uri?partnerID=HzOxMe3b&scp=85115445759&origin=inward'}], 
                 'prism:publicationName': 'ACM Computing Surveys', 'source-id': '23038', 'citedby-count': '0', 'prism:volume': '54', 'subtype': 're', 'dc:title': 'A Comprehensive Review and a Taxonomy Proposal of Team Formation Problems', 'openaccess': '0', 'openaccessFlag': 'false', 'prism:doi': '10.1145/3465399', 'prism:issn': '15577341 03600300', 'article-number': '153', 'dc:identifier': 'SCOPUS_ID:85115445759', 'dc:publisher': 'Association for Computing Machinery'}}}
"""

print("Recuperar el abstract vía HTML")# no funciona porque no he hecho login
#2-s2.0-85115445759&origin=inward&txGid=d9dc2629ed665381429d3098f1f5b7fe
# https://www.scopus.com/inward/record.uri?partnerID=HzOxMe3b&scp=85115445759&origin=inward <-- No me ha funcionado
# https://www.scopus.com/record/display.uri?eid=2-s2.0-85115445759&origin=inward&txGid=b11226e3d3dcf46ab746aa15c2fc4505
#abstract_url = paper['link'][2]['@href']
#abstract_url = "https://www.scopus.com/record/display.uri?eid=" + paper['eid'] + '&origin=inward'
abstract_url = "https://www.scopus.com/record/display.uri?eid=2-s2.0-85115445759&origin=inward"
# Me redirige a una página en la que me pide hacer el login
#abstract_url = "https://www.sciencedirect.com/science/article/pii/S0014579301033130"
# https://www.sciencedirect.com/science/article/pii/S096599782100106X

# Con este enlace me aperece el abstract en la siguiente tiqueta (con metadata de formato): <script type="application/json" data-iso-key="_0">
cookies = {
   'scopus.machineID':'EB311B9CAC627FA31AB1AB0DDA7C30D0.i-0bbbb402331aa2a10',
   'SCOPUS_JWT':'eyJraWQiOiJjYTUwODRlNi03M2Y5LTQ0NTUtOWI3Zi1kMjk1M2VkMmRiYmMiLCJhbGciOiJSUzI1NiJ9.eyJhbmFseXRpY3NfaW5mbyI6eyJhY2NvdW50SWQiOiIyNzg2NDEiLCJ1c2VySWQiOiJhZToxMzM0MTI1MyIsImFjY2Vzc1R5cGUiOiJhZTpBTk9OOjpHVUVTVDoiLCJhY2NvdW50TmFtZSI6IlNjb3B1cyBQcmV2aWV3In0sInN1YiI6IjEzMzQxMjUzIiwiaW5zdF9hY2N0X25hbWUiOiJTY29wdXMgUHJldmlldyIsInN1YnNjcmliZXIiOmZhbHNlLCJkZXBhcnRtZW50SWQiOiIyODk4MzkiLCJpc3MiOiJTY29wdXMiLCJpbnN0X2FjY3RfaWQiOiIyNzg2NDEiLCJpbnN0X2Fzc29jX21ldGhvZCI6IiIsInBhdGhfY2hvaWNlIjpmYWxzZSwiYXVkIjoiU2NvcHVzIiwibmJmIjoxNjQwMTc1OTcwLCJmZW5jZXMiOltdLCJpbmR2X2lkZW50aXR5X21ldGhvZCI6IiIsImluc3RfYXNzb2MiOiJHVUVTVCIsImluZHZfaWRlbnRpdHkiOiJBTk9OIiwiZXhwIjoxNjQwMTc2ODY5LCJhdXRoX3Rva2VuIjoiMzZjYmQ4ZTcyYWY4Yjk0NDM1ODljMTc1ZmE1MzYxNzljZDQ5Z3hycWIiLCJpYXQiOjE2NDAxNzU5NzB9.q2eXeUR1uejjf0Z79TFOLjbxe9Qp0rupsvJZBdb6Lo0XzNkylhubcJNiA1LL5Vbqaq7LRgGzO2N60rFsu2HtIwN1STlOiJLrh0ipi1R-7OErmplSPZF6CMFOoS_DEcKpFMRoQwVeuFptdGqxX018u9g51uxpOCXB8hgzcKfe7IVBPvSIJUpPw6v9VR4GI41VUWdzp2XA6NXWd8Aosmfl8iAtK6W9k1bXTcXbYxNqXKnR4BPVQxQfBSaz9tKtnuMS4KzQi1SmgLjA1spuSd3D-IGOt9oH0txzyEGBAJedExKfuYosI3a1SAcEkumTWBSAJZHjUokMfDbEnhMP1v0zSw',
   '':'',
   '':'',
   '':''
    }
print(abstract_url)
s = requests.Session()
s.max_redirects = 100
r = s.get(abstract_url, headers = xml_headers) # , cookies = cookies
#print(r.cookies)
#print(r.headers)
#print(r.text)
save_tmp(r.text)


"""
from elsapy.elsclient import ElsClient
from elsapy.elsprofile import ElsAuthor, ElsAffil
from elsapy.elsdoc import FullDoc, AbsDoc
from elsapy.elssearch import ElsSearch

elsapy utiliza URLs antiguas que ya no funcionan.

myCl = ElsClient(my_key)

myDocSrch = ElsSearch('star+trek+vs+star+wars','scopus')
print(myDocSrch.uri)

result = myDocSrch.execute(myCl, False)
print(result)


myDocSrch = ElsSearch('star+trek+vs+star+wars','scidir') # con este parámetro da error
# HTTPError: HTTP 410 Error from https://api.elsevier.com/content/search/scidir?query=star%2Btrek%2Bvs%2Bstar%2Bwars
# and using headers {'X-ELS-APIKey': '1ff1345f7b2e66316522ec31ab816511', 'User-Agent': 'elsapy-v0.5.0', 'Accept': 'application/json'}:
   

myDocSrch = ElsSearch('scrum','scidir') 
print(myDocSrch.query)
result = myDocSrch.execute(myCl, False)
print(result)

"""

print("Done.")
