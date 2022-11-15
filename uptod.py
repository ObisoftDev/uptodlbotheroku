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
            img = item.find('img')['src']
            searchList.append({'name':name,'url':url,'img':img})
        except:pass

    return searchList

def req_file_size(req):
    try:
        return int(req.headers['content-length'])
    except:
        return 0

def getInfo(item):
    try:
        downUrl = item['url'] + '/descargar'

        session = requests.Session()

        resp = session.get(downUrl)
        html = str(resp.text)
        soup = BeautifulSoup(html, "html.parser")
        try:
            directUrl = soup.find('a',{'id':'detail-download-button'})['href']
        except:
            directUrl = soup.find('button',{'id':'detail-download-button'})['data-url']
        divInfo = soup.find('div',{'class':'notice'})
        text = ''
        imgs = divInfo.find_all('img')
        for img in imgs:
            try:
                text += img.next
            except:pass
        return {'url':directUrl,'text':text,'name':item['name'] + ' Url'}
    except:pass
    return None

#list = search('naruto')
#info = getInfo(list[0])
#print(list)
