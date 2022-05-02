import requests
from requests import Session
from bs4 import BeautifulSoup


PATH = 'https://www.uptodown.com/'
SEARCH = 'buscar'


def search(name='',tag='windows'):
    global PATH

    searchUrl = PATH + tag + '/' + SEARCH
    payload = {'singlebutton':'','q':name}
    resp = requests.post(searchUrl,data=payload)
    html = str(resp.text)
    soup = BeautifulSoup(html, "html.parser")
    items = soup.find_all('div',{'class':'item'})
    searchList = []

    for item in items:
        try:
            divname = item.find('div',{'class':'name'}).find('a')
            name = divname.next
            url =  divname['href']
            img = item.find('figure').find('img')['data-src']
            searchList.append({'name':name,'url':url,'img':img})
        except:pass

    return searchList

def req_file_size(req):
    try:
        return int(req.headers['content-length'])
    except:
        return 0

def getInfo(item):
    downUrl = item['url'] + '/descargar'

    session = requests.Session()

    resp = session.get(downUrl)
    html = str(resp.text)
    soup = BeautifulSoup(html, "html.parser")
    directUrl = soup.find('a',{'id':'detail-download-button'})['href']
    divInfo = soup.find('div',{'class':'notice'})
    text = divInfo.find_all('img')[0].next
    return {'url':directUrl,'text':text,'name':item['name'] + ' Url'}

#list = search('nod32')
#print(list)