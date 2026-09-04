# Wishlist-aware recommendations — clickable prototype

Eight mobile screens at a fixed 390 × 844, built from the real Myntra layout and real
product photography. No Stitch, no generated imagery.

## Run it

Double-click `index.html`. Everything is relative and self-contained, so no server is
required. To serve it instead:

```bash
python3 -m http.server 8765 --directory deck/app-mockups
# then open http://127.0.0.1:8765/index.html
```

## The path through it

1. **Search — "Black Tops Women"** (`1-search.html`). The strip below the promo chips is
   the feature: the black tops the user already saved, surfaced at the moment she is
   searching for exactly that. The rail scrolls horizontally — the header reads
   "5 matches" and the last cards peek off the right edge to signal there is more.
2. **Any product** — all five visible tops open a real page, so an evaluator can tap
   anything. Each has a **Pair with this** rail of saved *bottoms*, never tops.
3. **Dismissal** — the `×` on any saved card greys it in place, badges it HIDDEN and
   offers UNDO. `3-dismiss.html` is the static still of that state.
4. **Why this?** — opens `4-preferences.html`, which explains the reasoning before
   offering any controls.

## Screens

| File | Purpose |
|---|---|
| `1-search.html` | Surface A — wishlist strip in search results |
| `2-pdp-1-hm-graphic-tee.html` | Surface B — jeans, shorts, track pants |
| `2-pdp-2-sassafras-high-neck.html` | Surface B — pants, jeans, white shorts |
| `2-pdp-3-stylecast-printed.html` | Surface B — shorts, pants, track pants |
| `2-pdp-4-stylecast-slyck-flared.html` | Surface B — jeans, white shorts, pants |
| `2-pdp-5-glitchez-striped.html` | Surface B — shorts, jeans, pants |
| `2-pdp-6-roadster-ribbed.html` | Surface B — jeans, white shorts, pants (placeholder top) |
| `2-pdp-7-dressberry-puff.html` | Surface B — shorts, track pants, jeans (placeholder top) |
| `3-dismiss.html` | Mitigation 1 — dismissal with undo |
| `4-preferences.html` | Mitigation 2 — transparency and consent |

## Editing

`1-search.html` and `4-preferences.html` are hand-authored. Everything else is
generated:

```bash
python3 build_pdps.py      # 5 product pages + 3-dismiss.html
./render.sh                # PNGs at 2x into render/, all identical size
```

Products, prices and pairings are plain data at the top of `build_pdps.py` — edit the
`TOPS` and `BOTTOMS` dictionaries and rerun. `3-dismiss.html` is derived from
`1-search.html`, so the two cannot drift apart.

`_shared.css` holds the design tokens (Myntra pink is `#FF3F6C`). `_proto.js` handles
the two interactions: tapping a card navigates, tapping `×` hides with undo.

## Note on the data

Every price, discount and rating came from the real product pages, with one exception:
the H&M tee's rating of 4.3 / 2.1k is invented, since only its price was supplied.
