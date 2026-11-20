# ashudev-website

The site served at `https://ashudev.com`.

## Two trees

| Path | What it is |
|---|---|
| `src/` | The site as it is written: static HTML and its assets, no build step |
| `finbiz-html/` | The purchased template's own files, kept as the reference for markup and styles |

There is no bundler, no `package.json`, and nothing to compile: `src/index.html`
and the files next to it are the site.

## Where the styles live

| File | What it holds |
|---|---|
| `src/assets/css/style.css` | The template's stylesheet, used as delivered except for the font import |
| `src/assets/css/fonts.css` | Red Hat Display and DM Sans, self-hosted: the page requests no third party |
| `src/assets/css/ashudev.css` | Overrides for this site: wordmark, client logos, footer, contact form |

Fonts are SIL Open Font License 1.1; the licence texts sit next to the `.woff2`
files in `src/assets/fonts/`.

## Local preview

```bash
python3 -m http.server -d src 8000
```

Then open `http://127.0.0.1:8000/`. Serving the directory matters: opening the
file directly breaks the relative asset paths.

## The contact form

The site is static and has no form backend. The form composes an e-mail in the
visitor's own mail client and sends nothing to a server, which is what the
privacy page states. Sending it directly (Formspree, Web3Forms, an API of your
own) means changing the form's `action` and the privacy page with it.

## How it is published

The **`gh-pages`** branch is the site's content. Since 2026-11-20 the homelab
cluster serves `ashudev.com`: the `ashudev-website` chart in the `homelab`
repository clones that branch into an nginx pod and re-fetches it every 60
seconds. Nothing publishes automatically: the branch is written by hand.
GitHub Pages still builds it, but the domain's DNS points at the cluster, so the
build is no longer what a visitor receives.

Publishing the current `src/` over it:

```bash
git fetch origin
git switch gh-pages
git rm -rq --ignore-unmatch .          # empty the published tree
git checkout origin/develop -- src     # take the site from the branch you published
mv src/* . && rmdir src
printf 'ashudev.com\n' > CNAME
touch .nojekyll
git add -A && git commit -m "🌐 site: publish"
git push origin gh-pages
```

`CNAME` and `.nojekyll` date from when Pages served the domain. The cluster
ignores both — it clones the branch and nginx serves it — so they are kept only
to leave the branch a valid Pages source.

After the push, the cluster's clone fetches the new commit on its next 60-second
interval.

## What used to publish it

A workflow on every push to `main` synced a `dist/` directory to
`s3://ashudev-website` through CloudFront. The bucket, the distribution and the
certificate were destroyed on 2026-11-20 with the move to GitHub Pages, and the
`dist/` directory had stopped being produced when the site became static. The
workflow was deleted rather than repaired: it deployed something that no longer
existed, to a place that no longer existed.
