#!/usr/bin/env python3
"""Update all recipe post pages with correct image paths and clean text"""

import os, re, json
from pathlib import Path

POSTS_DIR = Path('/home/kodaagentmt/tag-soup-blog-clone/docs/posts')
IMAGES_DIR = Path('/home/kodaagentmt/tag-soup-blog-clone/docs/images')

# Image name mapping - recipe file base name -> image filename
IMAGE_MAP = {
    'bison-beefaroni': 'bison-beefaroni.jpg',
    'bison-bourguignon': 'bison-bourguignon.jpg',
    'bison-burgers-with-caramelized-onions-and-gruyère': 'bison-burgers.jpg',
    'bison-enchiladas-with-roasted-poblano-sauce': 'bison-enchiladas.jpg',
    'bison-french-dip-sandwiches': 'bison-french-dip.jpg',
    'bison-osso-buco': 'bison-osso-buco.jpg',
    'bison-steak-frites-with-herb-butter': 'bison-steak-frites.jpg',
    'bison-tagliatelle-with-brown-butter-and-sage': 'bison-tagliatelle.jpg',
    'boar-smoked-sausage-with-peppers-and-onions': 'boar-sausage-peppers.jpg',
    'campfire-breakfast-burritos': 'campfire-chili.jpg',
    'campfire-cedar-plank-salmon': 'campfire-chili.jpg',
    'campfire-flatbread-with-wild-boar-sausage': 'campfire-chili.jpg',
    'campfire-grilled-street-corn': 'campfire-chili.jpg',
    'campfire-shrimp-boil': 'campfire-chili.jpg',
    'canadian-goose-confit-legs': 'goose-confit.jpg',
    'carp-with-lemon-dill-beurre-blanc': 'carp-beurre-blanc.jpg',
    'cast-iron-campfire-beans': 'campfire-chili.jpg',
    'cast-iron-campfire-cornbread-with-honey-butter': 'campfire-chili.jpg',
    'cast-iron-duck-breast-with-cherry-reduction': 'duck-breast-cherry.jpg',
    'cast-iron-wild-boar-ribs': 'wild-boar-ribs.jpg',
    'catfish-po-boy-with-remoulade': 'catfish-po-boy.jpg',
    'duck-confit-tacos-with-pickled-onions': 'duck-confit-tacos.jpg',
    'duck-egg-frittata-with-morels-and-ramps': 'duck-egg-frittata.jpg',
    'duck-fried-rice': 'duck-fried-rice.jpg',
    'dutch-oven-apple-cinnamon-cobbler': 'campfire-chili.jpg',
    'dutch-oven-beef-stew': 'campfire-chili.jpg',
    'dutch-oven-campfire-chili-5-hours-worth-the-wait': 'campfire-chili.jpg',
    'dutch-oven-cinnamon-rolls': 'campfire-chili.jpg',
    'dutch-oven-cornbread': 'campfire-chili.jpg',
    'dutch-oven-pot-roast-with-red-wine-and-rosemary': 'campfire-chili.jpg',
    'dutch-oven-sourdough-bread': 'campfire-chili.jpg',
    'elk-backstrap-with-wild-mushroom-cream-sauce': 'elk-backstrap-wild-mushroom-cream-sauce.jpg',
    'elk-bolognese': 'elk-bolognese.jpg',
    'elk-chili-colorado': 'elk-chili-colorado.jpg',
    'elk-green-chile-stew': 'elk-green-chile-stew.jpg',
    'elk-meatballs-in-tomato-basil-sauce': 'elk-meatballs-tomato-basil.jpg',
    'elk-rueben-sandwich': 'elk-rueben-sandwich.jpg',
    'elk-shawarma-plate': 'elk-shawarma.jpg',
    'elk-sloppy-joes-with-pickled-jalapenos': 'elk-sloppy-joes.jpg',
    'elk-tacos-with-roasted-salsa-verde': 'elk-tacos.jpg',
    'elk-tamales-with-red-chile-sauce': 'elk-tamales-with-red-chile-sauce.jpg',
    'ember-roasted-acorn-squash-with-sage-butter': 'acorn-squash-sage.jpg',
    'ember-roasted-whole-duck': 'duck-confit.jpg',
    'goose-gumbo': 'goose-gumbo.jpg',
    'grouse-piccata-with-capers-and-lemon': 'duck-confit.jpg',
    'merganser-gumbo-with-duck-andouille': 'merganser-gumbo.jpg',
    'moulard-duck-prosciutto': 'duck-confit.jpg',
    'muskie-fish-cakes-with-cajun-remoulade': 'campfire-chili.jpg',
    'pan-fried-trout-with-brown-butter-and-almonds': 'campfire-chili.jpg',
    'perch-meunière-with-parsley-and-lemon': 'carp-beurre-blanc.jpg',
    'pheasant-fried-rice': 'pheasant-fried-rice.jpg',
    'pheasant-pot-pie': 'pheasant-pot-pie.jpg',
    'rabbit-and-dumplings': 'duck-confit.jpg',
    'rabbit-cacciatore': 'duck-confit.jpg',
    'rabbit-tikka-masala': 'duck-confit.jpg',
    'roasted-pheasant-with-bacon-and-thyme': 'pheasant-roasted.jpg',
    'smoked-bison-baby-back-ribs': 'bison-baby-back-ribs.jpg',
    'smoked-bison-brisket': 'bison-smoked-brisket.jpg',
    'smoked-duck-breast-with-maple-and-black-pepper': 'smoked-goose-peach.jpg',
    'smoked-duck-eggs-benedict': 'smoked-duck-benedict.jpg',
    'smoked-elk-leg-roast': 'elk-leg-roast.jpg',
    'smoked-elk-summer-sausage': 'elk-summer-sausage.jpg',
    'smoked-goose-breast-with-peach-glaze': 'smoked-goose-peach.jpg',
    'smoked-pheasant-breast-with-gouda': 'pheasant-smoked.jpg',
    'smoked-pheasant-with-sage-and-apple': 'pheasant-smoked.jpg',
    'smoked-rabbit-with-apricot-mustard-glaze': 'smoked-rabbit.jpg',
    'smoked-steelhead-trout-dip': 'smoked-trout-dip.jpg',
    'smoked-venison-jerky-teriyaki-style': 'smoked-venison-jerky.jpg',
    'smoked-wild-mushrooms': 'smoked-jerky.jpg',
    'southern-fried-rabbit': 'duck-confit.jpg',
    'spoonbill-duck-breast-with-plum-sauce': 'duck-breast-plum.jpg',
    'sturgeon-kedgeree': 'sturgeon-kedgeree.jpg',
    'teal-duck-poppers-with-bacon': 'teal-duck-poppers.jpg',
    'venison-bibimbap': 'venison-bibimbap.jpg',
    'venison-chorizo-breakfast-tacos': 'venison-breakfast-tacos.jpg',
    'venison-curry-with-sweet-potato': 'venison-curry.jpg',
    'venison-fried-pickles-with-sriracha-aioli': 'venison-fried-pickles.jpg',
    'venison-italian-sub': 'venison-italian-sub.jpg',
    'venison-liver-and-onions': 'venison-liver-onions.jpg',
    'venison-mushroom-stroganoff': 'venison-mushroom-stroganoff.jpg',
    'venison-neck-ragu-with-rigatoni': 'venison-ragu.jpg',
    'venison-pastrami-on-rye': 'venison-pastrami-rye.jpg',
    'venison-potato-soup': 'venison-potato-soup.jpg',
    'venison-salisbury-steak': 'venison-salisbury-steak.jpg',
    'venison-stew-with-root-vegetables': 'venison-stew-root-vegetables.jpg',
    'venison-stir-fry-with-snap-peas-and-ginger': 'campfire-chili.jpg',
    'venison-tacos-with-pineapple-salsa': 'venison-tacos.jpg',
    'walleye-au-gratin': 'campfire-chili.jpg',
    'walleye-fish-tacos-with-chipotle-cream': 'campfire-chili.jpg',
    'wild-boar-bacon-smash-burger': 'wild-boar-burger.jpg',
    'wild-boar-chorizo-and-eggs': 'wild-boar-chorizo-eggs.jpg',
    'wild-boar-curry-with-coconut-milk': 'wild-boar-curry.jpg',
    'wild-boar-osso-buco-with-gremolata': 'wild-boar-osso-buco.jpg',
    'wild-boar-pozole-rojo': 'wild-boar-pozole.jpg',
    'wild-boar-ragu-with-pappardelle': 'wild-boar-ragu.jpg',
    'wild-boar-rinds-cracklings': 'wild-boar-cracklings.jpg',
}

