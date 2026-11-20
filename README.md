# ashudev-website

The site served at `https://ashudev.com`.

## Two trees

| Path | What it is |
|---|---|
| `src/` | The site as it is written: static HTML and its assets, no build step |
| `finbiz-html/` | The purchased template, no longer used by the site; kept as the reference it came from |

There is no bundler, no `package.json`, and nothing to compile: `src/index.html`
and the files next to it are the site.

## Where the work is tracked

The repository has a project on the Vikunja board at <https://vikunja.kub.local>
(LAN only): `ashudev-website`, with one kanban view, `Board`, whose columns are
`Idea`, `Shaping`, `Backlog`, `Doing`, `Validation` and `Done`.

Pending work is a card there, and nowhere else: no `TODO.MD`, no checklist in
this file. A ticked box says an agent ran out of steps; a card says whether the
work was accepted. The process is `homelab/docs/agent-protocol.md` — in short,
agents move tasks between `Doing` and `Validation`, and only the operator moves
one to `Done`.

## What the page is

One page, written to bring in contracts: who you are, what you do, where you
worked, how to reach you, and the CV. Nothing else, and no JavaScript.

| File | What it holds |
|---|---|
| `src/index.html` | The page itself |
| `src/confidentialite.html` | The privacy policy |
| `src/assets/css/ashudev.css` | The whole stylesheet: typography, layout, mobile, print |
| `src/assets/css/fonts.css` | Red Hat Display and DM Sans, self-hosted: the page requests no third party |

Fonts are SIL Open Font License 1.1; the licence texts sit next to the `.woff2`
files in `src/assets/fonts/`.

## Local preview

```bash
python3 -m http.server -d src 8000
```

Then open `http://127.0.0.1:8000/`. Serving the directory matters: opening the
file directly breaks the relative asset paths.

## The CV

`src/assets/cv/valentin-ronteix-cv.pdf` (French) and `-cv-en.pdf` (English) are
served as they are. They are built from the YAML in
`scripts/cv/resume-generator`, which owns the content:

```bash
cd ../../scripts/cv/resume-generator
python3 generate_pdf.py --lang fr,en --outdir output
```

Copy the two files into `src/assets/cv/` under these names. Nothing regenerates
them at deploy time, so a CV edit has to be followed by that copy.

## Contact

There is no form and no backend. The buttons are `mailto:` and `tel:` links, so
a visitor writes from their own mail client and the site stores nothing. The
privacy page says so.

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
