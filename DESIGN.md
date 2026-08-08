# DESIGN.md — Boom Pots

The visual system for the Boom Pots landing page. Every color here was sampled out of the
game's own screenshots in `assets/screens/`, not invented.

## Direction: The Dome

Symmetric and centred, following the shape of the candycrush.com landing page: a sky band with
confetti and a skyline, the wordmark sitting in it, then a wide arch rising out of the horizon
that the rest of the page lives on.

Translated into this game's world rather than that one's:

- **Sky** — the painted river valley under a heavy scrim, dotted, with the game's own coins,
  stars and energy bolts drifting through it.
- **Flanking pair** — two large pots either side of the wordmark, the way the reference flanks
  its logo with a candy cluster and an egg. Decorative.
- **The dome** — fired clay instead of pink. Its arch rises *behind* the wordmark, so the lower
  half of the logo sits on clay and the upper half on sky. Everything from the headline down
  lives on it.
- **Cards** — parchment on clay, one screenshot each, dark display titles.

The dome is pulled up under the wordmark with a negative margin on the sky band, and its top
padding is increased by the same amount so the headline does not ride up with it. Change one
without the other and either the arch stops overlapping the logo or a dead band of clay opens
between them.

Colour is **drenched**: green sky, clay dome, parchment cards, savanna footer. Structural
grammar is borrowed from casual-game UI (Candy Crush's CSS was the reference for *how*, never
for *what*): chunky surfaces with a top inset highlight and a bottom inset shadow, generous
radii, sticker headlines with layered outlines, and torn parchment strips.

**The dome's arch is elliptical on purpose** — `50% 50% 0 0 / 260px` — so it stays a wide
shallow arch at every width. A single-value radius turns into a circle on narrow screens.

## Color

OKLCH. No `#000`, no `#fff`. Every neutral is tinted warm toward the terracotta hue.

### Sampled from the game

| Token | OKLCH | Sampled from |
|---|---|---|
| `--jungle` | `oklch(0.79 0.17 132)` | grass highlight, `map-jungle-close.jpg` |
| `--jungle-mid` | `oklch(0.64 0.16 138)` | mid grass |
| `--jungle-deep` | `oklch(0.42 0.09 131)` | canopy shadow, `how-to-play.jpg` |
| `--jungle-ink` | `oklch(0.28 0.06 128)` | deepest foliage |
| `--parchment` | `oklch(0.87 0.06 84)` | level panel, `level-start.jpg` |
| `--parchment-hi` | `oklch(0.94 0.04 88)` | panel highlight |
| `--parchment-shade` | `oklch(0.75 0.08 76)` | panel shadow |
| `--gold` | `oklch(0.86 0.14 84)` | the button fill, every screen |
| `--gold-deep` | `oklch(0.74 0.16 72)` | button lower stop |
| `--gold-edge` | `oklch(0.52 0.14 55)` | button outline |
| `--savanna` | `oklch(0.57 0.09 62)` | dry rock, `map-savanna.jpg` |
| `--savanna-deep` | `oklch(0.40 0.07 52)` | ridge shadow |
| `--terracotta` | `oklch(0.55 0.12 48)` | pot body |
| `--terracotta-deep` | `oklch(0.38 0.09 45)` | pot rim |
| `--cyan` | `oklch(0.83 0.11 218)` | the star icon |
| `--grape` | `oklch(0.60 0.21 320)` | booster orbs |
| `--ink` | `oklch(0.26 0.04 60)` | warm dark brown — all body text |

### Color strategy

**Drenched**. Three grounds, top to bottom:

1. **Sky** — the valley map under a green scrim. Wordmark and confetti.
2. **Dome** — fired clay. Everything from the headline to the notify form.
3. **Ridge** — the savanna map under a dark scrim. Footer.

Parchment is the only surface color. Gold is the only button color. Grape and cyan appear once
each, as small accents, and never carry meaning alone.

### Contrast rules

- `--gold` is a **fill** color. Text on gold is always `--gold-edge` or darker (≥ 8:1). Gold is
  never used as text on parchment or on green.
- Body copy on `--jungle-deep` is `--parchment-hi` (≈ 8:1), never pure white.
- Body copy on `--parchment` is `--ink` (≈ 10:1).
- Focus ring is `--cyan` at 3px with a 2px `--ink` inner ring so it survives on both gold and
  green.

## Typography

Voice words: **sun-baked, hand-painted, mischievous.**

