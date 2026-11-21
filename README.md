# ashudev-website

The site served at `https://ashudev.com`.

## One tree

The site is a directory of static files and nothing else.

| Path | What it is |
|---|---|
| `src/` | The site as it is written: static HTML and its assets, no build step |

There is no bundler, no `package.json`, and nothing to compile: `src/index.html`
and the files next to it are the site.

The purchased template this page was built from is not in the repository. It was
`finbiz-html/`, 550 files with a `mailer.php` behind ten forms and a 239 KB
jQuery UI bundle that nothing called; it was deleted on 2026-11-21 rather than
kept as a reference nothing read.

## Where the work is tracked

The repository has a project on the operator's self-hosted Vikunja board:
`ashudev-website`, with one kanban view, `Board`, whose columns are
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
seconds. GitHub Pages still builds it, but the domain's DNS points at the
cluster, so the build is no longer what a visitor receives.

`.github/workflows/publish.yml` owns that branch. It runs on every push to
`main` and does four things:

1. It runs `tools/pdf-actions.py` over both CV files. It decompresses every
   stream in each PDF and looks for an action that fires when a reader opens
   it (`/OpenAction`, `/JavaScript`, `/Launch`, `/SubmitForm`). Both files print
   `0 marker(s)`, which is the expected answer; anything else stops the publish
   before the branch is touched.
2. It adds a throwaway worktree on `gh-pages` and empties it.
3. It copies `src/` into the root of that worktree, then writes `CNAME`
   (`ashudev.com`) and an empty `.nojekyll`.
4. It commits as `🌐 site: publish`, with the source commit in the body, and
   pushes.

So the push to `main` is the release, and nothing is copied by hand. The branch
is never edited directly. Starting the same workflow from the Actions tab
republishes `main` as it stands, which is what to use when the cluster's clone
needs a fresh commit without a source change.

The workflow copies `src/` rather than listing the published paths: its worktree
is fresh, so it holds no untracked file to sweep in by accident, and a new
top-level file on the site needs no change to the workflow.

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

Between 2026-11-20 and 2026-11-21 the branch was written by hand from a recipe
in this file. The workflow above replaced it: a hand copy is no longer part of
the publish path, and `gh-pages` is not edited directly.
