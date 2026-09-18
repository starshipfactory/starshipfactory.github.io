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

Images for a **new** post go in its bundle, next to `index.md`, and are referenced by
filename. Use the theme's shortcode rather than raw HTML:

```markdown
{{< img src="werkstatt.jpg" alt="Die Werkstatt an einem Dienstagabend" caption="Dienstagabend." >}}
```

Every image needs meaningful alt text — the theme is built around accessibility and the site
config has a real `accessibility` block.

**The migrated archive is the exception.** The 58 images belonging to the posts migrated from
the old Jekyll site live flat in `static/img/blog/`, shared by the German and English version
of each post rather than duplicated into two bundles. Do not follow that pattern for new
posts — and do not recreate `static/assets/`, which was removed when the archive was
reorganised. That move also dropped the old `/assets/images/…` URLs; page URLs were not
affected, and Hugo `aliases` cannot cover static files.

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
There are three such overrides today (`layouts/index.html`,
`layouts/partials/footer.html`, `layouts/partials/blog/byline.html`), each with a comment at
the top saying what it forked and why. Reach for CSS before forking a template, and never
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

### ⚠️ The cutover is manual

At the time of writing, **`master` still serves the old Jekyll site**, and the new Hugo site
lives on `feature/new-website-with-hugo`. Merging that branch into `master` is what replaces
the live website, and that merge is performed **by hand, deliberately, by a human** — it is
not a routine step and not the tail end of someone's feature work.

Once the cutover has happened, this section can go and the normal flow applies: branch → PR
→ green build → merge to `master` → deployed.
