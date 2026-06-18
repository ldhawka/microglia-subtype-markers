# microglia_scorer — auto-annotate microglia by the subtype atlas

Validated scoring recipe (see ../LITERATURE_VALIDATION.md): score each **sub-state** signature
flat (mean z of denoised up-genes − mean z of down-genes), take argmax, roll up to the
**umbrella**. ~73% family-level accuracy vs annotated ALS microglia. Family-level gene
aggregation was tested and is worse — don't aggregate.

```python
import anndata as ad
from microglia_scorer import load_atlas, score_adata

atlas = load_atlas("../data/microglia_subtypes_hierarchical.json")
adata = ad.read_h5ad("your_data.h5ad")

# gene_col = the var column holding HUGO symbols (e.g. "feature_name"); None = use var_names
res = score_adata(adata, atlas, gene_col="feature_name")
adata.obs["mg_substate"]    = res["substate"]    # fine-grained call
adata.obs["mg_umbrella"]    = res["umbrella"]     # family-level call (more robust)
adata.obs["mg_confidence"]  = res["score_margin"] # gap between top-2 signatures
```

**Notes**
- Counts are auto-log1p'd if they look raw; data are z-scored across the cells you pass.
- Restrict to microglia first (e.g. `restrict_to=mask`) for best results — the atlas assumes myeloid input.
- `score_margin` is a confidence proxy: low margin = a cell sitting between states on the continuum.
- Pure-artifact signatures (<3 denoised genes, e.g. Stress/HSP) are auto-excluded from the classifier.
