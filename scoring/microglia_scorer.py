"""
microglia_scorer.py — annotate microglia by the hierarchical subtype-marker atlas.

Validated pipeline (see ADVERSARIAL_REVIEW.md): score each SUB-STATE signature flat
(mean z of denoised up-genes minus mean z of down-genes), take the argmax, then roll up
to the umbrella family. Reaches ~73% family-level accuracy vs annotated ALS microglia.
Family aggregation (union/mean/max of member genes) was tested and performs WORSE — do
not aggregate genes across a family.

Usage:
    import anndata as ad
    from microglia_scorer import load_atlas, score_adata
    atlas = load_atlas("microglia_subtypes_hierarchical.json")   # + signatures_denoised.json
    res = score_adata(adata, atlas, gene_col="feature_name")     # gene_col: var column of symbols, or None for var_names
    adata.obs["mg_substate"] = res["substate"]
    adata.obs["mg_umbrella"] = res["umbrella"]
"""
import json
import numpy as np

def load_atlas(hier_json, denoised_json=None):
    hier = json.load(open(hier_json))
    sub2umb, sigs_up, downs = {}, {}, {}
    for u in hier:
        for s in u["sub_subtypes"]:
            name = s["sub_subtype"]
            sub2umb[name] = u["umbrella"]
            # Use the denoised column when present (even if EMPTY — an empty denoised set
            # marks a pure-artifact state and must stay empty so it is excluded below).
            # Only fall back to the raw human list if the denoised key is entirely absent.
            up = s["upregulated_genes_denoised"] if "upregulated_genes_denoised" in s else s["upregulated_genes_human"]
            sigs_up[name] = [g.strip().upper() for g in up.split(",") if g.strip()]
            downs[name]  = [g.strip().upper() for g in s.get("downregulated_genes_human","").split(",") if g.strip()]
    # drop sub-states with too few up-genes (pure-artifact) from the classifier
    keep = {k for k,v in sigs_up.items() if len(v) >= 3}
    return {"sub2umb":sub2umb, "up":{k:sigs_up[k] for k in keep},
            "down":{k:downs.get(k,[]) for k in keep}, "hier":hier}

def _zscore(X):
    mu = X.mean(0); sd = X.std(0); sd[sd==0] = 1.0
    return (X - mu) / sd

def score_adata(adata, atlas, gene_col=None, layer=None, restrict_to=None):
    """Return per-cell substate + umbrella calls and the full score matrix.
    restrict_to: optional boolean mask or obs-query to limit to microglia."""
    from scipy.sparse import issparse
    A = adata
    if restrict_to is not None:
        A = adata[restrict_to]
    syms = (A.var[gene_col].astype(str).str.upper().values if gene_col and gene_col in A.var.columns
            else np.array([str(s).upper() for s in A.var_names]))
    s2i = {}
    for i, s in enumerate(syms):
        s2i.setdefault(s, i)
    genes = sorted({g for v in atlas["up"].values() for g in v} | {g for v in atlas["down"].values() for g in v})
    present = [g for g in genes if g in s2i]
    cols = [s2i[g] for g in present]
    X = A.layers[layer] if layer else A.X
    X = X[:, cols]
    X = X.toarray() if issparse(X) else np.asarray(X)
    if X.max() > 50:  # looks like raw counts
        X = np.log1p(X)
    Z = _zscore(X)
    gi = {g: j for j, g in enumerate(present)}
    names = list(atlas["up"].keys())
    S = np.full((Z.shape[0], len(names)), np.nan)
    for k, nm in enumerate(names):
        up = [gi[g] for g in atlas["up"][nm] if g in gi]
        dn = [gi[g] for g in atlas["down"][nm] if g in gi]
        sc = Z[:, up].mean(1) if up else np.zeros(Z.shape[0])
        if dn:
            sc = sc - Z[:, dn].mean(1)
        S[:, k] = sc
    best = np.nanargmax(S, axis=1)
    substate = np.array([names[b] for b in best])
    umbrella = np.array([atlas["sub2umb"][s] for s in substate])
    margin = np.sort(S, axis=1)[:, -1] - np.sort(S, axis=1)[:, -2]  # confidence
    return {"substate":substate, "umbrella":umbrella, "score_margin":margin,
            "scores":S, "signature_names":names, "n_genes_present":len(present)}
