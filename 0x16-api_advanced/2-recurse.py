#!/usr/bin/python3
"""
2-recurse module
"""
import requests

def recurse(subreddit, hot_list=[], after=None):
    """
    Recursively queries the Reddit API and returns a list containing the titles
    of all hot articles for a given subreddit. If no results are found, returns None.

    Args:
        subreddit (str): The subreddit to query.
        hot_list (list): The list of hot article titles (used for recursion).
        after (str): The 'after' parameter for pagination (used for recursion).

    Returns:
        list: List of titles of hot articles, or None if no valid subreddit.
    """
    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {"User-Agent": "custom User-Agent"}
    params = {"limit": 100, "after": after}

    try:
        response = requests.get(url, headers=headers, params=params, allow_redirects=False)
        if response.status_code == 200:
            data = response.json().get("data", {})
            children = data.get("children", [])
            for post in children:
                hot_list.append(post.get("data", {}).get("title"))

            after = data.get("after")
            if after is not None:
                return recurse(subreddit, hot_list, after)
            else:
                return hot_list if hot_list else None
        else:
            return None
    except Exception:
        return None

