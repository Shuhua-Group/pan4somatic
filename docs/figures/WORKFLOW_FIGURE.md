# pan4somatic v1.0.4 workflow figure

The overview shows implemented routing from FASTQ or existing aligned BAMs to platform-specific variant outputs. Reference/graph options are GRCh38/HPRC1, GRCh38/CPC1+HPRC1 and CHM13/CPC2; CPC2 is not openly released. Graph choice applies to FASTQ processing; existing BAMs bypass graph personalization and alignment and must match the selected linear reference.

For paired FASTQ runs, normal reads personalize one graph used for both tumor and normal alignment. Tumor-only runs use tumor reads. NGS calls SNVs/indels with Mutect2. HiFi supports DeepSomatic for SNVs/indels and Sniffles2 for SVs, independently or together. Paired Sniffles2 outputs independent tumor/normal VCF and SNF files, not a somatically subtracted callset. GAM is generated internally and is not a supported direct entry.

`full` includes alignment and calling; `align_only` stops after BAM preflight; `call_from_bam` starts at BAM preflight. Existing BAMs are checked, not automatically realigned or duplicate-marked.

This is an implementation overview, not evidence of variant-calling accuracy. HG002 subset and same-source paired runs are engineering acceptance tests.

## Files and reproduction

- PNG: GitHub preview, 2125 × 1346 pixels; 300 dpi.
- SVG: editable vector text and shapes; 180 mm wide, minimum font size 6 pt.
- PDF: vector export at 180 × 114 mm; minimum font size 6 pt at this size. Reducing the figure below 180 mm wide also reduces its effective font size.
- [draw_workflow.py](../scripts/draw_workflow.py): drawing source. From the repository root, run `python3 docs/scripts/draw_workflow.py` with Matplotlib installed; outputs are written to `docs/figures/`.

Generated with Python/Matplotlib 3.6.2 and DejaVu Sans on 2026-09-23. SVG text remains text; PDF uses embedded TrueType fonts. No experimental data are plotted.

Audited against the frozen v1.0.4 source (`main.nf`, configuration and local modules), source archive SHA-256: `960d0708e92dff0a0e14ef459d2bbe8ea32fc28d44716f998c538f2196c7846d`. See [MANUAL.md](../../MANUAL.md) for exact parameters and [RESOURCES.md](../../RESOURCES.md) for resource acquisition.

Typography revision: restored the original horizontal swimlane layout with moderately enlarged labels for 180 mm final width. The overview now includes the paired FASTQ known-issue note; see [audit](../AUDIT.md#paired-fastq-routing).
