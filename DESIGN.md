---
name: Olaryn
description: A graphite working surface for infrastructure engineers. Panes, hairline seams, one azure accent, real material.
colors:
  ground-light: "#E3E7EA"
  ground-dark: "#0B0E10"
  seam-light: "#C2CAD0"
  seam-dark: "#262D33"
  pane-light: "#FAFBFC"
  pane-dark: "#12161A"
  pane-raised-light: "#EEF1F3"
  pane-raised-dark: "#181D22"
  ink-light: "#10151A"
  ink-dark: "#E8EBED"
  muted-light: "#4F5B65"
  muted-dark: "#9AA5AD"
  azure-light: "#0A59C0"
  azure-dark: "#62B2FF"
  azure-hover-light: "#084A9F"
  azure-hover-dark: "#8CC7FF"
  ok-light: "#0B7240"
  ok-dark: "#5CD18C"
  hold-light: "#8A5100"
  hold-dark: "#F2B94B"
  err-light: "#B3261E"
  err-dark: "#FF8272"
typography:
  display:
    fontFamily: "Archivo, system-ui, sans-serif"
    fontSize: "clamp(2.4rem, 1.3rem + 3.3vw, 4rem)"
    fontWeight: 700
    lineHeight: 1
    letterSpacing: "-0.02em"
    fontVariation: "font-stretch: 80%"
  headline:
    fontFamily: "Archivo, system-ui, sans-serif"
    fontSize: "clamp(1.5rem, 1.05rem + 1.4vw, 2.25rem)"
    fontWeight: 650
    lineHeight: 1.1
    letterSpacing: "-0.015em"
    fontVariation: "font-stretch: 88%"
  title:
    fontFamily: "Archivo, system-ui, sans-serif"
    fontSize: "1.1875rem"
    fontWeight: 650
    lineHeight: 1.25
    fontVariation: "font-stretch: 92%"
  lead:
    fontFamily: "Archivo, system-ui, sans-serif"
    fontSize: "1.0625rem"
    fontWeight: 400
    lineHeight: 1.55
  body:
    fontFamily: "Archivo, system-ui, sans-serif"
    fontSize: "16px"
    fontWeight: 400
    lineHeight: 1.55
  table:
    fontFamily: "Archivo, system-ui, sans-serif"
    fontSize: "15px"
    fontWeight: 400
    lineHeight: 1.55
  label:
    fontFamily: "Archivo, system-ui, sans-serif"
    fontSize: "12px"
    fontWeight: 600
    lineHeight: 1.2
    letterSpacing: "0.09em"
  code:
    fontFamily: "JetBrains Mono, ui-monospace, monospace"
    fontSize: "13.5px"
    fontWeight: 400
    lineHeight: 1.7
rounded:
  none: "0"
  button: "2px"
spacing:
  hairline: "1px"
  sm: "8px"
  md: "16px"
  lg: "clamp(18px, 2.4vw, 28px)"
  section: "clamp(40px, 6vw, 80px)"
components:
  button-primary:
    backgroundColor: "{colors.azure-light}"
    textColor: "#FFFFFF"
    rounded: "{rounded.button}"
    height: "44px"
    padding: "0 18px"
  button-primary-hover:
    backgroundColor: "{colors.azure-hover-light}"
  button-outline:
    backgroundColor: "transparent"
    textColor: "{colors.ink-light}"
    rounded: "{rounded.button}"
    height: "44px"
    padding: "0 18px"
  pane:
    backgroundColor: "{colors.pane-light}"
    rounded: "{rounded.none}"
  pane-head:
    backgroundColor: "{colors.pane-raised-light}"
    textColor: "{colors.muted-light}"
    typography: "{typography.label}"
    height: "40px"
    padding: "0 16px"
---

# Design System: Olaryn

## Overview

**Creative North Star: "The Working Surface"**

The site is a console, not a brochure. Every page is a sheet of panes sitting on a ground; panes are divided by single hairline seams and nothing else. There is no shadow, no gradient, no rounded card. What fills a pane is real: the live OIDC discovery document, a playable reservation ledger, request shapes taken from the service source. Where a pane is not live it says so (snapshot, simulation, illustrative).

Density is moderate and deliberate. Headlines are condensed and heavy; everything else is quiet. One accent (azure) marks the primary action and the keys in code; green, amber and red appear only as state. Ownership markers, bars and tracks are ink or muted, never accent. Light and dark are two renderings of the same graphite surface, chosen by the OS and overridable with a toggle.

**Key Characteristics:**
- Panes tiled in a 12-column sheet; the 1px grid gap *is* the divider.
- Square corners; the only radius is 2px on buttons and the toggle.
- Condensed Archivo for headings, normal-width Archivo for text, JetBrains Mono only for code and data.
- One accent, three state colours, no decoration.
- Each product page has its own structure: Authward is a request/response transcript, Tallyward is a playable ledger.

## Colors

A cool graphite neutral ramp with one azure accent and three state colours. Every token is a `light-dark()` pair in `assets/base.css`.

