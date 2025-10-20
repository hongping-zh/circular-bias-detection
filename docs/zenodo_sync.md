# Zenodo Auto-Sync Guide (GitHub → Zenodo)

Use this guide to archive every GitHub release on Zenodo and keep DOIs in sync for JOSS and long-term citation.

---

## 1) Enable GitHub-Zenodo Integration

1. Go to Zenodo: Account → GitHub
2. Toggle on repository: `hongping-zh/circular-bias-detection`
3. Leave "Archive every GitHub release" enabled

[SCREENSHOT: zenodo_github_toggle.png]

---

## 2) Control Metadata with .zenodo.json (recommended)

- Keep repository-level metadata in `.zenodo.json` (authors, title, description, license, keywords)
- Ensure these fields align with `CITATION.cff` where applicable

[SCREENSHOT: zenodo_json_preview.png]

---

## 3) Create a Tagged GitHub Release

1. In GitHub → Releases → Draft a new release
2. Tag format: `vX.Y.Z` (e.g., `v0.1.0`)
3. Title and notes: summarize changes
4. Publish

Zenodo will automatically archive and mint a DOI for this release.

[SCREENSHOT: github_create_release.png]

---

## 4) Use Concept DOI vs Version DOI

- Concept DOI: stable across versions (use in README badges)
- Version DOI: minted per release (use in release notes, archival references)

Workflow:
- Put Concept DOI badge in `README.md`
- Reference the specific Version DOI in each release notes

[SCREENSHOT: zenodo_concept_vs_version.png]

---

## 5) Keep Versions Aligned

- `CITATION.cff: version` must match the Git tag (without the `v` prefix)
- Use the included GitHub Action `.github/workflows/check_citation_version.yml` to enforce this

[SCREENSHOT: github_actions_pass.png]

---

## 6) Add Badges to README

- Add a DOI badge for visibility
- After the first Zenodo archive, update to the Concept DOI badge

Example (Version DOI):

```markdown
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17201032.svg)](https://doi.org/10.5281/zenodo.17201032)
```

Example (Concept DOI – replace with your concept DOI once available):

```markdown
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.CONCEPT_ID.svg)](https://doi.org/10.5281/zenodo.CONCEPT_ID)
```

[SCREENSHOT: readme_badges.png]

---

## 7) Tips

- Prefer `.zenodo.json` as the single source of metadata for Zenodo
- Mirror essential citation info in `CITATION.cff`
- Reuse the Version DOI in papers’ “Code/Data availability” sections for reproducibility

---

## 8) Troubleshooting

- Release archived but no DOI? Re-check Zenodo GitHub integration toggles
- Wrong metadata on Zenodo? Update `.zenodo.json` and publish a new release
- CI failing on version mismatch? Ensure `CITATION.cff: version` = tag without `v` (e.g., tag `v0.1.0` → version `0.1.0`)