- **Display — Chango** (Google Fonts, single weight). Drawn after Latin American poster
  lettering: heavy, slightly irregular, warm. It reads as a painted market sign rather than a
  vector cartoon face. Used for section eyebrows, card titles, and the type fallback if the wordmark image is missing.
  Rejected by reflex first: Luckiest Guy, Fredoka, Baloo 2, Titan One — the casual-game
  training-data defaults.
- **Body — Nunito Sans** (400 / 600 / 800). Round terminals echo the pot silhouettes; stays
  legible at 15px on a phone in sunlight.

Scale is fluid `clamp()`, ratio ≥ 1.3 between steps:

```
--step-0: clamp(1rem, 0.95rem + 0.25vw, 1.0625rem)   body
--step-1: clamp(1.3rem, 1.2rem + 0.5vw, 1.5rem)      lead
--step-2: clamp(1.75rem, 1.5rem + 1.2vw, 2.4rem)     headline
--step-3: clamp(2.4rem, 1.9rem + 2.4vw, 4rem)        section headings
--step-4 is only used by the type fallback wordmark
--step-4: clamp(3.2rem, 2.2rem + 5vw, 7rem)          hero / wordmark
```

Measure capped at 62ch. Light-on-dark blocks get +0.06 line-height.

### Sticker headline treatment

Display type on colored grounds gets a layered outline, not a drop shadow: a hard
`-webkit-text-stroke` in `--jungle-ink` plus a stacked `text-shadow` offset down 4–6px in the
same ink. This is the casual-game grammar the audience reads instantly. Never a gradient fill.

## Surfaces

One surface recipe, used everywhere. Chunky, not flat:

```css
background: var(--parchment);
border: 3px solid var(--parchment-shade);
border-radius: 22px;
box-shadow:
  inset 0 3px 0 0 var(--parchment-hi),      /* lit from above */
  inset 0 -4px 0 0 var(--parchment-shade),  /* thickness       */
  0 6px 0 0 oklch(0.62 0.08 70),            /* the slab edge   */
  0 14px 24px -8px oklch(0.28 0.06 50 / 0.45);
```

Buttons use the same recipe in gold and lose 4px of `translateY` plus the slab edge on
`:active`, so they physically compress. Radii: `12px` small, `22px` default, `999px` pill.

## Grounds

Two of the three bands sit on the game's own painted world map (`map1-4_road.png`, sliced in its
natural orientation so nothing is flipped): the green river valley under the hero, the savanna
skull ridge under the download band. The trail between them stays a gradient, because no single
slice of the map spans green to ochre.

**The scrim is what sets contrast, not the token.** The map is far too bright to put text on
directly: grass sits around L 0.80 and the sand path around L 0.92. A radial scrim at
0.84 → 0.94 alpha holds the effective ground near L 0.36 and leaves the map as texture. Text
contrast on these bands is verified by sampling rendered pixels, not by reading token values.
Lowering a scrim alpha means re-measuring.

Surfaces carry real paper grain and faint ruin glyphs (`bg/parchment.jpg`, cropped from the
game's popup panel) multiplied under the parchment colour.

## Wordmark

The supplied artwork is transparent RGBA and carries its own warm bloom, so it is used as-is.
`.logo-glow` adds only a soft outer halo and a contact shadow; a second full glow on top turns
the letterforms muddy.

## Torn parchment chrome

The game frames every screen with a torn paper strip top and bottom. The page does the same: an
inline SVG with an irregular torn edge, `preserveAspectRatio="none"`, filled `--parchment` with
a `--parchment-shade` deckle line and faint ruin glyphs at 12% opacity. It is decoration and is
`aria-hidden`.

## Motion

- Idle: the hero phone bobs ±6px over 6s; loose coins drift. Transform and opacity only.
- Scroll: trail nodes scale from 0.9 and fade in via `IntersectionObserver`, staggered 80ms.
- Press: buttons translate down 4px in 80ms.
- The pot smash: shards fly on individual keyframes, a coin arcs out, the HUD counter ticks.
- Easing is `cubic-bezier(0.22, 1, 0.36, 1)` (ease-out-quint) everywhere. No bounce, no elastic.
- `prefers-reduced-motion: reduce` kills the bob, the drift, and the reveal; the smash becomes
  an instant state swap and the counter still increments.

## Banned here

On top of impeccable's absolute bans:

- Gradient text of any kind. The wordmark is solid with a layered outline.
- Glassmorphism. This world is painted, not glass.
- Dark mode. Boom Pots happens in daylight. There is no dark variant.
- Emoji as icons.
- A card grid of icon + heading + paragraph. The trail replaces it.
- Any color that wasn't sampled from `assets/screens/`.
