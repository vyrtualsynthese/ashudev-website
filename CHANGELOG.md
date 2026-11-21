# Changelog

All notable changes to this site are recorded here. The format is
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the versions
follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2026-11-21

The first tagged release: the site is one hand-written page and the CV it links.

### Added

- The page: the role, four service blocks, the track record, the contact links,
  and the CV, written in French with no JavaScript.
- The CV as two PDFs, French and English, served from `src/assets/cv/`.
- `confidentialite.html`, the privacy policy: no cookie, no audience
  measurement, no resource loaded from a third party, no form.
- `tools/pdf-actions.py`, run before every publish: it decompresses every stream
  of both CV PDFs and counts the markers an automatic action needs.

### Changed

- The site is served by the homelab cluster from the `gh-pages` branch.
  GitHub Pages still builds that branch, but the domain no longer points at it.
- The SRE block states its three figures as career-wide results rather than as
  one engagement's outcome, and spells out what MTTR means in plain French.
- The publish routine stages the published paths by name instead of
  `git add -A`, and says why.
- The README describes the repository as it is now: one tree, the board, and
  the publish sequence.

### Removed

- `finbiz-html/`, the purchased template the page was built from: 550 files
  nothing served, among them a PHP mail sink behind ten forms and a jQuery UI
  bundle no document called.
- The AWS deploy workflow, from every branch that still carried it, and the
  `v1` and `renovate/configure` branches themselves.

### Security

- Both published documents send `no-referrer`, so a click on LinkedIn, GitHub
  or the CNIL no longer tells that service which page the visitor came from.
- `.gitignore` covers `.env*`, `*.pem`, `*.key` and `id_*`.
- The pull request open against `main` from `renovate/configure` was closed and
  its branch deleted. Its workflow ran `npm i` on the branch's own code and then
  read two AWS credentials on every `pull_request` event.

[Unreleased]: https://github.com/vyrtualsynthese/ashudev-website/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/vyrtualsynthese/ashudev-website/releases/tag/v1.0.0
