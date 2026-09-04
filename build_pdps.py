#!/usr/bin/env python3
"""Generate one product page per top shown on the search screen.

A working demo lets the evaluator tap any product, so every visible top needs its
own 'Pair with this' rail. Rails are drawn from a shared pool of saved bottoms and
assigned per top below, so the pairing never repeats the same trio twice in a row.
"""

import pathlib
import re

OUT = pathlib.Path(__file__).parent

# ---------------------------------------------------------------- saved bottoms
BOTTOMS = {
    "shorts": dict(
        img="bottom-shorts.png", brand="SASSAFRAS BASICS",
        name="Washed High-Rise Denim Shorts",
        now="₹614", mrp="₹1499", off="(59% OFF)",
    ),
    "jeans": dict(
        img="bottom-jeans.png", brand="glitchez",
        name="Wide Leg Light Fade Jeans",
        now="₹990", mrp="₹2199", off="(₹1209 OFF)",
    ),
    "pants": dict(
        img="bottom-pants.png", brand="Blissclub",
        name="The Ultimate Straight Pants Lite",
        now="₹999", mrp="₹1999", off="(50% OFF)",
    ),
    "track": dict(
        img="bottom-track.png", brand="HRX by Hrithik Roshan",
        name="Rapid-Dry Flared Training Track Pants",
        now="₹629", mrp="₹1499", off="(₹870 OFF)",
    ),
    "white": dict(
        img="bottom-white-shorts.png", brand="DressBerry",
        name="High Rise Clean Look Denim Shorts",
        now="₹867", mrp="₹2855", off="(70% OFF)",
    ),
}

# --------------------------------------- saved complements beyond bottoms
# A top's wishlist companions are not only bottoms — footwear and layering complete the
# look too. These are shared across tops (saved shoes/shrugs pair with any top).
# Footwear = real saved products. Layering image is still a PLACEHOLDER
# (assets/pair-shrug.png) — swap it and its fields when the real item is supplied.
FOOTWEAR = [
    dict(img="pair-heels.png", brand="Lavie",
         name="Party Block Mules with Bows", now="₹761", mrp="₹3999", off="(81% OFF)"),
    dict(img="pair-sneakers.png", brand="ASICS",
         name="JOLT 5 Round-Toe Running Shoes", now="₹3659", mrp="₹5999", off="(39% OFF)"),
]
LAYERING = [
    dict(img="pair-shrug.png", brand="SASSAFRAS",
         name="Longline Open-Front Shrug", now="₹899", mrp="₹1,999", off="(55% OFF)"),
]

# ------------------------------------------------- tops visible on the search screen
# `saved` marks tops that are themselves in the wishlist, so the CTA reads WISHLISTED.
TOPS = [
    dict(
        slug="hm-graphic-tee", img="oversized-tee-card.png", saved=True,
        brand="H&M", name="Oversized Graphic Tee",
        rating="4.3", count="2.1k Ratings",
        now="₹899", mrp="₹1299", off="(31% OFF)",
        pairs=["jeans", "shorts", "track"],
    ),
    dict(
        slug="sassafras-high-neck", img="saved-top-2.png", saved=True,
        brand="SASSAFRAS", name="High Neck Cropped Top",
        rating="4.4", count="68.5k Ratings",
        now="₹409", mrp="₹999", off="(59% OFF)",
        pairs=["pants", "jeans", "white"],
    ),
    dict(
        slug="stylecast-printed", img="saved-top-1.png", saved=True,
        brand="STYLECAST", name="Printed High Neck Top",
        rating="4.6", count="394 Ratings",
        now="₹517", mrp="₹1399", off="(63% OFF)",
        pairs=["shorts", "pants", "track"],
    ),
    dict(
        slug="stylecast-slyck-flared", img="saved-top-3.png", saved=False,
        brand="STYLECAST X SLYCK", name="Flared Sleeve Shirt Style Top",
        rating="4.6", count="394 Ratings",
        now="₹606", mrp="₹1799", off="(66% OFF)",
        pairs=["jeans", "white", "pants"],
    ),
    dict(
        slug="glitchez-striped", img="striped-top.png", saved=False,
        brand="glitchez", name="Striped Top",
        rating="3.5", count="41 Ratings",
        now="₹405", mrp="₹999", off="(59% OFF)",
        pairs=["shorts", "jeans", "pants"],
    ),
    # The two extra "more matches" black tops (scroll to reveal). Real Myntra products.
    dict(
        slug="sassafras-ribbed", img="saved-top-4.png", saved=True,
        brand="SASSAFRAS", name="Black Ribbed Square-Neck Fitted Top",
        rating="4.3", count="1.1k Ratings",
        now="₹569", mrp="₹1299", off="(56% OFF)",
        pairs=["jeans", "white", "pants"],
    ),
    dict(
        slug="glitchez-offshoulder", img="sim-chemistry.png", saved=True,
        brand="GLITCHEZ", name="Gathers Detail Off-Shoulder Fitted Top",
        rating="4.1", count="720 Ratings",
        now="₹559", mrp="₹1299", off="(57% OFF)",
        pairs=["shorts", "track", "jeans"],
    ),
]

