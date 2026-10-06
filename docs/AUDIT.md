# v1.0.4 source and routing validation

Reviewed on 2026-09-24. The published v1.0.4 package uses explicit resource paths and contains no private-server resource map, deployment/toy scripts, interval presets, SIF autodiscovery, fixed Slurm queue or unchanged-resource retry policy. No compatibility aliases or wrapper scripts were added.

## Paired FASTQ correction

NGS and HiFi read tuples are combined with the pair's graph by `pair_id`. In paired mode, normal reads build one personalized graph and both tumor and normal use it.

The routing regression test executes the actual `main.nf` and configuration while replacing only bioinformatics process bodies in a temporary copy. It covers NGS/HiFi × `full`/`align_only`/`call_from_bam` × tumor-only/paired: 12/12 cases passed. It checks graph-source roles, process counts, both paired samples reaching BAM preflight, caller selection and graph-free BAM entry.

The negative control restores the faulty `join`: paired NGS then runs only one alignment/preflight and never starts paired Mutect2. This confirms that the test detects the corrected failure mode. See `VALIDATION.md` in the release assets and source package.

## Validation boundary

Shell/JSON checks and launcher help/version checks pass. The routing tests do not run vg, KMC, samtools, GATK, DeepSomatic or Sniffles2. A fresh real-data server acceptance run of this corrected package remains required before public release.

The supplied HG002 subset results demonstrate earlier engineering execution and valid output generation. Because paired samples came from the same HG002 source, they do not establish biological somatic accuracy, sensitivity, specificity or full-depth WGS performance.
