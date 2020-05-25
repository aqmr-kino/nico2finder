# coding: utf-8
"""ニコニコ動画上の動画や生放送を検索します
"""
import json
import urllib.request

API_DOMAIN = 'https://api.search.nicovideo.jp'

API_ENDPOINTS = {
    'search': '/api/v2/video',
    'search-video': '/api/v2/video',
    'search-live': '/api/v2/live',
}

class Sort():
    """検索結果ソート順オプション

    Oldest          : 投稿日時の古い順
    Latest          : 投稿日時の新しい順
    LeastCommented  : コメント数の少ない順
    MostCommented   : コメント数の多い順
    LeastPlayed     : 再生回数の少ない順
    MostPlayed      : 再生回数の多い順
    Shortest        : 再生時間の短い順
    Longest         : 再生時間の長い順
    RecentCommented : コメントの新しい順
    """
    Oldest = '+startTime'
    Latest = '-startTime'
    LeastCommented = '+commentCounter'
    MostCommented = '-commentCounter'
    LeastPlayed = '+viewCounter'
    MostPlayed = '-viewCounter'
    Shortest = '+lengthSeconds'
    Longest = '-lengthSeconds'
    RecentCommented = '-lastCommentTime'

class SearchFilter():
    """検索フィルタ
    絞り込み検索条件設定
    """
    def __init__(self, user_id=None,
                 least_views=None, most_views=None,
                 least_comments=None, most_comments=None,
                 least_mylists=None, most_mylists=None,
                 shortest_length=None, longest_length=None,
                 posted_after=None, posted_before=None,
                 tag=None, genre=None):
        """
        user_id        : 投稿者ID
        least_views    : 最少再生回数
        most_views     : 最大再生回数
        least_comments : 最少コメント数
        most_comments  : 最大コメント数
        least_mylists  : 最少マイリスト数
        most_mylists   : 最大マイリスト数
        shortest_length: 最短再生時間
        longest_length : 最長再生時間
        posted_after   : 投稿日時(〜より新しい)
        posted_before  : 投稿日時(〜より古い)
        tag            : タグ絞りこみ
        genre          : ジャンル絞り込み
        """
        self.filters = {}

        self.__set_attr("[userId][0]", user_id)
        self.__set_attr("[viewCounter][gte]", least_views)
        self.__set_attr("[viewCounter][lte]", most_views)
        self.__set_attr("[commentCounter][gte]", least_comments)
        self.__set_attr("[commentCounter][lte]", most_comments)
        self.__set_attr("[mylistCounter][gte]", least_mylists)
        self.__set_attr("[mylistCounter][lte]", most_mylists)
        self.__set_attr("[lengthSeconds][gte]", shortest_length)
        self.__set_attr("[lengthSeconds][lte]", longest_length)
        self.__set_attr("[startTime][gte]", posted_after)
        self.__set_attr("[startTime][lte]", posted_before)
        self.__set_attr_multiple("[tags][%d]", tag)
        self.__set_attr_multiple("[genre][%d]", genre)

    def __set_attr(self, key, value):
        if value is not None:
            self.filters["filters" + key] = value

    def __set_attr_multiple(self, key, value):
        if value is not None:
            if type(value) in (tuple, list):
                for i, v in enumerate(value):
                    self.__set_attr(key % (i,), v)
            else:
                self.__set_attr(key % (0,), value)

    def get_query(self):
        return self.filters

class NicoVideoFinder():
    """動画検索
    """
    def __init__(self, app_name=None):
        self.response_fields = {
            'contentId': True,
            'title': True,
            'description': False,
            'userId': False,
            'viewCounter': True,
            'mylistCounter': True,
            'lengthSeconds': False,
            'thumbnailUrl': False,
            'startTime': True,
            'threadId': False,
            'commentCounter': True,
            'lastCommentTime': False,
            'categoryTags': False,
            'channelId': False,
            'tags': False,
            'tagsExact': False,
            'lockTagsExact': False,
            'genre': False,
            'genre.keyword': False
        }
        self.app_name = app_name if app_name is not None else "python-nico2finder"

    def set_response_fields(self, **opts):
        """検索結果に含めるフィールドを設定します

        contentId      : コンテンツID
        title          : タイトル
        description    : コンテンツの説明文
        userId         : 投稿者のユーザID
        viewCounter    : 再生数
        mylistCounter  : マイリスト数
        lengthSeconds  : 再生時間(秒)
        thumbnailUrl   : サムネイルのURL
        startTime      : 動画の投稿時間
        threadId       : スレッドのID
        commentCounter : コメント数
        lastCommentTime: 最終コメント時間
        categoryTags   : カテゴリタグ
        channelId      : チャンネルID
        tags           : タグ(空白区切り)
        tagsExact      : タグ完全一致(空白区切り)
        genre          : ジャンル
        genre.keyword  : ジャンル完全一致
        """
        for key in opts:
            if key in self.response_fields:
                self.response_fields[key] = opts[key]

    def current_response_fields(self):
        """検索結果に含まれるフィールドを確認します
        """
        return self.response_fields

    def find_video(self, query, targets="title", filters=None, sort=Sort.Latest, limit=10):
        """動画を検索します

        query   : 検索キーワード
        targets : 検索対象(title, description, tags)
        sort    : 並び順
        filters : 検索フィルタ
        limit   : 取得件数
        """
        params = {
            "q": query,
            "targets": targets,
            "fields": ','.join([f for f in self.response_fields if self.response_fields[f]]),
            "_sort": sort,
            "_context": self.app_name,
            "_limit": limit,
        }

        if filters is not None:
            params.update(filters.get_query())

        uri = '{domain}{endpoint}/contents/search?{query}'.format(
            domain=API_DOMAIN,
            endpoint=API_ENDPOINTS['search'],
            query=urllib.parse.urlencode(params)
        )

        req_headers = {
            "Accept": 'application/json, */*;q=0.8',
            "User-Agent": 'python-nico2finder',
        }

        req = urllib.request.Request(uri, headers=req_headers)

        with urllib.request.urlopen(req) as response:
            body = response.read().decode('utf-8')
            data = json.loads(body)

        return data
