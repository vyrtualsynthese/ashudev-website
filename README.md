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
served as they are. They are built from the YAML in `../scripts/cv/resume-generator`,
which owns the content. That generator is a separate checkout beside this one —
`../scripts/cv/resume-generator` from this repository's root, which is the
layout under `~/projets`, where `ashudev-website` sits next to `scripts`. It is
not a directory inside this repository, so the command below starts at the root:

```bash
cd ../scripts/cv/resume-generator
python3 generate_pdf.py --lang fr,en --outdir output
```

`generate_pdf.py` is not on the generator's `main` yet: it exists on its
`feat/cv-pdf` branch, so run `git switch feat/cv-pdf` there first. Until that
branch merges, the command fails on `main` with "No such file".

It writes `output/cv_valentin_ronteix_fr.pdf` and `output/cv_valentin_ronteix_en.pdf`.
Copy them into `src/assets/cv/` as `valentin-ronteix-cv.pdf` and
`valentin-ronteix-cv-en.pdf`. Nothing regenerates them at deploy time, so a CV
edit has to be followed by that copy.

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

`.github/workflows/publish.yml` owns that branch. On every push to `main` it
does three things:

1. It adds a throwaway worktree on `gh-pages` and empties it.
2. It copies `src/` into the root of that worktree, then writes `CNAME`
   (`ashudev.com`) and an empty `.nojekyll`.
3. It commits as `🌐 site: publish`, with the source commit in the body, and
   pushes.

Before any of that, a first job runs `tools/pdf-actions.py` over both CV files.
It runs on pull requests too, where it is the only job. It decompresses every
stream in each PDF and looks for an action that fires when a reader opens it
(`/OpenAction`, `/JavaScript`, `/Launch`, `/SubmitForm`). Both files print
`0 marker(s)`, which is the expected answer; anything else fails the check, and
on `main` it stops the publish before the branch is touched.

A publish that fails on `main` opens an issue saying the site still serves the
previous commit, with the run in it, and the next successful publish comments
and closes it. Without that the failure would be a red run nobody looks at.
Issues are switched off on this repository, so the alarm cannot open one yet:
until that changes, a failed publish reports itself only as a failed run, and
the alert job says so in the run's error annotation.

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

## Branches

`main` publishes and `develop` integrates; every change reaches both through a
pull request. The repository allows one merge method, rebase, so a release
rewrites the release commits: `main` moves to new SHAs while `develop` keeps the
old ones. `.github/workflows/realign-develop.yml` replays `develop` onto `main`
after every push to `main`, which puts the two branches back on one line — a
fast-forward when `develop` has nothing new, a rebase of its new commits when it
has. Starting it from the Actions tab realigns a repository that drifted before
the workflow existed. A rebase that cannot apply fails the run and leaves
`develop` untouched, rather than half moved.

Because the workflow rewrites `develop`, a local `develop` in the canonical
checkout follows it with `git fetch && git reset --hard origin/develop` rather
than `git pull`, which would add a merge commit back into the line.

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
