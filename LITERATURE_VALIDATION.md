# Literature Validation & Designation Assessment

Cross-check of the up/down markers and subtype designations against three authoritative
**human** sources, read in full text:
- **Sun et al. 2023** (Cell) — 194k human snRNA microglia, 443 subjects, **12 states (MG0–MG12)** — the current human gold standard
- **HuMicA / Martins-Ferreira et al. 2025** (Nat Commun) — Human Microglia Atlas across neurodegeneration
- **Paolicelli et al. 2022** (Neuron) — the field's nomenclature consensus

## Q: Are the up/down markers validated against the latest literature?

**Partially — and the honest picture is nuanced.** I cross-checked every sub-state's denoised
up-markers against the combined full text of the three papers above. Mean coverage = **50%**, but
coverage is *not* a pass/fail score — these are AD/atlas-focused papers, so absence of e.g. cell-cycle
genes is expected, not a marker error. Coverage by tier:

| Coverage | Sub-states | Reading |
|---|---|---|
| **High (≥55%)** | Inflammatory DAM (70%), DIM (80%), Pre-activated (100%), GRID2+ (94%), Human MG-AD (56%), ALS/FTLD (64%), MS-rim (67%), Neonatal/PAM (69%), Ribosomal (55%) | hallmark genes explicitly in human literature — well validated |
| **Moderate (30–55%)** | Homeostatic (53%), Lipid DAM (43%), ARM (46%), CRM (50%), Embryonic (54%), BAM (33%), MHC-II (31%) | core markers present, extended lists partly curated |
| **Low (<30%)** | Proliferating (0%), IFN/Transitional-IFN (25%), Advanced DAM (29%), APC/DC-like (27%) | **expected** — these states (cell-cycle, type-I IFN, DC-like) are not the focus of AD-cortex atlases; not evidence of wrong markers |

Full per-marker table: `literature_marker_coverage.csv` (lists exactly which up-genes were/weren't found).

**Caveat that stands:** the *extended* gene lists, ortholog conversions, and the protein column remain
literature-informed curation, not exhaustively citation-pinned per gene. The hallmark markers are validated;
the long tails are not all individually sourced.

## Q: Are the subtype designations appropriate?

**Mostly yes — they map cleanly onto Sun 2023's 12 human states — with three corrections.**

| My umbrella | Sun 2023 state | Verdict |
|---|---|---|
| Homeostatic / Surveillant | MG0 homeostatic | ✓ direct |
| Disease-Associated (DAM continuum) | MG1/MG4 lipid-processing + inflammatory I–III | ✓ continuum matches |
| Inflammatory / Monocyte-derived | MG10 inflammatory | ✓ |
| Interferon-Responsive | MG11 antiviral | ✓ direct |
| Proliferative | MG12 cycling | ✓ direct |
| Border-Associated | (excluded as non-microglia) | ✓ correctly separated |
| Antigen-Presenting (MHC-II/DC-like) | folded into inflammatory | ~ I split finer than Sun |
| QC / Artifact-prone | MG3 ribosome-biogenesis, MG6 stress | ⚠ see correction |

**Corrections this analysis forces:**
1. **The "artifact" label is too strong.** Sun 2023 reports ribosomal (MG3) and stress (MG6) as *bona fide*
   states with upstream regulators — not just dissociation noise. I should reframe these as
   **"interpret with caution / partly technical"**, not "exclude". (Marsh 2022's caveat is real but Sun shows a biological core exists.)
2. **Ribosomal DAM 1 vs 2 is over-granular.** Sun resolves *one* ribosomal state (MG3); splitting into two
   is finer than the human data support. Recommend merging or marking as one state with sub-variants.
3. **Missing state — MG7 glycolytic.** Sun describes a metabolic/glycolytic microglial state that my atlas
   lacks entirely. This is a genuine gap worth adding.

**GRID2+ homeostatic** is not a Sun state and scored 94% on neuronal/ambient genes — consistent with the
existing snRNA-ambient flag; keep flagged.

## Bottom line
- **Markers:** hallmark genes are well-supported in the latest human literature; extended lists are curated.
- **Designations:** the umbrella structure matches the human gold standard (Sun 2023) closely. Three fixes:
  soften the ribosomal/stress "artifact" claim, merge the two ribosomal states, and add the glycolytic state.
