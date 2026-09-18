# Website scaffolding & setup plan

Step-by-step instructions for building the new Starship Factory Hugo site from the current
empty working tree.

**Read `CLAUDE.md` first.** It holds the standing rules — theme boundaries, branding,
responsive constraints, what is excluded. This file is the *order of operations*; `CLAUDE.md`
is the *law*. Where they disagree, `CLAUDE.md` wins and this file should be corrected.

Work through the phases in order. Each phase ends with a **Done when** checklist and a
**commit** — do not batch ten phases into one commit. Run the verification for a phase before
starting the next; a broken phase 2 makes phase 6 impossible to debug.

---

## Phase 0 — Preconditions

1. Confirm the branch: `git rev-parse --abbrev-ref HEAD` → `feature/new-website-with-hugo`.
2. Confirm the tree is empty apart from `.git` and `.idea`: `ls -a`.
3. Confirm Node ≥ 22: `node --version`. Do **not** install Hugo by hand — it arrives via the
   `hugo-extended` npm package in phase 1.

**Done when:** on the right branch, Node available, no stray files.

---

## Phase 1 — Repository skeleton

```bash
git submodule add https://github.com/cncf/dot-org-hugo-theme.git themes/dot-org-hugo-theme

# Take only these four from the theme's exampleSite. Do NOT copy exampleSite/static
# (CNCF demo images), exampleSite/content, or exampleSite/layouts (empty).
cp themes/dot-org-hugo-theme/exampleSite/package.json .
cp themes/dot-org-hugo-theme/exampleSite/package-lock.json .
cp themes/dot-org-hugo-theme/exampleSite/postcss.config.js .
cp -r themes/dot-org-hugo-theme/exampleSite/config .

cp themes/dot-org-hugo-theme/.gitignore .
```

Then three edits, all of which are wrong-by-default after copying:

1. **Strip `--themesDir=../..` from every script in `package.json`.** Those paths exist
   because `exampleSite` lives *inside* the theme repo. Here the theme is at `themes/`, which
   is Hugo's default, so the flag points at the wrong place and the build fails or silently
   picks up nothing. Affected scripts: `build:production`, `dev:start`,
   `dev:start:with-pagefind`.
2. **Fix `postcss.config.js`.** It ships `overrideBrowserslist: ["> 0.5% in US"]` — a US
   browser market share list, on a Swiss site. Change to `["> 0.5% in CH", "last 2 versions"]`
   or drop the override and use browserslist defaults.
3. **Extend `.gitignore`** with the entries listed in `CLAUDE.md` → Setup:
   `static/pagefind/` and `.idea/` in particular.

```bash
npm install
npm run build     # smoke test — must succeed before going further
```

The build will produce a near-empty site with the theme's demo config. That is expected.

**Done when:** `npm run build` exits 0 and `public/index.html` exists.
**Commit:** `feat: scaffold hugo site with dot-org theme`

---

## Phase 2 — Configuration

Rewrite the three copied config files. Full key list and rationale in `CLAUDE.md` →
"Site configuration" and "Multilingual"; do not re-derive it here.

**`config/_default/hugo.yaml`** — set `baseURL`, `title`, `theme`,
`timeZone: "Europe/Zurich"` (the copied value is `America/Los_Angeles` and **must** change),
`contentDir: content/de/`, `defaultContentLanguage: de`,
`defaultContentLanguageInSubdir: false`, `enableRobotsTXT`, `enableGitInfo`,
`module.hugoVersion`, `pagination.pagerSize`, `permalinks`, `taxonomies`, and keep the
theme's `markup.goldmark.renderer.unsafe` and `privacy` blocks.

Delete `hasCJKLanguage: true` — it is in the copied file and is meaningless for de/en.

**`config/_default/languages.yaml`** — replace the demo `en`/`es` block entirely with `de`
(weight 1, `languageCode: de-CH`) and `en` (weight 2, `contentDir: content/en`). Each gets
`title`, `params.description`, `params.accessibility`, `params.main_cta`,
`params.footer_cta`, `copyright`, and its `menu.main` (7 entries) + `menu.legal` (2 entries)
per `CLAUDE.md` → "Content sections".

**`config/_default/params.yaml`** — set `logo_on_white`, `logo_on_black`, `custom_css`,
`social_links` (the four real URLs), `github.repo_url`, `sticky_header`, `show_search`.
Empty every `social_links` key the theme ships that we do not use; a leftover CNCF LinkedIn
URL in the footer is a real risk here.

Create **`config/production/hugo.yaml`** for production-only overrides.

