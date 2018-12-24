# coding: utf-8 
import os 
from datetime import datetime 
from queue import Queue
from threading import Thread
import requests
requests.packages.urllib3.disable_warnings()

from bs4 import BeautifulSoup
import re

if not os.path.exists('img'):
    os.mkdir('img')


Q = Queue()

def producer(pages):
    for page in range(1,pages+1):
        print("[-] 收集第 {} 页".format(str(page)))
        url = "http://simpledesktops.com/browse/"+str(page)+"/"
        r = requests.get(url,verify=False)
        html = r.text
        soup = BeautifulSoup(html,'html.parser')
        try:
            imgs = soup.find_all('img')
            for img in imgs:
                img_url = img['src']
                Q.put(img_url)
        except:
            pass

def worker(i):
    while not Q.empty():
        img_url = Q.get()
        text = re.search('(http://static.simpledesktops.com/uploads/desktops/\d+/\d+/\d+/(.*?png)).*?png',img_url)
        new_img_url = text.group(1)

        r = requests.get(new_img_url,verify=False)
        path = "img/"+text.group(2)
        print("[-] 线程 {} 开始下载 {} 开始时间：{}".format(i,text.group(2),datetime.now()))

        with open(path,'wb') as f:
            f.write(r.content)
    
    Q.all_tasks_done


if __name__ =="__main__":
    # text = "http://static.simpledesktops.com/uploads/desktops/2015/09/25/Siri.png.295x184_q100.png"
    # i = re.search('(http://static.simpledesktops.com/uploads/desktops/\d+/\d+/\d+/(.*?png)).*?png',text)
    # print(i.group(1))
    # print(i.group(2))
    producer(50)

    ts = [Thread(target=worker,args=(i,)) for i in range(50)]
    for t in ts:
        t.start()

    for t in ts:
        t.join()