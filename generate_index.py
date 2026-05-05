#!/usr/bin/env python3
"""Generate the index.html listing all 99 recipe posts"""

import json, random
from pathlib import Path

BLOG_DIR = Path("/home/kodaagentmt/tag-soup-blog-clone")
POSTS_DIR = BLOG_DIR / "posts"

with open(BLOG_DIR / "posts.json") as f:
    posts = json.load(f)

BASE_IMAGES = [
    "elk-bolognese.jpg",
    "campfire-chili.jpg",
    "bison-steak.jpg",
    "venison-stew.jpg",
    "duck-confit.jpg",
    "smoked-jerky.jpg",
]

cards_html = ""
for post in posts:
    slug = post['filename'].replace('.html', '')
    image = random.choice(BASE_IMAGES)
    cards_html += f'''
      <div class="post-card">
        <a href="posts/{post["filename"]}">
          <div class="post-thumb"><img src="images/{image}" alt="{post["title"]}"></div>
          <div class="post-body">
            <span class="post-tag">{post["tag"]}</span>
            <span class="post-title">{post["title"]}</span>
          </div>
        </a>
      </div>'''

html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Tag Soup — Wild Game & Outdoor Recipes</title>
  <meta name="description" content="Daily wild game recipes, outdoor cooking tips, and game-day meals from Tag Soup.">
  <meta property="og:image" content="https://kodaagentmt-max.github.io/tag-soup-blog/images/campfire-chili.jpg">
  <meta property="og:image:width" content="940">
  <meta property="og:image:height" content="650">
  <meta property="og:title" content="Tag Soup — Wild Game & Outdoor Recipes">
  <meta property="og:type" content="website">
  <link rel="alternate" type="application/rss+xml" title="Tag Soup RSS" href="rss.xml">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Playfair+Display:ital,wght@0,700;1,400&display=swap" rel="stylesheet">
  <style>
    :root {{ --bg: #0f0a04; --surface: #1a1108; --card: #251808; --border: #3a2510; --accent: #e87820; --gold: #f5c518; --text: #f0e0c0; --muted: #9a8060; --white: #fff; }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ background: var(--bg); color: var(--text); font-family: 'Inter', sans-serif; line-height: 1.6; min-height: 100vh; -webkit-font-smoothing: antialiased; }}
    a {{ color: var(--accent); text-decoration: none; }}
    a:hover {{ color: var(--gold); }}
    img {{ max-width: 100%; }}
    .topbar {{ background: var(--surface); border-bottom: 1px solid var(--border); padding: 0 40px; height: 64px; display: flex; align-items: center; justify-content: space-between; position: sticky; top: 0; z-index: 100; }}
    .topbar-brand {{ display: flex; align-items: center; gap: 10px; }}
    .topbar-brand img {{ height: 42px; width: auto; }}
    .topbar-brand .name {{ font-weight: 700; font-size: 17px; color: var(--white); letter-spacing: 0.5px; }}
    .topbar-brand .name span {{ color: var(--accent); }}
    .topbar-right {{ display: flex; align-items: center; gap: 16px; }}
    .topbar-right a {{ font-size: 13px; font-weight: 500; color: var(--muted); }}
    .topbar-right a:hover {{ color: var(--accent); }}
    .btn-rss {{ background: var(--accent); color: #000; font-size: 12px; font-weight: 600; padding: 6px 14px; border-radius: 4px; }}
    .hero {{ background: linear-gradient(135deg, var(--surface) 0%, #0f0804 100%); border-bottom: 1px solid var(--border); padding: 70px 40px; text-align: center; }}
    .hero-logo {{ height: 80px; margin-bottom: 20px; border-radius: 16px; }}
    .hero h1 {{ font-family: 'Playfair Display', serif; font-size: 52px; font-weight: 700; color: var(--white); letter-spacing: -1px; margin-bottom: 8px; }}
    .hero h1 em {{ color: var(--accent); font-style: italic; }}
    .hero p {{ font-size: 17px; color: var(--muted); font-weight: 400; }}
    .container {{ max-width: 1100px; margin: 0 auto; padding: 50px 40px; }}
    .section-head {{ display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 24px; border-bottom: 1px solid var(--border); padding-bottom: 14px; }}
    .section-head h2 {{ font-family: 'Playfair Display', serif; font-size: 22px; font-weight: 700; color: var(--white); }}
    .posts-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 18px; }}
    .post-card {{ background: var(--card); border: 1px solid var(--border); border-radius: 10px; overflow: hidden; transition: all 0.2s; }}
    .post-card:hover {{ border-color: var(--accent); transform: translateY(-2px); }}
    .post-thumb {{ height: 180px; overflow: hidden; background: #2a1a08; }}
    .post-thumb img {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
    .post-body {{ padding: 18px; }}
    .post-tag {{ font-size: 9px; text-transform: uppercase; letter-spacing: 1.5px; color: var(--accent); font-weight: 700; margin-bottom: 6px; display: block; }}
    .post-title {{ font-size: 15px; font-weight: 600; color: var(--white); line-height: 1.4; display: block; margin-bottom: 8px; }}
    .post-date {{ font-size: 12px; color: var(--muted); }}
    .footer {{ text-align: center; padding: 40px; color: var(--muted); font-size: 13px; border-top: 1px solid var(--border); margin-top: 60px; }}
    @media (max-width: 600px) {{ .topbar {{ padding: 0 20px; }} .hero {{ padding: 40px 20px; }} .hero h1 {{ font-size: 36px; }} .container {{ padding: 30px 20px; }} }}
  </style>
</head>
<body>
  <div class="topbar">
    <div class="topbar-brand">
      <img src="images/logo.png" alt="Tag Soup" onerror="this.style.display='none'">
      <div class="name">Tag <span>Soup</span></div>
    </div>
    <div class="topbar-right">
      <a href="rss.xml">RSS Feed</a>
    </div>
  </div>
  <div class="hero">
    <h1>Wild Game & <em>Outdoor Cooking</em></h1>
    <p>Daily recipes from the field — elk, venison, bison, wildfowl, and more.</p>
  </div>
  <div class="container">
    <div class="section-head">
      <h2>All Recipes ({len(posts)})</h2>
    </div>
    <div class="posts-grid">
{cards_html}
    </div>
  </div>
  <div class="footer">
    🔥 Tag Soup — Wild Game & Outdoor Cooking
  </div>
</body>
</html>'''

(BLOG_DIR / "index.html").write_text(html)
print(f"index.html updated with {len(posts)} recipe cards.")