**Done when:** `npm run build` still exits 0; `public/` now contains `/en/`; no CNCF or
"Dot Org Theme Demo" strings survive: `grep -ri "cncf\|dot org theme demo" public/ | grep -v pagefind`.
**Commit:** `feat: configure site, languages and params`

---

## Phase 3 — Files the theme requires

Create the structural files listed in `CLAUDE.md` → "Required files the theme expects".
Placeholder body text is fine at this stage; the structure is what matters.

```
content/de/_index.md              content/en/_index.md
content/de/blog/_index.md         content/en/blog/_index.md
content/de/search.md              content/en/search.md      # both contain {{< search_form >}}
i18n/de.yaml                      i18n/en.yaml
data/authors.yaml
archetypes/default.md  archetypes/blog.md                   # copied from the theme, adapted
```

For `i18n/*.yaml`: start by grepping the theme for translatable strings so nothing is
missed —

```bash
grep -rno 'i18n "[^"]*"' themes/dot-org-hugo-theme/layouts | sort -u
```

— then define every key found, in both languages.

**Done when:** `/search` and `/blog/` both render in `npm run start` (and their `/en/`
counterparts), and the header search icon leads somewhere real.
**Commit:** `feat: add required content, i18n and data files`

---

## Phase 4 — Brand assets

Follow `CLAUDE.md` → "Branding: logo & colours" exactly; it carries the hex values, the
contrast measurements and the favicon rules.

1. **Logo:** `git show master:assets/images/logo.svg > static/img/logo.svg`.
2. **Dark variant:** create `static/img/logo-on-dark.svg` with the planet recoloured white
   for the black footer.
3. **Favicons:** author `static/favicon.svg` by hand as a square-`viewBox` crop of the mark,
   then generate `favicon.ico` (real multi-size ICO), `favicon-32x32.png` and
   `apple-touch-icon.png` (180×180, **opaque white background**). Reference for the framing:
   `git show master:favicon.ico` — note it is a 32×32 PNG despite the extension.
4. **Social icons:** `static/img/social-icons/signal.svg` and `discourse.svg`, monochrome,
   31×31, matching the theme's existing icons. The old
   `master:assets/images/icons/*_256x256.png` files show the intended marks but cannot be
   used directly — the partial hardcodes `.svg`.
5. **Palette:** create `static/css/custom.css` with the brand custom-property block and the
   `.header .logo, .footer .logo { height: auto; }` fix. Register it in `params.yaml` as
   `custom_css: ["/css/custom.css"]`.

**Done when:** header and footer logos are undistorted and correctly coloured against their
backgrounds; all four social icons render; the tab icon is Starship Factory's, **not**
CNCF's (hard-refresh — favicons cache aggressively); links and buttons show brand blue and
orange rather than CNCF green.
**Commit:** `feat: add starship factory branding, logo and favicons`

---

## Phase 5 — Footer override

The only template fork the site needs. Per `CLAUDE.md` → "Footer links":

```bash
cp themes/dot-org-hugo-theme/layouts/partials/footer.html layouts/partials/footer.html
```

Add a row ranging over `.Site.Menus.legal` near the copyright, using `relLangURL` and the
theme's existing footer classes. Add a comment at the top of the file recording the theme
version it was forked from and why. **Change nothing else in it.**

Verify the fork is otherwise clean:

```bash
diff themes/dot-org-hugo-theme/layouts/partials/footer.html layouts/partials/footer.html
```

The diff should show the header comment and the legal row — nothing more.

**Done when:** Datenschutz and Impressum appear in the footer in both languages; Statuten and
Reglement appear there too (automatically, via `menu.main`) and are not duplicated.
**Commit:** `feat: add legal links row to footer`

---

## Phase 6 — Content migration

Do the pages first, the blog second — the blog is the long tail and should not block a
reviewable site.

**German and English are migrated together.** Per `CLAUDE.md` → "Translating", English is
produced by translating the German, and nothing is committed German-only. Treat
"port the page" and "translate the page" as one unit of work, not two phases — coming back
later to translate a hundred pages is how a site ends up half-translated forever.

### 6a. The nine pages

For each of the seven nav pages plus Datenschutz and Impressum:

1. Read the old source: `git show master:_pages/<name>.md`.
2. Port the body to `content/de/<slug>/index.md`, convert front matter, strip Jekyll syntax,
   add `aliases` for any changed URL (Statuten and Reglement both moved out of
   `/organisation/`).
3. **Translate it to `content/en/<translated-slug>/index.md` in the same step**, with a
   matching `translationKey` and the English slug from the table in `CLAUDE.md` →
   "Content sections".

Legal pages (Impressum, Datenschutz, Statuten, Reglement) carry the "German is the legally
binding version" note on their English versions — see `CLAUDE.md` → "Translating".

