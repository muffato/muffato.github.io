---
title: CV
position: 2
---

# Experience

## European Bioinformatics Institute (EMBL-EBI), Hinxton, United Kingdom

I work in the Comparative Genomics team of the Ensembl genome browser. We are in charge of
comparing the genomes to one another, implementing new methods and algorithms
(extending our API and database schema), and applying them on new datasets. Scalability is
our main focus as we have to process hundreds (soon thousands !) of genomes in a limited timescale.

I am also involved in the development of the eHive workflow manager, a system for creating
and running workflows on a distributed compute resource. It is now responsible for
scheduling and executing in excess of 1,000 CPU years of compute per year in Ensembl.

### Principal Developer

_Since Oct 2019_

<u>Keywords</u>: Development management. Technical leadership. Recruitment. Mentorship.
API development. Database design and optimisation. Workflow design and development. 
User support (data, API, workflows).
<u>Team size</u>: 3 people.

In this role, I transfer the knowledge I have accumulated in the past 8 years
to the new Project Leader and the developers, whilst helping them and
overseeing the development of the software.

We are undertaking a massive revamp of our compute workflows and data storage
strategy, in order to cope with the scale of data that projects such as the
Darwin Tree of Life will generate. Our aim is ambitious: provide comparative
analyses on tens of thousands of genomes, and more.

I still maintain and contribute to the development of the eHive workflow manager,
keeping it the most efficient solution for the Ensembl Comparative Genomics workflows.

### Project Leader

_May 2014 to Sep 2019_

<u>Keywords</u>: Project planning and management. Scientific and public communication. Technical leadership. Recruitment. Mentorship.
Development management. Reporting. Data-production planning and operational management.
API development. Database design and optimisation. Workflow design and development. Data
production under tight deadlines. Processing of large datasets. User support (data, API, workflows).
<u>Team size</u>: 2-6 people.

I managed the whole Comparative Genomics team of the Ensembl project,
incl. the development of the eHive workflow manager.
We had to provide technical support to other Ensembl teams
who were using our software. During this period, we wrote an extensive user manual
for eHive.

### Interim Manager

_May 2013 to May 2014_

<u>Keywords</u>: Development management. Reporting. Technical advisor. Data-production planning and operational management.
API development. Database design and optimisation. Workflow design and development. Data
production under tight deadlines. Processing of large datasets. User support (data, API, workflows).
<u>Team size</u>: 2 people.

I was managing part of the Comparative Genomics team of
Ensembl, incl. the development of the eHive workflow manager,
and was still carrying on my developer duties. Our work was focused on
the reconstruction of phylogenetic trees and gene families, improving and
extending the software. I was still giving some Ensembl API workshops.

### Software Developer

_Jan 2011 to May 2013_

<u>Keywords</u>: API development. Database design and optimisation. Workflow design and development. Data
production under tight deadlines. Processing of large datasets. User support (data, API, workflows).

I focused on the reconstruction of protein phylogenetic trees, reshaping the
API, improving and extending the software. I also gave some Ensembl API
workshops.

## École normale supérieure, Paris, France

### PhD student

_Sep 2006 to Dec 2010_

<u>Title</u>: Reconstruction of ancestral vertebrate genomes

