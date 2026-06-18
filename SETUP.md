# Setup — publish this as a GitHub Pages site

These files are a ready-to-publish repository. Two ways to get it online.

## Option A — web UI (no command line)

1. Go to https://github.com/new and create an **empty** repository
   (e.g. `microglia-subtype-markers`). Do **not** add a README/license — these files include them.
2. On the new repo page, click **"uploading an existing file"** and drag in the
   entire contents of this folder (`README.md`, `index.html`, `.nojekyll`, `LICENSE`,
   and the `data/` and `assets/` folders). Commit.
3. Go to **Settings → Pages**. Under *Build and deployment* → *Source*, choose
   **Deploy from a branch**, branch **main**, folder **/ (root)**. Save.
4. Wait ~1 minute. Your site will be live at
   `https://<your-username>.github.io/microglia-subtype-markers/`.

## Option B — command line

```bash
# from inside this folder
git init
git add .
git commit -m "Microglia subtype marker atlas — updated 2025"
git branch -M main
git remote add origin https://github.com/<your-username>/microglia-subtype-markers.git
git push -u origin main
```

Then do step 3 above (Settings → Pages → deploy from `main` / root).

## Notes
- `.nojekyll` is included so GitHub Pages serves the files as-is (no Jekyll build).
- The site works offline too: just open `index.html` in a browser (data is embedded
  inline as a fallback; when served over http it loads `data/microglia_subtypes.json`).
- To update the table later, edit `data/microglia_subtypes.json` (and re-export the CSV);
  the website reads that file when served over http(s).

## Repository layout
```
.
├── README.md                         # rendered table + methods (repo front page)
├── index.html                        # searchable / sortable / filterable site
├── .nojekyll                         # serve static files as-is on GitHub Pages
├── LICENSE                           # MIT (code); table cites primary sources
├── assets/
│   └── microglia_subtype_markers_heatmap.png
└── data/
    ├── microglia_subtypes_updated.csv     # full updated table
    ├── microglia_subtypes.json            # same data, powers the website
    ├── microglia_subtypes_baseline.csv    # original 2024/2025 list
    └── literature_corpus.csv              # mined literature (~490 papers)
```