**Stop and ask** rather than inventing: membership fees, bank/donation details, the exact
address and opening hours, and anything on Datenschutz/Impressum that looks outdated. Port
what `master` says verbatim and flag anything that appears stale — legal pages are not a
place to improvise.

### 6b. The blog

Migrate `master:_posts/*.md` into `content/de/blog/`. Per `CLAUDE.md` → "Blog migration":
front matter conversion, `author` keys resolving against `data/authors.yaml`, permalinks via
config (not per-post aliases), `/feed.xml` → `/index.xml` alias, and images moved into page
bundles rather than a bulk `static/` copy.

**Each post is translated into `content/en/blog/` as it is migrated**, in the same batch and
the same commit. The archive gets translated too — old posts are not an exception.

There are ~100 posts, so this is the long pole of the project. Migrate in dated batches
(e.g. one year per batch), committing per batch, so a mistake in the conversion or the
translation is cheap to find and fix. Report progress by count — "2013–2015 done, 31 posts,
both languages" — rather than calling the phase complete while batches remain.

Posts are page bundles, so a translated post lives at
`content/en/blog/<translated-slug>/index.md` and **shares no image files with the German
version** — reference the images from the German bundle via the shared `static/img/` path if
duplication becomes a problem, or accept the duplication for small images.

**Done when:** every nav entry resolves, no page 404s in either language, every German page
and post has an English counterpart reachable via the language selector, and a sample of old
post URLs still work.
**Commit:** per page group and per blog batch, each containing both languages.

---

## Phase 7 — Responsive & accessibility QA

Per `CLAUDE.md` → "Responsive design". Check at **375px**, **768px** and **1280px**:
hamburger opens/closes, all seven nav entries reachable, logo undistorted, footer groups
reflow, no horizontal scroll on any page. Pay particular attention to the Anfahrt map and any
wide tables migrated from the old site.

Also: every image has alt text, `params.accessibility` is filled in for both languages, and
the brand colours still pass the contrast figures recorded in `CLAUDE.md`.

**Commit:** `fix: responsive and accessibility corrections`

---

## Phase 8 — CI/CD

Two workflows in `.github/workflows/`, both per `CLAUDE.md` → "Deployment":

- **`build.yml`** — on pull requests: checkout with `submodules: recursive` and
  `fetch-depth: 0`, setup Node 22, `npm ci`, `npx hugo --gc --minify --environment production`,
  `npx -y pagefind --site public`. No deploy.
- **`deploy.yml`** — on push to the default branch: the same build, then
  `actions/upload-pages-artifact` + `actions/deploy-pages`. Cache `resources/_gen`.

Add `static/CNAME` containing `starship-factory.ch`.

The single most common failure here is a missing `submodules: recursive` — the build fails
with confusing "missing layout" errors rather than "missing theme".

**Done when:** the PR workflow is green.
**Commit:** `ci: add build and github pages deploy workflows`

---

## Phase 9 — Tooling

Per `CLAUDE.md` → "Tooling & maintenance": `.editorconfig`, a Prettier config plus a
`format` script, Renovate or Dependabot covering **both** npm and the git submodule, and a
link checker in CI. Left until last deliberately — none of it blocks the site, and a link
checker is only meaningful once the content exists.

**Commit:** `chore: add editorconfig, prettier, dependency updates and link checking`

---

## Cutover — **Max does this manually. Claude never does.**

`master` still serves the old Jekyll site, and merging this branch replaces the live website.
**Max performs the merge himself, by hand, once the site is complete.**

That means Claude must not:

- merge `feature/new-website-with-hugo` into `master`,
- push to `master`,
- open or merge a pull request against `master` as a "final step",
- or treat the merge as the natural conclusion of phase 9.

The deliverable is a finished site on `feature/new-website-with-hugo`. When every phase is
done, say so, hand over the verification results, and stop.

Have this ready for the handover so the merge decision is an informed one: link check passes,
all old URLs resolve via aliases, the feed alias works, favicons and branding verified in a
real browser, every page and post present in both languages, and someone from the club has
read the German copy — and ideally the English too, since it is machine-translated.

---

## Working notes

- **Verify each phase in a browser, not only via exit codes.** A Hugo build succeeds happily
  with a broken layout, an unstyled page or a missing icon.
- **Report honestly.** If a phase is partly done — say, 60 of 100 posts migrated — say so
  with the number, rather than calling the phase complete.
- **`themes/dot-org-hugo-theme/` is read-only.** If a fix seems to require editing it, that
  is the signal to re-read `CLAUDE.md` → "Repository layout" and find the override or the CSS
  hook instead.
- The theme's `exampleSite/content/` is a useful reference for shortcode usage even though we
  do not copy it.
