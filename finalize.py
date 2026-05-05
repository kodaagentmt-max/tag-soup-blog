#!/usr/bin/env python3
"""Finalize: clean old files, copy generated images, update pages with correct images, push"""

import os, json, shutil, random
from pathlib import Path

BLOG_DIR = Path("/home/kodaagentmt/tag-soup-blog-clone")
POSTS_DIR = BLOG_DIR / "posts"
GEN_IMAGES_DIR = BLOG_DIR / "images" / "generated"
MAIN_IMAGES_DIR = BLOG_DIR / "images"

# 1. Copy generated images to main images dir
for img in GEN_IMAGES_DIR.glob("*.jpg"):
    shutil.copy(img, MAIN_IMAGES_DIR / img.name)
    print(f"  Copied {img.name}")

# 2. Remove old/duplicate posts
old_files = ["elk-bolognese.html", "recipes-20260426.html", "smoked-venison-jerky.html", "smoked-venison-jerky.jpg"]
for f in old_files:
    fp = POSTS_DIR / f
    if fp.exists():
        fp.unlink()
        print(f"  Removed old: {f}")

# 3. Build image mapping from filename
IMAGE_MAP = {}
for img in GEN_IMAGES_DIR.glob("*.jpg"):
    # acorn-squash-sage.jpg -> acorn squash sage
    key = img.stem.replace("-", " ")
    IMAGE_MAP[key] = img.name

# 4. Update each recipe page to use its correct image if available
RECIPE_IMAGE_PAIRS = [
    ("elk-sloppy-joes-with-pickled-jalapenos", "elk-sloppy-joes.jpg"),
    ("elk-tamales-with-red-chile-sauce", "elk-bolognese.jpg"),
    ("elk-shawarma-plate", "elk-bolognese.jpg"),
    ("elk-green-chile-stew", "elk-green-chile-stew.jpg"),
    ("venison-chorizo-breakfast-tacos", "venison-breakfast-tacos.jpg"),
    ("venison-bibimbap", "venison-bibimbap.jpg"),
    ("venison-neck-ragu-with-rigatoni", "venison-ragu.jpg"),
    ("venison-fried-pickles-with-sriracha-aioli", "venison-fried-pickles.jpg"),
    ("venison-liver-and-onions", "venison-liver-onions.jpg"),
    ("venison-pastrami-on-rye", "venison-pastrami-rye.jpg"),
    ("bison-french-dip-sandwiches", "bison-french-dip.jpg"),
    ("bison-tagliatelle-with-brown-butter-and-sage", "bison-tagliatelle.jpg"),
    ("bison-enchiladas-with-roasted-poblano-sauce", "bison-enchiladas.jpg"),
    ("smoked-bison-baby-back-ribs", "bison-baby-back-ribs.jpg"),
    ("wild-boar-bacon-smash-burger", "wild-boar-burger.jpg"),
    ("wild-boar-osso-buco-with-gremolata", "wild-boar-osso-buco.jpg"),
    ("wild-boar-curry-with-coconut-milk", "wild-boar-curry.jpg"),
    ("wild-boar-rinds-cracklings", "wild-boar-cracklings.jpg"),
    ("teal-duck-poppers-with-bacon", "teal-duck-poppers.jpg"),
    ("merganser-gumbo-with-duck-andouille", "merganser-gumbo.jpg"),
    ("spoonbill-duck-breast-with-plum-sauce", "duck-breast-plum.jpg"),
    ("duck-egg-frittata-with-morels-and-ramps", "duck-egg-frittata.jpg"),
    ("carp-with-lemon-dill-beurre-blanc", "carp-beurre-blanc.jpg"),
    ("catfish-po-boy-with-remoulade", "catfish-po-boy.jpg"),
    ("sturgeon-kedgeree", "sturgeon-kedgeree.jpg"),
    ("ember-roasted-acorn-squash-with-sage-butter", "acorn-squash-sage.jpg"),
]

BASE_IMAGES = ["elk-bolognese.jpg", "campfire-chili.jpg", "bison-steak.jpg", "venison-stew.jpg", "duck-confit.jpg", "smoked-jerky.jpg"]

for slug, correct_image in RECIPE_IMAGE_PAIRS:
    html_file = POSTS_DIR / f"{slug}.html"
    if html_file.exists():
        content = html_file.read_text()
        # Replace the image src
        import re
        content = re.sub(r'src="../images/[^"]*"', f'src="../images/{correct_image}"', content)
        html_file.write_text(content)

print(f"\nUpdated image references in recipe pages.")

# 5. Count final posts
html_files = list(POSTS_DIR.glob("*.html"))
print(f"Final post count: {len(html_files)}")

# 6. Update index.html to use correct images too
with open(BLOG_DIR / "posts.json") as f:
    posts = json.load(f)

# Build slug -> correct image map
slug_to_image = {slug: img for slug, img in RECIPE_IMAGE_PAIRS}

cards_html = ""
for post in posts:
    slug = post['filename'].replace('.html', '')
    correct_img = slug_to_image.get(slug)
    image = correct_img if correct_img else random.choice(BASE_IMAGES)
    cards_html += f'''
      <div class="post-card">
        <a href="posts/{post["filename"]}">
          <div class="post-thumb"><img src="../images/{image}" alt="{post["title"]}"></div>
          <div class="post-body">
            <span class="post-tag">{post["tag"]}</span>
            <span class="post-title">{post["title"]}</span>
          </div>
        </a>
      </div>'''

index_html = f'''<!DOCTYPE html>
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

(BLOG_DIR / "index.html").write_text(index_html)
print(f"index.html updated.")
print(f"\nAll done! Run: git add . && git commit && git push")
