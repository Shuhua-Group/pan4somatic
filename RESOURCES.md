# Resource downloads and preparation

For pan4somatic v1.0.4. Official release pages were checked on 2026-09-23. Links identify public sources; large assets were not downloaded or byte-matched to the historical validation server. Example `/data/...` paths in the manual are local destinations, not download addresses.

## Choose only the resources you need

| Run | Required resources |
|---|---|
| Every run | Matching FASTA + `.fai`; samtools environment |
| FASTQ entry | Matching graph `.gbz` + `.hapl`; KMC and vg; GATK also for NGS alignment |
| NGS calling | FASTA dictionary, PoN + `.tbi`, germline VCF + `.tbi`, GATK |
| HiFi SNV/Indel | DeepSomatic |
| HiFi SV | Sniffles2 |
| Existing BAM entry | Coordinate-sorted reference-matched BAM + BAI; no graph files or KMC/vg needed |

Start with one public graph option (HPRC1 or CPC1+HPRC1). Current download sources are below. No project-hosted resource bundle is available.

## HG002 sequencing test data

The [manual test-data section](MANUAL.md#11-hg002-test-data-direct-downloads) provides direct links to both HG002 NovaSeq PCR-free 30× FASTQs and both PacBio Revio HiFi source BAMs. It explains their relationship to the smaller engineering-test subsets. These sequencing inputs are separate from the reference/graph resources listed below.

## Resource-to-download map

| Manual variable | Public source / download | Select and prepare |
|---|---|---|
| `GRCH38_FASTA` | [UCSC GRCh38 analysis-set directory](https://hgdownload.soe.ucsc.edu/goldenPath/hg38/bigZips/analysisSet/) · [FASTA download](https://hgdownload.soe.ucsc.edu/goldenPath/hg38/bigZips/analysisSet/GCA_000001405.15_GRCh38_no_alt_analysis_set.fna.gz) | `GCA_000001405.15_GRCh38_no_alt_analysis_set.fna.gz`, UCSC-style contig names; decompress and index. Use this no-alt analysis set rather than silently substituting another hg38 FASTA. |
| `HPRC1_PREFIX` | [HPRC graph/index downloads](https://data.humanpangenome.org/alignments) | Select release v1.1, GRCh38, minigraph-cactus, `hprc-v1.1-mc-grch38.d9.gbz` and the corresponding graph/index assets. Prepare a matching `.hapl` for that exact GBZ. |
| `CPC1_HPRC1_PREFIX` | [CPC official downloads](https://pog.fudan.edu.cn/cpc/#/data) · [CPC1 release repository](https://github.com/Shuhua-Group/Chinese-Pangenome-Consortium-Phase-I) | Under **CPC & HPRC pangenome reference → CPC.HPRC.Phase1.GRCh38-MAF01.cactus264**, download `CPC_HPRC_reconstruct_GRCh38ref_T2Tplus_CN1plus.d21.gbz` and `.dist`. Generate the matching `.ri` and `.hapl` as below. The `.full.gbz` and unsuffixed `.gbz` are different graph variants. |
| `GRCH38_PON` | [Broad PoN VCF](https://storage.googleapis.com/gatk-best-practices/somatic-hg38/1000g_pon.hg38.vcf.gz) · [TBI](https://storage.googleapis.com/gatk-best-practices/somatic-hg38/1000g_pon.hg38.vcf.gz.tbi) · [official PoN documentation](https://gatk.broadinstitute.org/hc/en-us/articles/360035890631-Panel-of-Normals-PON) | Public upstream `1000g_pon.hg38.vcf.gz`; check compatibility with the selected FASTA. A public PoN does not necessarily match your assay or processing protocol. |
| `GRCH38_GERMLINE` | [Broad AF-only gnomAD VCF](https://storage.googleapis.com/gatk-best-practices/somatic-hg38/af-only-gnomad.hg38.vcf.gz) · [TBI](https://storage.googleapis.com/gatk-best-practices/somatic-hg38/af-only-gnomad.hg38.vcf.gz.tbi) · [official resource guidance](https://gatk.broadinstitute.org/hc/en-us/community/posts/360059022691-germline-resource) | Public upstream AF-only resource; the server's `.mainchr.fixed.corrected` file is a processed derivative, not the original download. |
| `CHM13_FASTA` | [T2T-CHM13 official downloads](https://github.com/marbl/CHM13#analysis-set) | Select `chm13v2.0.fa.gz` from the analysis-set links. The masked-Y, no-Y and rCRS variants are distinct assets; do not interchange them with the graph-matched validation reference. |
| `CPC2_PREFIX` | Not publicly downloadable for this workflow release | The configured `cpc2-20250707-mc-chm13.d46` graph is not supplied as an open download. [CPC Phase II official page](https://pog.fudan.edu.cn/cpc/#/phaseii) is available, but the graph has not been released. This is a project page, not a download or an established access route. Use HPRC1 or CPC1+HPRC1 for a public-resource setup. |
| `CHM13_PON` | Public GRCh38 PoN source above; [official T2T liftover resources](https://github.com/marbl/CHM13#liftover-resources) | No verified public URL for the exact tested `somatic-hg38_1000g_pon.chm13.fixed.vcf.gz` was found in the delivery. It must be obtained as the documented derivative or regenerated with a recorded coordinate-conversion/QC procedure. Renaming contigs is not liftover. |
| `CHM13_GERMLINE` | [T2T public variant resources](https://github.com/marbl/CHM13#variant-calls), including lifted gnomAD v3.1.2; Broad source above | Public starting resources exist, but the exact tested `af-only-gnomad.chm13.fixed.vcf.gz` is a local derivative. A public lifted gnomAD VCF is not automatically the same AF-only GATK resource; validate fields, alleles and coordinates. |
| `SIF_DIR` | Tool distribution links below | This is a directory of tool images, not one downloadable dataset. Public software/images and the exact validated SIF binaries are distinct. |

For CPC1+HPRC1, the official download page visibly lists the exact `.d21.gbz` and `.d21.dist` names used by this release. The page exposes download buttons, so its release page and exact filenames are provided rather than a guessed backend URL.

## Download public GRCh38 inputs

Requires `curl`, `gzip`, `samtools` and `gatk` on PATH (or equivalent commands within your configured containers). These commands download upstream resources; they do not recreate the server's corrected VCF derivatives.

```bash
set -euo pipefail
RESOURCE_DIR="$PWD/resources"
mkdir -p "$RESOURCE_DIR/reference" "$RESOURCE_DIR/gatk/grch38"

curl -fL --retry 3 \
  'https://hgdownload.soe.ucsc.edu/goldenPath/hg38/bigZips/analysisSet/GCA_000001405.15_GRCh38_no_alt_analysis_set.fna.gz' \
  -o "$RESOURCE_DIR/reference/GRCh38.fa.gz"
gzip -dc "$RESOURCE_DIR/reference/GRCh38.fa.gz" > "$RESOURCE_DIR/reference/GRCh38.fa"
samtools faidx "$RESOURCE_DIR/reference/GRCh38.fa"
gatk CreateSequenceDictionary -R "$RESOURCE_DIR/reference/GRCh38.fa" \
  -O "$RESOURCE_DIR/reference/GRCh38.dict"

BROAD_URL=https://storage.googleapis.com/gatk-best-practices/somatic-hg38
for asset in 1000g_pon.hg38.vcf.gz 1000g_pon.hg38.vcf.gz.tbi \
             af-only-gnomad.hg38.vcf.gz af-only-gnomad.hg38.vcf.gz.tbi; do
  curl -fL --retry 3 "$BROAD_URL/$asset" -o "$RESOURCE_DIR/gatk/grch38/$asset"
done
```

After any contig filtering, normalization or liftover, regenerate the VCF index and record the exact operation and checksum. The workflow checks contig compatibility, but that alone does not validate AF semantics, transformed alleles or population suitability. The historical validation evidence is summarized in [SUPPLEMENT.md](SUPPLEMENT.md).

## Prepare graph indexes consistently

The pipeline expects `<prefix>.gbz` and `<prefix>.hapl`. Do not mix a haplotype index from another filtered/full graph just because the release names look similar. The HPRC catalog also lists an unsuffixed `.hapl`; compatibility with the `.d9.gbz` is not established by filenames alone. The historical workflow built its haplotype index from the selected graph.

With vg 1.75.1 available, adapt this example from the delivered index-preparation script. `GRAPH_PREFIX` points to downloaded `.gbz` and matching `.dist` files. Run in a new staging location to avoid replacing existing indexes:

```bash
GRAPH_PREFIX=/data/graphs/cpc1_hprc1/CPC_HPRC_reconstruct_GRCh38ref_T2Tplus_CN1plus.d21
THREADS=16
vg gbwt -p --num-threads "$THREADS" \
  -r "${GRAPH_PREFIX}.ri" -Z "${GRAPH_PREFIX}.gbz"
vg haplotypes -v 2 -t "$THREADS" \
  -d "${GRAPH_PREFIX}.dist" -r "${GRAPH_PREFIX}.ri" \
  -H "${GRAPH_PREFIX}.hapl" "${GRAPH_PREFIX}.gbz"
```

Index builds need substantial memory and scratch space. The downloaded `.dist` is used here to build `.hapl`; the workflow subsequently builds personalized mapping indexes. A different graph or vg version requires its own compatibility checks.

## Public tool sources and the SIF directory

| Expected SIF filename | Tool/version | Public distribution |
|---|---|---|
| `vg_1.75.1.sif` | vg 1.75.1 | [release and official container URI](https://github.com/vgteam/vg/releases/tag/v1.75.1): `quay.io/vgteam/vg:v1.75.1` |
| `gatk_4.7.0.0.sif` | GATK 4.7.0.0 | [Broad GATK releases](https://github.com/broadinstitute/gatk/releases) |
| `deepsomatic_1.10.0.sif` | DeepSomatic 1.10.0 | [Google DeepSomatic installation/container instructions](https://github.com/google/deepsomatic) |
| `sniffles2_2.8.0.sif` | Sniffles2 2.8.0 | [Sniffles releases](https://github.com/fritzsedlazeck/Sniffles/releases) |
| `kmc.sif` | KMC; release manifest does not pin its version | [KMC releases](https://github.com/refresh-bio/KMC/releases) |
| `samtools.sif` | samtools; release manifest does not pin its version | [samtools releases](https://github.com/samtools/samtools/releases) |

An example conversion from the confirmed vg container URI is:

```bash
mkdir -p /data/containers/pan4somatic
apptainer pull /data/containers/pan4somatic/vg_1.75.1.sif \
  docker://quay.io/vgteam/vg:v1.75.1
```

Locally converted or rebuilt images need version/tool checks and a new checksum; they are not assumed byte-identical to the tested SIF files. The historical tested-image checksums are retained in SUPPLEMENT.md. The links here identify upstream software sources; the exact tested SIF binaries are not currently provided as project-hosted downloads.

## Finish the setup

1. Download the chosen public reference/graph assets and keep their release/version metadata.
2. Prepare matching indexes and caller resources; verify sequence dictionaries and record SHA-256 hashes.
3. Set the manual's local variables or edit `conf/resources.config` to point to these prepared files.
4. Run an appropriate bounded acceptance test before production. Keep download provenance, transformation commands and output checksums with the run.

CPC2 is deliberately excluded from the public-download route. Public availability of upstream resources does not mean every locally corrected/indexed artifact in the historical validation manifest is available as an identical public binary.
