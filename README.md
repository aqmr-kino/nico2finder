# nico2finder

## 概要
ニコニコ動画コンテンツ検索APIv2( https://site.nicovideo.jp/search-api-docs/search.html )を利用して動画の検索を行うことができるPythonのライブラリです。

## 使用方法
```python
from nico2finder import finder

nvf = finder.NicoVideoFinder()

# "きりたん"で検索
result = nvf.find_video('きりたん')

for v in result['data']:
  print(v['title'], v['contentId'])

# "ミク"で1000再生以上の動画を検索(コメントの新しい順に50件)
result = nvf.find_video(
  query='ミク',
  filters=finder.SearchFilter(least_views=1000),
  sort=finder.Sort.RecentCommented,
  limit=50
)

for v in result['data']:
  print(v['title'], v['contentId'])
```

## 動画検索 (NicoVideoFinder オブジェクト)

### 動画検索
#### NicoVideoFinder.**find_video(*query, targets='title', filters=None, sort=Sort.Latest, limit=10*)**
*query*をキーワードとして動画を検索します。*targets*には**title**(タイトル検索), **description**(説明文検索), もしくは**tags**(タグ検索)が指定可能です。  
*filters*には**SearchFilter**オブジェクトを指定することで、検索結果を条件でフィルタすることが可能です。  
*sort*には**Sort**オブジェクトを指定することで検索結果の並び替え順を指定可能です。  

戻り値は下記形式の辞書(dictionary)オブジェクトです。  

|キー|型|内容|
|:--|:--|:--|
|meta|dictionary|リクエスト結果概要|
|data|list[dictionary]|検索結果|

### 検索結果設定
#### NicoVideoFinder.**set_response_fields(*\*\*options*)**  
検索結果として取得可能なフィールドは**NicoVideoFinder**インスタンスの**set_respose_fields**メソッドで指定可能です。  
デフォルト値は、`contentId`, `title`, `viewCounter`, `mylistCounter`, `commentCounter`, `startTime`です。  

*\*\*options*には引数として指定可能なパラメータとデフォルト値は下記の通りです。  

|設定名|説明|デフォルト値|
|:--|:--|:--|
|contentId      | コンテンツID | True |
|title          | タイトル | True |
|description    | コンテンツの説明文 | False |
|userId         | 投稿者のユーザID | False |
|viewCounter    | 再生数 | True |
|mylistCounter  | マイリスト数 | True |
|lengthSeconds  | 再生時間(秒) | False |
|thumbnailUrl   | サムネイルのURL | False |
|startTime      | 動画の投稿時間 | True |
|threadId       | スレッドのID | False |
|commentCounter | コメント数 | True |
|lastCommentTime| 最終コメント時間 | False |
|categoryTags   | カテゴリタグ | False |
|channelId      | チャンネルID | False |
|tags           | タグ(空白区切り) | False |
|tagsExact      | タグ完全一致(空白区切り) | False |
|genre          | ジャンル | False |
|genre.keyword  | ジャンル完全一致 | False |

```python
nvf = finder.NicoVideoFinder()

# description, lengthSeconds, startTime を有効化する場合
nvf.set_response_fields(
  description=True,
  lengthSeconds=True,
  startTime=True
)
```

## 検索フィルタ (SearchFilter オブジェクト)

検索の条件を指定するオブジェクトです。
投稿時間関連の時間はISO8601形式文字列(*yyyy-mm-dd*T*HH:MM:SS*+09:00)、それ以外は整数値で指定可能です。 

|属性名|型|説明|
|:--|:--|:--|
|user_id        | int | 投稿者ID |
|least_views    | int | 最少再生回数 |
|most_views     | int | 最大再生回数 |
|least_comments | int | 最少コメント数 |
|most_comments  | int | 最大コメント数 |
|least_mylists  | int | 最少マイリスト数 |
|most_mylists   | int | 最大マイリスト数 |
|shortest_length| int | 最短再生時間(秒) |
|longest_length | int | 最長再生時間(秒) |
|posted_after   | str (ISO8601) | 投稿日時(〜より新しい) |
|posted_before  | str (ISO8601) | 投稿日時(〜より古い) |
|tag            | str, tuple(str), list(str) | タグ絞りこみ(複数指定可) |
|genre          | str, tuple(str), list(str) | ジャンル絞り込み(複数指定可) |

```python
# 1,000回以上再生されている動画
SearchFilter(least_views=1000)

# 1,000,000回以上再生されている1分以下の動画
SearchFilter(least_views=1000000, longest_length=60)

# 2015年以前に投稿された10,000マイリス以上の動画
SearchFilter(least_mylists=10000, posted_before='2015-12-31T23:59:59+09:00')
```

## 検索ソート (Sort オブジェクト)
検索結果の並び替え順を指定します。下記の定数の中から任意の１つを選択可能です。

|定数名|説明|
|:--|:--|
|Oldest          | 投稿日時の古い順|
|Latest          | 投稿日時の新しい順|
|LeastCommented  | コメント数の少ない順|
|MostCommented   | コメント数の多い順|
|LeastPlayed     | 再生回数の少ない順|
|MostPlayed      | 再生回数の多い順|
|Shortest        | 再生時間の短い順|
|Longest         | 再生時間の長い順|
|RecentCommented | コメントの新しい順|
