# Credits and attribution (mandatory)

This dataset and the kernel `zhuating/sis-splice-20261120` reuse public construction code and ideas.

## GeiserX (primary)
- Source: Sergio Fernandez Rubio (GeiserX), https://github.com/GeiserX/squares-in-squares
  Kaggle: https://www.kaggle.com/sergiofernndezrubio
- Code license: Apache-2.0 (see geiserx/LICENSE). Layouts/docs/tables: CC BY 4.0
  (see geiserx/LICENSE-CC-BY-4.0.txt). The NOTICE file is retained verbatim in geiserx/NOTICE.
- Files reused unmodified: k123_join.py (norm/rot/Lay/seams/join), k123_step57.py (boxed/chains/step/step_up),
  k123_tartan.py (Hole/start/fit/best_fit/layout), methods_lp.py (load/normal/side/min_gap/best_axes),
  family_step.py (read/build/squeeze/fq_quench, SQ_LOOSE reader), frontier_stacks.py, frontier_read.py.
- The author explicitly requires credit even when only ideas are used or when the work is used solely
  for a Kaggle submission (README "Credit and disclosure", family_step.py header, AI_NOTICE.md).
  Any submission/write-up derived from this campaign must name Sergio Fernandez Rubio (GeiserX) as a source.

## Roberto Ono (supplementary)
- Source: https://github.com/RobertoOno/squares-in-square, runs/2026-11-11_fable-5.2/search/
- License: MIT, Copyright (c) 2026 Roberto Ono (see ono/LICENSE).
- The diagonal-period reduce_ operator and the corner-anchored greedy fill used for the n=234 lane
  follow diagper.py / blockseed.py; the kernel adapter re-implements them in numpy (no numba) and
  repairs starts with the evand fq engine instead of Ono's penalty/polish pipeline.

## Joost de Winter (supplementary)
- Source: https://github.com/jlevy/squares,
  packing/resources/web/de-winter-method-132-157-2026-11-12/source/method_n132_n157/
- License: MIT (see dewinter/LICENSE). Credit: Joost de Winter, Delft University of Technology.
- surgery.py (up_y/up_step axis-aligned row/column insertion) and slp.py (verts/pair_data overlap test)
  are used for the 747 -> 802 -> 803 propagation lane. Repair/compaction is done with fq, not nlp.py.
- n292-type constructions must be described as "de Winter after Cantrell".

## evand / alexchilton
- fq engine: https://github.com/evand/square-packing (MIT), built inside the kernel.
- Official metric: alexchilton/squares-in-squares-starter-kit (metric.py v20).