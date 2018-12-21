import threading 
from datetime import datetime 
import queue,csv
from bs4 import BeautifulSoup
import requests,os
requests.packages.urllib3.disable_warnings()

now = datetime.now()
year = str(now.year)
month = str(now.month)
day = str(now.day)
hour = str(now.hour)
minute = str(now.minute)
second = str(now.second)

Q = queue.Queue()

filename = year+'-'+month+'-'+day+'-'+hour+'-'+minute+'-'+second+'.csv'
   
if not os.path.exists(filename):
    with open(filename,'w')as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Title", "Link"])

def worker():
    '''
    rtype list
    '''
    links = []
    url = "https://salttiger.com/archives/"
    r = requests.get(url,verify=False)
    if r.status_code == 200:
        html = r.text
        soup = BeautifulSoup(html,"html.parser")
        uls = soup.find_all('ul',class_="car-monthlisting")
        for ul in uls:
            links += ul.find_all('a')
    else:
        print("[-]Error. The status code is {}".format(r.status_code))
    
    for link in links:
        Q.put(link['href'])
    

def fetch_result(url):
    hrefs = []
    r = requests.get(url,verify=False)
    html = r.text
    soup = BeautifulSoup(html,"html.parser")
    title = soup.find('h1','entry-title')
    div = soup.find('div',class_='entry-content')
    links = div.find_all('a')[1:]
    for link in links:
        hrefs.append(link['href'])

    return title.get_text(),hrefs

def write_to_csv(title,links):
    with open(filename,'a')as csvfile:
        writer = csv.writer(csvfile)
        links.insert(0,title)
        writer.writerow(links)

def producer(i):
    while not Q.empty():
        link = Q.get()
        title,links = fetch_result(link)
        print("[-] 线程 {} 获取《{}》 的下载地址 - {}".format(i,title,datetime.now()))
        write_to_csv(title,links)
    Q.all_tasks_done




if __name__ =="__main__":
    # links = worker()
    # for link in links:
    #     print(link['href'])
    title,links = fetch_result('https://salttiger.com/learning-swift-3rd-edition/')
    print("title: {} and links is {}".format(title,links))
    # title,links = fetch_result('https://salttiger.com/galaxy-s-ii-the-missing-manual/')
    # print("title: {} and links is {}".format(title,links))
    write_to_csv(title,links)
    # start = datetime.now()
    # worker()
    # thrades = [threading.Thread(target=producer,args=(i,)) for i in range(50)]
    # for t in thrades:
    #     t.start()

    # for t in thrades:
    #     t.join()
    # end = datetime.now()

    # print("[-] 耗时 {} s".format(end - start))

