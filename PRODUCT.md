# PRODUCT.md — Boom Pots

## Register

`brand` — this is a marketing landing page. The design *is* the product. Its only job is to
make a stranger want to tap Download.

## What it is

**Boom Pots** is a mobile tap-and-break puzzle game for iOS and Android. You tap clay pots on a
grid, smash them, and collect the coins inside before the timer runs out. Some pots are worth
points. Some hide a surprise. The pattern painted on a pot tells you which is which, so the
skill is memory and pattern reading, not luck.

Levels are laid out along a winding trail across a hand-painted world map: a green river valley
first, then a sun-bleached savanna with a horned skull on the ridge. Boosters (bomb, potion,
hammer) cost coins and clear pots you can't reach in time. Each level scores 1 to 3 stars
against escalating point targets.

## Users

**Primary — the commute player.** 25 to 45, plays in 4 to 9 minute bursts on a phone, one
thumb, often standing. Already plays Candy Crush, Royal Match, or Toon Blast. Reaches this page
from an ad, a friend's link, or a store listing they bounced out of. Decides in under six
seconds whether to tap Download. Does not read paragraphs.

**Secondary — the store scout.** Browsing for the next casual puzzle to install. Wants to see
actual gameplay, not promises. Scrolls to the screenshots first, then leaves or installs.

**Tertiary — press and partners.** Looking for a press kit, a contact address, and proof the
game is real and supported.

## Purpose

One conversion: **tap the App Store or Google Play button.** Everything else on the page exists
to earn that tap. Second-order goal: make the game legible in three seconds so the install
isn't a mystery-box download that uninstalls on day one.

## Brand personality

Three words: **sun-baked, hand-painted, mischievous.**

Not cute. Not slick. The game world is a painted adventure map with real dirt and real sunlight
in it, and the core verb is *smashing something.* The page should feel like it was painted, not
generated: warm, chunky, tactile, with a grin. Buttons should look pressable enough that you
want to press them.

Voice: short, physical, second person. "Tap it. Break it. Take the coins." Never
"revolutionizing mobile puzzle experiences." No exclamation-mark stacking.

## Anti-references

- **Enterprise SaaS landing pages.** No centered stack of icon-heading-paragraph cards. No
  gradient-mesh hero. No "trusted by" logo strip.
- **Neon / cyber / dark-mode-by-default game sites.** Wrong genre. This world is daylight.
- **Cutesy pastel candy palettes.** Candy Crush is a structural reference for how casual-game
  UI is *built* (layered chunky surfaces, sticker headlines, dome radii), never for its colors.
  Borrow the mechanics, not the pink.
- **Generic "African-themed" clip art.** No mudcloth-pattern background stock, no tribal-mask
  vector packs, no acacia-tree-at-sunset silhouette. The theme comes from the game's own
  painted world: the jungle greens, the savanna ochres, the terracotta pots and their painted
  spiral patterns.
- **Fake urgency.** No countdown timers, no "10,000 players online now" counters we can't back.

## Design principles

1. **Show the game, don't describe it.** Real screenshots at real phone aspect ratio, large.
   Every claim on the page should be visible in a screenshot next to it.
2. **The download button is the loudest object on every fold.** If a section doesn't lead back
   to it, it shouldn't exist.
3. **Chunky, not flat.** Surfaces get a top inset highlight and a bottom inset shadow. Buttons
   have a physical depth that compresses on press. This is the casual-game grammar and the
   audience reads it instantly.
4. **Daylight.** The page is lit. Light theme, no dark-mode variant.
5. **One screen, one idea.** Long scroll, generous pacing, one dominant thought per fold.
6. **Weight over count.** Fewer sections, each fully committed, beats eight thin ones.

## Accessibility

WCAG 2.2 AA, non-negotiable.

- The gold button color fails AA as small text on light backgrounds. Use it as a **fill** behind
  dark-brown text, never as small text on parchment.
- Never rely on color alone. Star ratings, level states, and booster types carry an icon or a
  label.
- Respect `prefers-reduced-motion`: parallax, floating pots, and entrance reveals all collapse
  to static.
- Every screenshot gets alt text that says what's happening in the game, not "screenshot 3".
- Full keyboard path to both store buttons; visible focus ring that survives on gold and green.
- Tap targets ≥ 44px.

## Constraints

- Single static page. HTML + Tailwind (CDN or prebuilt) + vanilla JS. No framework, no build
  step that GitHub Pages can't serve from a repo.
- Deployed to GitHub Pages. All asset paths relative.
- Mobile-first: most traffic arrives on the device the game runs on.
- Total page weight budget: keep hero interactive under ~1.5MB.
