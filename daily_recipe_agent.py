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

APPROVED_IMAGES = [
    "elk-bolognese.jpg",
    "campfire-chili.jpg",
    "bison-steak.jpg",
    "venison-stew.jpg",
    "duck-confit.jpg",
    "smoked-jerky.jpg",
]

def get_approved_image():
    chosen = random.choice(APPROVED_IMAGES)
    return {
        "url": f"https://kodaagentmt-max.github.io/tag-soup-blog/images/{chosen}",
        "local_path": f"../images/{chosen}",
        "alt": chosen.replace(".jpg", "").replace("-", " ").title()
    }

WILD_RECIPES = [
    # ELK
    {
        "tag": "Elk",
        "title": "Elk Bolognese Over Hand-Cut Noodles",
        "body": "A hearty, old-world pasta built for cold nights after a long day in the field. Ground elk shoulder melts into a rich, deeply flavored sauce that rivals any beef version. The secret: a splash of red wine and a long, patient simmer. Serve with fresh parmesan and crusty bread to soak up the remaining sauce.",
        "description": "A rich, slow-simmered elk bolognese over hand-cut egg noodles. Old-world technique, field-to-table result."
    },
    {
        "tag": "Elk",
        "title": "Smoked Elk Summer Sausage",
        "body": "Elk gets coarsely ground with pork fat, stuffed into collagen casings, and slow-smoked until deeply set. The smoke does the heavy lifting. Slice thin and serve on hunting camp crackers with sharp cheddar. It keeps for weeks in the cooler and tastes better each day.",
        "description": "Coarsely ground elk and pork fat, slow-smoked until deeply set. A project that rewards patience."
    },
    {
        "tag": "Elk",
        "title": "Elk Backstrap with Wild Mushroom Cream Sauce",
        "body": "Elk backstrap seared hard in a ripping hot cast iron, then finished with a rich cream sauce made from foraged porcinis and shallots. The key is not overcooking — pull it at medium-rare and let it rest. The cream sauce ties everything together.",
        "description": "Sear-fired elk backstrap with a wild mushroom cream sauce. Simple, elegant, unforgettable."
    },
    {
        "tag": "Elk",
        "title": "Elk Chili Colorado",
        "body": "Dried New Mexico chiles rehydrate and blend into a deep red braising liquid that transforms elk shoulder into something remarkable. Rich, smoky, slightly spicy. Serve over white rice with fresh lime and cilantro.",
        "description": "Elk shoulder braised in dried chile sauce. Deep red, smoky, and built for big appetites."
    },
    {
        "tag": "Elk",
        "title": "Elk Meatballs in Tomato Basil Sauce",
        "body": "Ground elk mixed with bread crumbs, egg, and parmesan, rolled and browned, then simmered in a scratch tomato basil sauce. These meatballs are lighter than beef and take on the sauce beautifully. Serve over spaghetti or on crusty toasted bread.",
        "description": "Tender elk meatballs in a scratch tomato basil sauce. A camp classic, elevated."
    },
    {
        "tag": "Elk",
        "title": "Elk Rueben Sandwich",
        "body": "Thin-sliced elk roast, caramelized kraut, Swiss cheese, Russian dressing, and rye bread pressed on a flattop griddle. The elk takes the place of corned beef and the results are exceptional — leaner, gamier, more interesting than the original.",
        "description": "Thin-sliced elk on rye with kraut, Swiss, and Russian dressing. The camp deli sandwich."
    },
    {
        "tag": "Elk",
        "title": "Elk Osso Buco",
        "body": "Elk shanks cross-cut, dredged in flour, browned, then braised in red wine with tomatoes, carrots, and fresh herbs until the meat falls off the bone. Serve with gremolata — a zesty mix of lemon zest, garlic, and parsley — over creamy polenta.",
        "description": "Elk shanks braised in red wine with tomatoes. Falls off the bone every time."
    },
    {
        "tag": "Elk",
        "title": "Elk Tacos with Roasted Salsa Verde",
        "body": "Ground elk seasoned with cumin, smoked paprika, and a touch of cinnamon, piled into warm corn tortillas with a bright roasted salsa verde, diced onion, and cilantro. The gamey elk matches perfectly with the tangy green salsa.",
        "description": "Seasoned elk in warm tortillas with roasted salsa verde. Fast, bold, and everything you want."
    },
    {
        "tag": "Elk",
        "title": "Smoked Elk Leg Roast",
        "body": "Elk leg roast deboned, rolled, and tied, brined overnight in salt, sugar, and juniper berries, then smoked at 225°F until it hits 145°F internal. The meat is rosy and tender with a deep smoky flavor from the juniper and oak.",
        "description": "Brined elk leg roast smoked at 225°F. Juniper and oak smoke, incredibly tender."
    },
    # DEER / VENISON
    {
        "tag": "Deer / Venison",
        "title": "Venison Stew with Root Vegetables",
        "body": "A slow-braised venison stew with carrots, parsnips, and potatoes. This is the meal that fills the hunting camp kitchen with warmth on a winter afternoon. Venison benefits from long, slow cooking to break down the connective tissue. Add a glug of red wine and fresh thyme.",
        "description": "A slow-braised venison stew with carrots, parsnips, and potatoes. Rich and deeply satisfying."
    },
    {
        "tag": "Deer / Venison",
        "title": "Smoked Venison Jerky — Teriyaki Style",
        "body": "Venison sliced thin, marinated overnight in soy sauce, worcestershire, brown sugar, garlic, and smoked paprika, then smoked at 130°F for 4-5 hours until dry and leathery. Chewy, sweet, savory, with serious smoke flavor. Keeps for weeks.",
        "description": "Thin-sliced venison marinated in teriyaki, smoked at 130°F until leathery. Keeps for weeks."
    },
    {
        "tag": "Deer / Venison",
        "title": "Venison Stir-Fry with Snap Peas and Ginger",
        "body": "Venison loin sliced thin against the grain, seared at extremely high heat with snap peas, ginger, garlic, and soy sauce. The whole thing comes together in under five minutes. Serve over jasmine rice with a fried egg on top.",
        "description": "Venison loin, snap peas, ginger, and garlic — a five-minute weeknight wild game dinner."
    },
    {
        "tag": "Deer / Venison",
        "title": "Venison Tacos with Pineapple Salsa",
        "body": "Ground venison seasoned with cumin, chili powder, and a hint of cinnamon, piled into warm corn tortillas with fresh pineapple salsa, diced onion, cilantro, and a squeeze of lime. The sweetness of the pineapple cuts right through the gamey richness.",
        "description": "Seasoned venison in warm tortillas with fresh pineapple salsa. Fast, bold, and everything you want."
    },
    {
        "tag": "Deer / Venison",
        "title": "Slow-Cooker Venison Roast",
        "body": "Venison roast seared hard, then loaded into a slow cooker with onions, garlic, beef broth, and onion soup mix. Eight hours on low and the meat falls apart at the touch of a fork. Serve over mashed potatoes or with crusty bread.",
        "description": "Set it and forget it — venison roast that melts after eight hours in the slow cooker."
    },
    {
        "tag": "Deer / Venison",
        "title": "Venison Salisbury Steak",
        "body": "Ground venison shaped into patties, browned, then simmered in a rich onion gravy. Old-school comfort food made with wild game. Serve over egg noodles or mashed potatoes with the gravy poured over top.",
        "description": "Venison patties in rich onion gravy. Old-school comfort food, upgraded with wild game."
    },
    {
        "tag": "Deer / Venison",
        "title": "Venison Italian Sub",
        "body": "Thinly sliced venison roast, provolone, pepperoncinis, giardiniera, and a robust red wine vinaigrette on a hoagie roll. Pressed on a flattop until the cheese melts and the bread gets crispy.",
        "description": "Venison deli slices, provolone, and pepperoncinis on a hoagie. Pressed and messy and perfect."
    },
    {
        "tag": "Deer / Venison",
        "title": "Venison Potato Soup",
        "body": "A thick, creamy potato soup made richer with shredded venison jerky stirred in at the end. Russets break down into the broth creating a velvety base. Top with chives, crispy fried shallots, and black pepper.",
        "description": "Thick and velvety potato soup with shredded venison jerky stirred in at the end."
    },
    {
        "tag": "Deer / Venison",
        "title": "Venison Curry with Sweet Potato",
        "body": "Ground venison browned and simmered with sweet potatoes, coconut milk, and a bold curry spice blend. The sweetness of the potato tempers the gamey venison and creates a rich, warming stew. Serve over basmati rice with naan.",
        "description": "Venison and sweet potato in coconut curry. Warming, bold, and deeply satisfying."
    },
    {
        "tag": "Deer / Venison",
        "title": "Venison Mushroom Stroganoff",
        "body": "Egg noodles and sautéed venison strips in a rich sour cream and mushroom sauce. The venison stays tender in the quick-cooking sauce and the stroganoff comes together in 30 minutes. A camp classic that never gets old.",
        "description": "Egg noodles and sautéed venison in a rich sour cream and mushroom sauce. 30 minutes, always a hit."
    },
    # BISON
    {
        "tag": "Bison",
        "title": "Bison Steak Frites with Herb Butter",
        "body": "Thick-cut bison sirloin, screaming hot cast iron, compound herb butter melting over the top. Super-high heat and fast timing — bison is leaner than beef and can go from perfect to tough in seconds. Rest it for half the cook time.",
        "description": "Thick-cut bison sirloin, screaming hot cast iron, compound herb butter. Simple and perfect."
    },
    {
        "tag": "Bison",
        "title": "Bison Bourguignon",
        "body": "Bison chuck braised in red wine with pearl onions, carrots, mushrooms, and bacon until fork-tender. This is a cold-weather camp classic that rewards patience. The long braise transforms a tough cut into something extraordinary. Serve over wide egg noodles.",
        "description": "Bison chuck braised in red wine with pearl onions, mushrooms, and bacon. A camp classic."
    },
    {
        "tag": "Bison",
        "title": "Bison Burgers with Caramelized Onions and Gruyère",
        "body": "Ground bison formed into thick patties, griddled to medium-rare, topped with caramelized onions that have been cooking for an hour and a slice of Gruyère that melts into everything. The lean meat stays juicy if you don't overcook it. Serve on a brioche bun with whole-grain mustard.",
        "description": "Thick bison patties, caramelized onions, and Gruyère on a brioche bun. Right at home at camp."
    },
    {
        "tag": "Bison",
        "title": "Bison Beefaroni",
        "body": "Bison ground and browned with onions and garlic, then tossed with rigatoni in a simple tomato sauce with a pinch of cinnamon. One-pot camp meal in 30 minutes that tastes like it took all day.",
        "description": "One-pot bison and rigatoni in a scratch tomato sauce. 30 minutes, camp-friendly, incredible."
    },
    {
        "tag": "Bison",
        "title": "Smoked Bison Brisket",
        "body": "Bison brisket rub-a-dubbed with salt, pepper, garlic, and brown sugar, then smoked low and slow at 225°F for 8 hours until it hits 203°F internal. Wrap in butcher paper, rest for an hour, then cut against the grain. Serve on buns with your favorite BBQ sauce.",
        "description": "Bison brisket smoked 8 hours at 225°F. Wrap, rest, slice, and serve with BBQ sauce."
    },
    {
        "tag": "Bison",
        "title": "Bison Osso Buco",
        "body": "Bison shanks cross-cut, dredged in flour, browned, then braised in white wine and chicken stock with tomatoes, olives, and herbs until the meat falls off the bone. Serve with gremolata — lemon zest, garlic, and parsley — over polenta or risotto.",
        "description": "Bison shanks braised in white wine with tomatoes and olives. Falls off the bone every time."
    },
    {
        "tag": "Bison",
        "title": "Bison Meatballs in Smoky BBQ Sauce",
        "body": "Ground bison rolled into meatballs with bread crumbs, egg, and smoked paprika, browned, then simmered in a tangy scratch BBQ sauce. Serve over creamy coleslaw or on their own as an appetizer that disappears fast.",
        "description": "Bison meatballs in a smoky BBQ sauce. Appetizer that disappears before the main course."
    },
    {
        "tag": "Bison",
        "title": "Grilled Bison Ribeye with Chimichurri",
        "body": "Bison ribeye stripped simple — salt, pepper, high heat, fast sear — then finished with a bright chimichurri of parsley, oregano, garlic, and red wine vinegar. The herbacid cuts right through the rich bison meat. No sauce needed.",
        "description": "Bison ribeye with bright chimichurri. Stripped simple, no sauce needed."
    },
    # WILD BOAR
    {
        "tag": "Wild Boar",
        "title": "Cast Iron Wild Boar Ribs",
        "body": "Wild boar ribs get a brown sugar and chili rub, then braised in apple cider until tender. Finish them in a ripping-hot cast iron to caramelize the glaze. Sticky, sweet, slightly gamey. Serve with a vinegar slaw to cut through the richness.",
        "description": "Brown sugar and chili rubbed boar ribs, braised in cider, finished in hot cast iron."
    },
    {
        "tag": "Wild Boar",
        "title": "Wild Boar Ragu with Pappardelle",
        "body": "Wild boar shoulder slow-braised with San Marzano tomatoes, red wine, and aromatics until the meat falls apart. Shred it into the sauce and toss with wide pappardelle pasta. The slightly gamey, intensely flavored boar elevates this above any standard pork ragu.",
        "description": "Wild boar shoulder slow-braised into a rich ragu over pappardelle. Worth the effort."
    },
    {
        "tag": "Wild Boar",
        "title": "Wild Boar Chorizo and Eggs",
        "body": "Homemade wild boar chorizo crumbled and fried until crispy, served alongside scrambled eggs, warm corn tortillas, and fresh salsa verde. The fattiness of the chorizo plays perfectly against the light eggs. Breakfast in camp doesn't get better than this.",
        "description": "Wild boar chorizo with scrambled eggs and warm tortillas. Breakfast worth waking up for."
    },
    {
        "tag": "Wild Boar",
        "title": "Boar Smoked Sausage with Peppers and Onions",
        "body": "Wild boar smoked sausage sliced and seared until crispy on the edges, piled high with caramelized peppers and onions on a hoagie roll. A hit of yellow mustard and a side of baked beans complete the camp cookout feel.",
        "description": "Boar sausage with caramelized peppers and onions on a hoagie. Classic camp cookout."
    },
    {
        "tag": "Wild Boar",
        "title": "Wild Boar Pozole Rojo",
        "body": "Wild boar shoulder braised in a deep red posole rojo with dried chiles, hominy, and Mexican oregano until the meat shreds apart. Serve in deep bowls with shredded cabbage, radishes, avocado, and a squeeze of lime over tostadas.",
        "description": "Wild boar in a deep red posole rojo with hominy. A Mexican camp classic."
    },
    # DUCK & GOOSE
    {
        "tag": "Wildfowl",
        "title": "Duck Confit Tacos with Pickled Onions",
        "body": "Duck leg confit shredded into crispy shreds, piled into warm corn tortillas with quick-pickled red onions, cotija cheese, and a squeeze of lime. The richness of the duck fat balanced against the bright acid of the pickles makes these tacos unforgettable.",
        "description": "Duck leg confit in warm corn tortillas with pickled onions and cotija. Rich, bright, unforgettable."
    },
    {
        "tag": "Wildfowl",
        "title": "Smoked Goose Breast with Peach Glaze",
        "body": "Goose breast brined overnight in salt-sugar, then smoked at 200°F until medium-rare. The last 20 minutes, hit it with a peach bourbon glaze. Slice thin against the grain and serve on rye with whole-grain mustard and sliced peaches.",
        "description": "Brined, smoked goose breast with peach bourbon glaze. Sliced thin on rye with mustard and peaches."
    },
    {
        "tag": "Wildfowl",
        "title": "Duck Fried Rice",
        "body": "Leftover duck confit shredded into crispy bits and stirred into a hot wok with day-old rice, scrambled eggs, peas, carrots, and heavy soy sauce. The duck fat takes the place of any oil and makes this fried rice exceptionally good.",
        "description": "Shredded duck confit in a hot wok fried rice. The duck fat makes everything better."
    },
    {
        "tag": "Wildfowl",
        "title": "Goose Gumbo",
        "body": "A rich, dark roux-based gumbo with goose giblets, smoked sausage, and okra. Goose liver added at the end creates a velvety depth. Serve over jasmine rice with a side of hot sauce. Plan for a few hours — but worth every minute.",
        "description": "Dark roux gumbo with goose giblets and smoked sausage. A project meal that rewards patience."
    },
    {
        "tag": "Wildfowl",
        "title": "Cast Iron Duck Breast with Cherry Reduction",
        "body": "Score the duck skin in a crosshatch, season heavily with salt and pepper, and sear skin-side down in a cold cast iron that heats up with the meat. Render the fat slowly. Flip for 30 seconds at the end. Plate over a cherry reduction with fresh thyme.",
        "description": "Duck breast seared in its own fat, served with a cherry-thyme reduction. Restaurant-quality camp meal."
    },
    {
        "tag": "Wildfowl",
        "title": "Smoked Duck Eggs Benedict",
        "body": "Cold-smoked duck breast sliced thin, on a toasted English muffin with poached eggs, hollandaise, and chives. The smokiness of the duck plays off the richness of the hollandaise in a way that beef bacon never could.",
        "description": "Cold-smoked duck breast with poached eggs and hollandaise on an English muffin."
    },
    {
        "tag": "Wildfowl",
        "title": "Moulard Duck Prosciutto",
        "body": "Duck breast thinly sliced like prosciutto, cured with salt, sugar, and fresh thyme for 3 days, then hung to dry for 2 weeks. The result is a deeply flavored, silky-sliced cured meat that rivals any imported Italian prosciutto.",
        "description": "Duck breast cured like prosciutto for 2 weeks. Silky, deeply flavored, and worth the wait."
    },
    {
        "tag": "Wildfowl",
        "title": "Canadian Goose Confit Legs",
        "body": "Goose legs confited submerged in their own fat at 200°F for 3 hours until tender. The legs can then be roasted skin-side down for crispy results, or shredded for tacos, pozole, or nachos. The most underrated part of the goose.",
        "description": "Goose legs confited in goose fat, then crisped. The most underrated part of the goose."
    },
    # RABBIT
    {
        "tag": "Rabbit",
        "title": "Southern Fried Rabbit",
        "body": "Whole rabbit cut into pieces, soaked in buttermilk overnight, then dredged in seasoned flour and fried in a cast iron skillet until golden and crispy. Double-dredge for extra crunch. Serve with mashed potatoes drenched in the frying oil and hot honey.",
        "description": "Buttermilk-soaked rabbit, double-dredged and fried crispy in cast iron. A Southern classic."
    },
    {
        "tag": "Rabbit",
        "title": "Rabbit Cacciatore",
        "body": "Rabbit pieces browned hard, then braised in a rich tomato sauce with bell peppers, olives, capers, and white wine. Long braise makes the rabbit meat pull away from the bone and soak up all the sauce. Serve over linguine with heavy pour of braising liquid.",
        "description": "Rabbit braised in white wine tomato sauce with peppers, olives, and capers. Italian wild game done right."
    },
    {
        "tag": "Rabbit",
        "title": "Smoked Rabbit with Apricot Mustard Glaze",
        "body": "Whole rabbit brined, then smoked at 225°F until internal temp hits 160°F. The last 30 minutes, glaze with a mix of apricot preserves and whole-grain mustard. Sweet-savory glaze caramelizes outside, meat stays moist inside.",
        "description": "Brined, smoked whole rabbit with apricot mustard glaze. Sweet, smoky, and fork-tender."
    },
    {
        "tag": "Rabbit",
        "title": "Rabbit and Dumplings",
        "body": "Rabbit braised low and slow in chicken stock until fork-tender, topped with slow-cooked biscuit dumplings that absorb all the braising liquid. Dumplings cook covered in the pot, turning golden and pillowy. Soul food from the hunting camp.",
        "description": "Braised rabbit with slow-cooked biscuit dumplings. Soul food from the hunting camp."
    },
    {
        "tag": "Rabbit",
        "title": "Rabbit Tikka Masala",
        "body": "Rabbit pieces marinated in yogurt and spices, then braised in a rich tomato and cream tikka masala sauce. The gaminess of rabbit takes to the bold spices beautifully. Serve over basmati rice with warm naan and mango chutney.",
        "description": "Rabbit in a bold tikka masala sauce. Unexpected, bold, and completely satisfying."
    },
    # PHEASANT & GROUSE
    {
        "tag": "Pheasant",
        "title": "Pheasant Pot Pie",
        "body": "Pulled pheasant breast and thigh meat in a creamy sauce with carrots, peas, and celery, topped with a buttery, flaky pie crust. The ultimate cold-weather comfort meal — the kind that makes the whole camp smell incredible while it bakes.",
        "description": "Creamy pheasant pot pie with a flaky butter crust. The ultimate cold-weather camp comfort food."
    },
    {
        "tag": "Pheasant",
        "title": "Smoked Pheasant Breast with Gouda",
        "body": "Pheasant breasts brined in apple cider and brown sugar, smoked at 200°F with applewood until just cooked through. Lay sliced breast over baby arugula, shaved Gouda, and a warm bacon vinaigrette. Light, smoky, deeply satisfying.",
        "description": "Apple-brined smoked pheasant with Gouda and arugula. Light, smoky, ready in an hour."
    },
    {
        "tag": "Pheasant",
        "title": "Pheasant Fried Rice",
        "body": "Ground pheasant stir-fried with cold rice, scrambled egg, peas, carrots, and soy sauce in a screaming-hot wok. The lean pheasant stays tender and takes on the wok char beautifully. Top with sliced green onions and sesame oil.",
        "description": "Ground pheasant in a hot wok fried rice. Fast, lean, and full of flavor."
    },
    {
        "tag": "Pheasant",
        "title": "Roasted Pheasant with Bacon and Thyme",
        "body": "Whole pheasant stuffed with bacon, garlic, and thyme, roasted at 400°F until the internal breast temp hits 145°F. The bacon baste keeps the breast juicy and renders into the most incredible pan drippings. Rest 10 minutes before carving.",
        "description": "Whole pheasant stuffed with bacon and thyme, roasted until perfectly medium-rare."
    },
    {
        "tag": "Pheasant",
        "title": "Grouse Piccata with Capers and Lemon",
        "body": "Boneless grouse breasts pounded thin, dredged in flour, and sautéed in butter with capers and lemon juice until golden. The quick cook keeps the lean breast incredibly tender. Serve over egg noodles or mashed potatoes.",
        "description": "Thin-sliced grouse sautéed in butter with capers and lemon. Quick, elegant, and tender."
    },
    # FISH
    {
        "tag": "Fish",
        "title": "Walleye Fish Tacos with Chipotle Cream",
        "body": "Walleye fillets cut into strips, seasoned with cumin and smoked paprika, griddled until crispy at the edges, tucked into warm flour tortillas with chipotle crema, shredded cabbage, and pickled jalapeños. The flaky, mild walleye stands up to the bold toppings.",
        "description": "Crispy walleye strips in flour tortillas with chipotle crema and pickled jalapeños."
    },
    {
        "tag": "Fish",
        "title": "Campfire Cedar Plank Salmon",
        "body": "Salmon fillet seasoned with lemon, dill, and brown sugar, set on a cedar plank, cooked over campfire coals for 20 minutes. The plank infuses subtle smoky, woody flavor and keeps the fish from sticking. Serve with roasted new potatoes and asparagus.",
        "description": "Salmon on a cedar plank over campfire coals. Subtle smoke, simple ingredients, pure result."
    },
    {
        "tag": "Fish",
        "title": "Pan-Fried Trout with Brown Butter and Almonds",
        "body": "Whole trout dusted in flour and seared in a cast iron with brown butter, fresh almonds, and lemon juice. The nutty brown butter and toasted almonds transform a simple campfire fish into something restaurant-made. Serve with crusty bread to soak up the butter.",
        "description": "Cast iron trout with brown butter and toasted almonds. Simple and restaurant-quality."
    },
    {
        "tag": "Fish",
        "title": "Smoked Steelhead Trout Dip",
        "body": "Cold-smoked steelhead trout flaked and blended with cream cheese, horseradish, lemon zest, and fresh dill. Rich, smoky dip that spreads beautifully on crackers or toasted baguette. Make ahead and let flavors meld overnight.",
        "description": "Smoked steelhead blended into a rich, zesty dip. Make ahead and let it meld overnight."
    },
    {
        "tag": "Fish",
        "title": "Walleye Au Gratin",
        "body": "Walleye fillets layered in a casserole with a rich cream sauce, cheddar cheese, and cracker crumbs, baked until bubbly and golden. The fish stays flaky while the topping gets crispy. Converts non-walleye people.",
        "description": "Walleye in a rich cream and cheddar casserole, topped with cracker crumbs. Pure comfort."
    },
    {
        "tag": "Fish",
        "title": "Perch Meunière with Parsley and Lemon",
        "body": "Perch fillets dredged in flour and seared in clarified butter in a screaming-hot stainless steel pan until golden and crisp. Finish with brown butter, lemon, and a heavy hand with fresh parsley. Simple French technique, incredible results.",
        "description": "Perch in brown butter with lemon and parsley. Simple French technique, incredible results."
    },
    {
        "tag": "Fish",
        "title": "MuskieFish Cakes with Cajun Remoulade",
        "body": "Cooked muskie flaked and mixed with mashed potato, egg, and cajun seasoning, formed into patties and pan-fried until golden. Serve with a tangy remoulade sauce. A great way to use any leftover muskie from a big day on the water.",
        "description": "Muskie fish cakes with Cajun remoulade. A great way to use a big muskie catch."
    },
    # CAMPSITE / CAMPFIRE
    {
        "tag": "Campfire",
        "title": "Dutch Oven Campfire Chili — 5 Hours, Worth the Wait",
        "body": "Five hours over coals transforms tough elk shoulder into something that falls apart at the touch of a fork. Brown the meat hard, layer in beans and tomatoes, add chili spices, and let the fire do the rest. Bone-deep warmth and rich gamey flavor.",
        "description": "Elk shoulder chili baked five hours in a Dutch oven. Serve with jalapeño cornbread."
    },
    {
        "tag": "Campfire",
        "title": "Campfire Flatbread with Wild Boar Sausage",
        "body": "Homemade dough stretched into thin flatbreads, cooked directly on campfire coals until charred on the bottom, then topped with crumbled wild boar sausage, caramelized onions, fontina cheese, and fresh rosemary. The char from the coals is the secret ingredient.",
        "description": "Thin flatbreads cooked on coals, topped with boar sausage, fontina, and rosemary."
    },
    {
        "tag": "Campfire",
        "title": "Dutch Oven Sourdough Bread",
        "body": "A sourdough starter activated the night before, shaped into a boule, and baked in a covered Dutch oven over coals for 45 minutes. The steam trapped inside creates a crackling crust and an open, airy crumb. Nothing tastes like camp bread baked in a Dutch oven.",
        "description": "Sourdough boule baked in a covered Dutch oven. Crackling crust, airy inside, camp-made."
    },
    {
        "tag": "Campfire",
        "title": "Campfire Shrimp Boil",
        "body": "Large shrimp, red potatoes, corn on the cob, and smoked sausage boiled together in a massive pot of Old Bay and lemon. Drain and dump onto a picnic table covered in newspaper. Serve with melted butter and extra lemon wedges. Messy, fun, everyone loves it.",
        "description": "Shrimp boil dumped on a newspaper-covered table. Old Bay, lemon, and the best kind of mess."
    },
    {
        "tag": "Campfire",
        "title": "Ember-Roasted Whole Duck",
        "body": "A whole duck stuffed with quartered oranges, thyme, and garlic, buried in hot campfire embers and roasted for 45 minutes, turning once. The skin crisps to a deep mahogany and the meat steams internally. Serve with wild rice and roasted root vegetables.",
        "description": "Whole duck buried in hot embers and roasted. The原始 campfire cooking method."
    },
    {
        "tag": "Campfire",
        "title": "Campfire Breakfast Burritos",
        "body": "Fluffy scrambled eggs, crumbled breakfast sausage, hash browns, peppers, onions, and shredded cheddar rolled into large flour tortillas and grilled over coals until the outside gets crispy and the cheese melts. Wrap in foil to transport.",
        "description": "Eggs, sausage, hash browns, and cheese rolled into tortillas and grilled over coals."
    },
    # DUTCH OVEN
    {
        "tag": "Dutch Oven",
        "title": "Dutch Oven Beef Stew",
        "body": "Bison or elk chuck cubed and browned, then slow-braised with carrots, potatoes, celery, and onion in beef stock with tomato paste and fresh herbs. The cast iron Dutch oven distributes heat evenly and the stew comes out silky and rich.",
        "description": "Slow-braised wild game stew with root vegetables in a Dutch oven. Rich and silky."
    },
    {
        "tag": "Dutch Oven",
        "title": "Dutch Oven Cornbread",
        "body": "Cast iron cornbread baked over coals with whole kernel corn, green chiles, and a touch of honey. The edge gets crispy and golden while the center stays perfectly crumbly. This is the side that disappears first at any camp meal.",
        "description": "Cast iron cornbread baked over coals with corn, chiles, and honey. First to disappear."
    },
    {
        "tag": "Dutch Oven",
        "title": "Dutch Oven Pot Roast with Red Wine and Rosemary",
        "body": "Venison or bison roast seared hard, then slow-braised in red wine with carrots, onion, garlic, and fresh rosemary until fork-tender. The Dutch oven holds heat perfectly and the braising liquid reduces into an incredible jus to pour over sliced meat.",
        "description": "Wild game pot roast slow-braised in red wine and rosemary. Fork-tender and perfect."
    },
    {
        "tag": "Dutch Oven",
        "title": "Dutch Oven Apple Cinnamon Cobbler",
        "body": "Sliced apples tossed with sugar, cinnamon, and a touch of nutmeg, topped with a simple biscuit dough and baked in a covered Dutch oven until bubbly and golden. Serve warm with vanilla ice cream or a drizzle of heavy cream.",
        "description": "Campfire apple cobbler with biscuit topping baked in a Dutch oven. Warm and perfect."
    },
    # SMOKER
    {
        "tag": "Smoker",
        "title": "Smoked Elk Summer Sausage",
        "body": "Elk coarsely ground with pork fat, mixed with curing salt and spices, stuffed into fibrous casings, and smoked at 150°F for 6 hours with hickory or applewood. The low temp slowly sets the sausage and builds smoke ring without cooking the interior too fast.",
        "description": "Elk and pork smoked at 150°F for 6 hours. Slice thin, serve with crackers and cheddar."
    },
    {
        "tag": "Smoker",
        "title": "Smoked Venison Jerky — Teriyaki Style",
        "body": "Venison sliced thin, marinated overnight in soy sauce, worcestershire, brown sugar, garlic, and smoked paprika, then smoked at 130°F for 4-5 hours until dry and leathery. Chewy, sweet, savory with serious smoke flavor. Keeps for weeks.",
        "description": "Thin-sliced venison marinated in teriyaki, smoked at 130°F until leathery. Keeps for weeks."
    },
    {
        "tag": "Smoker",
        "title": "Smoked Duck Breast with Maple and Black Pepper",
        "body": "Duck breasts brined in maple brine, then smoked at 200°F for 90 minutes until medium-rare. The sugar in the brine caramelizes on the exterior. Slice thin and serve on a salad of arugula, shaved pear, and walnut vinaigrette.",
        "description": "Maple-brined smoked duck breast sliced thin over arugula and pear salad."
    },
    {
        "tag": "Smoker",
        "title": "Smoked Pheasant with Sage and Apple",
        "body": "Whole pheasant brined in salt, sugar, and sage, then smoked at 225°F over applewood until golden and just cooked through. The applewood smoke infuses subtle sweetness and the brine keeps the breast incredibly juicy.",
        "description": "Brined pheasant smoked over applewood with sage. Subtle sweetness, incredibly juicy."
    },
    # CAST IRON
    {
        "tag": "Cast Iron",
        "title": "Cast Iron Wild Boar Ribs",
        "body": "Wild boar ribs with brown sugar and chili rub, braised in apple cider until tender. Finish in a ripping-hot cast iron to caramelize the glaze. Sticky, sweet, slightly gamey. Serve with a vinegar slaw.",
        "description": "Boar ribs braised in cider, finished in hot cast iron with a sticky glaze."
    },
    {
        "tag": "Cast Iron",
        "title": "Cast Iron Venison Chop with Peach Compote",
        "body": "Thick-cut venison chops seared in a ripping-hot cast iron to medium-rare, rested, then topped with a warm compote of fresh peaches, brown sugar, and a splash of bourbon. The sweet-tart peach against the mineraly venison is an unexpectedly perfect match.",
        "description": "Thick-cut venison chop with warm peach compote. Unexpectedly perfect flavor pairing."
    },
    {
        "tag": "Cast Iron",
        "title": "Cast Iron Quail with Honey and Thyme",
        "body": "Semiboneless quail scored on the breast, seared skin-side down in cold cast iron that heats up with the bird. Render the skin slowly until deep golden. Flip for 30 seconds, then plate over a drizzle of honey-thyme reduction.",
        "description": "Cast iron quail with slow-rendered skin, finished with honey and thyme. Small bird, big flavor."
    },
    {
        "tag": "Cast Iron",
        "title": "Cast Iron Reverse-Seared Elk Ribeye",
        "body": "Elk ribeye roasted low in a cast iron at 275°F until internal hits 115°F, then seared in a smoking-hot pan for 90 seconds per side. The reverse sear gives you a perfect medium-rare from edge to edge with a serious bark on the outside.",
        "description": "Elk ribeye reverse-seared — low roast, then hard sear. Perfect medium-rare, serious bark."
    },
    # SIDES
    {
        "tag": "Sides",
        "title": "Smoked Wild Mushrooms",
        "body": "Mixed wild mushrooms — chanterelles, porcini, whatever the forest gives you — tossed with olive oil, garlic, and thyme, then smoked at 180°F for 45 minutes until leathery and intense. Use to top steaks, fold into risotto, or scatter over creamy polenta.",
        "description": "Wild mushrooms smoked with garlic and thyme. Intense, leathery, and incredibly versatile."
    },
    {
        "tag": "Sides",
        "title": "Cast Iron Campfire Beans",
        "body": "Dried navy beans soaked overnight, then slow-baked in a Dutch oven with molasses, ketchup, mustard, and salt pork for 6 hours. The beans absorb everything and come out glossy, sweet, and smoky. The ultimate side for any smoked meat.",
        "description": "Slow-baked beans with molasses, ketchup, and mustard. Six hours and completely worth it."
    },
    {
        "tag": "Sides",
        "title": "Campfire Grilled Street Corn",
        "body": "Corn on the cob grilled directly over campfire coals until charred in spots, then rolled in a mixture of mayo, cotija cheese, chili powder, and lime. The char and the creamy, spicy mixture make this the most-requested side at any campout.",
        "description": "Grilled corn rolled in mayo, cotija, and chili powder. The most-requested side at campouts."
    },
]

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
        content = content.replace('<div class="featured">', f'{featured_section}\n<DEL>', 1)
        content = content.replace('<DEL>', '')
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