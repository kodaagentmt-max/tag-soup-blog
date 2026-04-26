#!/usr/bin/env python3
"""
Tag Soup Daily Recipe Agent
Generates a daily wild game recipe post with approved food photography
Run daily via cron — outputs to projects/tag-soup-blog/posts/
"""

import json, os, random
from datetime import datetime
from pathlib import Path

BLOG_DIR = Path("/home/kodaagentmt/.openclaw/workspace/projects/tag-soup-blog")
POSTS_DIR = BLOG_DIR / "posts"
IMAGES_DIR = BLOG_DIR / "images"

# Pre-approved food images — all vetted by KC
APPROVED_IMAGES = [
    "elk-bolognese.jpg",
    "campfire-chili.jpg",
    "bison-steak.jpg",
    "venison-stew.jpg",
    "duck-confit.jpg",
    "smoked-jerky.jpg",
]

def get_approved_image():
    """Pick a random approved food image."""
    chosen = random.choice(APPROVED_IMAGES)
    return {
        "url": f"https://kodaagentmt-max.github.io/tag-soup-blog/images/{chosen}",
        "local_path": f"../images/{chosen}",
        "alt": chosen.replace(".jpg", "").replace("-", " ").title()
    }

WILD_RECIPES = [
    {
        "tag": "Elk",
        "title": "Elk Bolognese Over Hand-Cut Noodles",
        "body": "A hearty, old-world pasta built for cold nights after a long day in the field. Ground elk shoulder melts into a rich, deeply flavored sauce that rivals any beef version. The secret: a splash of red wine and a long, patient simmer. Serve with fresh parmesan and crusty bread to soak up the remaining sauce.",
        "category": "elk",
        "description": "Thin-cut venison backstrap, smoke-low and slow, finished with a teriyaki glaze."
    },
    {
        "tag": "Campfire",
        "title": "Dutch Oven Campfire Chili — 5 Hours, Worth the Wait",
        "body": "Five hours over coals transforms tough elk shoulder into something that falls apart at the touch of a fork. This dutch oven campfire chili is the ultimate field-to-table meal. Brown the meat hard, layer in the beans and tomatoes, and let the fire do the rest. The bone-deep warmth and rich gamey flavor make this the definitive camp meal for cold nights.",
        "category": "campfire",
        "description": "Five hours over coals transforms tough elk shoulder into something that falls apart at the touch of a fork."
    },
    {
        "tag": "Bison",
        "title": "Bison Steak Frites with Herb Butter",
        "body": "Thick-cut bison sirloin, screaming hot cast iron, compound herb butter melting over the top. This is the kind of meal that makes your whole camp sit up and pay attention. The key is super-high heat and fast timing — bison is leaner than beef and can go from perfect to tough in seconds. Rest it for half the cook time and serve with frites tossed in rosemary salt.",
        "category": "bison",
        "description": "Thick-cut bison sirloin, screaming hot cast iron, compound herb butter melting over the top."
    },
    {
        "tag": "Deer/Venison",
        "title": "Venison Stew with Root Vegetables",
        "body": "A slow-braised venison stew with carrots, parsnips, and potatoes. This is the meal that fills the hunting camp kitchen with warmth on a winter afternoon. Venison benefits from long, slow cooking to break down the connective tissue. Add a glug of red wine and a handful of fresh thyme. The result is rich, gamey, and deeply satisfying.",
        "category": "venison",
        "description": "A slow-braised venison stew with carrots, parsnips, and potatoes."
    },
    {
        "tag": "Wildfowl",
        "title": "Duck Confit Tacos with Pickled Onions",
        "body": "Duck leg confit shredded into crispy shreds, piled into warm corn tortillas with quick-pickled red onions, cotija cheese, and a squeeze of lime. The richness of the duck fat balanced against the bright acid of the pickles makes these tacos unforgettable. Make the confit low and slow in your dutch oven, then crisp the skin in a hot cast iron skillet right before service.",
        "category": "wildfowl",
        "description": "Duck leg confit shredded into crispy shreds, piled into warm corn tortillas."
    },
    {
        "tag": "Elk",
        "title": "Smoked Elk Summer Sausage",
        "body": "Elk gets coarsely ground with pork fat, stuffed into纤维素 casings, and slow-smoked until deeply set. This is a project that rewards patience — the smoke does the heavy lifting. Slice thin and serve on hunting camp crackers with sharp cheddar. It keeps for weeks in the cooler and tastes better each day.",
        "category": "elk",
        "description": "Elk gets coarsely ground with pork fat, stuffed and slow-smoked until deeply set."
    },
    {
        "tag": "Cast Iron",
        "title": "Cast Iron Wild Boar Ribs",
        "body": "Wild boar ribs get a brown sugar and chili rub, then braised in apple cider until tender. Finish them in a ripping-hot cast iron to caramelize the glaze. The result is sticky, sweet, and slightly gamey — nothing like domestic pork ribs. Serve with a vinegar slaw to cut through the richness.",
        "category": "cast-iron",
        "description": "Wild boar ribs get a brown sugar and chili rub, then braised in apple cider."
    },
    {
        "tag": "Sides",
        "title": "Campfire Dutch Oven Cornbread",
        "body": "Cast iron cornbread baked over coals with whole kernel corn, green chiles, and a touch of honey. The edge gets crispy and golden while the center stays perfectly crumbly. This is the side that disappears first at any camp meal. Serve warm with butter and a drizzle of hot honey.",
        "category": "sides",
        "description": "Cast iron cornbread baked over coals with whole kernel corn, green chiles, and honey."
    },
]

