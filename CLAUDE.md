# CLAUDE.md

Guidance for Claude Code when working in this repository.

## Project

The website of **Starship Factory**, the makerspace/hackerspace in Basel, Switzerland
(https://starship-factory.ch).

**Status: live.** The Hugo rewrite was merged into `master` (PR #29) and is published to
GitHub Pages at <https://starship-factory.ch/>. The greenfield rewrite and the content
migration are **done** — this is now a maintained site, not a build-out.

`master` is the deployed branch: every push to it redeploys the live website via
`.github/workflows/deploy.yml`. Work on a feature branch and open a pull request; do not
commit or push to `master` directly, and do not merge a PR without being asked to.

The previous site was a Jekyll site using the `minimal-mistakes` theme. It was removed in
commit `cdf4f44` ("refactor: removed old clutter"), so **`master` no longer carries it** —
the last commit that does is `cdf4f44^`. Read old content and assets from there:

```bash
git show cdf4f44^:_pages/anfahrt.md          # read a single old file
git show cdf4f44^:assets/images/logo.svg     # extract an old asset
git ls-tree -r --name-only cdf4f44^          # list all old files
```

Much of what follows describes how the site was built and migrated. It is kept in the
present tense because it records **why things are the way they are** — the constraints,
the deliberate exclusions and the rules for new content all still apply. Where a section
describes a one-off step that has already been carried out, treat it as the reason not to
undo it rather than as work to do.

## Tech stack

- **Static site generator:** [Hugo](https://github.com/gohugoio/hugo), **extended** edition
  (the theme compiles SCSS via `sass-embedded`). The theme declares `min_version = "0.121.0"`
  in `theme.toml`; the version actually used is whatever the **`hugo-extended` npm
  dependency** resolves to (`^0.148.1` at the time of writing).
- **Theme:** [cncf/dot-org-hugo-theme](https://github.com/cncf/dot-org-hugo-theme),
  `theme_version` 0.1.8, MIT.
- **Node.js:** required — it supplies the Hugo binary (`hugo-extended`) *and* the PostCSS /
  autoprefixer pipeline. Use Node 22+.
- **Search:** [Pagefind](https://pagefind.app/), run as a post-build step over `public/`.

**The Hugo binary comes from npm.** Do not install Hugo separately in CI or you end up
running a different version than local. Add a floor in config so a wrong version fails loudly
instead of strangely:

```yaml
# config/_default/hugo.yaml
module:
  hugoVersion:
    min: "0.121.0"
    extended: true
```

Do not swap the SSG or theme, and do not hand-roll layouts the theme already provides.
Prefer theme shortcodes and params over custom HTML.

## Setup

The theme is consumed as a **git submodule** in `themes/dot-org-hugo-theme`, so a plain
`git clone` produces a tree that cannot build (Hugo reports missing *layouts*, not a
missing theme):

```bash
git clone --recurse-submodules https://github.com/starshipfactory/starshipfactory.github.io.git
npm install

git submodule update --init --recursive   # if you already cloned without it
git submodule update --remote --merge     # to update the theme
```

`package.json`, `postcss.config.js` and `config/` were seeded from the theme's
`exampleSite/`, which remains the reference implementation when looking for how a theme
feature is meant to be configured.

`.gitignore` is in place and must keep covering at least `public/`, `resources/`,
`node_modules/`, `.hugo_build.lock`, `hugo_stats.json`, `.DS_Store`, `.idea/` and
`static/pagefind/` (the generated search index).

## Repository layout

```
config/_default/hugo.yaml       # core Hugo config (see "Site configuration")
config/_default/languages.yaml  # per-language: title, params, main + legal menus
config/_default/params.yaml     # logos, social_links, custom_css, search toggle
config/production/hugo.yaml     # production-only overrides (hugo.Environment)
content/de/                     # German content (default language)
content/en/                     # English content
content/fr/                     # French content
i18n/de.yaml, i18n/en.yaml      # UI strings — the theme ships NO i18n files
data/authors.yaml               # blog authors, keyed by GitHub username
archetypes/                     # copied from the theme, adapted
layouts/partials/footer.html    # override: adds the legal link row (see Footer below)
layouts/partials/head.html      # override: honours front-matter `meta_title`
layouts/blog/list.html          # override: makes /blog/ searchable (see "Search")
layouts/robots.txt              # override: adds the Sitemap line
layouts/sitemap.xml             # override: drops noindex pages from the sitemap
layouts/partials/image.html     # shared image-pipeline renderer (see "Images & media")
layouts/partials/head/custom-head.html       # canonical + hreflang; calls schema.html
layouts/partials/head/schema.html            # schema.org JSON-LD
layouts/shortcodes/img.html     # override: routes {{< img >}} through the pipeline
layouts/_default/_markup/render-image.html   # markdown image render hook
lychee.toml                     # link-check config (internal links only)
.github/workflows/              # build.yml (PRs) and deploy.yml (master -> Pages)
static/CNAME                    # starship-factory.ch, copied into public/ on build
static/css/custom.css           # branding + small fixes (see "Branding")
static/img/                     # logo variants, social share image
assets/img/blog/                # blog archive images, flat, shared by de + en + fr
assets/img/home/                # home page photos
static/img/social-icons/        # signal.svg, discourse.svg (see Footer below)
static/favicon.ico              # + favicon.svg, favicon-32x32.png, apple-touch-icon.png
themes/dot-org-hugo-theme/      # submodule — NEVER edit files in here
```

Anything that needs changing in the theme is done by **overriding** the corresponding file
under the project's own `layouts/` directory — Hugo resolves project files before theme
files. Never patch the submodule. Keep overrides minimal and rare: copy the theme's version
of the file, make the smallest possible change, and note at the top which theme file it
forked and why, so theme updates can be re-merged. Reach for CSS before forking a
template. Current forks of a theme (or Hugo built-in) file: `footer.html` (legal link
row), `head.html` (front-matter `meta_title`), `byline.html` (per-language post dates and
a guarded author lookup), `img.html` (image pipeline), `blog/list.html` (search indexing
of `/blog/`), `robots.txt` (Sitemap line) and `sitemap.xml` (drops noindex pages).
Additive, not forks — the theme has no equivalent: `index.html` (home page),
`partials/image.html`, the render hook, `head/schema.html` and
`head/custom-head.html` (which fills a designated extension point the theme ships empty).

The theme provides these designated extension points; use them instead of forking:
`params.custom_css`, `params.custom_js`, `layouts/partials/head/custom-head.html`,
`layouts/partials/footer/custom-js.html`.

## Required files the theme expects

The theme silently degrades — or serves CNCF's assets — when these are missing. They all
exist now; the table records why, so they do not get tidied away:

| File | Why |
|------|-----|
| `content/<lang>/search.md` | `show_search: true` renders a header link to `/search`. That page does not exist unless you create it, containing `{{< search_form >}}`. Without it the search icon 404s. |
| `content/<lang>/blog/_index.md` | Section list page. Without it the blog section renders empty. |
| `content/<lang>/_index.md` | Home page. |
| `static/favicon.ico`, `static/favicon.svg`, `static/favicon-32x32.png`, `static/apple-touch-icon.png` | **The theme ships its own CNCF favicons in its `static/`, which get published to the site root.** Browsers request `/favicon.ico` unprompted, so without ours the CNCF icon is what people bookmark. `head/favicons.html` only emits `<link>` tags for files that exist with *exactly* these names. Regenerate all four from the old favicon — see "Favicons" under Branding. |
| `i18n/de.yaml`, `i18n/en.yaml`, `i18n/fr.yaml` | The theme has **no `i18n/` directory at all**; template strings such as `social_link_title` fall back to hardcoded English. Any UI string that should be German or French must be defined here. One file per language, same four keys in each. |
| `data/authors.yaml` | The blog archetype has an `author:` field resolved against this file, keyed by GitHub username. |
| `static/img/social-icons/signal.svg`, `discourse.svg` | See "Footer links". |

## Site configuration

Beyond the multilingual keys, `config/_default/hugo.yaml` needs:

```yaml
baseURL: "https://starship-factory.ch/"
timeZone: "Europe/Zurich"     # the theme's example says America/Los_Angeles — CHANGE IT
                              # or every blog date renders in the wrong zone
enableRobotsTXT: true         # Jekyll gave this via jekyll-sitemap; Hugo needs the flag.
                              # The sitemap is automatic.
enableGitInfo: true           # lastmod from git history (needs full checkout depth in CI)

pagination:
  pagerSize: 25               # the old site used `paginate: 5`; 25 keeps the 96-post
                              # archive to 4 pages instead of 20.
                              # NOTE: `paginate` was renamed in Hugo 0.128 and is dead.

permalinks:
  blog: "/:year/:month/:day/:slug/"   # reproduces the old Jekyll permalink structure

taxonomies:                   # the old site used both; declare them explicitly
  tag: tags
  category: categories
```

`config/production/` holds production-only overrides. The theme's `head/csp.html` branches on
`hugo.Environment`, and the npm scripts pass `--environment=production`, so the split is real
and must be kept.

**Analytics: leave off.** The theme's `head.html` unconditionally includes Hugo's
`_internal/google_analytics.html`. It emits nothing while `services.googleAnalytics.ID` is
unset — keep it that way. Do not enable Google Analytics. If the club ever wants numbers, use
a self-hosted privacy-friendly option (they already run `cloud.starship-factory.ch`) **and
update the Datenschutz page first**.

**Fonts are self-hosted** by the theme (Oswald + Nunito as local `woff2` in its
`static/fonts/`, preloaded in `head/preload.html`). There is no Google Fonts request and
there must not become one — do not "fix" fonts by adding a CDN `<link>`; it would be a
data-protection regression.

## Multilingual

German is the **main/default** language; English and French are secondary.

In `config/_default/hugo.yaml`:

```yaml
contentDir: content/de/
defaultContentLanguage: de
defaultContentLanguageInSubdir: false
```

German therefore lives at the site root (`/anfahrt/`), English under `/en/`
(`/en/how-to-find-us/`) and French under `/fr/` (`/fr/nous-trouver/`). In
`config/_default/languages.yaml` define `de` (weight 1, `languageCode: de-CH`), `en`
(weight 2, `contentDir: content/en`) and `fr` (weight 3, `languageCode: fr-CH`,
`contentDir: content/fr`), each with its own `title`, `params.description`, CTA texts and
menus.

**Adding the third language needed no template changes, and a fourth would not either.**
The theme's `language-selector.html` ranges over `.Site.Languages`, `head/custom-head.html`
loops `.AllTranslations` for hreflang (keeping `x-default` pinned to German),
`head/schema.html` derives its `@id` from the default language, `blog/byline.html` takes its
date layout from `i18n`, and the forked `footer.html` ranges `.Site.Menus.legal`. Adding a
language is config + `i18n/<lang>.yaml` + `content/<lang>/`, nothing more.

Rules:

- **German is written first and is the source of truth. English and French are produced by
  translating it.** Never author an English or French page independently — it drifts from the
  German and nobody notices. **Translate from the German, never from the other translation:**
  English and French are siblings, not intermediates, and relay translation compounds drift.
- **Every German page and every blog post gets an English *and* a French translation**,
  produced as part of the same task that creates or changes the German. A German page
  committed without both counterparts is unfinished work, not a backlog item. Hugo's fallback
  to the default language exists as a safety net, not as a plan.
- **Parity is all-or-nothing.** The theme's language selector falls back to
  `href="/{{ .Lang }}/"` for a page with no translation — which yields `/de/`, a 404, since
  German is at the root. One missing translation therefore breaks the switcher on that page's
  *other* two languages too, not just its own.
- Link translated pages with an explicit `translationKey` in front matter, so the theme's
  language selector works even when the slugs differ.
- UI strings go in `i18n/de.yaml` / `i18n/en.yaml` / `i18n/fr.yaml`, never hardcoded in a
  template. All three carry the same four keys (`breadcrumb_home`, `by`,
  `social_link_title`, `date_format`).
- German content uses Swiss German orthography: **"ss" instead of "ß"** (`Strasse`,
  `Schliessfach`), and Swiss number/date conventions.
- Address the reader with the informal **"du"** — that is the tone of the space. In English
  use the equivalent plain, direct register ("you", contractions, no corporate voice); in
  French use **"tu"** (tutoiement). **The one exception is the privacy policy**, which the
  German itself writes in the formal register ("Sie"); the French mirrors that with "vous"
  and says so in its opening note. Register follows the source document, not the site
  average.

### Translating

Translate the meaning, not the words. The English and French sites should read as though
written by a member, not as output from a translation tool.

**French specifics.** Standard French, with every Swiss fact preserved verbatim (CHF, Swiss
addresses and date formats, BVB line numbers, street and stop names) — no Romandie-only
vocabulary. French typography: a no-break space before `: ; ! ?`, `«  »` for quotation
marks, `’`-style apostrophes in prose, and times as `19h30`. **Every internal link and
`{{< button link= >}}` in `content/fr/` starts with `/fr/`** — see the warning at the end of
this section.

- **Translate the slug too**, and keep it in the front matter: `/mitglied-werden/` becomes
  `/en/become-a-member/`, not `/en/mitglied-werden/`. Front matter `title`, `description`,
  `summary` and image alt text all get translated as well — not just the body.
  **One exception: `search.md` keeps its filename in all three languages.** The theme's
  `header.html` hardcodes `{{ "/search" | absLangURL }}`, so a German `suche.md` or a French
  `recherche.md` would leave the header's search icon pointing at a 404. Translate its
  `title` ("Suche", "Recherche"), not its path.
- **Do not translate proper nouns**: "Starship Factory", street and place names, Basel
  transport lines and stop names, "Verein" when it names the legal entity, product and
  machine names. Keep the German term and add a short gloss on first use where an English or
  French reader would otherwise be lost (e.g. *Verein* — a Swiss registered association, or
  *une association de droit suisse*).
- Keep German terms that have no clean English or French equivalent and that members
  actually say, rather than inventing new ones.
- Convert nothing factual: prices in CHF stay CHF, dates and addresses keep Swiss format,
  IBANs and opening hours are copied verbatim. A translation must not change a number.
- Keep the Markdown structure identical — same headings, same links, same images, same
  shortcodes — so the three languages stay diffable against each other. Where the German
  itself is garbled or self-contradictory, translate the evident meaning literally rather
  than repairing it, so the copies keep lining up.
- **Legal pages are a special case.** Translate Impressum, Datenschutz, Statuten and
  Reglement/Charta for comprehension, but add a line at the top of each translated version
  stating that the German original is the legally binding version, and never reword a legal
  clause to "improve" it. If a passage is genuinely ambiguous, translate it literally and
  flag it rather than interpreting it. Those notices are the **only** place a translated page
  links to a German URL (`/impressum/`, `/datenschutz/`, `/statuten/`, `/reglement/`) — that
  is deliberate, because they point at the binding original.
- When the German changes later, update the English **and** the French in the same commit.

**The trap that lychee cannot catch.** The theme's `button` shortcode does *not* apply
`relLangURL`, so internal links in content carry their language prefix literally: German
writes `link="/anfahrt/"`, English `link="/en/how-to-find-us/"`, French
`link="/fr/nous-trouver/"`. A French page that kept an `/en/…` or a bare `/anfahrt/` link
would silently send the reader to the wrong language, and the link check would pass, because
the target genuinely exists. Gate it with a grep instead — this must print nothing:

```bash
grep -rnoE '(link="|\]\()/[a-z0-9-]+' content/fr --include='*.md' \
  | grep -vE '/fr/|/img/|/attachments/|/datenschutz/|/impressum/|/reglement/|/statuten/'
```

## Content sections

This is the site as published. Menu order, German (default) URLs, and their English and
French counterparts. `identifier:` values are identical across all three language menus, so
the three `menu.main` blocks stay diffable against each other — keep it that way.

| Menu entry (de / en / fr) | German URL | English URL | French URL | Notes |
|---------------------------|------------|-------------|------------|-------|
| Home / Home / Accueil | `/` | `/en/` | `/fr/` | `content/<lang>/_index.md` |
| Blog | `/blog/` | `/en/blog/` | `/fr/blog/` | List + 96 posts, migrated from the old `_posts/` |
| Anfahrt / How to find us / Nous trouver | `/anfahrt/` | `/en/how-to-find-us/` | `/fr/nous-trouver/` | Address, public transport, map |
| Forum | — | — | — | External link to `https://discourse.starship-factory.ch/`; no page of its own |
| **Werkstatt / Workshop / Atelier** | — | — | — | Grouping entry only, no page — the six machine areas below are its children |
| 3D-Druck / 3D printing / Impression 3D | `/3d-druck/` | `/en/3d-printing/` | `/fr/impression-3d/` | |
| CNC-Bearbeitung / CNC machining / Usinage CNC | `/cnc-bearbeitung/` | `/en/cnc-machining/` | `/fr/usinage-cnc/` | |
| Laser | `/laser/` | `/en/laser/` | `/fr/laser/` | |
| Elektronik / Electronics / Électronique | `/elektronik/` | `/en/electronics/` | `/fr/electronique/` | |
| Holzwerkstatt / Wood workshop / Atelier bois | `/holzwerkstatt/` | `/en/wood-workshop/` | `/fr/atelier-bois/` | |
| Textil / Textiles / Textile | `/textil/` | `/en/textiles/` | `/fr/textile/` | |
| **Verein / Association / Association** | — | — | — | Grouping entry only, no page |
| Mitglied werden / Become a member / Devenir membre | `/mitglied-werden/` | `/en/become-a-member/` | `/fr/devenir-membre/` | Membership info; also the header + footer CTA |
| Spenden / Donate / Dons | `/spenden/` | `/en/donate/` | `/fr/dons/` | Donation options |
| Statuten / Statutes / Statuts | `/statuten/` | `/en/statutes/` | `/fr/statuts/` | From `cdf4f44^:_pages/organisation/statuten.md` |
| Reglement/Charta / Charter / Charte | `/reglement/` | `/en/charter/` | `/fr/charte/` | From `cdf4f44^:_pages/organisation/reglement.md` |

French slugs stay ASCII (`electronique`, `confidentialite`); the accents live in `title` and
the menu `name` only.

**`params.main_cta` / `params.footer_cta` links are NOT prefixed.** The theme passes them
through `absLangURL`, so the French CTA is `link: "/devenir-membre/"`, not
`/fr/devenir-membre/` — the latter would render as `/fr/fr/devenir-membre/`. Menu `url:`
values are likewise unprefixed (`footer.html` applies `relLangURL`). Only links *inside
content* carry the prefix.

Six top-level entries, two of them dropdowns. **Werkstatt and Verein are grouping entries
with no `url:` and no page** — the theme renders a parent with children as `href="#"` plus
a dropdown on desktop, a nested list in the hamburger menu, and a column heading with its
children beneath it in the footer. All three behaviours are already styled; do not give
either entry a page to "fix" the `#` href.

The two dropdowns are what keeps the menu from crowding the CTA. If a further top-level
entry is ever needed, put it under an existing parent before adding a seventh at the top
level. The header CTA (`params.main_cta`) and footer CTA (`params.footer_cta`) both point
at "Mitglied werden", which is why it sits under Verein rather than at top level — it is
not duplicated.

Two further pages exist for the **footer only** (`menu.legal`, see below) and must not be
added to `menu.main`:

| Page | German URL | English URL | French URL | Source at `cdf4f44^` |
|------|------------|-------------|------------|----------------------|
| Datenschutz / Privacy / Confidentialité | `/datenschutz/` | `/en/privacy/` | `/fr/confidentialite/` | `_pages/datenschutz.md` |
| Impressum / Imprint / Mentions légales | `/impressum/` | `/en/imprint/` | `/fr/mentions-legales/` | `_pages/impressum.md` |

The old site nested Statuten and Reglement under `/organisation/`; this site flattens
them, and `aliases: ["/organisation/statuten/"]` (resp. `reglement`) in their front matter
keeps the old URLs working. Leave those aliases in place. **Those aliases are German-only,
and so are the two in the blog archive** — the old Jekyll site had no English or French URLs
to preserve, so translated pages get no `aliases` at all.

### Deliberately excluded

- **The wiki is out of scope entirely.** The old site had a `wiki` collection, a
  `_layouts/wiki.html`, a `wiki-sidebar.html` and a `Wiki` nav entry pointing at
  `https://wiki.starship-factory.ch/`. Do **not** migrate any of it, do **not** add a wiki
  section, and do **not** add a wiki link to the header or footer. If wiki content comes up,
  skip it and say so rather than porting it. (The header's "Forum" entry links to
  Discourse, not the wiki — do not turn it into one.)
- The old `verein`, `events`, and archive pages (`category-archive`, `tag-archive`,
  `year-archive`) are not part of the sections above. Do not add them unless asked.
- A 404 page needs no work: the theme ships `layouts/404.html`, and GitHub Pages serves
  `/404.html` automatically. Add `content/<lang>/404.md` only if custom copy is wanted.

### Blog: the migrated archive and new posts

**The migration is complete** — all 96 old posts live under `content/de/blog/`,
`content/en/blog/` and `content/fr/blog/` and are published. The originals are at
`cdf4f44^:_posts/YYYY-MM-DD-slug.md`, with Jekyll front matter and a
`/:year/:month/:day/:title/` permalink; consult them when a migrated post looks wrong, not
to re-run the migration. Everything below applies to new posts as well, except where it is
explicitly about the old ones.

- Create new posts with the theme's archetype: `hugo new content blog/my-post.md`. Copy
  `archetypes/{default,blog,faq}.md` from the theme into the project root and adapt them.
  With a multilingual `contentDir`, pass the language explicitly or create the file under
  `content/de/blog/` by hand.
- Convert front matter to Hugo (`title`, `description`, `date`, `author`, `draft`, `tags`,
  `categories`). `author` must match a key in `data/authors.yaml`.
- The permalink structure is handled by the `permalinks` config above, not per post. Use
  `aliases` only for posts whose slug had to change.
- **The feed URL changes, deliberately.** Jekyll served `/feed.xml`; Hugo's built-in RSS
  output serves `/index.xml`, and that is the feed the site uses. Do **not** add a
  `/feed.xml` alias, a custom output format or a redirect for the old URL — backwards
  compatibility for existing subscribers is explicitly out of scope. Leave the theme's
  and Hugo's default RSS mechanism alone.
- Jekyll-isms (`{% include %}`, `{% highlight %}`, `/assets/images/...` paths) were
  rewritten during the migration; blog images now live at `/img/blog/...`. If one survives
  somewhere, fix it the same way.
- **Every post gets an English and a French translation** under `content/en/blog/` and
  `content/fr/blog/`, per the "Translating" rules above. The archive is fully translated,
  96 posts in each of the three languages; keep it that way — a post committed German-only
  breaks the pairing.
- Post `date` and `author` must be identical in all three languages; only the prose, `title`,
  `description`, `slug`, `tags` and `categories` are translated. Keep the same
  `translationKey` on all three — **the German-derived key is the shared one**, so the English
  and French files carry keys like `loop-schal`, not their own slug. A few keys are quirky and
  must be copied verbatim rather than guessed: trailing hyphens
  (`feinmechanikerschraubenzieherset-von-bruetschruegger-werkzeuge-ag-`), mixed case
  (`Arduino-ISP`, `Ziemlich_schnelles_Internet`), underscores (`digitaluhr_selbst_bauen`) and
  date-prefixed keys that disambiguate the two "wir ziehen um" posts
  (`2019-05-20-wir-ziehen-um`, `2025-05-30-wir-ziehen-um` — note the latter's date does not
  match its own filename).
- **The byline is already fixed in `layouts/partials/blog/byline.html`** — two changes
  against the theme, documented at the top of that file: the date layout comes from `i18n`
  so German posts render "30. August 2026", and the author lookup is guarded, because the
  theme's unguarded `index` aborts the build on any post without an `author` (none of the
  96 migrated posts have one). Do not revert either when re-merging a theme update.
- The old posts used German `ß` (`großen`, `gießen`); these were normalised to Swiss `ss`,
  per the orthography rule above. New posts follow the same rule.
- Old posts carry minimal-mistakes front matter such as `header.teaser`, which has no Hugo
  equivalent — map it to the page bundle's cover image or drop it.

## Images & media

The old site carries a large `assets/images/uploads/` tree. Do not bulk-copy it into
`static/`.

**Three homes, and which to pick.** `static/` is copied verbatim with no processing;
`assets/` and page bundles both go through Hugo's image pipeline. Default to a page
bundle, use `assets/` when several languages share one file, and keep `static/` for files
that need a fixed, unhashed URL (favicons, `logo.svg`, `social-share.png`).

- Migrate images **as page bundles**: `content/de/blog/my-post/index.md` with its images
  beside it.
- **Exception, already applied to the blog archive.** The 58 images referenced by the
  migrated posts live flat in `assets/img/blog/`, rather than in per-post bundles, because
  all three language versions of a post reference the same file and bundles would duplicate
  every one of them. New posts should still use page bundles. **Adding French therefore added
  no image files at all** — only the `alt` and `title` text is translated.

  This tree was reorganised out of `static/assets/images/snippet_images/{content,content_small}/`
  — the old Jekyll/Zinnia paths — and 82 unreferenced files were deleted at the same time.
  The old image URLs (`/assets/images/…`) therefore no longer resolve; page URLs were not
  affected. `aliases` cannot help here, as they only work for pages, not static files.
  Do not reintroduce `static/assets/`.

  It later moved again, from `static/img/blog/` to `assets/img/blog/`, so the archive
  gets pipeline treatment while all three languages keep sharing one copy of each file.
  **The markdown still says `/img/blog/foo.jpg`** — the render hook strips the leading
  slash and looks the path up in `assets/`. That deliberately avoids rewriting the image
  line in all 288 archive files and keeps the three language copies diffable. Do not
  "fix" those paths to match the new location.
- **Markdown images go through the pipeline automatically**, via
  `layouts/_default/_markup/render-image.html`. Plain `![alt](foo.jpg "title")` is the
  preferred syntax: the hook converts bundle and `assets/` rasters to WebP, caps them at
  the theme's 895px content width, adds a 2x `srcset` when the original is wide enough,
  and emits intrinsic `width`/`height`. SVG and GIF pass through untouched; remote URLs
  and unresolvable paths fall back to a plain `<img>`.

  `{{< img >}}` is overridden in `layouts/shortcodes/img.html` and goes through the same
  `partials/image.html`, so both syntaxes produce identical markup. Use the shortcode when
  you need `loading="eager"`, `fetchpriority`, a `caption` (it emits `<figure>`/
  `<figcaption>`) or a `class` — markdown syntax cannot express those. Unlike the theme's
  version, the override does **not** invent alt text from the filename; a missing `alt`
  stays empty rather than becoming plausible-sounding nonsense for screen readers.

  **Bundle-relative paths do not work inside `{{< column >}}` or `{{< card >}}`.** Those
  shortcodes render their body with `.Inner | markdownify`, which loses the page context:
  inside them the render hook's `.Page` is the site home with no resources, so
  `![alt](foo.jpg)` silently falls through unprocessed (`.PageInner` does not help).
  Root-relative `/img/…` asset paths are unaffected, which is why `content/<lang>/_index.md`
  — built entirely from columns — keeps its images in `assets/img/home/` and refers to them
  by root-relative path. Nested `{{< img >}}` shortcodes are fine: shortcode invocations
  keep their page context, only markdownify-rendered markdown loses it. Verified on 0.148.1.

  **Home page images live in `assets/img/home/`** for that reason. Two of them
  (`cnc-portalfraese.jpg`, `laser-kh-3020.jpg`) were hotlinked from
  `wiki.starship-factory.ch` and are now vendored: the home page must not depend on a
  second origin staying up, and every image should be served from our own domain.

  The hook sits at the legacy `layouts/_default/_markup/` path rather than the 0.146+
  `layouts/_markup/`, because that works with no deprecation warning and stays compatible
  with the `min: "0.121.0"` floor. On the new path it would silently stop firing below
  0.146 instead of failing loudly.
- Once a page's images all go through the pipeline, set `build: {publishResources: false}`
  in its front matter, or the unprocessed original ships alongside the derivative. This is
  a page-bundle concern only — `assets/` files are published only when something calls
  `RelPermalink` on them.
- Pipeline defaults are configured once, in `config/_default/hugo.yaml`:

  ```yaml
  imaging:
    quality: 80
    resampleFilter: Lanczos
  ```
- Every image needs meaningful alt text; the theme is built around accessibility and
  `params.accessibility` is a real config block (`skip_text`, `help_text`, `help_url`) —
  fill it in, in all three languages.
- The Anfahrt map and any video go through the theme's iframe styles and the
  `youtube_enhanced` shortcode, never a raw `<iframe>`.

## Search

Search is [Pagefind](https://pagefind.app/), run over the **built `public/` directory** as a
post-build step — it is not something Hugo generates. `content/<lang>/search.md` holds the
theme's `{{< search_form >}}` shortcode, which loads `/pagefind/pagefind-ui.js`; both CI
workflows run `npx -y pagefind --site public` right after the Hugo build. `static/pagefind/`
is generated and gitignored.

`npm run start` does **not** build the index, so `/search` renders an empty box and the
script 404s. Use `npm run dev:start:with-pagefind` when touching search; its index is a
snapshot and goes stale until the script is rerun.

**What gets indexed is decided by `data-pagefind-body`.** The theme's `baseof.html` puts that
attribute on `#content` for `.IsPage` only. Pagefind's rule is all-or-nothing: once *any*
page on the site carries the attribute, every page without one is skipped entirely. That
covers every regular page and every blog post, in all three languages.

Section and home pages are **not** `.IsPage`, so they need their own wrapper —
`baseof.html` must not be forked for this. One project template supplies one:
`layouts/blog/list.html` wraps the content and the post listing on `/blog/` and
`/en/blog/`, but **only on the first paginator page**. `/blog/page/2/` and later repeat
summaries that are already indexed on the posts themselves and would return duplicate
results. It also sets `data-pagefind-meta="title:…"`, since baseof's `<h1>` sits outside
the `main` block.

Deliberately left out of the index:

- **The home pages** (`/`, `/en/`). Their content is a set of teasers that all link on to
  the real page, so a hit on the home page is a detour. `layouts/index.html` is therefore
  *not* a search-related override — do not add a wrapper to it.
- **Taxonomy list pages** (`/tags/…`, `/categories/…`). Keyword listings, ~400 of them, that
  would crowd out real pages.
- Not by choice: the `/search` page indexes itself as a near-empty result. Excluding it
  cleanly would need `data-pagefind-ignore` on an ancestor of `#content`, i.e. a
  `baseof.html` fork, which is not worth it.

Pagefind splits the index by the `<html lang>` attribute on its own, so a German search
returns German pages only, and its UI strings are localised without anything in `i18n/`. It
picked up French unprompted: the build emits `wasm.fr.pagefind`, i.e. a real French stemmer
rather than the `unknown` fallback.

After a build, `public/pagefind/pagefind-entry.json` reports the per-language page counts —
check it when changing what is indexed. The three languages should agree; they currently read
**111 pages each** (112 content files per language, minus the deliberately excluded home
page). A page with a near-zero word count there is a content problem, not a search one — the
six workshop pages were front-matter-only stubs for a while and were findable by title alone;
they have bodies now. Check that count after adding a page.

## Branding: logo & colours

### Logo

Use the **Starship Factory logo from the old website**, at `cdf4f44^:assets/images/logo.svg`:

```bash
git show cdf4f44^:assets/images/logo.svg > static/img/logo.svg
```

Do not redesign it — it is the organisation's existing identity. It is a steel-blue planet
with an orange "SF" wordmark and an orange orbit ring, on transparent/white.

Wire it up via params (the header uses the first, the footer the second):

```yaml
# config/_default/params.yaml
logo_on_white: "/img/logo.svg"
logo_on_black: "/img/logo-on-dark.svg"
```

Two things to watch:

- **Aspect ratio.** The logo is `293.56 × 169.73` (≈1.73:1), but the theme hardcodes
  `width="150" height="40"` (3.75:1) on the `<img>`. The artwork is **not** distorted by
  this: `_header.scss` sets `object-fit: contain` alongside `max-width: 100px` /
  `max-height: 40px` (130px / 50px above 1000px), so the mark is letterboxed rather than
  squashed. What remains is dead space — the element box stays 100×40 while the logo fills
  only ≈69×40, and `object-position: 0 0` pushes the gap to the right of the mark. **Fix
  that in CSS, not by forking `header.html`** — that partial also contains the hamburger
  button and the whole mobile menu, and forking it puts the theme's responsive navigation at
  risk for a cosmetic problem:

  ```css
  .header .logo, .footer .logo { width: auto; height: auto; }
  ```

  Letting both axes size themselves makes the box hug the artwork while still honouring the
  theme's caps. Ensure the SVG keeps a `viewBox`.
- **The footer background is `var(--black)`.** The logo's blue (`#3e5f81`) sits at only
  ~3.2:1 against black. `logo-on-dark.svg` must recolour the planet to white (or a much
  lighter blue) and keep the orange, which reads well on black.

Derive the social share image (`params.images`) from the same logo — 1200×630 PNG, logo
centred on white.

### Favicons

**Reuse the favicon from the old website, regenerated as SVG.** The old one is at
`cdf4f44^:favicon.ico`:

```bash
git show cdf4f44^:favicon.ico > /tmp/old-favicon.ico
```

Two facts about that file matter:

- **It is not actually an ICO.** `file` reports `PNG image data, 32 x 32, 8-bit/color RGBA` —
  it is a 32×32 PNG that was simply named `.ico`. Browsers tolerate this, but do not copy it
  forward as `favicon.ico`; generate a real ICO instead.
- **It is a square crop of the logo mark**, not the whole logo: the planet with the orange
  "SF" and the orbit ring, centred and filling the square. The logo SVG is `293.56 × 169.73`
  (≈1.73:1), so a favicon is *not* the logo scaled down — it needs a square framing.

Regenerate, do not upscale. The 32×32 PNG is the *reference for the design*; the source of
truth for the vector is `static/img/logo.svg`, which is already true vector art in the same
two brand colours (`#ff6600`, `#3e5f81`).

**`static/favicon.svg`** — the primary favicon, and the one to author by hand:

- Copy the mark's paths out of `logo.svg` into a new SVG with a **square `viewBox`**
  (e.g. `viewBox="0 0 256 256"`), framing the planet + orbit + "SF" the way the old 32×32
  does, with even optical padding.
- Keep the brand colours as literal fills. Do not make it `currentColor`.
- Keep the background transparent.
- No `width`/`height` attributes — `viewBox` only, so it scales freely.
- Strip the Inkscape/sodipodi cruft that `logo.svg` carries (`inkscape:*`, `sodipodi:*`
  namespaces, metadata) so the file stays small.

**Then generate the raster fallbacks from that SVG**, all at the exact filenames
`head/favicons.html` checks:

| File | Size | Notes |
|------|------|-------|
| `static/favicon.svg` | vector | modern browsers; the master copy |
| `static/favicon.ico` | 16+32+48 multi-size | a **real** ICO. Still needed: browsers request `/favicon.ico` at the site root regardless of markup |
| `static/favicon-32x32.png` | 32×32 | PNG fallback |
| `static/apple-touch-icon.png` | 180×180 | iOS home screen. **Give it an opaque white background** — iOS composites transparency onto black, which would wreck the blue planet |

Legibility at 16px is the constraint that shapes the artwork: the thin orbit ring and the
small rocket detail in the full logo disappear at that size. The old favicon already solved
this by cropping tight to the mark — follow it. If the ring still muddies at 16px, thicken it
slightly in the SVG rather than shipping a blurry icon; a favicon is allowed to be a
simplified version of the logo.

Check the result at 16px, not just in the file browser.

### Colours

The palette comes from the logo itself — **orange, blue and white**:

| Role | Hex | Source |
|------|-----|--------|
| Orange | `#ff6600` | logo wordmark + orbit ring |
| Orange (dark) | `#b34700` | darkened for text/buttons |
| Blue | `#3e5f81` | logo planet |
| White | `#ffffff` | logo background / negative space |

> Note: the brief called these "red, blue and white". The logo's warm colour is **orange
> `#ff6600`**, not red — these hex values are taken from the SVG. Everything below uses the
> logo's actual colours.

Rebrand by **overriding the theme's CSS custom properties** in `static/css/custom.css`. The
theme drives its entire palette through `--primary-400` … `--primary-800`, so this needs no
SCSS fork and survives theme updates:

```css
:root {
  /* Starship Factory brand — from assets/images/logo.svg */
  --sf-orange: #ff6600;
  --sf-orange-dark: #b34700;
  --sf-orange-darker: #8f3900;
  --sf-blue: #3e5f81;
  --sf-blue-dark: #2e4760;
  --sf-blue-darker: #22354a;

  /* map onto the theme's roles */
  --primary-400: var(--sf-orange-dark);   /* secondary/tertiary button bg (white text) */
  --primary-500: var(--sf-orange-darker); /* its hover */
  --primary-600: var(--sf-blue);          /* body links */
  --primary-700: var(--sf-blue-dark);     /* primary button bg, link hover */
  --primary-800: var(--sf-blue-darker);   /* primary button hover */

  /* full-strength orange is safe on the black footer */
  --footer-link-color-hover: var(--sf-orange);
}
```

**Contrast is why the mapping is not the obvious one.** Measured against WCAG AA:

- `#3e5f81` on white — **6.6:1** ✓ safe for body text and links.
- `#ff6600` on white — **2.9:1** ✗ fails for text. Use full-strength orange only for
  non-text accents: the orbit/rule lines, icons, borders, large display shapes.
- `#b34700` on white — **5.5:1** ✓ this is why buttons and any orange text use the darkened
  variant. The theme's secondary/tertiary buttons put **white text on `--primary-400`**, so
  mapping raw `#ff6600` there would fail.
- `#ff6600` on black — **7.2:1** ✓ hence full orange for footer link hover.

Blue is the workhorse (links, primary buttons, headings); orange is the accent that makes it
Starship Factory; white is the ground. Do not introduce further brand colours. The theme's
greys (`--gray-200` … `--gray-800`) stay as they are.

## Footer links

The footer has **two distinct link groups**.

### 1. Social links: Signal, Instagram, GitHub, Discourse

`layouts/partials/footer/social-links.html` iterates over every non-empty key in
`params.social_links` and renders `/img/social-icons/<key>.svg`:

```yaml
# config/_default/params.yaml
social_links:
  signal: "https://signal.group/#CjQKIIt5fkwCXHlImGzm41tTrf-6umAhyM7ENTpqW4Y0P4SHEhDgMyhI63oL7v3mTk0N7G3t"
  instagram: "https://instagram.com/starship_factory"
  github: "https://github.com/starshipfactory"
  discourse: "https://discourse.starship-factory.ch"
```

Keys map 1:1 to icon filenames — a broken image means a missing icon file, not bad config.
The theme ships icons for a fixed set of networks that **does not include Signal or
Discourse**, so both must be added to `static/img/social-icons/`.

The old site already has artwork for them —
`cdf4f44^:assets/images/icons/signal_icon_256x256.png` and `discourse_icon_256x256.png` — but
the partial hardcodes the `.svg` extension, so PNGs cannot be dropped in as-is. Supply real
SVGs (official brand marks, monochrome, 31×31 like the theme's own icons). Changing the
extension logic would mean forking the partial; prefer supplying SVGs.

### 2. Legal links: Datenschutz, Impressum

**This needs a template override.** `layouts/partials/footer.html` renders only
`.Site.Menus.main` and has no concept of a secondary footer menu, so these two pages cannot
be added through config alone. Copy the theme's `footer.html` into
`layouts/partials/footer.html` and add a row ranging over a `legal` menu, near the copyright:

```yaml
# config/_default/languages.yaml, under de.menu (and en.menu)
menu:
  legal:
  - name: "Datenschutz"
    url: "/datenschutz/"
    weight: 1
  - name: "Impressum"
    url: "/impressum/"
    weight: 2
```

Keep the rest of the forked `footer.html` byte-identical to the theme's so future theme
updates stay easy to merge — including its existing responsive column layout. Use
`relLangURL` on the hrefs, as the theme does, so the links resolve per language.

Note that the theme's footer already lists every `menu.main` entry, so Statuten and
Reglement/Charta appear in the footer automatically now that they are in the main
navigation. Do not add them to `menu.legal` as well — that would duplicate them.

Other links carried over from the old site, for reference (only add if asked):
calendar `https://cloud.starship-factory.ch/apps/calendar/p/NBiqtDiWQZmAZYfq`,
contact `board@starship-factory.ch`. (The old wiki link is deliberately not listed — see
"Deliberately excluded".)

## Responsive design

The site must work on **desktop browsers, tablets and phones**.

**The theme is already fully responsive and that must not be broken.** It ships mobile-first
CSS, a working hamburger menu with a slide-in mobile navigation, a sticky header, responsive
footer columns and fluid images. This is not something to reimplement — the requirement is
satisfied by the theme, and our job is to add content and styling that stays inside its
system.

### Do not break

- **Never fork `layouts/partials/header.html`.** It contains the hamburger button, the
  `menu-item-has-children` dropdown markup and the mobile CTA/language/search wrapper, all
  wired to the theme's `scripts.js` and `hoverintent.min.js`. A fork silently freezes that
  markup at today's version and is the most likely way to break mobile navigation. Solve
  header problems with CSS (see the logo note above).
- **Do not restyle `.hamburger`, `.main-menu`, `.sub-menu` or `.footer__menu`.** The theme's
  `_hamburger.scss`, `_header.scss` and `_footer.scss` own those; overriding them from
  `custom.css` fights the theme's own media queries and breaks at one width or another.
- **Do not add a CSS framework or a competing grid.** No Bootstrap, no Tailwind — the theme's
  container/gutter variables are the layout system.
- **Do not disable or replace `params.sticky_header`** to work around a layout problem; the
  theme's JS reads it.
- Keep the forked `footer.html` structurally identical to the theme's (same wrapper divs and
  classes) so `_footer.scss` keeps laying it out correctly at every width. The legal link row
  should reuse the theme's existing footer classes rather than introduce new ones.

### When adding CSS

Custom CSS goes in **`static/css/custom.css`**, registered as `custom_css: ["/css/custom.css"]`
in `params.yaml`. Note this is *not* the asset pipeline: `head/custom-css.html` does
`{{ . | absURL }}` on the raw string, so the file must live under `static/`, and it is not
fingerprinted or minified. If the pipeline is ever needed (SCSS, fingerprinting), override
`head/custom-head.html` — a designated extension point — rather than moving the file.

Keep it small and additive: brand variables, the logo `height: auto` fix, and little else.
Reuse the theme's breakpoints and variables
(`themes/dot-org-hugo-theme/assets/scss/_variables.scss`) — never invent a second set:

```scss
$min-desktop: 1000px;   // desktop layout and horizontal nav start here
$mobile-max: 999px;     // hamburger menu and stacked layout at or below
$desktop-width: 1250px; // 1200px container + 2 x 25px gutter
--container-width: 1200px;
--content-width: 895px;
```

There is a single nav breakpoint at 1000px: tablets get the mobile layout and the hamburger
menu, not a separate tablet layout. Do not add an intermediate tablet breakpoint.

### Content rules

- Never set a fixed pixel width on content elements. Images get `max-width: 100%`; wide
  content — tables, code blocks, the embedded map on the Anfahrt page — goes in a container
  with `overflow-x: auto` so the page body never scrolls horizontally.
- Embedded iframes (maps, videos) must be fluid; the theme has `_iframe.scss` and a
  `youtube_enhanced` shortcode for this — use them instead of raw `<iframe>` tags.
- Do not shrink the footer social icons below the theme's 31px; they are tap targets.

### Verify

Check three widths before calling responsive work done: **~375px** (phone), **~768px**
(tablet — still the mobile layout) and **~1280px** (desktop). At each, confirm the hamburger
menu still opens and closes, the six top-level nav entries and the ten dropdown children are
all reachable, the logo is undistorted, and the footer's link groups reflow without
horizontal scroll. Check it on a `/fr/` page too, not only the German one: the language
selector now holds three entries, which is the one bit of theme CSS the third language
stresses.

## Commands

Run from the repository root (where `package.json` lives):

```bash
npm install                      # install hugo-extended + build deps
npm run start                    # dev server with drafts & future posts
npm run dev:start:with-pagefind  # dev server with a working search index
npm run build                    # production build into public/
npx -y pagefind --site public    # build/refresh the search index after a build
```

Prefer `npm run start` over a bare `hugo serve` — the scripts pass `--configDir=config` and
the flags the theme expects. Search results are stale until Pagefind reruns, so use the
`with-pagefind` script when touching search.

## Deployment

The repo is `starshipfactory/starshipfactory.github.io` and the site is served from
**GitHub Pages** at the custom domain `starship-factory.ch` (see `static/CNAME`).

Two workflows are in place — `.github/workflows/build.yml` (build check on pull requests,
including the Pagefind index and a lychee link check) and `.github/workflows/deploy.yml`
(build and deploy on `master`). Both must keep doing the following:

- **`actions/checkout` with `submodules: recursive`** — the theme *is* a submodule; without
  this the build fails confusingly with missing layouts. Add `fetch-depth: 0` as well, since
  `enableGitInfo` needs history.
- `actions/setup-node` (Node 22) with npm caching, then **`npm ci`**, not `npm install`.
- Build with `npx hugo --gc --minify --environment production`. Do **not** install Hugo
  separately — it comes from `hugo-extended`.
- Then `npx -y pagefind --site public`, in that order; the index is built from the output.
- Cache `resources/_gen` between runs to keep SCSS/image processing fast.
- Deploy with `actions/upload-pages-artifact` + `actions/deploy-pages`.

Other deployment notes:

- Keep a `CNAME` file (or the equivalent Pages setting) with `starship-factory.ch`.
- Set `baseURL: "https://starship-factory.ch/"` in config.
- Hugo `aliases` emit meta-refresh HTML pages, which is exactly what works on GitHub Pages.
  Netlify-style `_redirects` files do **not** work here — use `aliases` for every old URL.
- The theme ships a `netlify.toml`; it is a reference for the build steps, not the
  deployment target. Do not add Netlify config to this repo.
- **`master` is the live website.** A push to it deploys within a couple of minutes, with
  no review step in between. So: work on a feature branch, open a pull request, let
  `build.yml` go green, and stop there. Do not commit or push to `master`, and do not merge
  a pull request unless asked to — merging is publishing, and that call is Max's.

## Tooling & maintenance

- **`.editorconfig`** at the root; 2-space indent for YAML/HTML/CSS, LF endings.
- **Prettier** is already a theme devDependency — use it for HTML/CSS/YAML we write.
- **Dependabot** is configured in `.github/dependabot.yml` for the npm dependencies, the
  GitHub Actions *and* the theme submodule; the theme is actively developed and pinning it
  silently is how sites rot. A theme-submodule PR must get a local `npm run build` and a
  look at the rendered pages before it is merged — it can move layout, not just versions.
- **Link checking** runs in CI via lychee (`lychee.toml`, internal links only). The site
  carries many old URLs and `aliases` from the migration, so broken links are the most
  likely regression.
- Build with warnings visible before declaring work done. `npm run start` already passes
  `--printI18nWarnings` and `--printPathWarnings`; treat those as errors.

## Conventions

- Content is Markdown in `content/<lang>/`; page bundles (`page-name/index.md` plus its
  images) are preferred for pages that carry their own media.
- Theme front matter extras: `showHeader`, `noindex`. Theme shortcodes exist for buttons,
  cards, columns, tables, FAQ, table-of-contents and YouTube — use them instead of raw HTML.
- Set `description` in front matter: `head.html` uses it for the meta description and
  OpenGraph, falling back to a truncated summary.
- `markup.goldmark.renderer.unsafe: true` is enabled by the theme's example config, so inline
  HTML in Markdown renders. Use it sparingly.
- Verify with a build (`npm run build`) before declaring work done; Hugo fails loudly on
  broken refs.
- Commit messages follow the existing style in this repo: `feat:` / `fix:` / `refactor:`
  prefixes, or a short imperative sentence.
