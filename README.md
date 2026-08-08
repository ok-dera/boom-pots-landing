# Boom Pots — landing page

Single static page for **Boom Pots** by Sokando Games. Plain HTML, Tailwind v4 compiled to a
static stylesheet, and one inline script. No framework, no runtime build. Deploys to GitHub
Pages as-is.

```
index.html          the whole page
src/input.css       Tailwind source + design tokens (edit this, not styles.css)
styles.css          compiled output — committed so Pages can serve it directly
assets/screens/     the seven game screenshots
assets/pots/        transparent pot renders
PRODUCT.md          who it's for, voice, anti-references
DESIGN.md           the colour, type and surface system
```

## Working on it

```bash
nvm use 20
npm install
npm run dev      # rebuilds styles.css on change
npm run serve    # http://localhost:4173
```

`npm run build` produces the minified `styles.css`. **Commit `styles.css`** — GitHub Pages
serves the repo contents directly and does not run a build.

## Three things to fill in before launch

All three live at the top of the `<script>` block at the bottom of `index.html`.

```js
const STORE = { ios: "", android: "" };   // real store URLs
const NOTIFY_ENDPOINT = "";               // e.g. https://formspree.io/f/xxxxxxx
const TRAILER_ID = "";                    // YouTube video id only, e.g. dQw4w9WgXcQ
```

- **`STORE`** — while empty the buttons read "Coming soon to…" and jump to the notify form.
  Paste a URL and that button becomes a real "Download on…" link automatically.
- **`NOTIFY_ENDPOINT`** — while empty the form hands off to the visitor's mail client
  (`NOTIFY_MAILTO`). Any endpoint that accepts a JSON `{ email }` POST works.
- **`TRAILER_ID`** — while empty the trailer section is hidden entirely. Set it and the section
  appears, along with a "Watch the trailer" link in the hero. The player is a facade: the
  poster is a plain image and **no YouTube script loads until someone presses play**.

Also update before launch:

- `privacy.html` — the footer links to it and it does not exist yet.
- `mailto:hello@sokandogames.com` in the footer and in `NOTIFY_MAILTO`.

## Art

Every image path degrades on its own: if a file is missing, the `onerror` handler removes the
element rather than leaving a broken image. The page is presentable without any of these, but
it is much better with them.

| Path | What it is |
|---|---|
| `assets/icon.png` | app icon, 192×192 (also the favicon, so it stays PNG) |
| `assets/logo.webp` | **BOOM POTS** wordmark, lifted off its white plate |
| `assets/pots/clay.webp` | plain terracotta pot, two dots |
| `assets/pots/spiral.webp` | dark brown spiral + meander pot |
| `assets/pots/flame.webp` | red and gold maze pot |
| `assets/pots/amphora.webp` | green handled amphora |
| `assets/pots/bomb.webp` | cream and red pot with a lit fuse |
| `assets/pots/slime.webp` | black handled pot dripping green |
| `assets/fx/coin.webp` | the game's coin — confetti, and the smash burst |
| `assets/fx/star.webp` | the game's star — confetti |
| `assets/fx/bolt.webp` | the game's energy bolt — confetti |
| `assets/fx/booster-{bomb,potion,glue}.webp` | the three booster orbs, sliced from `tuto2.png` |
| `assets/sokando-text.webp` | Sokando's white wordmark (footer is dark, so it works) |
| `assets/bg/valley.jpg` | green river valley, sliced from the world map |
| `assets/bg/savanna.jpg` | savanna skull ridge, sliced from the world map |
| `assets/bg/parchment.jpg` | paper grain + ruin glyphs, from the game's popup panel |
| `assets/sokando-mark.webp` | Sokando's gold fingerprint mark |
| `assets/og.jpg` | 1200×630 social card, screenshotted from the hero |
| `assets/screens/*.jpg` | seven in-game screenshots |

Originals live in `assets/incoming/` (gitignored). They were processed with
`tools/art.py` where keying was needed, which keys backgrounds by flood-filling inward from the border, so white
*inside* the art (the ice letters of BOOM, the cream bands on a pot) survives while the white
plate around it does not. Three of the four pot renders had a white selection glow baked in;
that was stripped the same way.

Two things worth knowing before swapping art:

- **Pots** should arrive as transparent PNG, square-ish, pot centred, **no drop shadow or glow
  baked in** — the page adds its own. They are shipped as WebP at 480px wide, which is 2x the
  largest size any of them renders at.
- **Sokando's lockup is split into mark and wordmark and laid out horizontally.** Stacked, it
  is unreadable at footer scale. The footer ground is dark, so the white wordmark works as
  drawn — if the footer ever goes light again, the wordmark will vanish and the name has to be
  set in type instead.
- **The wordmark source is already transparent** — `logo-source-3.png` is RGBA with 81% of its
  pixels at alpha 0, including the warm bloom. It needs no keying at all: trim the transparent
  margin, scale, convert. Do not run it through `art.py`. An image viewer showing a grey
  backdrop behind it is showing you the viewer, not the file; check the alpha channel before
  concluding anything. `.logo-glow` only adds a soft outer halo and a contact shadow on top.

## Deploying to GitHub Pages

1. Push this folder to a repo.
2. Settings → Pages → Source: **Deploy from a branch**, branch `main`, folder `/ (root)`.
3. `.nojekyll` is already committed so `_`-prefixed paths are served normally.

Every asset path is relative, so it works at both `user.github.io/repo/` and a custom domain.

## Accessibility notes

Checked and intentional, don't regress these:

- Trail reveal animation is gated behind a `.js` class on `<html>`. With JS off the content is
  plain visible text, not `opacity: 0`.
- `prefers-reduced-motion` kills the float, the drift and the reveal. The pot still breaks and
  still increments the counter, just without the shard burst.
- Gold is a fill colour only. It is never small text on a light ground.
- The coin counter is `aria-live="polite"` so it announces when a pot breaks.
- Every screenshot has alt text describing what is happening in the game, not "screenshot 3".
