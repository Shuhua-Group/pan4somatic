# pan4somatic v1.0.4 — User manual

This guide describes `pan4somatic_v1.0.4.tar.gz`. Run commands on Linux after replacing example paths with your local resources.

## Start here

Use this page as a reference: choose one route below, prepare its resources, then expand only the example you need. The [README workflow diagram](README.md#workflow-overview) provides the overall view.

| Your starting point | Go to |
|---|---|
| NGS FASTQ, tumor-only | [Example A](#a-ngs-tumor-only-grch38hprc1-fastq-to-filtered-variants) |
| HiFi FASTQ, tumor-only | [Example D](#d-hifi-tumor-only-snvsindels-and-svs-together) |
| FASTQ, alignment only | [Example F](#f-stop-after-alignment) |
| Existing aligned HiFi BAM | [Example G](#g-call-hifi-variants-from-that-existing-bam) |
| Existing paired NGS BAMs | [Example H](#h-ngs-paired-call-from-bam-chromosome-1-acceptance-run) |
| Paired NGS FASTQ | [Example B](#b-ngs-paired-tumornormal-grch38cpc1hprc1) |
| Paired HiFi FASTQ | [Example E](#e-hifi-paired-tumornormal-snvsindels-and-svs) |
| Download HG002 reads | [Test data](#11-hg002-test-data-direct-downloads) |

**Reading order:** [install and resources](#4-install-and-configure-resources) → [one run example](#5-complete-run-examples) → [outputs](#9-find-and-interpret-outputs).

<details>
<summary>All manual sections</summary>

- [1. Capabilities](#1-what-you-can-choose)
- [2. Reference and graph](#2-choose-the-graph-and-coordinates-first)
- [3. Platform and variant class](#3-choose-the-platform-and-variant-class)
- [4. Installation and resources](#4-install-and-configure-resources)
- [5. Run examples](#5-complete-run-examples)
- [6. Regions, coverage and model](#6-target-regions-coverage-and-model-selection)
- [7. Parameter reference](#7-parameter-reference)
- [8. Slurm and resume](#8-localslurm-resources-and-resume)
- [9. Outputs](#9-find-and-interpret-outputs)
- [10. Troubleshooting](#10-troubleshooting-and-validation-limits)
- [11. HG002 downloads](#11-hg002-test-data-direct-downloads)

</details>

## 1. What you can choose

pan4somatic combines selectable pangenome references, read-informed graph personalization, graph alignment and established linear-reference variant callers in one Nextflow workflow.

| Capability | User choice | What the workflow does |
|---|---|---|
| Pangenome background | HPRC1, CPC1+HPRC1, or CPC2 | Selects the configured graph and matching linear reference |
| Sequencing platform | Illumina paired-end NGS or PacBio HiFi | Uses platform-specific alignment and caller branches |
| Sample design | Tumor-only or tumor–normal | Uses tumor reads for graph personalization in tumor-only mode; normal reads alone in paired mode |
| Execution stage | FASTQ → variants, FASTQ → BAM, or BAM → variants | Allows alignment and calling to be run independently |
| Variant class | NGS SNVs/indels; HiFi SNVs/indels, SVs, or both | Routes to Mutect2, DeepSomatic and/or Sniffles2 |
| Execution environment | Local machine or Slurm, with optional Singularity | Configures executor, containers and process resources |

The paired FASTQ workflow builds one personalized graph from normal reads, then aligns tumor and normal to that same graph. This keeps their graph background consistent. Alignment is projected to the selected linear reference before calling; output VCFs use that reference's coordinates. NGS and HiFi are separate runs, not a joint cross-platform caller.

## 2. Choose the graph and coordinates first

| Linear coordinates | Graph option | Required flags | Default when graph is omitted |
|---|---|---|---|
| GRCh38 | HPRC1 | `--genome grch38 --graph_version hprc1` | No |
| GRCh38 | CPC1+HPRC1 | `--genome grch38 --graph_version cpc1_hprc1` | Yes, for GRCh38 |
| CHM13 | CPC2 | `--genome chm13 --graph_version cpc2` | Yes, for CHM13 |

`--genome` defaults to `grch38`. State both flags explicitly for reproducible runs. CPC2_HPRC2 is not implemented. The graph names select configured assets; the software does not download or construct those cohort graphs automatically.

These combinations are available to both `ngs` and `tgs` in the workflow. Reported engineering runs cover all three for NGS and GRCh38/HPRC1 for HiFi; do not describe every platform/graph combination as experimentally validated.

Choose GRCh38/HPRC1 and GRCh38/CPC1_HPRC1 for comparisons in the same coordinate system. CPC2/CHM13 is a different reference/graph setting; VCF records cannot be compared directly across these coordinate systems without an explicit coordinate and allele-matching strategy. Graph choice itself does not guarantee improved accuracy.

### Using your own graph assets

For a supported profile, override the asset locations with `--graph_prefix /data/graph/prefix --ref_fasta /data/ref/reference.fa`. The prefix must omit `.gbz`/`.hapl`; both files must exist. `--ref_sample` defaults to `GRCh38` or `CHM13` and selects the PanSN reference-path sample prefix. Override it only when your graph uses a different matching prefix.

This is an asset-location override, not support for arbitrary new genome/graph labels. Reference paths and the FASTA must be compatible. For NGS calling, also supply matching PoN and germline resources. Graph/reference configuration remains selected even in `call_from_bam`, but that entry does not load a graph or realign reads: changing `--graph_version` cannot change an existing BAM's alignment history.

## 3. Choose the platform and variant class

**Supported variant classes are SNVs, indels and structural variants (SVs).** The CLI option `small` means SNV + Indel calling, not SNV-only. `sv` selects structural variant calling; `all` selects both branches for long reads. NGS and HiFi do not have identical variant-class support in v1.0.4.

| Data | Flags | Caller / behavior |
|---|---|---|
| Illumina paired-end | `--platform ngs --variant_type small` | Mutect2 SNVs/indels, orientation-bias and contamination estimation, FilterMutectCalls |
| PacBio HiFi SNVs/indels | `--platform tgs --longread_technology pacbio --variant_type small` | HiFi alignment preset and DeepSomatic SNV/Indel calling |
| PacBio HiFi SVs | `--platform tgs --longread_technology pacbio --variant_type sv` | HiFi alignment preset and Sniffles2 |
| PacBio HiFi both | `--platform tgs --longread_technology pacbio --variant_type all` | DeepSomatic and Sniffles2 as separate output branches |

The CLI value for HiFi is **`pacbio`**, not `hifi`; the platform value is **`tgs`**, not `pacbio`. NGS rejects `sv` and `all`.

ONT is also implemented through `--platform tgs --longread_technology ont`, using the `r10` alignment preset and ONT DeepSomatic models. ONT is not covered by the supplied HG002 HiFi validation. Long-read personalized haplotype sampling/indexing remains an experimental extension requiring independent accuracy assessment.

## 4. Install and configure resources

**Download links:** see [Resource downloads and preparation](RESOURCES.md) for the official GRCh38, CHM13, HPRC1, CPC1+HPRC1, PoN/germline and tool sources, exact asset choices, and index preparation. The [CPC Phase II official page](https://pog.fudan.edu.cn/cpc/#/phaseii) is available; its CPC2 graph has not been released. Local `.fixed/.corrected` VCFs and tested SIF binaries must be distinguished from their public upstream sources.

Download the workflow tarball and checksum from [v1.0.4 Release assets](https://github.com/Shuhua-Group/pan4somatic/releases/tag/v1.0.4), then:

```bash
sha256sum -c pan4somatic_v1.0.4.sha256
tar -xzf pan4somatic_v1.0.4.tar.gz
cd pan4somatic_v1.0.4
bash tests/static_checks.sh
./pan4somatic --help
```

Requirements: Linux, Nextflow >=22.10, Java compatible with your Nextflow version, and Singularity/Apptainer when using the `singularity` profile. The reported server environment used Nextflow 22.10.3, Java 17.0.5 and Singularity 3.10.2. Static checks do not run callers or validate your installed resource assets.

Set explicit resource paths in `conf/resources.config` or pass them on the command line. Define only the variables required by the example you select. `/data/...` paths are placeholders for files you have prepared; they are not bundled downloads. Public GRCh38 routes use:

```bash
SIF_DIR=/data/containers/pan4somatic
GRCH38_FASTA=/data/reference/GRCh38.fa
HPRC1_PREFIX=/data/graphs/hprc1/graph
CPC1_HPRC1_PREFIX=/data/graphs/cpc1_hprc1/graph
GRCH38_PON=/data/gatk/grch38/pon.vcf.gz
GRCH38_GERMLINE=/data/gatk/grch38/germline.vcf.gz
```

<details>
<summary>CHM13/CPC2 variables — only if you already have access to the graph</summary>

```bash
CHM13_FASTA=/data/reference/chm13v2.0.fa
CPC2_PREFIX=/data/graphs/cpc2/graph
CHM13_PON=/data/gatk/chm13/pon.vcf.gz
CHM13_GERMLINE=/data/gatk/chm13/germline.vcf.gz
```

</details>

| Asset | Required for |
|---|---|
| FASTA and adjacent `.fai` | Every entry/platform |
| FASTA dictionary, e.g. `GRCh38.dict` for `GRCh38.fa` | NGS calling |
| `<graph_prefix>.gbz` and `<graph_prefix>.hapl` | `full` and `align_only` |
| Coordinate-compatible PoN and germline `.vcf.gz`, each with `.tbi` | NGS calling, including paired mode |
| Coordinate-sorted BAM with adjacent `sample.bam.bai` or `sample.bai` | `call_from_bam` |

BAM preflight requires exactly one distinct read-group SM matching the corresponding `--tumor_id`/`--normal_id`. The complete BAM sequence dictionary (names and lengths) must equal the FASTA index, even for a chromosome-limited test. HiFi BAMs need not be duplicate-marked; the NGS FASTQ branch performs MarkDuplicates. For external NGS BAMs, supply appropriately prepared BAMs.

Expected SIF names: `kmc.sif`, `vg_1.75.1.sif`, `samtools.sif`, `gatk_4.7.0.0.sif`, `deepsomatic_1.10.0.sif`, `sniffles2_2.8.0.sif`. Images and reference assets are not shipped in the source tarball. Only the containers needed for the selected branch are required at startup. Pass `--sif_dir` or the individual `--container_*` paths.

## 5. Complete run examples

All examples run locally with containers using `-profile standard,singularity`. On Slurm use `-profile slurm,singularity` and configure your queue/resources (section 8). Run one sample or pair per invocation; no cohort samplesheet parameter is implemented. Use unique pair IDs and output directories.

### A. NGS tumor-only, GRCh38/HPRC1, FASTQ to filtered variants

<details>
<summary>Show command and explanation</summary>

```bash
./pan4somatic -profile standard,singularity \
  --entry full --genome grch38 --graph_version hprc1 \
  --platform ngs --variant_type small --analysis_mode tumor_only \
  --pair_id NGS01 --tumor_id NGS01_T \
  --tumor_fastq /data/reads/NGS01_T_R1.fastq.gz,/data/reads/NGS01_T_R2.fastq.gz \
  --ref_fasta "$GRCH38_FASTA" --graph_prefix "$HPRC1_PREFIX" \
  --pon "$GRCH38_PON" --germline "$GRCH38_GERMLINE" \
  --sif_dir "$SIF_DIR" --outdir results/NGS01_hprc1
```

NGS input is exactly two comma-separated FASTQ paths, R1 then R2. Avoid spaces in paths. To use CPC1+HPRC1, change `--graph_version` to `cpc1_hprc1`, `--graph_prefix` to `"$CPC1_HPRC1_PREFIX"`, and use a distinct output directory. Retain the same GRCh38 reference/caller resources.

</details>

### B. NGS paired tumor–normal, GRCh38/CPC1+HPRC1

<details>
<summary>Show command and explanation</summary>

```bash
./pan4somatic -profile standard,singularity \
  --entry full --genome grch38 --graph_version cpc1_hprc1 \
  --platform ngs --variant_type small --analysis_mode tumor_normal \
  --pair_id NGS02 --tumor_id NGS02_T --normal_id NGS02_N \
  --tumor_fastq /data/reads/NGS02_T_R1.fastq.gz,/data/reads/NGS02_T_R2.fastq.gz \
  --normal_fastq /data/reads/NGS02_N_R1.fastq.gz,/data/reads/NGS02_N_R2.fastq.gz \
  --ref_fasta "$GRCH38_FASTA" --graph_prefix "$CPC1_HPRC1_PREFIX" \
  --pon "$GRCH38_PON" --germline "$GRCH38_GERMLINE" \
  --sif_dir "$SIF_DIR" --outdir results/NGS02_cpc1_hprc1
```

Normal reads supply graph-personalization evidence. Tumor and normal are both aligned to that graph, then paired Mutect2 receives both BAMs. IDs must differ.

</details>

### C. NGS tumor-only, CHM13/CPC2

**Requires the unreleased CPC2 graph and compatible CHM13 resources.**

<details>
<summary>Show command and explanation</summary>

```bash
./pan4somatic -profile standard,singularity \
  --entry full --genome chm13 --graph_version cpc2 \
  --platform ngs --variant_type small --analysis_mode tumor_only \
  --pair_id NGS03 --tumor_id NGS03_T \
  --tumor_fastq /data/reads/NGS03_T_R1.fastq.gz,/data/reads/NGS03_T_R2.fastq.gz \
  --ref_fasta "$CHM13_FASTA" --graph_prefix "$CPC2_PREFIX" \
  --pon "$CHM13_PON" --germline "$CHM13_GERMLINE" \
  --sif_dir "$SIF_DIR" --outdir results/NGS03_cpc2
```

Use CHM13-compatible assets, not GRCh38 VCF resources with renamed contigs. Contig compatibility checks do not establish the biological suitability of a transformed PoN/germline resource.

</details>

### D. HiFi tumor-only, SNVs/indels and SVs together

<details>
<summary>Show command and explanation</summary>

```bash
./pan4somatic -profile standard,singularity \
  --entry full --genome grch38 --graph_version hprc1 \
  --platform tgs --longread_technology pacbio --variant_type all \
  --analysis_mode tumor_only --pair_id HIFI01 --tumor_id HIFI01_T \
  --tumor_fastq /data/reads/HIFI01_T.hifi.fastq.gz \
  --ref_fasta "$GRCH38_FASTA" --graph_prefix "$HPRC1_PREFIX" \
  --sif_dir "$SIF_DIR" --outdir results/HIFI01_all
```

One HiFi FASTQ is supplied per sample. `all` runs DeepSomatic and Sniffles2; change to `small` or `sv` to run only one branch. NGS PoN/germline flags are not required for these HiFi callers.

</details>

### E. HiFi paired tumor–normal, SNVs/indels and SVs

<details>
<summary>Show command and explanation</summary>

```bash
./pan4somatic -profile standard,singularity \
  --entry full --genome grch38 --graph_version hprc1 \
  --platform tgs --longread_technology pacbio --variant_type all \
  --analysis_mode tumor_normal \
  --pair_id HIFI02 --tumor_id HIFI02_T --normal_id HIFI02_N \
  --tumor_fastq /data/reads/HIFI02_T.hifi.fastq.gz \
  --normal_fastq /data/reads/HIFI02_N.hifi.fastq.gz \
  --ref_fasta "$GRCH38_FASTA" --graph_prefix "$HPRC1_PREFIX" \
  --sif_dir "$SIF_DIR" --outdir results/HIFI02_paired
```

DeepSomatic receives both BAMs. Sniffles2 produces independent tumor and normal VCF/SNF outputs; downstream somatic SV classification is separate.

</details>

### F. Stop after alignment

<details>
<summary>Show command and explanation</summary>

```bash
./pan4somatic -profile standard,singularity \
  --entry align_only --genome grch38 --graph_version hprc1 \
  --platform tgs --longread_technology pacbio --analysis_mode tumor_only \
  --pair_id HIFI03 --tumor_id HIFI03_T \
  --tumor_fastq /data/reads/HIFI03_T.hifi.fastq.gz \
  --ref_fasta "$GRCH38_FASTA" --graph_prefix "$HPRC1_PREFIX" \
  --sif_dir "$SIF_DIR" --outdir results/HIFI03_alignment
```

This runs graph personalization, alignment, normalization/indexing and BAM preflight, then stops. For NGS use `--platform ngs` and the two FASTQ paths; its published BAM is duplicate-marked. No caller resources are needed for `align_only`.

</details>

### G. Call HiFi variants from that existing BAM

<details>
<summary>Show command and explanation</summary>

```bash
./pan4somatic -profile standard,singularity \
  --entry call_from_bam --genome grch38 --graph_version hprc1 \
  --platform tgs --longread_technology pacbio --variant_type all \
  --analysis_mode tumor_only --pair_id HIFI03 --tumor_id HIFI03_T \
  --tumor_bam results/HIFI03_alignment/intermediates/tgs_alignment/HIFI03/tumor/HIFI03_T.sorted.bam \
  --ref_fasta "$GRCH38_FASTA" --sif_dir "$SIF_DIR" \
  --outdir results/HIFI03_calling
```

This skips FASTQ, KMC, graph construction and alignment. The existing BAM's coordinate system must match the selected FASTA. To use paired mode add `--analysis_mode tumor_normal`, `--normal_id` and `--normal_bam` (replace the existing mode flag, do not duplicate it).

</details>

### H. NGS paired call-from-BAM, chromosome 1 acceptance run

<details>
<summary>Show command and explanation</summary>

```bash
./pan4somatic -profile standard,singularity \
  --entry call_from_bam --genome grch38 --graph_version hprc1 \
  --platform ngs --variant_type small --analysis_mode tumor_normal \
  --pair_id NGS04 --tumor_id NGS04_T --normal_id NGS04_N \
  --tumor_bam /data/bam/NGS04_T.dedup.bam \
  --normal_bam /data/bam/NGS04_N.dedup.bam \
  --ref_fasta "$GRCH38_FASTA" \
  --pon "$GRCH38_PON" --germline "$GRCH38_GERMLINE" \
  --interval_bed chr1 --sif_dir "$SIF_DIR" --outdir results/NGS04_chr1
```

Here `--interval_bed chr1` limits NGS caller operations, not BAM validation or alignment. Omit the flag for unrestricted reference-wide NGS calling. The core workflow does not automatically scatter/merge by chromosome.

</details>

## 6. Target regions, coverage and model selection

### NGS target intervals

Choose one of these options:

| Choice | Arguments | Scope |
|---|---|---|
| No interval restriction | Omit `--interval_bed` | NGS calling on the selected reference |
| One chromosome | `--interval_bed chr1` | NGS Mutect2 branch |
| Several chromosomes | `--interval_bed chr1,chr2` | NGS Mutect2 branch |
| Custom intervals | `--interval_bed /data/targets/panel.bed` | NGS Mutect2 branch |

**v1.0.4 does not pass this region flag to DeepSomatic or Sniffles2.** It also does not restrict graph construction or mapping. No hidden CHIP/coding filter is applied.

### Graph-source coverage

`--min_graph_source_coverage 20` is the default minimum estimated raw coverage, calculated as graph-source read bases divided by total FASTA-index bases. For paired runs the source is normal; for tumor-only runs it is tumor. This is not measured alignment coverage and does not guarantee calling accuracy.

For deliberately tiny engineering tests only, `--min_graph_source_coverage 0` disables this gate. It does not make sparse data scientifically sufficient. Targeted panels may fail the genome-wide raw-coverage gate; investigate graph-personalization suitability before lowering it. This option has no role in `call_from_bam`.

### DeepSomatic model

| Technology | Mode | Automatically selected model |
|---|---|---|
| `pacbio` | `tumor_only` | `PACBIO_TUMOR_ONLY` |
| `pacbio` | `tumor_normal` | `PACBIO` |
| `ont` | `tumor_only` | `ONT_TUMOR_ONLY` |
| `ont` | `tumor_normal` | `ONT` |

Normally omit `--deepsomatic_model`. An explicit value must equal the expected model or the workflow rejects it. `--deepsomatic_use_default_pon_filtering true` is a tumor-only opt-in; it defaults to false and is blocked for CHM13. It does not supply the NGS PoN file to DeepSomatic.

## 7. Parameter reference

| Parameter | Default / accepted values | When to set it |
|---|---|---|
| `--entry` | `full`; `align_only`, `call_from_bam` | Choose the starting/ending stage |
| `--genome` | `grch38`; `chm13` | Select output reference coordinates |
| `--graph_version` | GRCh38: `cpc1_hprc1`; CHM13: `cpc2` | Explicit graph selection; GRCh38 also allows `hprc1` |
| `--platform` | `ngs`; `tgs` | Select short- or long-read branch |
| `--longread_technology` | `pacbio`; `ont` | Long-read mapping preset/model |
| `--variant_type` | `small`; TGS also `sv`, `all` | Select callers |
| `--analysis_mode` | `tumor_only`; `tumor_normal` | Select sample design |
| `--tumor_fastq`, `--normal_fastq` | Unset | FASTQ entry; normal required in paired mode |
| `--tumor_bam`, `--normal_bam` | Unset | BAM entry; normal required in paired mode |
| `--pair_id` | `pair1` | Output grouping; use unique IDs |
| `--tumor_id`, `--normal_id` | `tumor`, `normal` | Read-group sample names; external BAM SM must match |
| `--outdir` | `results` | Separate results per run |
| `--ref_fasta` | Unset | Required reference asset |
| `--graph_prefix` | Unset | Required for FASTQ entry, excluding extension |
| `--ref_sample` | `GRCh38` / `CHM13` | Override PanSN reference prefix if necessary |
| `--pon`, `--germline` | Unset | Required NGS caller resources |
| `--interval_bed` | Unset | Explicit NGS intervals |
| `--min_graph_source_coverage` | `20`, non-negative | Graph-source raw coverage gate |
| `--kmc_memory_gb` | `48`, positive | KMC memory setting; coordinate with scheduler memory |
| `--publish_gam` | `false` | Set true to publish large GAM intermediates |
| `--sif_dir` | Unset | SIF directory |
| `--singularity_bind` | Unset | Extra bind mounts, e.g. `/data,/scratch` |
| `--container_kmc`, `--container_vg`, `--container_samtools` | Derived from SIF directory | Individual container overrides |
| `--container_picard`, `--container_mutect2` | GATK SIF | Individual NGS tool image overrides |
| `--container_deepsomatic`, `--container_sniffles` | Derived from SIF directory | Individual long-read caller images |
| `--deepsomatic_model` | Derived from technology/mode | Must match the model table |
| `--deepsomatic_use_default_pon_filtering` | `false` | Tumor-only model filtering opt-in; CHM13 blocked |

IDs must start with a letter or digit, contain only letters, digits, `.`, `_`, `-`, and be at most 128 characters. Paired tumor and normal IDs must differ. Sample roles are user inputs; labels alone do not establish biological pairing.

## 8. Local/Slurm resources and resume

Nextflow options use one dash; pipeline parameters use two. Examples:

| Nextflow option | Purpose |
|---|---|
| `-profile standard,singularity` | Local executor with containers |
| `-profile slurm,singularity` | Slurm executor with containers |
| `-c /data/config/site.config` | Additional site configuration |
| `-work-dir /scratch/pan4somatic/NGS01` | Work/cache directory |
| `-resume` | Reuse eligible cached tasks; retain work directory and Nextflow cache |
| `-with-trace results/NGS01_trace.tsv` | Optional trace file; create its parent directory first |

Set the queue for your cluster in a site configuration. Example `site.config`:

```groovy
process {
    queue = 'your_partition'
    withLabel: process_graph {
        cpus = 32
        memory = 128.GB
        time = 48.h
    }
    withLabel: process_high {
        cpus = 32
        memory = 60.GB
        time = 24.h
    }
    withLabel: process_mutect2 {
        cpus = 16
        memory = 60.GB
        time = 48.h
    }
}
```

Other defaults: `process_medium` 16 CPUs/32 GB/12 h; `process_low` 8 CPUs/16 GB/8 h. These are requested resources, not validated minimum hardware or a production performance guarantee. For local execution, provision memory for concurrent tasks; per-task settings do not constitute a global memory cap. The bundled `conf/compute_node.config` selects local execution and `maxForks=1` per process, not a Slurm submission profile or a global single-task guarantee.

To resume, rerun your original command with `-resume` and the same work/cache location. Keep distinct output/work locations for separate graph comparisons. `--publish_gam false` prevents extra GAM publication; GAM and other intermediates may still consume space in the work directory.

## 9. Find and interpret outputs

Paths below are relative to `--outdir`; `<pair>` is `--pair_id` and `<sample>` is the corresponding sample ID.

| Branch | Published output |
|---|---|
| NGS alignment | `intermediates/ngs_alignment/<pair>/<role>/<sample>.dedup.bam` and `.bam.bai`; duplicate metrics |
| HiFi alignment | `intermediates/tgs_alignment/<pair>/<role>/<sample>.sorted.bam` and `.bam.bai` |
| Graph QC | `qc/graph/<pair>/graph_source_coverage.tsv`, `reference_path_audit.tsv` |
| BAM QC | `qc/bam/<pair>/<role>/` preflight, flagstat, stats, coverage |
| NGS variants | `variants/ngs_mutect2/<pair>/<pair>.filtered.vcf.gz`, `.tbi`, metrics and resource compatibility report |
| HiFi SNVs/indels | `variants/tgs_deepsomatic/<pair>/<pair>.deepsomatic.vcf.gz`, `.tbi`, metrics |
| Tumor SV | `variants/tgs_sv_sniffles2/<pair>/<pair>.tumor.mosaic.vcf.gz`, `<pair>.tumor.snf`, tumor metrics |
| Paired normal SV | Same SV directory: `<pair>.normal.vcf.gz`, `<pair>.normal.snf`, normal metrics |
| Run reports | `pipeline_info/pan4somatic_report.html`, `pan4somatic_timeline.html` |

`align_only` has no caller output. `call_from_bam` has no newly published alignment-stage BAMs; its preflight staging copies remain in the work directory. Sniffles2 `.tbi` publication is not declared by this release's output contract; do not assume every SV VCF has a published index.

A `filtered.vcf.gz` may contain records with non-PASS FILTER labels; its name does not mean PASS-only. Metrics report total and PASS record counts, not precision or recall. Empty variant output can be scientifically valid but needs inspection of logs, input coverage and filters. `formal_status.txt` and `chromosome_metrics.tsv` in historical server runs are helper-generated outputs, not standard outputs of every core invocation.

## 10. Troubleshooting and validation limits

| Symptom | Check |
|---|---|
| Invalid genome/graph combination | Use one of the three combinations in section 2 |
| Missing graph index | Prefix excludes extension; both `.gbz` and `.hapl` exist |
| Coverage below minimum | Inspect graph-source coverage; confirm input completeness and sample role |
| BAM SM mismatch | Match IDs to existing BAM read groups; paired IDs must differ |
| BAM/FASTA contig mismatch | Use the exact matching reference and complete dictionary; renaming alone is insufficient |
| Mutect2 missing resources | Provide matching PoN/germline plus `.tbi`, FASTA plus `.fai` and dictionary |
| Coding/CHIP preset unavailable | Configure GRCh38 BED paths or use explicit compatible intervals |
| HiFi region flag appears ineffective | Region arguments are not forwarded to long-read callers in v1.0.4 |
| DeepSomatic model conflict | Omit override or select the exact technology/mode model |
| Missing container | Check SIF directory/name and selected branch dependencies |
| Process failed | Inspect `.nextflow.log` and that task's work-directory `.command.err` / `.command.sh` |

Reported acceptance used HG002 subsets (NGS 1,000,000 read pairs; HiFi 100,000 reads). NGS calling covered chr1–chr22 for three graphs; paired engineering tests used same-source HG002-derived tumor/normal. These establish bounded execution and output generation, not real somatic sensitivity, specificity, VAF performance, full-depth WGS runtime, or clinical validity. See [RELEASE_NOTES.md](RELEASE_NOTES.md) and [SUPPLEMENT.md](SUPPLEMENT.md) for historical evidence and hashes.

Implementation references inside the source archive: `main.nf` (routing and validation), `nextflow.config` (defaults and profiles), `conf/resources.config` (asset mapping), and `modules/*.nf` (actual command lines and output contracts).

## 11. HG002 test data: direct downloads

All reported engineering tests used HG002 (NA24385). The project authors supplied the following original input-data links. Click a filename to download directly from the hosting repository; the large read files are not stored in this GitHub repository.

| Platform / input | Direct download |
|---|---|
| Illumina NovaSeq PCR-free WGS, 30× — R1 | [HG002.novaseq.pcr-free.30x.R1.fastq.gz](https://storage.googleapis.com/brain-genomics-public/research/sequencing/fastq/novaseq/wgs_pcr_free/30x/HG002.novaseq.pcr-free.30x.R1.fastq.gz) |
| Illumina NovaSeq PCR-free WGS, 30× — R2 | [HG002.novaseq.pcr-free.30x.R2.fastq.gz](https://storage.googleapis.com/brain-genomics-public/research/sequencing/fastq/novaseq/wgs_pcr_free/30x/HG002.novaseq.pcr-free.30x.R2.fastq.gz) |
| PacBio HiFi Revio — run 231005, s1 | [HG002_PacBio-Revio_m84039_231005_222902_s1.hifi_reads.bam](https://ftp.ncbi.nlm.nih.gov/ReferenceSamples/giab/data/AshkenazimTrio/HG002_NA24385_son/PacBio_HiFi-Revio_20231031/HG002_PacBio-Revio_m84039_231005_222902_s1.hifi_reads.bam) |
| PacBio HiFi Revio — run 230928, s3 | [HG002_PacBio-Revio_m84039_230928_213653_s3.hifi_reads.bam](https://ftp.ncbi.nlm.nih.gov/ReferenceSamples/giab/data/AshkenazimTrio/HG002_NA24385_son/PacBio_HiFi-Revio_20231031/HG002_PacBio-Revio_m84039_230928_213653_s3.hifi_reads.bam) |

**NGS source:** the two matched FASTQ files are the HG002 Illumina NovaSeq PCR-free 30× WGS dataset. Download both R1 and R2.

**HiFi source:** the project authors report that the two PacBio Revio HiFi BAM files above were merged to obtain the source dataset used for TGS testing. These are source read BAMs, not the graph-aligned, reference-matched BAMs required by `call_from_bam`. For the FASTQ entry, reads must be exported to FASTQ after preparing the source dataset. Download both BAMs to obtain the stated source input.

**Full source data versus tested subsets:** these links provide the original datasets. The reported bounded validation used 1,000,000 NGS read pairs and 100,000 HiFi reads, not the complete downloads. The exact historical merge/export/subsampling commands and subset input checksums are not specified here, so downloading these sources alone does not reproduce the exact historical subset. Same-source HG002-derived tumor/normal inputs were used for paired engineering acceptance; they are not independent biological tumor/normal samples or somatic truth data.

### Resumable download commands

Run in a new download directory with sufficient storage. `wget -c` resumes interrupted downloads. These commands only download the original files; they do not merge BAMs, export FASTQ, subsample reads or start the workflow.

```bash
mkdir -p HG002_source_data
cd HG002_source_data
wget -c "https://storage.googleapis.com/brain-genomics-public/research/sequencing/fastq/novaseq/wgs_pcr_free/30x/HG002.novaseq.pcr-free.30x.R1.fastq.gz"
wget -c "https://storage.googleapis.com/brain-genomics-public/research/sequencing/fastq/novaseq/wgs_pcr_free/30x/HG002.novaseq.pcr-free.30x.R2.fastq.gz"
wget -c "https://ftp.ncbi.nlm.nih.gov/ReferenceSamples/giab/data/AshkenazimTrio/HG002_NA24385_son/PacBio_HiFi-Revio_20231031/HG002_PacBio-Revio_m84039_231005_222902_s1.hifi_reads.bam"
wget -c "https://ftp.ncbi.nlm.nih.gov/ReferenceSamples/giab/data/AshkenazimTrio/HG002_NA24385_son/PacBio_HiFi-Revio_20231031/HG002_PacBio-Revio_m84039_230928_213653_s3.hifi_reads.bam"
```