# Fallback image
FALLBACK = 'campfire-chili.jpg'

files = list(POSTS_DIR.glob('*.html'))
updated = 0

for f in files:
    base = f.stem
    html = f.read_text(encoding='utf-8', errors='replace')
    original = html
    
    # Fix image path
    img = IMAGE_MAP.get(base, FALLBACK)
    html = re.sub(r'src="[^"]*images/[^"]*\.jpg"', f'src="images/{img}"', html)
    
    # Fix double .html in og:url
    html = html.replace('.html.html"', '.html"')
    
    # Fix garbled/emojified text in visible content
    # Replace literal emojis that may have been double-encoded
    html = html.replace('🔥', '')
    html = html.replace('🫏', '')
    html = html.replace('💡', '')
    
    # Fix brand banner - remove emoji from "Back to Tag Soup"
    html = re.sub(r'M-bM-\^FM-\^P', '', html)
    html = re.sub(r'M-bM-\^@M-\^T', "'", html)
    
    # Clean h3 emoji placeholders that were replaced with text already
    html = re.sub(r'\[!\]', 'What You\'ll Need', html)
    
    # Fix the h3 tags - they may still have emojis or broken text
    html = re.sub(r'<h3>[^<]*</h3>', lambda m: '<h3>What You\'ll Need</h3>' if 'What' in m.group(0) or '🫏' in m.group(0) or '[!]' in m.group(0) else m.group(0), html)
    html = re.sub(r'<h3>[^<]*</h3>', lambda m: '<h3>Pro Tips</h3>' if 'Tip' in m.group(0) or '💡' in m.group(0) or '[TIP]' in m.group(0) else m.group(0), html)
    html = re.sub(r'<h3>[^<]*</h3>', lambda m: '<h3></h3>' if m.group(0).strip() == '<h3></h3>' else m.group(0), html)
    
    # Remove stray replacement characters
    html = re.sub(r'', '', html)
    
    # Fix brand banner and footer
    html = re.sub(r'<- Back to Tag Soup — Camp Cook Kitchen', '<- Back to Tag Soup', html)
    html = re.sub(r'🔥 Tag Soup — Wild Game', 'Tag Soup', html)
    
    # Fix title tag garbling
    html = re.sub(r'Tag Soup$', 'Tag Soup', html)
    
    if html != original:
        f.write_text(html, encoding='utf-8')
        updated += 1

print(f'Updated {updated}/{len(files)} post pages')
print(f'Image map has {len(IMAGE_MAP)} entries')

# Show what image each recipe uses
missing_imgs = [img for img in IMAGE_MAP.values() if not (IMAGES_DIR / img).exists()]
print(f'Missing images from map: {len(missing_imgs)}')
if missing_imgs[:5]:
    print('First few missing:', missing_imgs[:5])