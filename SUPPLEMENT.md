# Historical validation evidence

This page summarizes the supplied HG002 engineering evidence. Use [MANUAL.md](MANUAL.md) for current instructions and [RESOURCES.md](RESOURCES.md) for resource acquisition.

## What was reported

- HG002 subsets: 1,000,000 NGS read pairs and 100,000 HiFi reads.
- NGS alignment and autosomal Mutect2 results for GRCh38/HPRC1, GRCh38/CPC1+HPRC1 and CHM13/CPC2.
- HiFi alignment, DeepSomatic and Sniffles2 results for GRCh38/HPRC1.
- Paired call-from-BAM acceptance and clean-room NGS paired chr1 / TGS paired SV acceptance.
- Paired samples were derived from the same HG002 source. These tests do not establish biological somatic accuracy or paired FASTQ end-to-end correctness.

These runs predate the paired FASTQ routing correction in the current package. See the [current validation scope](docs/AUDIT.md).

## Provenance

Output VCF checksums are recorded in [RELEASE_NOTES.md](RELEASE_NOTES.md). Server outputs were not independently rehashed during GitHub preparation. Exact merge/export/subsampling commands and subset input hashes are not established by the public data-source links.

## Supplied container checksum entries

These entries are evidence from the supplied delivery, not newly verified downloads. They do not establish a download location or redistribution permission.

| File | Version | SHA-256 |
|---|---|---|
| `vg_1.75.1.sif` | vg 1.75.1 | `22d7b7a419d7142ffdff529333a2f70f8ef446b9eaafa6f1d70ab96595591604` |
| `kmc.sif` | KMC 3.2.4 | `427b48f9c8d28b895f7e36ed38c89068f944c5628b4946010bb8bcb756a811bc` |
| `samtools.sif` | samtools 1.17 | `b30a74176e5bf7647038f9ac3ad8209278edcbc1d5494840d7e5e5a0d2f41703` |
| `gatk_4.7.0.0.sif` | GATK 4.7.0.0 | `0ccc066f010ac3bb2b341c4a2677e60a305b002bdc4a17026950395b54ad5c58` |
| `deepsomatic_1.10.0.sif` | DeepSomatic 1.10.0 CPU | `6abb145055599e93ca0028ebef27194958b6cafc6a83ce107727de76a0f91e31` |
| `sniffles2_2.8.0.sif` | Sniffles2 2.8.0 | `7f1a2492d27c8d46605fd391c16f4de4fed9bdd9b9e4b27ea9d0738896525648` |
