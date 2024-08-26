#!/usr/bin/python3
"""
100-count module
"""
import requests

def count_words(subreddit, word_list, after=None, counts=None):
    """
    Queries the Reddit API, parses the title of all hot articles,
    and prints a sorted count of given keywords.

    Args:
        subreddit (str): The subreddit to query.
        word_list (list): List of keywords to count in the hot article titles.
        after (str): The 'after' parameter for pagination.
        counts (dict): A dictionary to store counts of keywords.

    Returns:
        None
    """
    if counts is None:
        counts = {}

    if after is None:
        after = ''

    url = f'https://www.reddit.com/r/{subreddit}/hot.json'
    headers = {'User-Agent': 'custom User-Agent'}
    params = {'limit': 100, 'after': after}
    
    response = requests.get(url, headers=headers, params=params, allow_redirects=False)

    if response.status_code != 200:
        return

    data = response.json().get('data', {})
    children = data.get('children', [])
    
    for child in children:
        title = child.get('data', {}).get('title', '').lower().split()
        for word in word_list:
            word_lower = word.lower()
            counts[word_lower] = counts.get(word_lower, 0) + title.count(word_lower)
    
    after = data.get('after')
    if after is not None:
        count_words(subreddit, word_list, after, counts)
    else:
        if counts:
            sorted_counts = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
            for word, count in sorted_counts:
                if count > 0:
                    print(f"{word}: {count}")

