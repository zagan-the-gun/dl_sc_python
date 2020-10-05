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
    try:
        track = track.split('\n')[0]
        print(track)
        print('Track #{} / {}'.format(count, all_count))

        soup = BeautifulSoup(requests.get(track).text, 'lxml')
        img_url = soup.find('img', itemprop='image').get('src')
        print(img_url)
        r = requests.get(base + track, timeout=None)
        if r.status_code == 200:
            resp = json.loads(r.content)
            cdn = resp['recorded']
            filename = track.split('/')[-1] + '.mp3'
            file_path = path+filename
            r = requests.get(cdn)
            if r.status_code == 200:
                with open(file_path, 'wb') as fd:
                    for chunk in r.iter_content(chunk_size):
                        fd.write(chunk)
            else:
                print('Error 2:- Track #{} Failed !'.format(count))

            try:
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