# ------------------------------------------------- SIMILAR PRODUCTS pool
# Every image here is distinct from all wishlist-strip and PDP-hero photos, so
# "Similar products" can never repeat a saved item or a page's own hero. Images that
# double as search-grid cards keep the SAME brand/name here, so one photo == one product
# everywhere in the demo.
SIMILAR = [
    dict(img="sim-corsica.png", brand="CORSICA", name="Embellished Round-Neck Top",
         now="₹456", mrp="₹1499", off="(70% OFF)"),
    dict(img="sim-tiedye.png", brand="DRESSBERRY", name="Tie & Dye Bell-Sleeve Top",
         now="₹649", mrp="₹1499", off="(56% OFF)"),
    dict(img="grid-roadster.png", brand="Roadster", name="Lace-Trim Cami Top",
         now="₹524", mrp="₹1199", off="(56% OFF)"),
]

STAR = ('<svg width="10" height="10" viewBox="0 0 10 10" fill="#03A685">'
        '<path d="M5 0l1.3 3.2L9.7 3.6 7.2 5.9l.8 3.5L5 7.6 2 9.4l.8-3.5L.3 3.6l3.4-.4z"/></svg>')
XMARK = ('<svg width="7" height="7" viewBox="0 0 8 8" fill="none">'
         '<path d="M1 1l6 6M7 1l-6 6" stroke="#282C3F" stroke-width="1.3" stroke-linecap="round"/></svg>')
HEART_FILLED = ('<svg width="13" height="12" viewBox="0 0 20 18" fill="#FF3F6C">'
                '<path d="M10 16.5C-3.2 9.1 5.1-2.4 10 3.6 14.9-2.4 23.2 9.1 10 16.5Z"/></svg>')


def slug_to_file(slug):
    for i, t in enumerate(TOPS, start=1):
        if t["slug"] == slug:
            return f"2-pdp-{i}-{slug}.html"
    return "1-search.html"


def comp_card(item):
    """One saved-complement card, used for bottoms, footwear and layering alike."""
    price = f'<span class="now">{item["now"]}</span>'
    if item.get("mrp"):
        price += f'<span class="mrp">{item["mrp"]}</span>'
    if item.get("off"):
        price += f'<span class="off">{item["off"]}</span>'
    return f'''        <div class="wl-card">
          <div class="wl-img">
            <img src="assets/{item["img"]}" alt="{item["brand"]} {item["name"]}">
            <span class="saved">SAVED</span>
            <span class="xbtn">{XMARK}</span>
          </div>
          <div class="wl-brand">{item["brand"]}</div>
          <div class="wl-desc">{item["name"]}</div>
          <div class="price">{price}</div>
        </div>'''


def rail(items):
    return "\n".join(comp_card(it) for it in items)


def sim_card(item):
    """A 'Similar products' card — display-only, no SAVED badge and no wishlist ×."""
    price = f'<span class="now">{item["now"]}</span>'
    if item.get("mrp"):
        price += f'<span class="mrp">{item["mrp"]}</span>'
    if item.get("off"):
        price += f'<span class="off">{item["off"]}</span>'
    return f'''      <div class="wl-card">
        <div class="wl-img"><img src="assets/{item["img"]}" alt="{item["brand"]} {item["name"]}"></div>
        <div class="wl-brand">{item["brand"]}</div>
        <div class="wl-desc">{item["name"]}</div>
        <div class="price">{price}</div>
      </div>'''


