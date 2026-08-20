<div align="center">

# Harbour &amp; Hills

**Cross-border payment solutions.** *One world, one money.*

`Hong Kong` · `India` · `United States` · `Canada`

</div>

---

## About Harbour &amp; Hills

Harbour &amp; Hills is a cross-border payment provider based in Hong Kong's financial district, simplifying global commerce for businesses of all sizes. Founded by industry experts and drawing on 15 years of delivering payments worldwide, the firm pairs technology with deep operational experience to remove the friction from international trade.

**Mission** — simplify international payments so clients can grow their businesses without borders.

**Vision** — become the leading provider of cross-border payment solutions, building trust and opening business opportunities through innovation.

### What we do

- **Cross-border payment processing** — multi-currency settlement, materially faster than traditional banking rails, at rates built for SMEs and enterprises alike
- **Multi-currency accounts** — hold and manage funds in several currencies without opening a bank account for each
- **Fraud prevention &amp; risk management** — real-time monitoring and detection, with assessment tools that surface threats before they land
- **FX services** — competitive rates and real-time conversion on international transactions

Payments run on **H Intelligence** — the company's legacy platform extended with AI to speed up and secure transaction processing — alongside the unified **Edge+** platform.

---

## About this repository

A hand-built static site: plain HTML, one stylesheet, one script. No framework, no bundler, no `node_modules`. Every page ships exactly what the browser receives.

Each region gets its own directory of pages sharing a single design system and a single asset bundle. The root `index.html` is a client-side router that sends visitors to the right region instantly.

## Structure

```
.
├── index.html          # geo router → redirects to a regional site
├── hk/                 # Hong Kong  (canonical — source of truth for design)
├── in/                 # India
├── us/                 # United States
├── ca/                 # Canada
├── assets/
│   ├── css/style.css   # the entire stylesheet
│   ├── js/main.js      # Lenis smooth scroll, Anime.js reveals, nav
│   └── images/
└── hk/DESIGN_SYSTEM.md # tokens, type scale, grid, animation specs
```

Every region carries the same five pages — `index`, `about`, `services`, `why-hh`, `contact` — plus HK-only `csr.html` and `privacy-policy.html`.

## Regional routing

`index.html` picks a region in three steps, all client-side and instant:

1. **Timezone** — `Intl.DateTimeFormat().resolvedOptions().timeZone` (e.g. `Asia/Kolkata` → `in/`)
2. **Locale fallback** — `navigator.language` when the timezone is ambiguous (`en-CA` → `ca/`)
3. **Default** — Hong Kong

No server logic, no geo-IP lookup, no request round-trip.

## Design system

Defined in [hk/DESIGN_SYSTEM.md](hk/DESIGN_SYSTEM.md). The short version:

| Token | Value |
|---|---|
| Base dark | `#0c0f19` |
| Accent green | `#00d97e` |
| Text light | `#ffffff` |
| Text muted | `#707070` / `#8e8e8e` |
| Typeface | Inter |

Motion: [Lenis](https://lenis.darkroom.engineering/) for smooth scroll, [Anime.js](https://animejs.com/) for staggered fade / translate / blur reveals.

**HK is canonical.** When a shared component changes, change it in `hk/` first, then propagate.

## Local development

No build step — open the file, or serve the directory so the root router works:

```bash
python3 -m http.server 8000
```

Then visit http://localhost:8000.

## Maintenance scripts

Small one-purpose Python helpers, run from the repo root:

| Script | Purpose |
|---|---|
| `add_gtm.py` | Install the GTM container across all regions |
| `validate_page.py` | Sanity-check page markup and shared includes |
| `cleanup_usa.py` | One-off `usa/` → `us/` migration |

## Branches

| Branch | Purpose |
|---|---|
| `main` | Production |
| `uat` | Staging / testing |

## Analytics

**Google Tag Manager (`GTM-NQGPK2N2`) is the only tracking code on the site.** The container snippet is the first element in `<head>` on every page, with the `<noscript>` iframe immediately after `<body>`.

All tags — including Google Analytics — are configured inside GTM by the marketing team, not in this repo. There is deliberately no hardcoded `gtag.js`: running both would double-count pageviews.

If analytics stops reporting, check that the GTM container has been **published** (Submit → Publish) rather than only saved — an unpublished container loads on the site but fires nothing.

---

<div align="center"><sub>© Harbour &amp; Hills</sub></div>
