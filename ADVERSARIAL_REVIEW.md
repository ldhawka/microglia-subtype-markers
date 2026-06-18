# Adversarial Review — Microglia Subtype Marker Atlas (24 subtypes)

This document reports an adversarial validation of the updated marker table, in response to four
questions: marker specificity, literature support, subtype distinctness, and ground-truth performance.
Unlike the table itself, this review is designed to **find problems**, and it found several.

## TL;DR
- **Distinctness:** 23/24 subtypes have ≥1 uniquely-private up-marker. The exception (Neonatal CD11c+/PAM)
  is a *contextual* state with no private gene — it re-uses the DAM program.
- **Specificity:** A handful of genes (TREM2, APOE, ITGAX, SPP1, GPNMB) appear in 7–8 subtypes each and
  carry little discriminatory weight on their own. The DAM family is a continuum, not discrete clusters.
- **Ground truth (your data):** Scoring all 24 signatures against your annotated microglia in 3 ALS
  datasets gives **73% family-level accuracy** (8/11 annotated groups matched the correct signature family).
  Failures are concentrated in (a) DAM sub-states competing with each other and (b) your MHC-II-annotated
  cells scoring highest for the DIM/inflammatory signature.
- **Per-gene sourcing:** Hallmark genes trace to the cited primary papers; full per-gene sourcing is limited
  by paywalled full text (marker lists live in figures/supplementary tables not always machine-retrievable).

---

## 1. Marker specificity (how discriminating is each marker?)

Counting how many of the 24 subtypes list each gene as "up":

| Gene | # subtypes | Interpretation |
|---|---|---|
| TREM2 | 8 | pan-DAM/activation — NOT discriminating alone |
| APOE | 8 | pan-DAM/activation |
| ITGAX (CD11c) | 7 | pan-DAM/developmental |
| SPP1 | 7 | pan-activation |
| GPNMB | 7 | pan-DAM/lipid |
| CD74 | 6 | activation/MHC |
| LGALS3, CD63, LPL, CD68 | 5 each | DAM/phagocytic |

**Implication:** these are good *positive* microglia-activation markers but cannot, by themselves,
separate one DAM sub-state from another. Discrimination requires the **private** markers
(e.g. S100A8/A9 for Advanced DAM, FABP4/PLIN2/CD36 for Lipid DAM, MX1/IFI44L for IFN-DAM,
SLC11A1/ACSL1 for MS-rim, MS4A6A for ALS/FTLD, CIITA/HLA-DP for APC). Full per-subtype private/promiscuous
breakdown is in `specificity_scores.csv`.

**One subtype has no private marker at all:** Neonatal CD11c+/PAM — every one of its genes appears in
another subtype. It is distinguishable only by developmental *context*, not by a marker panel. Flagged.

## 2. Literature support

- Each **subtype** and its **hallmark genes** trace to the cited DOIs (verified during curation).
- **Caveat — this is honest:** the *extended* gene lists, the mouse→human ortholog conversions, and the
  **protein/surface-marker column** are curation layered on the literature; I did **not** pin every
  individual gene token to a specific figure/table in a specific paper. Attempted automated per-gene
  sourcing was limited because key papers (e.g. Keren-Shaul 2017, Cell) return only abstract/metadata via
  open APIs — their marker tables are in paywalled figures/supplements. Marschallinger 2020 (LDAM): 6/13
  hallmark genes confirmed in the open-access main text, remainder in figures.
- **Recommendation before publishing:** for each subtype, cite the *specific* supplementary table the gene
  set came from, or mark genes as "curated/derived" vs "primary".

## 3. Distinctness (is every subtype separable?)

- Pairwise Jaccard of up-gene sets: **max overlap 0.42** (ARM ↔ Advanced DAM). No two subtypes are duplicates.
- But the DAM family (Inflammatory, Lipid, ARM, Advanced, Human MG-AD, MS-rim, ALS/FTLD, IFN-DAM, ATM/WAM)
  overlaps heavily by design — these are **states on a continuum / trajectory**, which is biologically
  correct, not a table error. They should be presented as a family, not as 9 independent clusters.

## 4. Ground-truth check against YOUR annotated data

Signatures (mean z-scored expression of each up-gene set) scored against your harmonized microglia
annotations in three ALS datasets (Takeuchi brain n=3,038; Takeuchi spinal n=6,213; bioturing n=15,173).
Per-group score matrices: `validation_scores_*.csv`; figure: `validation_groundtruth_heatmap.png`.

**Family-level accuracy: 8/11 (73%).** What matched and what didn't:

| Your annotation | Result | Top-scoring signature |
|---|---|---|
| Homeostatic (brain, bioturing) | ✓ | Homeostatic / Homeostatic-GRID2+ |
| Homeostatic-GRID2 (spinal) | ✓ | Homeostatic-GRID2+ |
| Ribosomal DAM (brain, bioturing) | ✓ | Ribosomal DAM 1 |
| Inflammatory DAM (spinal) | ✓ (family) | Human MG-AD/GPNMB+ DAM |
| ARM_DAM (bioturing) | ✓ (family) | MS-rim DAM |
| DIM (bioturing) | ✓ | Disease-Inflammatory Macrophages |
| **Adv_DAM (brain)** | ✗ | Ribosomal DAM 2 (artifact sig) |
| **MAC_MHCII (brain)** | ✗ | DIM / inflammatory |
| **MHCII (spinal)** | ✗ | DIM / inflammatory |

**Key failure mode — actionable:** Your MHC-II-annotated cells score *positive* for the MHC-II signature
(all 16 MHC-II genes are detected), but the **DIM signature out-competes it** because DIM is loaded with
immediate-early/heat-shock genes (FOS, JUN, JUNB, DUSP1, HSPA1A/B…) that light up broadly in any
activated/dissociated population. This is the dissociation-artifact problem contaminating a *real* signature.

**Tested fix — pruning to private markers did NOT help** (64% vs 73%): it let the iron-heavy MS-rim
signature win broadly instead. The correct fixes are:
1. **Strip IEG/HSP genes from the DIM signature** (or split DIM into "monocyte-origin" vs "stress-response").
2. **Score DAM sub-states as a family first**, then sub-classify — don't force a winner among 9 overlapping DAM signatures.
3. The Advanced-DAM↔Ribosomal-DAM confusion in brain reflects the low-quality nature of both the
   Adv_DAM cluster (n=413) and the ribosomal signatures (flagged artifacts) — treat with caution.

## Caveats on this review itself
- bioturing X may be raw counts (log1p applied as fallback); brain/spinal are log-normalized. Normalization
  differences could shift absolute scores but not the qualitative winner pattern.
- Your annotations are themselves a reference, not absolute truth — a "mismatch" can mean my signature is
  off OR the annotation lumps a mixed population (the MHC-II groups look mixed/activated).
- Only ~9 of 24 subtypes have a matching annotated group in your ALS data; the developmental, BAM, IRN,
  and several human-AD states are untested here.

## Bottom line
The table is a **reasonable, literature-grounded reference**, but it is **not validated as a discrete
classifier**. It performs well for clearly-separated states (homeostatic, ribosomal, DIM) and poorly where
the biology is a continuum (DAM sub-states) or where a non-specific signature (DIM/stress) contaminates
the comparison. Before publishing as a definitive resource, I recommend: de-noise the DIM signature,
present DAM as a family, mark curated-vs-primary genes, and add this validation section as a transparency note.
