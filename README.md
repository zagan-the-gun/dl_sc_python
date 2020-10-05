# dl_sc_python

## 初期セットアップ
```
$ python3.7 -m venv venv3.7
$ source venv3.7/bin/activate
$ pip install -r requirements.txt
```
## ダウンロードディレクトリの用意
```
$ mkdir likes
```

### htmlから自動ダウンロードする場合
https://soundcloud.com/[他人または自分のユーザ名]/likes
ページを開き htmlソースをコピー
一番下までスクロールしてからコピーしよう

指定のファイル名でhtmlを保存する
```
$ vi like_list.html
```

プログラムファイルを書き換える
コメントアウトだけで無く、手間だけどコードの上下も切り替える
```
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
```


### URLリストから自動ダウンロードする場合
指定のファイル名でURLのリストを作る

```
$ vi likelinks.txt
```

プログラムファイルを書き換える
コメントアウトだけで無く、手間だけどコードの上下も切り替える
```
"""
#htmlの時はコレ使う
fname = 'like_list.html'
like_list_html = BeautifulSoup(open(fname), 'html.parser')
all_count = len(like_list_html.find_all('li', class_='soundList__item'))
for like in like_list_html.find_all('li', class_='soundList__item'):
    track = like.find('a', class_='sound__coverArt').get('href')
"""

#ファイルリストの時はコレ使う
fname = 'likelinks.txt'
with open(fname) as f:
    content = f.readlines()
all_count = len(content)
for track in content:
```
