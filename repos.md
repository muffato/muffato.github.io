---
title: Repositories
position: 6
---

# Repositories

The complete list of repositories is available on [![icon](/assets/img/icon/github.png) GitHub](https://github.com/muffato).

Find below a selection organised by themes:

{::comment}
{:/comment}
* [![icon](/assets/img/icon/ensembl.png) Ensembl Compara](#COMPARA)
* [![icon](/assets/img/icon/guihive.png) eHive workflow manager](#EHIVE)
* [![icon](/assets/img/icon/tol.png) Tree of Life Nextflow pipelines](#SANGERTOL)
* [![icon](/assets/img/icon/nfcore.png) nf-core](#NFCORE)
* [![icon](/assets/img/icon/shpc.png) Singularity HPC for container-based computing](#SHPC)
* [![icon](/assets/img/icon/genomicus.png) Genomicus and ancestral genome reconstruction](#GENOMICUS)

## ![icon](/assets/img/icon/ensembl.png) Ensembl Compara {#COMPARA}

<dl>
<dt>[Ensembl/ensembl-compara](https://github.com/Ensembl/ensembl-compara)</dt>
<dd>
The Ensembl Compara Perl API and SQL schema \\
Last update: 2025-11
</dd>
<dt>[Ensembl/treebest](https://github.com/Ensembl/treebest)</dt>
<dd>
TreeBeST: Tree Building guided by Species Tree (Ensembl Compara modifications) \\
Last update: 2024-06
</dd>
<dt>[muffato/docker-ensembl-linuxbrew-compara](https://github.com/muffato/docker-ensembl-linuxbrew-compara)</dt>
<dd>
Docker image with all dependencies to run the Ensembl Compara pipelines \\
Last update: 2023-01
</dd>
<dt>[muffato/docker-ensembl-linuxbrew-basic-dependencies](https://github.com/muffato/docker-ensembl-linuxbrew-basic-dependencies)</dt>
<dd>
Docker image with the basic dependencies for the Ensembl linuxbrew installation \\
Last update: 2023-01
</dd>
<dt>[muffato/pyEnsemblRest](https://github.com/muffato/pyEnsemblRest)</dt>
<dd>
Python wrapper of the Ensembl REST API \\
Last update: 2023-01
</dd>
</dl>

## ![icon](/assets/img/icon/guihive.png) eHive workflow manager {#EHIVE}

<dl>
<dt>[Ensembl/ensembl-hive](https://github.com/Ensembl/ensembl-hive)</dt>
<dd>
EnsEMBL Hive - a system for creating and running pipelines on a distributed compute resource \\
Last update: 2025-08
</dd>
<dt>[Ensembl/guiHive](https://github.com/Ensembl/guiHive)</dt>
<dd>
Graphical interface for the eHive workflow manager \\
Last update: 2025-01
</dd>
<dt>[Ensembl/ensembl-hive-docker-swarm](https://github.com/Ensembl/ensembl-hive-docker-swarm)</dt>
<dd>
'Docker Swarm' implementation of Ensembl Hive Meadow interface \\
Last update: 2025-01
</dd>
<dt>[Ensembl/XML-To-Blockly](https://github.com/Ensembl/XML-To-Blockly)</dt>
<dd>
Takes RelaxNG schema as input and generates corresponding code for a Blockly block to represent the same \\
Last update: 2024-12
</dd>
<dt>[Ensembl/ensembl-hive-pbspro](https://github.com/Ensembl/ensembl-hive-pbspro)</dt>
<dd>
'PBS Pro' implementation of Ensembl Hive Meadow interface \\
Last update: 2024-11
</dd>
<dt>[Ensembl/ensembl-hive-slurm](https://github.com/Ensembl/ensembl-hive-slurm)</dt>
<dd>
Slurm Meadow for Ensembl Hive \\
Last update: 2024-11
</dd>
<dt>[Ensembl/ensembl-hive-sge](https://github.com/Ensembl/ensembl-hive-sge)</dt>
<dd>
SGE Meadow for Ensembl Hive \\
Last update: 2024-11
</dd>
<dt>[Ensembl/ensembl-hive-htcondor](https://github.com/Ensembl/ensembl-hive-htcondor)</dt>
<dd>
HTCondor Meadow for Ensembl Hive \\
Last update: 2024-11
</dd>
<dt>[muffato/eHive-Blockly](https://github.com/muffato/eHive-Blockly)</dt>
<dd>
Playground for Blockly and eHive \\
Last update: 2023-01
</dd>
</dl>

## ![icon](/assets/img/icon/tol.png) Tree of Life Nextflow pipelines {#SANGERTOL}

<dl>
<dt>[sanger-tol/insdcdownload](https://github.com/sanger-tol/insdcdownload)</dt>
<dd>
Nextflow DSL2 pipeline to download assemblies from INSDC. \\
Last update: 2025-12
</dd>
<dt>[sanger-tol/ensemblrepeatdownload](https://github.com/sanger-tol/ensemblrepeatdownload)</dt>
<dd>
Nextflow DSL2 pipeline to download repeat annotations from Ensembl. \\
Last update: 2025-12
</dd>
<dt>[sanger-tol/ensemblgenedownload](https://github.com/sanger-tol/ensemblgenedownload)</dt>
<dd>
Nextflow DSL2 pipeline to download gene annotations from Ensembl. \\
Last update: 2025-12
</dd>
<dt>[sanger-tol/variantcomposition](https://github.com/sanger-tol/variantcomposition)</dt>
<dd>
Nextflow DSL2 pipeline to analyse variants. \\
Last update: 2025-12
</dd>
<dt>[sanger-tol/nf-core-modules](https://github.com/sanger-tol/nf-core-modules)</dt>
<dd>
Repository to host Tree of Life's Nextflow DSL2 modules \\
Last update: 2025-12
</dd>
<dt>[sanger-tol/blobtoolkit](https://github.com/sanger-tol/blobtoolkit)</dt>
<dd>
Nextflow DSL2 pipeline to generate data for a BlobToolKit analysis. This workflow is part of the Tree of Life production suite. \\
Last update: 2025-11
</dd>
<dt>[sanger-tol/variantcalling](https://github.com/sanger-tol/variantcalling)</dt>
<dd>
Nextflow DSL2 pipeline to call variants on long read alignment. \\
Last update: 2025-10
</dd>
<dt>[sanger-tol/readmapping](https://github.com/sanger-tol/readmapping)</dt>
<dd>
Nextflow DSL2 pipeline to align short and long reads to genome assembly. This workflow is part of the Tree of Life production suite. \\
Last update: 2025-09
</dd>
<dt>[sanger-tol/genomenote](https://github.com/sanger-tol/genomenote)</dt>
<dd>
Nextflow DSL2 pipeline to generate a Genome Note, including assembly statistics, quality metrics, and Hi-C contact maps. This workflow is part of the Tree of Life production suite. \\
Last update: 2025-09
</dd>
<dt>[sanger-tol/sequencecomposition](https://github.com/sanger-tol/sequencecomposition)</dt>
<dd>
Nextflow DSL2 pipeline to extract statistics from a genome about its sequence composition \\
Last update: 2025-05
</dd>
</dl>

## ![icon](/assets/img/icon/nfcore.png) nf-core {#NFCORE}

<dl>
<dt>[nf-core/modules](https://github.com/nf-core/modules)</dt>
<dd>
Repository to host tool-specific module files for the Nextflow DSL2 community! \\
Last update: 2026-01
</dd>
<dt>[nf-core/tools](https://github.com/nf-core/tools)</dt>
<dd>
Python package with helper tools for the nf-core community. \\
Last update: 2025-12
</dd>
<dt>[nf-core/nft-utils](https://github.com/nf-core/nft-utils)</dt>
<dd>
nf-test utility functions \\
Last update: 2025-12
</dd>
</dl>

## ![icon](/assets/img/icon/shpc.png) Singularity HPC for container-based computing {#SHPC}

<dl>
<dt>[singularityhub/singularity-hpc](https://github.com/singularityhub/singularity-hpc)</dt>
<dd>
Local filesystem registry for containers (intended for HPC) using Lmod or Environment Modules. Works for users and admins. \\
Last update: 2025-12
</dd>
</dl>

## ![icon](/assets/img/icon/genomicus.png) Genomicus and ancestral genome reconstruction {#GENOMICUS}

<dl>
<dt>[DyogenIBENS/Agora](https://github.com/DyogenIBENS/Agora)</dt>
<dd>
Algorithm For Gene Order Reconstruction in Ancestors \\
Last update: 2025-08
</dd>
<dt>[DyogenIBENS/LibsDyogen](https://github.com/DyogenIBENS/LibsDyogen)</dt>
<dd>
Library of usual classes and functions written in python and used in the Dyogen team for comparative genomics applications \\
Last update: 2024-09
</dd>
<dt>[muffato/phd-thesis-scripts](https://github.com/muffato/phd-thesis-scripts)</dt>
<dd>
Backup of the scripts I used during my PhD thesis to build the Agora ancestral-genome reconstruction toolkit \\
Last update: 2024-04
</dd>
<dt>[muffato/ensembl-download-java](https://github.com/muffato/ensembl-download-java)</dt>
<dd>
Java code to download genomes and orthologues from Ensembl \\
Last update: 2023-01
</dd>
<dt>[muffato/pywaltrap](https://github.com/muffato/pywaltrap)</dt>
<dd>
Python interface for the community detection program Walktrap \\
Last update: 2023-01
</dd>
</dl>

