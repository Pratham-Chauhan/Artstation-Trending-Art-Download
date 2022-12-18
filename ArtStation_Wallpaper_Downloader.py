#from selenium import webdriver
from bs4 import BeautifulSoup
##from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import random
import os
import json
import ctypes
import requests as r
#import undetected_chromedriver as uc

# option = webdriver.ChromeOptions()
# option.add_argument('--headless')
# d = uc.Chrome(options=option)
##d.get('https://www.artstation.com/sitemap.xml')


##d = webdriver.Chrome(ChromeDriverManager().install())
##d.get('https://www.artstation.com/sitemap.xml')


# In[47]:

def Download_All_Artists_Name():
    total_n = 703
    # Download Artstation Artists
    for n in range(1, total_n+1)[2:3]:
        print(n, end=', ')
    #     sleep(random.random())
        url = 'https://www.artstation.com/sitemap-artists-%s.xml'%n
        d.get(url)
        
        soup = BeautifulSoup(d.page_source, 'lxml')
        with open('./art/artstation-artists-%s.xml'%n,'w', encoding='utf-8') as f:
            links = soup.find_all('loc')
            print(len(links))
            links = [l.text.split('/')[-1] for l in links]
            f.write('\n'.join(links))

        merge_to_single_txt()

def merge_to_single_txt():
    all_artists = []
    for i in range(1, total_n+1)[:]:
        with open('./art/artstation-artists-%s.xml'%i, 'r') as o:
            all_artists.extend(o.read().split('\n'))
            
    # Save all Artist to Single File
    with open('./art/All_Artstation_Artists_Username.txt','w', encoding='utf-8') as k:
        k.write('\n'.join(all_artists))

tdata = []
def Trending_Art_Download():
    global refresh, tdata
    if refresh:
        print("Refreshing...")
        trend_url = "https://www.artstation.com/api/v2/community/explore/projects/trending.json?page=%s&dimension=all&per_page=100"%(random.randint(1, 50))
        tdata = r.get(trend_url).json()['data']

    rn = random.randint(1, 100)
    artwork = tdata[rn]

    art_hash = artwork['hash_id']
    print(artwork['user']['username'],'-', artwork['title'])
    print('Hash:',art_hash) 

    refresh = 0
    download_art(art_hash)
    

def Find_Art_Hash():
    # Finding Random Art to Download
    with open('./art/All_Artstation_Artists_Username.txt','r', encoding='utf-8') as ll:
        arts = ll.read().split('\n')   

    rn = random.randint(0, len(arts))
    artist = arts[rn]
    artist_url = "https://www.artstation.com/users/%s/projects.json"%(artist)
    print('Artist:', artist, artist_url )
    x1 = r.get(artist_url)

    images = x1.json()['data']
    if images:
        rn_art = random.choice(images)
    else: 
        print( 'No Art Found for this artist!')
        return
    
    art_hash = rn_art['hash_id']
    print('Title:',rn_art['title'], art_hash)

    download_art(art_hash)
 
 
def download_art(art_hash):
    art_url ="https://www.artstation.com/projects/%s.json"%art_hash
    x2 = r.get(art_url)

    jjson = x2.json()
    img_title = jjson['title']

    img_url = jjson['assets']
    i_urls = []
    for each in img_url:
    #     print(each['has_embedded_player'])
        if each['asset_type'] == "image":
            if each['width'] >= each['height']:
                print('{w}x{h}'.format(w=each['width'], h=each['height']))
                i_urls.append(each['image_url'])
    if not i_urls: return
    c = input('> ')
    if c: c = int(c)-1
    else: return
    
    dl_img_url = i_urls[c]
            

    # confirm = input('Want to Downlaod Art?')
    # if confirm in ['n', 'N']: return
   
    img_name = 'aa.jpg' #rn_art['title']+'.jpg' 

    x = r.get(dl_img_url)
    if x.status_code == 200:
        with open('./art/'+img_name,'wb') as img_dl:
            img_dl.write(x.content)

        set_wallpaper(img_name)

        if input('Save it? ').lower() == 'y':
            with open(f'./{img_title}.jpg','wb') as img_dl:
                img_dl.write(x.content)

        
    else: print('Unable to Download Art!')
    
    

def set_wallpaper(img_name):
    abs_path_img = r"C:\Users\Pratham\Pictures\Artstation\art\%s"%img_name
    ctypes.windll.user32.SystemParametersInfoW(20, 0, abs_path_img, 0)


# Find_Art_Hash()
refresh = 1
while True:
    #y = input('Refresh?')
    #if y == 'q': break
    print()
    Trending_Art_Download()
    
