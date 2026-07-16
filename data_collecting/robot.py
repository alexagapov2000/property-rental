import urllib.robotparser
from urllib.parse import urlsplit

def can_fetch(url, user_agent='*'):
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(url)
    rp.read()
    return rp.can_fetch(user_agent, url)

def get_robots_parser(base_url):
    """Return a RobotFileParser for the given base URL."""
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(base_url.rstrip('/') + '/robots.txt')
    rp.read()
    return rp

def can_fetch_with_parser(rp, url, user_agent='*'):
    """Check if fetching is allowed using a pre-initialized parser."""
    return rp.can_fetch(user_agent, url)