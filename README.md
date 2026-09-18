# Starship Factory — Website

The website of [Starship Factory](https://starship-factory.ch), the makerspace in Basel,
Switzerland.

Built with [Hugo](https://gohugo.io) (extended) and the
[cncf/dot-org-hugo-theme](https://github.com/cncf/dot-org-hugo-theme), bilingual in German
and English, published to GitHub Pages.

| | |
|---|---|
| Live site | <https://starship-factory.ch> |
| Site generator | Hugo extended, supplied by the `hugo-extended` npm package |
| Theme | `cncf/dot-org-hugo-theme`, a **git submodule** in `themes/` |
| Languages | German (default, at `/`) and English (at `/en/`) |
| Search | [Pagefind](https://pagefind.app), built as a post-build step |
| Hosting | GitHub Pages, custom domain `starship-factory.ch` |

Two further documents live alongside this one and go deeper:

- **[`CLAUDE.md`](CLAUDE.md)** — the standing rules: theme boundaries, branding, colours,
  responsive constraints, translation policy, what is deliberately excluded. Read it before
  changing anything structural.
- **[`SETUP.md`](SETUP.md)** — the phase-by-phase record of how the site was built from an
  empty tree. Historical, but useful when you need to know *why* something is the way it is.

---

## Setup for local development

### Prerequisites

**Node.js 22 or newer** — and nothing else. Node supplies both the Hugo binary and the
PostCSS pipeline.

> **Do not install Hugo separately.** It comes from the `hugo-extended` npm dependency, so
> everyone (and CI) runs the same version. A system-wide `hugo` on your `PATH` will be a
> different build and will produce different output.

### Clone and install

The theme is a git submodule, so a plain `git clone` gives you a repo that cannot build —
Hugo reports confusing "missing layout" errors rather than "missing theme".

```bash
git clone --recurse-submodules https://github.com/starshipfactory/starshipfactory.github.io.git
cd starshipfactory.github.io
npm install
```

Already cloned without the submodule? Fix it with:

```bash
git submodule update --init --recursive
```

### Run the dev server

```bash
npm run start
```

Serves at <http://localhost:1313> with live reload, drafts and future-dated posts included.
It also passes `--printI18nWarnings` and `--printPathWarnings`; **treat anything they print
as an error**, not as noise.

### The other commands

| Command | What it does |
|---|---|
| `npm run start` | Dev server, drafts + future posts, warnings on. The everyday command. |
| `npm run dev:start:with-pagefind` | Same, but builds the Pagefind index first so `/search` actually returns results. Use this whenever you touch search. |
| `npm run build` | Production build into `public/`. |
| `npm run format` | Prettier over the JSON/YAML/HTML/CSS/JS we own. |
| `npm run format:check` | The same as a check — what you want before pushing. |

Two things about `npm run build` that surprise people:

- It builds with Hugo's **production** environment, so `config/production/hugo.yaml` applies
  and every URL is absolute against `https://starship-factory.ch/`. That is correct for a
  deploy and useless for local browsing — use `npm run start` to look at the site.
- It does **not** build the search index. Pagefind is a separate step:
  `npx -y pagefind --site public`.

### Updating the theme

```bash
git submodule update --remote --merge
npm run build          # must still pass
```

Commit the submodule pointer change. **Never edit files under
`themes/dot-org-hugo-theme/`** — see "Changing the design" below.

---

## Adding content

### Where content lives

```
content/de/       German — the default language, served at the site root (/anfahrt/)
content/en/       English — served under /en/ (/en/how-to-find-us/)
```

Every page is a **page bundle**: a directory with an `index.md` inside it.

### The one rule that matters: German first, English always

German is the source of truth. English is produced by translating it, **in the same commit**.
A German page committed without its English counterpart is unfinished work, not a backlog
item — Hugo's fallback to German exists as a safety net, not as a plan.

A few specifics, with the full policy in [`CLAUDE.md`](CLAUDE.md) → "Translating":

- **Translate the slug too.** `/mitglied-werden/` becomes `/en/become-a-member/`, never
  `/en/mitglied-werden/`. The one exception is `search.md`, which keeps its filename in both
  languages because the theme hardcodes the `/search` path.
- **German uses Swiss orthography** — `ss`, never `ß` (`Strasse`, `Schliessfach`).
- **Address the reader as "du"**, and use the equivalent plain register in English.
- **Do not translate proper nouns**: Starship Factory, street and tram-stop names, machine
  names, *Verein* when it names the legal entity.
- **Change no numbers.** Prices stay CHF, dates and addresses stay Swiss, IBANs and opening
  hours are copied verbatim.
- **Legal pages** (Impressum, Datenschutz, Statuten, Reglement) carry a line on the English
  version stating that the German original is legally binding, and clauses are never reworded
  to "improve" them.
- Keep the Markdown structure identical between the two, so they stay diffable.

### A new blog post

```bash
npx hugo new content blog/2026-03-14-mein-neues-projekt/index.md
```

That lands in `content/de/blog/` automatically, because German is the default language's
content directory. Then create the English version by hand at
`content/en/blog/2026-03-14-my-new-project/index.md`.

**Two naming conventions the archetype does not enforce:**

1. **The directory is prefixed with the post's date**, `YYYY-MM-DD-name`, matching the `date:`
   in the front matter. This keeps the ~96-post archive in chronological order in the file
   browser. Names are lowercase, digits and hyphens only.
2. **Every post needs an explicit `slug:`.** The permalink is
   `/:year/:month/:day/:slug/`, and with no `slug:` Hugo falls back to the directory name —
   which now starts with the date, giving you `/2026/03/14/2026-03-14-mein-neues-projekt/`.
   Set it and the date appears once.

A complete post front matter:

```yaml
---
title: "Mein neues Projekt"
description: "Ein Satz für die Meta-Description und die Vorschau in sozialen Netzwerken."
date: 2026-03-14
slug: "mein-neues-projekt"           # required — see above
author: "starshipfactory"            # must be a key in data/authors.yaml
translationKey: "mein-neues-projekt" # identical in both languages
draft: false
tags: ["3d-druck"]
categories: ["Projekte"]
---
```

`date`, `author` and `translationKey` must be **identical** in both languages. Only `title`,
`description`, `slug`, `tags` and the prose get translated. `translationKey` is what wires
the language selector together when the slugs differ — without it, switching language on a
post drops you on the wrong page.

New authors go in [`data/authors.yaml`](data/authors.yaml), keyed by GitHub username. An
`author:` that is not in that file makes the byline silently fall back to the date alone.

### A new page

```bash
npx hugo new content mitmachen/index.md          # → content/de/mitmachen/index.md
```

Then the English translation at `content/en/get-involved/index.md`, with a matching
`translationKey`. If the page should appear in the navigation, add it to **both** language
menus in [`config/_default/languages.yaml`](config/_default/languages.yaml):

```yaml
menu:
  main:
    - identifier: "mitmachen"
      name: "Mitmachen"
      url: "/mitmachen/"
      weight: 3
```

Entries with a `parent:` become a dropdown — that is how Mitglied werden, Statuten and
Reglement/Charta sit under "Verein". A parent entry with children needs no `url` and no page
of its own; the theme renders it as `href="#"`.

`menu.legal` is the separate footer-only row (Datenschutz, Impressum). Do not put pages in
both — the footer already lists every `menu.main` entry.

### Images

Images are processed at build time: converted to WebP, rendered at five widths (448, 671,
895, 1343, 1790) as a `srcset`, and emitted with `width`/`height` so the page does not jump
around while loading. You commit one original and Hugo produces the rest. None of that
happens for files in `static/`, which is copied as-is.

Which of those five a visitor actually downloads is decided by the `sizes` attribute, and
that is the one thing you have to get right by hand — see "Images in columns" below.

So the only real question is **where to put the file**.

#### Most pages: `assets/img/<section>/`

Every German page has an English translation in its own directory
(`content/de/3d-druck/` and `content/en/3d-printing/`), so an image kept next to one of
them would have to be duplicated to be used by the other. Putting it in `assets/` keeps one
copy, shared by both languages:

```
assets/img/3d-druck/prusa.jpg
```

Both language versions reference it by the same root-relative path — only the alt text is
translated. The folder name under `assets/img/` is just a folder name and never appears in a
URL a visitor sees, so there is no need for an English variant of it.

In `content/de/3d-druck/index.md`:

```markdown
![Ein Prusa-Drucker beim Drucken](/img/3d-druck/prusa.jpg)
```

In `content/en/3d-printing/index.md`:

```markdown
![A Prusa printer mid-print](/img/3d-druck/prusa.jpg)
```

This is how `assets/img/home/` and `assets/img/blog/` already work.

#### Pages built from columns or cards

The home page and **Anfahrt** are built out of `{{< columns >}}` / `{{< card >}}`. Inside
those shortcodes a **bundle-relative** image quietly skips the pipeline: the theme renders
their contents in a way that loses track of which page it is on, so Hugo never finds the
resource. The picture still appears — the untouched original is served — which is exactly
why this is easy to miss. You just lose the WebP conversion, the resize and the
`width`/`height`. Root-relative `/img/…` paths are unaffected.

Inside a column or a card, always use a root-relative path:

```markdown
{{< column >}}
![Die Werkstatt an einem Dienstagabend](/img/home/werkstatt.jpg)
{{< /column >}}
```

Since `assets/img/<section>/` is the recommendation everywhere anyway, following it means
you will not hit this.

##### Images in columns

Inside `{{< columns count=2 >}}` an image is laid out at roughly half the container — at
most 582px, never the full 895px the pipeline assumes by default. The browser cannot work
that out on its own, so tell it:

```
{{< img src="/img/3d-druck/prusa.jpg" alt="Ein Prusa-Drucker beim Drucken" sizes="column" >}}
```

Leave `sizes` off and every phone with a 2x screen downloads the 1790px file for a slot
about 325px wide — roughly 300 KB per photo instead of 50 KB, on the connection least able
to afford it. Nothing looks wrong, which is what makes it easy to ship.

`sizes` takes `"column"`, `"full"` (the default, and what markdown images get) or a literal
CSS sizes string. Both presets are defined and explained in `layouts/partials/image.html`;
if the theme's column layout ever changes, that is the one place to update.

The first image on a page is also the one the visitor waits for. Give it
`loading="eager" fetchpriority="high"` so the browser fetches it immediately instead of
deferring it like the rest:

```
{{< img src="/img/laser/laser_xtool_cutter.jpeg" alt="XTool Laser Cutter" loading="eager" fetchpriority="high" sizes="column" >}}
```

#### Page bundles

A page bundle — the image sitting next to `index.md` — works on any page that is **not**
built from columns or cards, and is referenced by bare filename:

```
content/de/holzwerkstatt/
├── index.md
└── hobelmaschine.jpg
```
```markdown
![Die Hobelmaschine](hobelmaschine.jpg)
```

It is the tidiest option when an image belongs to exactly one page in one language, because
the image moves and gets deleted along with the page. For anything that appears in both
languages, prefer `assets/`. If you do use a bundle and all its images go through the
pipeline, add `build: {publishResources: false}` to the front matter, or the untouched
original ships next to the WebP.

For **blog posts**, `CLAUDE.md` asks for page bundles on anything new. Know the trade-off
before you follow it: the English translation of a post lives in `content/en/blog/…`, so a
bundle image has to be copied into both bundles — which is precisely what the migrated
archive avoids by keeping its 58 images flat in `assets/img/blog/` and referring to them as
`/img/blog/…` from both languages. If you would rather keep one copy, do what the archive
does. Either way: do not "fix" the archive's paths, and do not recreate `static/assets/`.

#### When to use `{{< img >}}` instead

`{{< img >}}` and `![alt](src)` produce identical markup — both go through
`layouts/partials/image.html`. Use the shortcode when you need something Markdown cannot
express:

```markdown
{{< img src="/img/home/hero.jpg" alt="Die Starship Factory bei Nacht" loading="eager" fetchpriority="high" >}}
{{< img src="/img/home/werkstatt.jpg" alt="Die Werkstatt" caption="Dienstagabend." >}}
```

- `loading="eager"` + `fetchpriority="high"` — for the one big image at the top of a page.
  Everything else should stay lazy.
- `caption` — wraps the image in `<figure>` with a `<figcaption>`.
- `class` — for the rare case CSS needs a hook.

#### Alt text

**Every image needs meaningful alt text, translated along with the rest of the page.**
Describe what is in the picture, not the filename. If an image is purely decorative, pass
`alt=""` deliberately. Leaving `alt` out entirely gives you an empty alt, which is only
correct for decoration — the site does not guess alt text from filenames, because the
guesses are wrong in a way that sounds plausible to a screen-reader user.

#### `static/` is for something else

Use it only for files that need a fixed, unhashed URL: the favicons, `logo.svg`,
`social-share.png`, the social icons. Photos do not belong there.

### Writing the Markdown

Use the theme's shortcodes instead of raw HTML — `button`, `card`, `cards`, `column`,
`columns`, `img`, `intro`, `responsive_table`, `spacer`, `toc`, `youtube_enhanced`. Wide
content (tables, embedded maps) must go through `responsive_table` or a container with
`overflow-x: auto`, so the page body never scrolls sideways on a phone.

### Changing the design

Custom CSS goes in [`static/css/custom.css`](static/css/custom.css) — mostly brand colours
mapped onto the theme's `--primary-*` custom properties. Keep it small.

The theme is a submodule and is **read-only**. Anything that needs changing is done by
copying the file into the project's own `layouts/` directory, which Hugo resolves first.
There are six such files today: `layouts/partials/footer.html`,
`layouts/partials/blog/byline.html`, `layouts/shortcodes/button.html`,
`layouts/shortcodes/img.html` and `layouts/blog/list.html` are copies of a theme file, and
`layouts/index.html` fills a gap the theme leaves. Each carries a comment at the top saying what it forked and why.
`layouts/partials/image.html` and `layouts/_default/_markup/render-image.html` are not
forks — the theme has no equivalent. Reach for CSS before forking a template, and never
fork `header.html` — it carries the hamburger menu and the whole mobile navigation.

### Before you commit

```bash
npm run build          # Hugo fails loudly on broken refs
npm run format:check
```

Check the result at ~375px, ~768px and ~1280px if you touched layout.

---

## Publishing to GitHub Pages

Deployment is automatic. Two workflows in [`.github/workflows/`](.github/workflows/):

### `build.yml` — on every pull request

Runs the full production build, the Pagefind index and a link check
([`lychee.toml`](lychee.toml), internal links only — the 2013-era external links in the
archive are expected to rot and do not fail the build). It publishes nothing. A PR that is
red here would have been red after merging.

### `deploy.yml` — on every push to `master`

The same build, then `actions/upload-pages-artifact` + `actions/deploy-pages`. Concretely:

```bash
npm ci                                        # npm ci, not install — respect the lock file
npx hugo --gc --minify --environment production
npx -y pagefind --site public                 # after Hugo: it indexes the built output
```

There is nothing to run by hand and no `gh-pages` branch to maintain. **Pushing to `master`
publishes the site.** A deploy takes a couple of minutes; watch it under the repo's Actions
tab.

Both workflows check out with `submodules: recursive` (the theme is a submodule) and
`fetch-depth: 0` (`enableGitInfo` derives `lastmod` from git history). If you ever write a
third workflow, it needs both.

### The custom domain

[`static/CNAME`](static/CNAME) contains `starship-factory.ch` and is copied into `public/`
on every build, which is what keeps the custom domain bound. `baseURL` is set to match in
`config/production/hugo.yaml`. Old URLs are preserved with Hugo `aliases` in front matter —
these emit meta-refresh pages, which is the only redirect mechanism GitHub Pages supports.
Netlify-style `_redirects` files do **not** work here.

### What search engines are told

[`layouts/partials/head/custom-head.html`](layouts/partials/head/custom-head.html) — the
theme's designated `<head>` extension point, which ships empty — adds `rel=canonical` and
the `hreflang` pairs that tell a search engine `/holzwerkstatt/` and `/en/wood-workshop/`
are the same page in two languages. `hreflang` values come from each language's
`languageCode`, so changing those in `config/_default/languages.yaml` changes the markup.
Canonical is deliberately omitted on paginated lists; the file says why.

The same file marks the **generated taxonomy pages** (`/tags/`, `/tags/laser/`,
`/categories/elektronik/`) as `noindex, follow`, and
[`layouts/sitemap.xml`](layouts/sitemap.xml) keeps anything marked noindex out of the
sitemap. They stay browsable and crawlable — only the listings are kept out of search
results. There were 282 of them against 15 real content pages per language, 73% listing a
single post, all sharing one meta description, and their titles were competing with the
pages that should rank. Pagefind already excluded them for the same reason.

If you add a page that should not be indexed, put `noindex: true` in its front matter: the
theme emits the meta tag and the sitemap template drops it, with no second list to update.

Any page can set **`meta_title`** in its front matter to change the `<title>` element
without changing `.Title`. The home pages use it, which is the only reason
[`layouts/partials/head.html`](layouts/partials/head.html) is forked — one added line.
Reach for it when a page needs a longer, keyword-bearing title than its heading; leave
`.Title` alone, since that also feeds `og:title` and the RSS channel name.

Do **not** solve this by changing `title:` in `config/_default/languages.yaml`. That value
is the suffix on every other page's title, plus `og:site_name`, the logo alt text, the RSS
channel title and `Organization.name` in the JSON-LD. Measured: it pushed pages with titles
over 60 characters from 60 to 211, and named the association after a slogan.

[`layouts/partials/head/schema.html`](layouts/partials/head/schema.html) emits schema.org
JSON-LD: an `Organization` + `Place` + `WebSite` graph on the two home pages, and a
`BlogPosting` on each post. The Place carries the address, the coordinates and the opening
hours, which is what lets a search engine treat Starship Factory as somewhere you can go
rather than just a website.

Those facts live in `params.organization` in
[`config/_default/params.yaml`](config/_default/params.yaml) — **but the address and hours
are also prose in `content/<lang>/_index.md` and the Anfahrt page.** There is no single
source; if the club moves or changes its hours, both have to be updated.

The Organization has one `@id` for the whole site, built from the German home page, because
the German and English pages describe the same association rather than two of them.

### ⚠️ The cutover is manual

At the time of writing, **`master` still serves the old Jekyll site**, and the new Hugo site
lives on `feature/new-website-with-hugo`. Merging that branch into `master` is what replaces
the live website, and that merge is performed **by hand, deliberately, by a human** — it is
not a routine step and not the tail end of someone's feature work.

Once the cutover has happened, this section can go and the normal flow applies: branch → PR
→ green build → merge to `master` → deployed.
