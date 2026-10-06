# pan4somatic v1.0.4 — internal validation release

This release provides the cleaned pan4somatic Nextflow workflow for Illumina NGS and PacBio HiFi, with SNV/Indel and long-read SV calling.

## Source status

- Corrected paired FASTQ routing for both NGS and HiFi: normal reads build one personalized graph and tumor/normal both use it.
- Removed private-server resource defaults, deployment/toy scripts, duplicate resource templates, interval presets, SIF autodiscovery, fixed Slurm queue and unchanged-resource retries.
- Resource paths are explicit. No compatibility aliases or wrapper scripts were added.
- Shell/JSON checks and 12/12 Nextflow routing cases passed. Bioinformatics tool bodies were mocked in the routing tests; a fresh real-data server acceptance run remains required before public release.

## Supported profiles

- GRCh38/HPRC1
- GRCh38/CPC1+HPRC1
- CHM13/CPC2, when the unreleased CPC2 graph is available

NGS uses Mutect2 for SNVs/indels. HiFi uses DeepSomatic for SNVs/indels and Sniffles2 for SVs. Paired Sniffles2 produces separate tumor and normal calls without automatic somatic subtraction.

## Supplied HG002 evidence

Earlier engineering runs reported NGS alignment and Mutect2 results for all three profiles; GRCh38/HPRC1 HiFi alignment, DeepSomatic and Sniffles2; paired call-from-BAM acceptance; and clean-room NGS paired chr1/TGS paired SV acceptance. NGS used 1,000,000 read pairs and HiFi used 100,000 reads.

The paired inputs derive from the same HG002 source. These results demonstrate workflow execution and output generation, not biological somatic accuracy or full-depth WGS performance. They predate the current routing correction and are not a fresh acceptance test of this package.

| Output | SHA-256 |
|---|---|
| NGS HPRC1 autosomal filtered VCF | `16c83441427a1d7449bd09390b55a6d7531572f9c73437ec5270e79a6dbd2092` |
| NGS CPC1+HPRC1 autosomal filtered VCF | `589c8118d87dd3e4a4cdef2f8062062dac420eab8c6853bbc500df72e64d4316` |
| NGS CPC2 autosomal filtered VCF | `0a2c2fcbc62746285291766075f76c3e19e183708d0dd115dea992c198302da2` |
| HiFi DeepSomatic VCF | `7295b3c1f03c3824f05abac67a72fcac1cbd636dafe3b66db3ac1a21dacacc6b` |

The project owner supplied these output checksums. The server files were not independently rehashed during GitHub preparation. Release-archive verification is documented by the attached `.sha256` file and `VALIDATION.md`.