### Primary
- **Signal Azure** (#0A59C0 light / #62B2FF dark): the primary button, code keys, the focus ring and the dot in the Olaryn mark. Hover: #084A9F / #8CC7FF.

### Neutral
- **Ground** (#E3E7EA / #0B0E10): the page behind the sheets.
- **Seam** (#C2CAD0 / #262D33): every divider, border and track edge.
- **Pane** (#FAFBFC / #12161A): the surface content sits on.
- **Raised Pane** (#EEF1F3 / #181D22): pane headers, table headers, code beside text, the "available" figure.
- **Ink** (#10151A / #E8EBED): text, brand marks.
- **Muted** (#4F5B65 / #9AA5AD): secondary text and labels. Both meet AA on Pane and Raised Pane.

### State
- **OK** (#0B7240 / #5CD18C): a settled hold.
- **Hold** (#8A5100 / #F2B94B): a pending hold.
- **Error** (#B3261E / #FF8272): a rejected or expired hold.

### Named Rules
**The One Accent Rule.** Azure is for the primary action and for keys (plus the Olaryn mark's dot). If a second thing wants to be azure, it is state or it is neutral.
**The State Colour Rule.** Green, amber and red mean a hold's state: settled, pending, rejected or expired. They never label a category and never decorate code.
**The No-Warm-Ground Rule.** The previous cream and pink-adjacent palette is retired. Do not reintroduce a warm paper ground or a pink or magenta hue.

## Typography

**Display and body:** Archivo (variable weight 400-800, width 75-125%), with the system sans as fallback.
**Code and data:** JetBrains Mono, only for code, endpoints, identifiers and measured values.

**Character:** a plain grotesque squeezed to a condensed width for headings so large type fits narrow panes, relaxed to normal width for reading.

### Hierarchy
- **Display** (700, clamp 2.4-4rem, 1.0, -0.02em, width 80%): page H1 only. The home wordmark scales to 6rem.
- **Headline** (650, clamp 1.5-2.25rem, 1.1, -0.015em, width 88%): section heads and the closing call to action.
- **Title** (650, 1.1875rem, 1.25, width 92%): step headings inside a pane.
- **Body** (400, 16px, 1.55): copy; max 40-52ch; muted unless it is the point.
- **Lead** (400, 17px, 1.55): the one sentence under a page H1.
- **Table** (400, 15px, 1.55): table cells.
- **Label** (600, 12px, 0.09em, uppercase): the title bar of a pane that holds an artifact (a document, a request, a ledger) and table column heads. Never a label above a heading, and never the heading of a section.
- **Code** (400, 13.5px, 1.7): panes of requests and documents; keys azure, verbs bold, comments muted, everything else ink.

### Named Rules
**The Plain Heading Rule.** Headings name the thing or state the fact: "How a login runs", "What the code enforces". No two-beat slogans, no italic accent word.
**The Artifact Title Rule.** A pane title bar names an artifact. A section's heading is a real heading at headline size, in a section head.

## Layout

A `.sheet` is a 12-column grid whose 1px gap shows the seam colour, bordered by the same seam. Children are `.pane`s that span full width on mobile and 4-8 columns from 960px. Sheets sit on the ground, 40-80px apart. The page shell is 1280px max with a 12-32px gutter. The top bar is sticky, 56px (95px on mobile with a scrolling nav row); the footer is a thin status line. Every row of panes must fill the sheet width so no bare seam colour shows.

Product pages open with a two-pane hero: the statement (5 columns) and a real artifact (7). Sections follow as sheets of 1-3 panes. Authward reads as a transcript of five request/response rows; Tallyward as a ledger with rules you can replay. Mobile stacks everything in reading order.

## Elevation & Depth

Flat. Depth comes from tone (Pane vs Raised Pane) and from the seam, never from shadow. The only motion is a 0.9s fade of an ink tint over a pane row or log line that just changed, button and link colour transitions of 0.15s, and a 3px arrow nudge on hover; all removed under `prefers-reduced-motion`.

## Shapes

Square. Panes, tables, chips (a 7px square marker), tracks and nodes are all rectangles with 1px edges. Buttons and the theme toggle have a 2px radius. Brand marks keep their own rounded strokes.

## Components

### Buttons
- **Shape:** 2px radius, 44px high (40px small), 14px/600 label.
- **Primary:** azure fill, white (light) or near-black (dark) text. One per view; given room around it.
- **Outline:** transparent with a muted border; on hover fills with ink.
- **Disabled:** 45% opacity, no hover change.

### Chips
Mono 12px marker plus text. The 7px square and the text take the state colour only when the chip reports a hold's state; otherwise they stay muted. Used for status in pane headers and ledger rows.

### Panes
Raised title bar (artifact name left, optional chip right, 40px) over a body on Pane. Foot strips use the same Raised Pane. Panes that are sections open with a section head instead.

### Tables
Full-width, 1px row seams, uppercase 12px muted column heads on Raised Pane, row heads at 600 weight.

### Navigation
A top bar: mark and name, hairline, "by Olaryn", text links, a small primary action, the theme toggle. Links are muted until hover. On mobile the nav drops to a second, horizontally scrolling row and the action is hidden.

### Ledger (signature)
One equation line (balance - held = available), action buttons, a holds table with per-row actions and an event log. "Try it" buttons in the rules table replay a rule here. Pure browser state; labelled "simulation, no network".

## Do's and Don'ts

### Do:
- **Do** let the 1px grid gap draw every divider.
- **Do** show real data in panes, and label snapshots, simulations and illustrative values.
- **Do** keep copy short and factual; every claim traceable to the Authward or Billing source.
- **Do** keep `light-dark()` pairs together in `base.css`; change a token once.

### Don't:
- **Don't** add shadows, gradients, glows, blur or rounded cards.
- **Don't** use a kicker or eyebrow above a heading, section numbers as decoration, or an italic accent word.
- **Don't** use azure for anything but the primary action and keys, or a state colour as a category label.
- **Don't** show a big number over a small label as a metric tile.
- **Don't** put internal per-app scopes or any invented customer, price or status on the pages.
