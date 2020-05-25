# coding: utf-8
import pytest
from nico2finder import finder

#
# SearchFilter UserID
#

def test_filter_userid():
    f = finder.SearchFilter(user_id=1)

    assert f.get_query() == {
        'filters[userId][0]': 1
    }

#
# SearchFilter Views
#

def test_filter_least_views():
    f = finder.SearchFilter(least_views=1000)

    assert f.get_query() == {
        'filters[viewCounter][gte]': 1000
    }

def test_filter_most_views():
    f = finder.SearchFilter(most_views=5000)
    
    assert f.get_query() == {
        'filters[viewCounter][lte]': 5000
    }

def test_filter_range_views():
    f = finder.SearchFilter(least_views=1000, most_views=5000)
    
    assert f.get_query() == {
        'filters[viewCounter][gte]': 1000,
        'filters[viewCounter][lte]': 5000,
    }

#
# SearchFilter Comments
#

def test_filter_least_comments():
    f = finder.SearchFilter(least_comments=1000)

    assert f.get_query() == {
        'filters[commentCounter][gte]': 1000
    }

def test_filter_most_comments():
    f = finder.SearchFilter(most_comments=5000)

    assert f.get_query() == {
        'filters[commentCounter][lte]': 5000
    }

def test_filter_range_comments():
    f = finder.SearchFilter(least_comments=1000, most_comments=5000)

    assert f.get_query() == {
        'filters[commentCounter][gte]': 1000,
        'filters[commentCounter][lte]': 5000,
    }

#
# SearchFilter MyLists
#

def test_filter_least_mylists():
    f = finder.SearchFilter(least_mylists=1000)

    assert f.get_query() == {
        'filters[mylistCounter][gte]': 1000
    }

def test_filter_most_mylists():
    f = finder.SearchFilter(most_mylists=5000)

    assert f.get_query() == {
        'filters[mylistCounter][lte]': 5000
    }

def test_filter_range_mylists():
    f = finder.SearchFilter(least_mylists=1000, most_mylists=5000)

    assert f.get_query() == {
        'filters[mylistCounter][gte]': 1000,
        'filters[mylistCounter][lte]': 5000,
    }

#
# SearchFilter Video length
#

def test_filter_shortest_length():
    f = finder.SearchFilter(shortest_length=60)

    assert f.get_query() == {
        'filters[lengthSeconds][gte]': 60
    }

def test_filter_longest_length():
    f = finder.SearchFilter(longest_length=600)

    assert f.get_query() == {
        'filters[lengthSeconds][lte]': 600
    }

def test_filter_range_length():
    f = finder.SearchFilter(shortest_length=60, longest_length=600)

    assert f.get_query() == {
        'filters[lengthSeconds][gte]': 60,
        'filters[lengthSeconds][lte]': 600,
    }

#
# SearchFilter Posted time
#

def test_filter_later_posted():
    f = finder.SearchFilter(posted_after='2011-01-01T00:00:00+09:00')

    assert f.get_query() == {
        'filters[startTime][gte]': '2011-01-01T00:00:00+09:00'
    }

def test_filter_earlier_posted():
    f = finder.SearchFilter(posted_before='2020-01-01T00:00:00+09:00')

    assert f.get_query() == {
        'filters[startTime][lte]': '2020-01-01T00:00:00+09:00'
    }

def test_filter_range_posted():
    f = finder.SearchFilter(
        posted_after='2011-01-01T00:00:00+09:00',
        posted_before='2020-01-01T00:00:00+09:00'
    )

    assert f.get_query() == {
        'filters[startTime][gte]': '2011-01-01T00:00:00+09:00',
        'filters[startTime][lte]': '2020-01-01T00:00:00+09:00',
    }

#
# SearchFilter Tag
#

def test_filter_tag():
    f = finder.SearchFilter(tag='VOCALOID')

    assert f.get_query() == {
        'filters[tags][0]': 'VOCALOID'
    }

def test_filter_multi_tags_tuple():
    f = finder.SearchFilter(tag=('VOCALOID', 'ミク', 'リン'))

    assert f.get_query() == {
        'filters[tags][0]': 'VOCALOID',
        'filters[tags][1]': 'ミク',
        'filters[tags][2]': 'リン',
    }

def test_filter_multi_tags_list():
    f = finder.SearchFilter(tag=['VOCALOID', 'ミク', 'リン'])

    assert f.get_query() == {
        'filters[tags][0]': 'VOCALOID',
        'filters[tags][1]': 'ミク',
        'filters[tags][2]': 'リン',
    }

#
# SearchFilter Genre
#
def test_filter_genre():
    f = finder.SearchFilter(genre='音楽・サウンド')

    assert f.get_query() == {
        'filters[genre][0]': '音楽・サウンド'
    }

def test_filter_multi_genres_tuple():
    f = finder.SearchFilter(genre=('音楽・サウンド', 'ゲーム', 'その他'))

    assert f.get_query() == {
        'filters[genre][0]': '音楽・サウンド',
        'filters[genre][1]': 'ゲーム',
        'filters[genre][2]': 'その他',
    }

def test_filter_multi_genres_list():
    f = finder.SearchFilter(genre=['音楽・サウンド', 'ゲーム', 'その他'])

    assert f.get_query() == {
        'filters[genre][0]': '音楽・サウンド',
        'filters[genre][1]': 'ゲーム',
        'filters[genre][2]': 'その他',
    }
