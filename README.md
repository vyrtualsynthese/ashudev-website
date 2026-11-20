# ashudev-website

The site served at `https://ashudev.com`.

## Two trees

| Path | What it is |
|---|---|
| `src/` | The site as it is written: static HTML and its assets, no build step |
| `finbiz-html/` | The purchased template's own files, kept as the reference for markup and styles |

There is no bundler, no `package.json`, and nothing to compile: `src/index.html`
and the files next to it are the site.

## How it is published

GitHub Pages serves the **`gh-pages`** branch with a legacy branch build and the
custom domain `ashudev.com` (`CNAME` in that branch, HTTPS enforced). Nothing
publishes automatically: the branch is written by hand.

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

Two details that break the site when they are missing: `CNAME` (without it Pages
drops the custom domain, and the certificate with it) and `.nojekyll` (without
it Pages runs Jekyll and hides every path that starts with an underscore).

After the push, `gh api repos/vyrtualsynthese/ashudev-website/pages/builds/latest`
answers `"status":"built"`, and the page is live within a minute.

## What used to publish it

A workflow on every push to `main` synced a `dist/` directory to
`s3://ashudev-website` through CloudFront. The bucket, the distribution and the
certificate were destroyed on 2026-11-20 with the move to GitHub Pages, and the
`dist/` directory had stopped being produced when the site became static. The
workflow was deleted rather than repaired: it deployed something that no longer
existed, to a place that no longer existed.
