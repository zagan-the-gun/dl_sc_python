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

### URLリストから自動ダウンロードする場合
指定のファイル名でURLのリストを作る

```
$ vi likelinks.txt
```
