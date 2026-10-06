# adamwhansen.com

Personal site of Adam W. Hansen. Plain HTML and CSS built by Jekyll, which GitHub Pages runs automatically: push to `gh-pages` and the live site updates in a minute or two. No framework, no analytics, no third-party requests. Type is Newsreader (SIL Open Font License), self-hosted in `assets/fonts/`.

Pages: the homepage (`index.html`), `/research/`, and a 404 page, plus Traditional Chinese (Taiwan) versions of the homepage and research page at `/zh-tw/` and `/zh-tw/research/`. Both languages share one layout: `_includes/home.html` and `_includes/research.html`.

## What to edit

Everything that changes lives in `_data/` (lists, in YAML) and `_copy/` (prose, in Markdown). You shouldn't need to touch layout files to keep the site current.

| To change… | Edit |
| --- | --- |
| Name, title line, photo, profile links | `_data/profile.yml` |
| The four facts under the intro | `_data/record.yml` |
| Intro paragraph | `_copy/intro.md` |
| "What I'm working on" | `_copy/now.md` |
| "From gene discovery to Geneial" text | `_copy/through-line.md` |
| The four-step progression under it | `_data/arc.yml` |
| "What I think" (the numbered positions in the dark band) | `_data/takes.yml` |
| Figure 1 (POLR2A variant map) | `_data/polr2a_variants.yml` |
| Figure 2 (Xia-Gibbs registry growth): refresh from the public dashboard now and then | `_data/xgs_registry.yml` |
| Papers (`selected: true` also shows one on the homepage) | `_data/publications.yml` |
| Conference abstracts (research page) | `_data/abstracts.yml` |
| NIH-funded projects (research page) | `_data/grants.yml` |
| Patents, reports, and code (research page) | `_data/other_work.yml` |
| Recognition and service | `_data/recognition.yml` |
| Press and coverage | `_data/coverage.yml` |
| Talks and panels (`selected: true` also shows one on the homepage) | `_data/talks.yml` |
| Speaking topics | `_copy/speaking.md` |
| Outside work, contact text | `_copy/outside.md`, `_copy/contact.md` |
| Outside-work photos (4:5 crops in `assets/img/outside/`) | `_data/outside_photos.yml` |
| Short description search engines read (not shown on the page) | `_copy/bio-short.md` |
| Top navigation | `_data/nav.yml` |
| Search title and description for the homepage | `_config.yml` |

**Prose files (`_copy/`)** are Markdown: `**bold**`, `[link text](https://…)`, and `- ` for bullets. Keep the `---` lines at the top; Jekyll needs them.

**Data files (`_data/`)** are YAML. Copy an existing entry and keep the indentation. Put any text containing a colon in straight double quotes, e.g. `title: "Start-ups: Where to Start?"`. You can edit these directly on github.com; GitHub rebuilds the site after each commit.

**Chinese version:** prose lives in `_copy/zh-tw/` (one file per English file in `_copy/`). In the data files, each item can carry a `zh:` block with the Chinese version of its text fields, e.g. `zh: { note: … }`; anything without one shows in English. Paper, abstract, and grant titles, author lists, and official talk titles stay in English on purpose. Section headings and other fixed labels are in `_data/ui.yml`. When you change English text, update its `zh:` version too.

**Sources:** almost every claim links to a third-party source (the small labeled tags). Keep it that way. Only add facts that are public and verifiable.

## Preview locally

One-time setup on a Mac: `brew install ruby@3.3`, then from this folder:

```sh
export PATH="/opt/homebrew/opt/ruby@3.3/bin:$PATH"
bundle config set --local path vendor/bundle
bundle install
```

Each time:

```sh
export PATH="/opt/homebrew/opt/ruby@3.3/bin:$PATH" LANG=en_US.UTF-8
bundle exec jekyll serve
```

Then open http://localhost:4000. Edits to `_data/` and `_copy/` reload on refresh; changes to `_config.yml` need a restart. The `github-pages` gem pins the Jekyll version and plugins GitHub uses, so what you see locally is what deploys.

## Deploy

GitHub Pages builds the `gh-pages` branch (custom domain in `CNAME`). Before pushing, build the site and run the language check, which fails if any Chinese text shows up on an English page (other than the "中文" link) or a page uses the wrong share image:

```sh
bundle exec jekyll build && python3 tools/check_languages.py _site
```

Then commit, push, and check the live site after a couple of minutes. If a build fails, GitHub shows the error in the repository's Actions tab and the previous version stays live.

## Regenerating images

The share previews (`assets/img/og-card.png`, and `og-card-zh-tw.png` for the Chinese pages) and the icons are rendered from HTML in `tools/` with headless Chrome:

```sh
tools/render.sh tools/og-card.html assets/img/og-card.png 1200 630
tools/render.sh tools/og-card-zh-tw.html assets/img/og-card-zh-tw.png 1200 630
tools/render.sh "tools/icon.html#180" assets/img/apple-touch-icon.png 180 180
tools/render.sh "tools/icon.html#32-rounded" /tmp/favicon-32.png 32 32 && python3 tools/png2ico.py /tmp/favicon-32.png favicon.ico
```

Re-render the cards if your name, title, or photo changes.
