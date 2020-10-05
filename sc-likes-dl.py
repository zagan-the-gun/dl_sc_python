# -*- coding: utf-8 -*-

import urllib
import requests
import json
from bs4 import BeautifulSoup
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, error



base = 'http://streampocket.com/json2?stream='
chunk_size = 1024 * 1024
path = './likes/'
count = 0



#ファイルリストの時はコレ使う
"""
fname = 'likelinks.txt'
with open(fname) as f:
    content = f.readlines()
all_count = len(content)
for track in content:
"""

#htmlの時はコレ使う
fname = 'like_list.html'
like_list_html = BeautifulSoup(open(fname), 'html.parser')
all_count = len(like_list_html.find_all('li', class_='soundList__item'))
for like in like_list_html.find_all('li', class_='soundList__item'):
    track = like.find('a', class_='sound__coverArt').get('href')

    count += 1
    #print('{} / {}'.format(count, all_count))
    try:
        #track = track.split('\r\n')[0]
        track = track.split('\n')[0]
        #track = track.rstrip('\n')
        #sound = urllib.quote_plus(track)
#        print('Making first request')
        #print(base+ urllib.parse.quote(track))
#        print(base+track)
        print(track)
        print('Track #{} / {}'.format(count, all_count))

        #print(requests.get(track).text)
        soup = BeautifulSoup(requests.get(track).text, 'lxml')
        #style = soup.find('div', class_='productPreview').find('span').get('style')
        #style = soup.find('div', class_='interactive').get('style')
        #style = soup.find('div', class_='interactive')
#        print(soup)
        img_url = soup.find('img', itemprop='image').get('src')
#        sc-artwork sc-artwork-placeholder-1  image__full g-opacity-transition
        print(img_url)
        #DL要らない
        #with urllib.request.urlopen(img_url) as web_file:
        #    data = web_file.read()
        #    with open(path + 'tmp.jpg', mode='wb') as local_file:
        #        local_file.write(data)
        r = requests.get(base + track, timeout=None)
        #r = requests.get('https://dev-common.maskapp.club/test/', timeout=30)
#        print('DEBUG DEBUG DEBUG : 0')
        if r.status_code == 200:
#            print(r.url)
#            print(r.text)
#            print(r.content)
            resp = json.loads(r.content)
            #resp = json.loads(r.text)
#            print('DEBUG DEBUG DEBUG : 0.1')
            cdn = resp['recorded']
#            print('cdn')
#            print(cdn)
#            print('DEBUG DEBUG DEBUG : 0.2')
            filename = track.split('/')[-1] + '.mp3'
#            print ('Name of track = ' + filename)
#            print ('Making second request')
            file_path = path+filename
#            print('file_path')
#            print(file_path)
            r = requests.get(cdn)
#            print('DEBUG DEBUG DEBUG : 1')
            if r.status_code == 200:
#                print('DEBUG DEBUG DEBUG : 1.1')
                #print(r.content)
                #print(r.text)
                with open(file_path, 'wb') as fd:
#                    print('DEBUG DEBUG DEBUG : 1.2')
                    for chunk in r.iter_content(chunk_size):
#                        print('DEBUG DEBUG DEBUG : 1.3')
                        fd.write(chunk)
            else:
                print('Error 2:- Track #{} Failed !'.format(count))
#            print('DEBUG DEBUG DEBUG : 2')

            try:
#                print(path + filename)
                audio = MP3(path + filename, ID3=ID3)
                if audio.tags is None:
                    audio.add_tags()

                audio.tags.add(
                  APIC(
                    encoding=3, # 3 is for utf-8
                    mime='image/jpeg', # image/jpeg or image/png
                    type=3, # 3 is for the cover image
                    desc=u'Cover',
                    data=requests.get(
                                       img_url,
                                       stream=True,
                                     ).raw.read()
                  )
                )
                audio.save()

            except Exception as e:
                print(e)

        else:
            print('Error 2:- Track #{} Failed !'.format(count))

    except Exception as e:
        print('Error')
        pass

    print('')
    print('')