# Track posted recipes by date
TRACK_FILE = BLOG_DIR / "posts.json"

def get_posts():
    if TRACK_FILE.exists():
        with open(TRACK_FILE) as f:
            return json.load(f)
    return []

def save_posts(posts):
    with open(TRACK_FILE, "w") as f:
        json.dump(posts, f, indent=2)

def generate_post_html(recipe, photo, slug):
    date_str = datetime.now().strftime("%B %d, %Y")
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{recipe['title']} — Tag Soup</title>
  <meta name="description" content="{recipe['description']}">
  <meta property="og:title" content="{recipe['title']}">
  <meta property="og:type" content="article">
  <meta property="og:image" content="{photo['url']}">
  <meta property="og:url" content="https://kodaagentmt-max.github.io/tag-soup-blog/posts/{slug}.html">
  <style>
    body {{ background: #1a0f00; color: #f0e0c0; font-family: Georgia, serif; margin: 0; }}
    .brand-banner {{ background: #e87820; padding: 10px 20px; text-align: center; }}
    .brand-banner a {{ color: #fff; text-decoration: none; font-size: 13px; font-weight: 600; font-family: Inter, sans-serif; letter-spacing: 0.5px; }}
    .brand-banner a:hover {{ color: #f5c518; }}
    .container {{ max-width: 720px; margin: 0 auto; padding: 40px 20px; }}
    .hero-img {{ width: 100%; max-height: 400px; object-fit: cover; border-radius: 8px; margin-bottom: 28px; display: block; }}
    .tag {{ font-size: 11px; text-transform: uppercase; letter-spacing: 2px; color: #e87820; margin-bottom: 10px; }}
    h1 {{ font-size: 28px; color: #f5c518; margin-bottom: 12px; line-height: 1.3; }}
    .meta {{ font-size: 12px; color: #c4a97a; margin-bottom: 24px; }}
    .body {{ font-size: 17px; line-height: 1.9; margin-bottom: 24px; }}
    .section {{ background: #2a1a00; border-left: 3px solid #e87820; padding: 14px 18px; margin: 24px 0; font-size: 15px; }}
    .section h3 {{ color: #e87820; font-size: 14px; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px; }}
    .back {{ color: #e87820; text-decoration: none; font-size: 13px; }}
  </style>
</head>
<body>
  <div class="brand-banner"><a href="/tag-soup-blog/">← Back to Tag Soup — Camp Cook Kitchen</a></div>
  <div class="container">
    <img class="hero-img" src="{photo['local_path']}" alt="{photo['alt']}" onerror="this.style.display='none'">
    <div class="tag">Wild Game / {recipe['tag']}</div>
    <h1>{recipe['title']}</h1>
    <div class="meta">🔥 Camp Cook Kitchen — Tag Soup • {date_str}</div>
    <p class="body">{recipe['body']}</p>
    <div class="section">
      <h3>Field Notes</h3>
      <p>{recipe['description']}</p>
    </div>
    <a class="back" href="/tag-soup-blog/">← Back to Tag Soup</a>
  </div>
</body>
</html>"""

def update_rss(recipe, photo, slug):
    rss_path = BLOG_DIR / "rss.xml"
    date_str = datetime.now().strftime("%a, %d %b %Y %H:%M:%S MDT")
    item = f"""
    <item>
      <title>{recipe['title']}</title>
      <link>https://kodaagentmt-max.github.io/tag-soup-blog/posts/{slug}.html</link>
      <guid isPermaLink="true">https://kodaagentmt-max.github.io/tag-soup-blog/posts/{slug}.html</guid>
      <pubDate>{date_str}</pubDate>
      <description><![CDATA[{recipe['description']}]]></description>
      <enclosure url="{photo['url']}" type="image/jpeg" length="100000"/>
      <media:content url="{photo['url']}" type="image/jpeg" medium="image"/>
    </item>
"""
    with open(rss_path) as f:
        content = f.read()
    # Insert after first <item>
    if "<item>" in content:
        content = content.replace("<item>", f"<item>\n{item}", 1)
    else:
        content = content.replace("</channel>", f"{item}\n  </channel>")
    with open(rss_path, "w") as f:
        f.write(content)

def update_index(recipe, photo, slug):
    index_path = BLOG_DIR / "index.html"
    with open(index_path) as f:
        content = f.read()
    
    # Update featured card
    featured_section = f'''<div class="featured">
      <div class="featured-img">
        <img src="{photo['local_path']}" alt="{recipe['title']}">
      </div>
      <div class="featured-content">
        <span class="featured-tag">Wild Game / {recipe['tag']}</span>
        <h2>{recipe['title']}</h2>
        <div class="meta">Tag Soup Kitchen — {datetime.now().strftime("%B %d, %Y")}</div>
        <p>{recipe['description']}</p>
        <a href="posts/{slug}.html" class="featured-btn">Read Recipe →</a>
      </div>
    </div>'''
    
    if '<div class="featured">' in content:
        content = content.replace('<div class="featured">', f'<!-- NEW FEATURED -->\n{featured_section}\n<!-- /NEW FEATURED -->\n<DEL>', 1)
        content = content.replace('<DEL><!-- /NEW FEATURED -->\n<DEL>', '')
        content = content.replace('\n<DEL>', '')
    
    with open(index_path, "w") as f:
        f.write(content)

def run():
    print(f"[{datetime.now()}] Tag Soup Recipe Agent starting...")
    
    today_id = datetime.now().strftime("%Y%m%d")
    posts = get_posts()
    
    if any(p.get("id") == today_id for p in posts):
        print(f"[{datetime.now()}] Already posted today ({today_id}). Skipping.")
        return
    
    recipe = random.choice(WILD_RECIPES)
    photo = get_approved_image()
    slug = f"recipes-{today_id}"
    date_str = datetime.now().strftime("%B %d, %Y")
    
    post_path = POSTS_DIR / f"{slug}.html"
    with open(post_path, "w") as f:
        f.write(generate_post_html(recipe, photo, slug))
    print(f"  Created: {post_path.name}")
    
    update_rss(recipe, photo, slug)
    print(f"  Updated RSS")
    
    update_index(recipe, photo, slug)
    print(f"  Updated index")
    
    posts.append({"id": today_id, "date": date_str, "title": recipe["title"]})
    save_posts(posts)
    
    print(f"[{datetime.now()}] Recipe posted: {recipe['title']}")

if __name__ == "__main__":
    run()