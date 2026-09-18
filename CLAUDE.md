# CLAUDE.md

Guidance for Claude Code when working in this repository.

## Project

The website of **Starship Factory**, the makerspace/hackerspace in Basel, Switzerland
(https://starship-factory.ch).

This branch (`feature/new-website-with-hugo`) is a **greenfield rewrite**. The previous site
was a Jekyll site using the `minimal-mistakes` theme; it has been removed (commit `cdf4f44`
"refactor: removed old clutter"). The working tree is intentionally empty apart from `.git`
and `.idea` — everything is built from scratch here.

The old site is still fully available on the `master` branch and is the source of truth for
migrating content and assets:

```bash
git show master:_pages/anfahrt.md          # read a single old file
git show master:assets/images/logo.svg     # extract an old asset
git ls-tree -r --name-only master           # list all old files
```

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

The theme is consumed as a **git submodule** in `themes/dot-org-hugo-theme`:

```bash
git submodule add https://github.com/cncf/dot-org-hugo-theme.git themes/dot-org-hugo-theme
```

The theme's `exampleSite/` is the reference implementation. Copy `package.json`,
`postcss.config.js` and `config/` from it into the repo root, then `npm install`.
Update the theme with `git submodule update --remote --merge`.

Copy the theme's `.gitignore` too, and extend it. It must contain at least:

```gitignore
public/
resources/
node_modules/
.hugo_build.lock
hugo_stats.json
.DS_Store
static/pagefind/     # generated search index
.idea/               # JetBrains project files, currently untracked in this repo
```

## Repository layout

```
config/_default/hugo.yaml       # core Hugo config (see "Site configuration")
config/_default/languages.yaml  # per-language: title, params, main + legal menus
config/_default/params.yaml     # logos, social_links, custom_css, search toggle
config/production/hugo.yaml     # production-only overrides (hugo.Environment)
content/de/                     # German content (default language)
content/en/                     # English content
i18n/de.yaml, i18n/en.yaml      # UI strings — the theme ships NO i18n files
data/authors.yaml               # blog authors, keyed by GitHub username
archetypes/                     # copied from the theme, adapted
layouts/partials/footer.html    # override: adds the legal link row (see Footer below)
layouts/blog/list.html          # override: makes /blog/ searchable (see "Search")
layouts/partials/image.html     # shared image-pipeline renderer (see "Images & media")
layouts/shortcodes/img.html     # override: routes {{< img >}} through the pipeline
layouts/_default/_markup/render-image.html   # markdown image render hook
static/css/custom.css           # branding + small fixes (see "Branding")
static/img/                     # logo variants, social share image
assets/img/blog/                # blog archive images, flat, shared by de + en
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
template. Current overrides: `footer.html` (legal link row), `byline.html` (per-language
post dates), `index.html` (home page), `button.html` (external link targets),
`img.html` (image pipeline) and `blog/list.html` (search indexing of `/blog/`).
`partials/image.html` and the render hook are not forks — the theme has no equivalent
files.

The theme provides these designated extension points; use them instead of forking:
`params.custom_css`, `params.custom_js`, `layouts/partials/head/custom-head.html`,
`layouts/partials/footer/custom-js.html`.

## Required files the theme expects

The theme silently degrades — or serves CNCF's assets — when these are missing. Create all
of them:

| File | Why |
|------|-----|
| `content/<lang>/search.md` | `show_search: true` renders a header link to `/search`. That page does not exist unless you create it, containing `{{< search_form >}}`. Without it the search icon 404s. |
| `content/<lang>/blog/_index.md` | Section list page. Without it the blog section renders empty. |
| `content/<lang>/_index.md` | Home page. |
| `static/favicon.ico`, `static/favicon.svg`, `static/favicon-32x32.png`, `static/apple-touch-icon.png` | **The theme ships its own CNCF favicons in its `static/`, which get published to the site root.** Browsers request `/favicon.ico` unprompted, so without ours the CNCF icon is what people bookmark. `head/favicons.html` only emits `<link>` tags for files that exist with *exactly* these names. Regenerate all four from the old favicon — see "Favicons" under Branding. |
| `i18n/de.yaml`, `i18n/en.yaml` | The theme has **no `i18n/` directory at all**; template strings such as `social_link_title` fall back to hardcoded English. Any UI string that should be German must be defined here. |
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
  pagerSize: 5                # the old site's `paginate: 5`.
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

German is the **main/default** language, English is secondary.

In `config/_default/hugo.yaml`:

```yaml
contentDir: content/de/
defaultContentLanguage: de
defaultContentLanguageInSubdir: false
```

German therefore lives at the site root (`/anfahrt/`) and English under `/en/`
(`/en/how-to-find-us/`). In `config/_default/languages.yaml` define `de` (weight 1,
`languageCode: de-CH`) and `en` (weight 2, `contentDir: content/en`), each with its own
`title`, `params.description`, CTA texts and menus.

Rules:

- **German is written first and is the source of truth. English is produced by translating
  it.** Never author an English page independently — it drifts from the German and nobody
  notices.
- **Every German page and every blog post gets an English translation**, produced as part of
  the same task that creates or changes the German. A German page committed without its
  English counterpart is unfinished work, not a backlog item. Hugo's fallback to the default
  language exists as a safety net, not as a plan.
- Link translated pages with an explicit `translationKey` in front matter, so the theme's
  language selector works even when the slugs differ.
- UI strings go in `i18n/de.yaml` / `i18n/en.yaml`, never hardcoded in a template.
- German content uses Swiss German orthography: **"ss" instead of "ß"** (`Strasse`,
  `Schliessfach`), and Swiss number/date conventions.
- Address the reader with the informal **"du"** — that is the tone of the space. In English
  use the equivalent plain, direct register ("you", contractions, no corporate voice).

### Translating

Translate the meaning, not the words. The English site should read as though written by a
member, not as output from a translation tool.

- **Translate the slug too**, and keep it in the front matter: `/mitglied-werden/` becomes
  `/en/become-a-member/`, not `/en/mitglied-werden/`. Front matter `title`, `description`,
  `summary` and image alt text all get translated as well — not just the body.
  **One exception: `search.md` keeps its filename in both languages.** The theme's
  `header.html` hardcodes `{{ "/search" | absLangURL }}`, so a German `suche.md` would leave
  the header's search icon pointing at a 404. Translate its `title` to "Suche", not its path.
- **Do not translate proper nouns**: "Starship Factory", street and place names, Basel
  transport lines and stop names, "Verein" when it names the legal entity, product and
  machine names. Keep the German term and add a short gloss on first use where an English
  reader would otherwise be lost (e.g. *Verein* — a Swiss registered association).
- Keep German terms that have no clean English equivalent and that members actually say,
  rather than inventing English ones.
- Convert nothing factual: prices in CHF stay CHF, dates and addresses keep Swiss format,
  IBANs and opening hours are copied verbatim. A translation must not change a number.
- Keep the Markdown structure identical — same headings, same links, same images, same
  shortcodes — so the two languages stay diffable against each other.
- **Legal pages are a special case.** Translate Impressum, Datenschutz, Statuten and
  Reglement/Charta for comprehension, but add a line at the top of each English version
  stating that the German original is the legally binding version, and never reword a legal
  clause to "improve" it. If a passage is genuinely ambiguous, translate it literally and
  flag it rather than interpreting it.
- When the German changes later, update the English in the same commit.

## Content sections

Menu order, German (default) URLs, and their English counterparts:

| Section        | German URL          | English URL              | Notes                                     |
|----------------|---------------------|--------------------------|-------------------------------------------|
| Home           | `/`                 | `/en/`                   | `content/<lang>/_index.md`                |
| Blog           | `/blog/`            | `/en/blog/`              | List + posts, migrated from old `_posts/` |
| Mitglied werden| `/mitglied-werden/` | `/en/become-a-member/`   | Membership info + main CTA                |
| Anfahrt        | `/anfahrt/`         | `/en/how-to-find-us/`    | Address, public transport, map            |
| Spenden        | `/spenden/`         | `/en/donate/`            | Donation options                          |
| Statuten       | `/statuten/`        | `/en/statutes/`          | From `master:_pages/organisation/statuten.md` |
| Reglement/Charta| `/reglement/`      | `/en/charter/`           | From `master:_pages/organisation/reglement.md` |

All seven are the **header navigation** (`menu.main`), in that order. The header CTA
(`params.main_cta`) and footer CTA (`params.footer_cta`) both point at "Mitglied werden".

Two further pages exist for the **footer only** (`menu.legal`, see below) and must not be
added to `menu.main`:

| Page            | German URL     | Source on `master`                  |
|-----------------|----------------|-------------------------------------|
| Datenschutz     | `/datenschutz/`| `_pages/datenschutz.md`             |
| Impressum       | `/impressum/`  | `_pages/impressum.md`               |

The old site nested Statuten and Reglement under `/organisation/`. The new site flattens
them; add `aliases: ["/organisation/statuten/"]` (resp. `reglement`) in the front matter so
the old URLs keep working.

Seven top-level entries is a lot for the horizontal desktop menu. If it wraps or crowds the
CTA, group Statuten and Reglement/Charta under a parent entry using the theme's `parent:`
menu key rather than dropping them — the theme renders children as a dropdown on desktop and
as a nested list in the hamburger menu, and both are already styled.

### Excluded from the new site

- **The wiki is out of scope entirely.** The old site had a `wiki` collection, a
  `_layouts/wiki.html`, a `wiki-sidebar.html` and a `Wiki` nav entry pointing at
  `https://wiki.starship-factory.ch/`. Do **not** migrate any of it, do **not** add a wiki
  section, and do **not** add a wiki link to the header or footer. If wiki content comes up
  during migration, skip it and say so rather than porting it.
- The old `verein`, `events`, and archive pages (`category-archive`, `tag-archive`,
  `year-archive`) are not part of the sections above. Do not add them unless asked.
- A 404 page needs no work: the theme ships `layouts/404.html`, and GitHub Pages serves
  `/404.html` automatically. Add `content/<lang>/404.md` only if custom copy is wanted.

### Blog migration

Old posts live at `master:_posts/YYYY-MM-DD-slug.md` with Jekyll front matter and a
`/:year/:month/:day/:title/` permalink.

- Create new posts with the theme's archetype: `hugo new content blog/my-post.md`. Copy
  `archetypes/{default,blog,faq}.md` from the theme into the project root and adapt them.
  With a multilingual `contentDir`, pass the language explicitly or create the file under
  `content/de/blog/` by hand.
- Convert front matter to Hugo (`title`, `description`, `date`, `author`, `draft`, `tags`,
  `categories`). `author` must match a key in `data/authors.yaml`.
- The permalink structure is handled by the `permalinks` config above, not per post. Use
  `aliases` only for posts whose slug had to change.
- **The feed URL changes.** Jekyll served `/feed.xml`; Hugo serves `/index.xml`. Add an
  alias or a redirect so existing subscribers do not silently break.
- Rewrite Jekyll-isms: `{% include %}`, `{% highlight %}`, and `/assets/images/...` paths
  (images now live at `/img/blog/...`).
- **Every post gets an English translation** under `content/en/blog/`, per the "Translating"
  rules above. Old posts are translated too — the archive is part of the site, not an
  exception. Translate a post in the same batch in which it is migrated, so no post is ever
  committed German-only.
- Post `date` and `author` must be identical in both languages; only the prose, `title`,
  `description`, `slug` and `tags` are translated. Keep `translationKey` on both.
- **Known theme limitation — the byline date is English-only.**
  `partials/blog/byline.html` hardcodes `.Date.Format "January 2, 2006"`, so German posts
  render "August 30, 2026" instead of "30. August 2026". Fixing it means overriding that one
  partial to format per language (e.g. via `time.Format` with a language-aware layout, or an
  `i18n` date string). Decide before migrating posts; it affects all 96.
- The old posts use German `ß` (`großen`, `gießen`). Normalise to Swiss `ss` during
  migration, per the orthography rule above.
- Old posts carry minimal-mistakes front matter such as `header.teaser`, which has no Hugo
  equivalent — map it to the page bundle's cover image or drop it.

## Images & media

The old site carries a large `assets/images/uploads/` tree. Do not bulk-copy it into
`static/`.

**Three homes, and which to pick.** `static/` is copied verbatim with no processing;
`assets/` and page bundles both go through Hugo's image pipeline. Default to a page
bundle, use `assets/` when two languages share one file, and keep `static/` for files
that need a fixed, unhashed URL (favicons, `logo.svg`, `social-share.png`).

- Migrate images **as page bundles**: `content/de/blog/my-post/index.md` with its images
  beside it.
- **Exception, already applied to the blog archive.** The 58 images referenced by the
  migrated posts live flat in `assets/img/blog/`, rather than in per-post bundles, because
  the German and English version of a post reference the same file and bundles would
  duplicate every one of them. New posts should still use page bundles.

  This tree was reorganised out of `static/assets/images/snippet_images/{content,content_small}/`
  — the old Jekyll/Zinnia paths — and 82 unreferenced files were deleted at the same time.
  The old image URLs (`/assets/images/…`) therefore no longer resolve; page URLs were not
  affected. `aliases` cannot help here, as they only work for pages, not static files.
  Do not reintroduce `static/assets/`.

  It later moved again, from `static/img/blog/` to `assets/img/blog/`, so the archive
  gets pipeline treatment while both languages keep sharing one copy of each file.
  **The markdown still says `/img/blog/foo.jpg`** — the render hook strips the leading
  slash and looks the path up in `assets/`. That deliberately avoids rewriting the image
  line in all 192 archive files and keeps the German and English copies diffable. Do not
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
  fill it in, in both languages.
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
covers every regular page and every blog post, in both languages.

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
- **Taxonomy list pages** (`/tags/…`, `/categories/…`). Keyword listings, 272 of them, that
  would crowd out real pages.
- Not by choice: the `/search` page indexes itself as a near-empty result. Excluding it
  cleanly would need `data-pagefind-ignore` on an ancestor of `#content`, i.e. a
  `baseof.html` fork, which is not worth it.

Pagefind splits the index by the `<html lang>` attribute on its own, so a German search
returns German pages only, and its UI strings are localised without anything in `i18n/`.
After a build, `public/pagefind/pagefind-entry.json` reports the per-language page counts —
check it when changing what is indexed. A page with a near-zero word count there is a
content problem, not a search one: **the seven workshop pages (`/laser/`, `/3d-druck/`,
`/cnc-bearbeitung/`, `/elektronik/`, `/holzwerkstatt/`, `/textil/`, `/folien-plotten/`) and
their English counterparts are front-matter-only stubs with no body**, so they are indexed
on their title alone and are effectively unfindable by anything else.

## Branding: logo & colours

### Logo

Use the **Starship Factory logo from the old website**, at `master:assets/images/logo.svg`:

```bash
git show master:assets/images/logo.svg > static/img/logo.svg
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
`master:favicon.ico`:

```bash
git show master:favicon.ico > /tmp/old-favicon.ico
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
`master:assets/images/icons/signal_icon_256x256.png` and `discourse_icon_256x256.png` — but
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
"Excluded from the new site".)

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
menu still opens and closes, the seven main-nav entries are all reachable, the logo is
undistorted, and the footer's link groups reflow without horizontal scroll.

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
**GitHub Pages** at the custom domain `starship-factory.ch` (see `CNAME` on `master`).

Two workflows: a build check on pull requests, and build-and-deploy on the default branch.
Both must:

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
- **`master` still serves the old Jekyll site, and merging is the user's job.** Do not merge
  this branch into `master`, do not push to `master`, and do not open the merge as a
  "finishing touch" — the merge replaces the live website and Max performs it manually once
  the site is complete. Finish the work on `feature/new-website-with-hugo`, report that it is
  ready, and stop there.

## Tooling & maintenance

- **`.editorconfig`** at the root; 2-space indent for YAML/HTML/CSS, LF endings.
- **Prettier** is already a theme devDependency — use it for HTML/CSS/YAML we write.
- **Renovate or Dependabot** for both the npm dependencies *and* the theme submodule; the
  theme is actively developed and pinning it silently is how sites rot.
- **Link checking** in CI (e.g. lychee) — this site is a migration with many old URLs and
  `aliases`, so broken links are the most likely regression.
- Build with warnings visible before declaring work done. `npm run start` already passes
  `--printI18nWarnings` and `--printPathWarnings`; treat those as errors during migration.

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