I have developed a set of new methods to predict the genome structure of
ancestral species (all the last common ancestors of any given group of
extant species. Here: about 50 vertebrate species) at different levels
(number of chromosomes, chromosome content, gene order). We have also set
up a database and a genome browser,
[Genomicus](http://www.dyogen.ens.fr/genomicus/), to make the data available
to the community. As we use the data from the Ensembl project, Genomicus is
updated every 2 months, after each Ensembl release.

Thesis (in French) and presentation (in English) available
[online](http://tel.archives-ouvertes.fr/tel-00552138_v1/).

# Education

|---|---|---|---|
| PhD | Bioinformatics | Sep 2006 to Dec 2010 | École normale supérieure, Paris, France |
| MSc | Bioinformatics | Sep 2005 to Aug 2006 | Évry university, France |
| MSc | Computer science, Software development, Mathematics | Sep 2003 to Aug 2006 | ENSIIE, Évry, France |
| BSc | Mathematics | Sep 2004 to Jun 2005 | Paris Diderot university, France |
| Classes préparatoires | Mathematics, Physics, Computer science | Sep 2001 to Jun 2003 | Lycée Louis-le-Grand, Paris, France |

# Projects

## 2019 Google Summer of Code Mentor

_May 2019 to Sep 2019_

<u>Title</u>: Using Deep Learning techniques to enhance orthology calls

This project was funded by the 2019 edition of the Google Summer of Code
program. [Harshit
Gupta](https://www.linkedin.com/in/harshit-gupta-a454a3149/) has been selected to develop a machine-learning
algorithm to predict orthologies in the Ensembl Genomes Browser organization
under the supervision of myself and [Mateus
Patricio](https://www.linkedin.com/in/mateus-patricio-03057aa8/).


We developed a machine-learning algorithm to predict orthologies, using
TensorFlow, directly from sequence data -without using any phylogenetics
methods-. The method achieved high accuracy (>90% in most settings) and we
are now developing a plan to use it in production in Ensembl.

<u>Project URL</u>: [GitHub](https://github.com/EnsemblGSOC/compara-deep-learning)

## 2016 Google Summer of Code Mentor

_May 2016 to Sep 2016_

<u>Title</u>: Graphical editor of XML files

This project was funded by the 2016 edition of the Google Summer of Code
program. [Anuj
Khandelwal](https://www.linkedin.com/in/anuj-khandelwal-2a7151103/) has been selected to work on a Graphical workflow
editor for eHive using Blockly in the Ensembl Genomes Browser organization
under the supervision of myself and [Leo
Gordon](https://www.linkedin.com/in/leo-gordon-cambridge/).

eHive is a system used to run computation pipelines in distributed
environments. Currently the eHive workflows are configured in a specific
file format that requires basic programming skills. This project aimed at
removing this drawback by creating a graphical editor for eHive workflows
using Google's Blockly library.

We were envisaging XML as the file format, with a Relax NG specification.
The backbone of this graphical editor would be an automated conversion of a
Relax NG specification to Blockly blocks and matching rules so that the
Blockly diagrams conform to the specification. The graphical interface will
have to be able to import existing XML files to visualize them in terms of
Blockly blocks, edit them, and export the diagram back to XML.

The project submitted to Google is not specific to eHive and the proposed
editor should be able of handling any specifications written using the
Relax NG schema.

<u>Project URL</u>: [Website](https://ensembl.github.io/XML-To-Blockly/),
[GitHub](https://github.com/Ensembl/XML-To-Blockly)


## EMBL Postdoc Retreat 2013

_May 2013_

The EMBL postdoc retreat is an official annual EMBL event under the
patronage of the EMBL Heads of Units. It promotes scientific exchange among
postdocs and provides a platform to address problems relevant to postdocs.

## Internship - Web interface for gene annotation

**École normale supérieure, Paris, France**

_Jun 2005 to Aug 2005_

I worked on improving the user interface of Exogean, a software for
annotating gene structures in eukaryotic genomic DNA.

## Contractor - Cost-analysis tool for electronics manufacturers

_2005_

Conception of a new software to analyse and manage costs for electronics
manufacturers (project & product visualisation, resources management).

## Personal project - 3D Renderer

_2002 to 2003_

I implemented a 3D renderer from scratch, i.e. without using any libraries
such as OpenGL. The program is able to render (project) 3D objects onto a
plane as raster images, including colours & transparency, but also
lightings and shadings. It's all written in C++.

I also know about ray-tracing, BSP trees, Bezier curves, B-splines.

# Certifications

## Project Fundamentals Qualification (PFQ) certification

_Association for Project Management (APM), 2017_

Course on project management. Principles and approaches have since been applied to all Ensembl
management layers to plan and manage projects (development and others).


## "Policy manager" and "Antivirus Client Security"

_F-Secure Corporation, 2004_