def similar_strip(idx):
    """Three items from the SIMILAR pool, rotated per page so the pages differ.
    Never draws from the wishlist, so it can't repeat a saved item."""
    start = (idx - 1) % len(SIMILAR)
    chosen = [SIMILAR[(start + i) % len(SIMILAR)] for i in range(3)]
    return "\n".join(sim_card(it) for it in chosen)


def render(idx, top):
    cta_second = ("WISHLISTED" if top["saved"] else "WISHLIST")
    bottoms_rail = rail(BOTTOMS[k] for k in top["pairs"])
    footwear_rail = rail(FOOTWEAR)
    layering_rail = rail(LAYERING)
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Product page · {top["brand"]} {top["name"]} — Pair with this</title>
<link rel="stylesheet" href="_shared.css">
</head>
<body>

<div class="phone">

  <div class="status">
    <span>19:44</span>
    <span class="icons">
      <svg width="17" height="11" viewBox="0 0 17 11" fill="currentColor"><rect x="0" y="7" width="3" height="4" rx="1"/><rect x="4.5" y="5" width="3" height="6" rx="1"/><rect x="9" y="2.5" width="3" height="8.5" rx="1"/><rect x="13.5" y="0" width="3" height="11" rx="1"/></svg>
      <svg width="16" height="12" viewBox="0 0 16 12" fill="currentColor"><path d="M8 11.2 10.1 8.8a3.1 3.1 0 0 0-4.2 0L8 11.2Zm-4-4.5a6.6 6.6 0 0 1 8 0l1.4-1.6a8.7 8.7 0 0 0-10.8 0L4 6.7ZM8 .8a11 11 0 0 0-7.1 2.6L2.3 5A9 9 0 0 1 8 3a9 9 0 0 1 5.7 2l1.4-1.6A11 11 0 0 0 8 .8Z"/></svg>
      <svg width="26" height="12" viewBox="0 0 26 12" fill="none"><rect x=".6" y=".6" width="21" height="10.8" rx="3" stroke="currentColor" stroke-opacity=".38"/><rect x="2.2" y="2.2" width="17" height="7.6" rx="1.8" fill="currentColor"/><path d="M23.2 4.2v3.6a2 2 0 0 0 0-3.6Z" fill="currentColor" fill-opacity=".45"/></svg>
    </span>
  </div>

  <div class="pdp-head">
    <span data-href="1-search.html"><svg width="9" height="16" viewBox="0 0 9 16" fill="none"><path d="M8 1 1.5 8 8 15" stroke="#282C3F" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg></span>
    <img class="mlogo" src="assets/myntra-logo.png" alt="Myntra">
    <span class="sp"></span>
    <svg width="19" height="19" viewBox="0 0 20 20" fill="none"><circle cx="8.5" cy="8.5" r="6.2" stroke="#282C3F" stroke-width="1.6"/><path d="m13.2 13.2 4.3 4.3" stroke="#282C3F" stroke-width="1.6" stroke-linecap="round"/></svg>
    <svg width="19" height="19" viewBox="0 0 20 18" fill="none"><path d="M10 16.2C-3 8.9 5.2-2.3 10 3.6 14.8-2.3 23 8.9 10 16.2Z" stroke="#282C3F" stroke-width="1.6" stroke-linejoin="round"/></svg>
    <svg width="19" height="19" viewBox="0 0 18 20" fill="none"><path d="M2 6h14l-1 12H3L2 6Z" stroke="#282C3F" stroke-width="1.6" stroke-linejoin="round"/><path d="M6 7.5V5a3 3 0 0 1 6 0v2.5" stroke="#282C3F" stroke-width="1.6" stroke-linecap="round"/></svg>
  </div>

  <div class="hero">
    <img src="assets/{top["img"]}" alt="{top["brand"]} {top["name"]}">
    <span class="count">1/5</span>
  </div>

  <div class="body">

    <div class="pdp-info">
      <div class="pdp-brand">{top["brand"]}</div>
      <div class="pdp-name">{top["name"]}</div>
      <span class="rate-pill">
        {top["rating"]} {STAR}
        <span style="color:var(--divider)">|</span><span class="cnt">{top["count"]}</span>
      </span>
      <div class="pdp-price">
        <span class="now">{top["now"]}</span>
        <span class="mrp">MRP <s>{top["mrp"]}</s></span>
        <span class="off">{top["off"]}</span>
      </div>
      <div class="tax">inclusive of all taxes</div>
    </div>

    <div class="size-row">
      <span class="lbl">SELECT SIZE</span>
      <span class="chart">SIZE CHART ›</span>
    </div>
    <div class="sizes">
      <span>XS</span><span>S</span><span class="on">M</span><span>L</span><span>XL</span><span>XXL</span>
    </div>

    <div class="cta">
      <button class="bag">
        <svg width="14" height="15" viewBox="0 0 18 20" fill="none"><path d="M2 6h14l-1 12H3L2 6Z" stroke="#fff" stroke-width="1.7" stroke-linejoin="round"/><path d="M6 7.5V5a3 3 0 0 1 6 0v2.5" stroke="#fff" stroke-width="1.7" stroke-linecap="round"/></svg>
        ADD TO BAG
      </button>
      <button>
        {HEART_FILLED}
        {cta_second}
      </button>
    </div>

    <!-- ============ PAIR WITH THIS — the feature ============ -->
    <div class="wl pair">
      <div class="wl-head">
        <div>
          <div class="wl-title">
            {HEART_FILLED}
            Pair with this · from your wishlist
          </div>
          <div class="wl-sub">You saved these — they finish this look</div>
        </div>
        <span class="why" data-href="4-preferences.html">Why this?</span>
      </div>

      <div class="pair-chips">
        <span class="pchip on" data-cat="bottoms">Bottoms</span>
        <span class="pchip" data-cat="footwear">Footwear</span>
        <span class="pchip" data-cat="layering">Layering</span>
      </div>

      <div class="wl-rail" data-cat="bottoms">
{bottoms_rail}
      </div>
      <div class="wl-rail" data-cat="footwear" hidden>
{footwear_rail}
      </div>
      <div class="wl-rail" data-cat="layering" hidden>
{layering_rail}
      </div>
    </div>

    <div class="sect-title">SIMILAR PRODUCTS</div>
    <div class="wl-rail" style="padding:0 14px">
{similar_strip(idx)}
    </div>

  </div>

  <div class="fade-bottom thin"></div>

