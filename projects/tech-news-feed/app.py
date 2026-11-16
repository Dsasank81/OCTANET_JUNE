"""Minimal RSS news feed. No API key required."""
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET
from html import unescape
from flask import Flask, render_template_string, request

FEEDS = {
    "Technology": "https://feeds.bbci.co.uk/news/technology/rss.xml",
    "Science": "https://www.sciencedaily.com/rss/computers_math/artificial_intelligence.xml",
}
app = Flask(__name__)
PAGE = """<!doctype html><title>Tech News Feed</title><h1>Tech News Feed</h1>
<form><select name=topic>{% for k in feeds %}<option {% if k==topic %}selected{% endif %}>{{k}}</option>{% endfor %}</select><button>Load</button></form>
{% if error %}<p>{{error}}</p>{% endif %}{% for item in items %}<article><h2><a href="{{item.link}}" rel="noopener">{{item.title}}</a></h2><p>{{item.summary}}</p></article>{% endfor %}"""
def load_feed(url):
    req = Request(url, headers={"User-Agent":"PersonalTechNewsFeed/1.0"})
    with urlopen(req, timeout=12) as response:
        root = ET.fromstring(response.read())
    items=[]
    for node in root.findall(".//item")[:25]:
        title=node.findtext("title") or "Untitled"
        link=node.findtext("link") or "#"
        desc=node.findtext("description") or ""
        items.append({"title":unescape(title),"link":link,"summary":unescape(desc)[:500]})
    return items
@app.route("/")
def index():
    topic=request.args.get("topic","Technology")
    if topic not in FEEDS: topic="Technology"
    error=""
    try: items=load_feed(FEEDS[topic])
    except Exception as exc: items=[]; error=f"Feed unavailable: {exc}"
    return render_template_string(PAGE, feeds=FEEDS, topic=topic, items=items, error=error)
if __name__=="__main__": app.run(debug=False, port=5000)