</div>

<script src="_proto.js"></script>
</body>
</html>
'''


def build_dismiss():
    """Static still of the dismissal state, derived from the search screen so the two
    can never drift apart. The live prototype produces this same state via _proto.js."""
    src = (OUT / "1-search.html").read_text()

    src = src.replace(
        "<title>Surface A · Search results — From your wishlist</title>",
        "<title>Mitigation 1 · Dismissing a wishlist suggestion</title>")

    # Grey the third saved card (STYLECAST printed) in place. Anchor on its unique image
    # so the still stays correct no matter how many cards precede or follow it.
    open_tag = '<div class="wl-card" data-href="2-pdp-3-stylecast-printed.html">'
    assert open_tag in src, "search screen markup changed; update build_dismiss()"
    src = src.replace(open_tag, '<div class="wl-card hidden">', 1)

    img_marker = ('<img src="assets/saved-top-1.png" '
                  'alt="STYLECAST printed high neck top">')
    assert img_marker in src, "dismissed card image changed; update build_dismiss()"
    src = src.replace(
        img_marker,
        img_marker + '\n            <span class="hidden-tag"><span>HIDDEN</span></span>',
        1)

    src = src.replace("    <!-- ============ organic results ============ -->",
                      '''    <div class="snackbar">
      <div class="msg">Hidden from recommendations.<b>Remove from wishlist too?</b></div>
      <span class="remove">REMOVE</span>
      <span class="undo">UNDO</span>
    </div>

    <!-- ============ organic results ============ -->''')

    (OUT / "3-dismiss.html").write_text(src)
    print("wrote 3-dismiss.html  (derived from 1-search.html)")


def main():
    # clear previously generated pages so renamed slugs don't linger
    for stale in OUT.glob("2-pdp-*.html"):
        stale.unlink()
    for i, top in enumerate(TOPS, start=1):
        path = OUT / f"2-pdp-{i}-{top['slug']}.html"
        path.write_text(render(i, top))
        print(f"wrote {path.name}  ({' + '.join(top['pairs'])})")
    build_dismiss()


if __name__ == "__main__":
    main()
