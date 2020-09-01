---
title: CV
position: 2
---

> Work in progress :construction_worker:

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

Keywords
: Development management. Technical leadership. Recruitment. Mentorship.
API development. Database design and optimisation. Workflow design and development. 
User support (data, API, workflows). Team size: 3 people.

Description
: In this role, I transfer the knowledge I have accumulated in the past 8 years
to the new Project Leader and the developers, whilst helping them and
overseeing the development of the software.

: We are undertaking a massive revamp of our compute workflows and data storage
strategy, in order to cope with the scale of data that projects such as the
Darwin Tree of Life will generate. Our aim is ambitious: provide comparative
analyses on tens of thousands of genomes, and more.

I still maintain and contribute to the development of the eHive workflow manager,
keeping it the most efficient solution for the Ensembl Comparative Genomics workflows.

### Project Leader

_May 2014 to Sep 2019._

Project planning and management. Scientific and public communication. Technical leadership. Recruitment. Mentorship.
Development management. Reporting. Data-production planning and operational management.
API development. Database design and optimisation. Workflow design and development. Data
production under tight deadlines. Processing of large datasets. User support (data, API, workflows).
Team size: 2-5 people.

I managed the whole Comparative Genomics team of the Ensembl project,
incl. the development of the eHive workflow manager.
We had to provide technical support to other Ensembl teams
who were using our software. During this period, we wrote an extensive user manual
for eHive.

### Interim Manager

_May 2013 to May 2014._

Development management. Reporting. Technical advisor. Data-production planning and operational management.
API development. Database design and optimisation. Workflow design and development. Data
production under tight deadlines. Processing of large datasets. User support (data, API, workflows).
Team size: 2 people.

I was managing part of the Comparative Genomics team of
Ensembl, incl. the development of the eHive workflow manager,
and was still carrying on my developer duties. Our work was focused on
the reconstruction of phylogenetic trees and gene families, improving and
extending the software. I was still giving some Ensembl API workshops.

### Software Developer

_Jan 2011 to May 2013._

API development. Database design and optimisation. Workflow design and development. Data
production under tight deadlines. Processing of large datasets. User support (data, API, workflows).

I focused on the reconstruction of protein phylogenetic trees, reshaping the
API, improving and extending the software. I also gave some Ensembl API
workshops.

## Education

### PhD, Bioinformatics

_ENS Paris / Évry university, France_

## MSc, Bioinformatics

_ENS Paris / Évry university, France_

## MSc, Computer Science

_ENSIIE, France_

## BSc, Mathematics

# Projects

## Google Summer of Code Mentor

_May 2019 to Sep 2019_

**Using Deep Learning techniques to enhance orthology calls**

This project was funded by the 2019 edition of the Google Summer of Code
program. Harshit Gupta has been selected to develop a machine-learning
algorithm to predict orthologies in the Ensembl Genomes Browser organization
under the supervision of myself and Mateus Patricio.


We developed a machine-learning algorithm to predict orthologies, using
TensorFlow, directly from sequence data -without using any phylogenetics
methods-. The method achieved high accuracy (>90% in most settings) and we
are now developing a plan to use it in production in Ensembl.

## Google Summer of Code Mentor

_May 2016 to Sep 2016_

**Graphical editor of XML files**

This project was funded by the 2016 edition of the Google Summer of Code
program. Anuj Khandelwal has been selected to work on a Graphical workflow
editor for eHive using Blockly in the Ensembl Genomes Browser organization
under the supervision of myself and Leo Gordon.

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

## EMBL Postdoc Retreat 2013

_May 2013_

The EMBL postdoc retreat is an official annual EMBL event under the
patronage of the EMBL Heads of Units. It promotes scientific exchange among
postdocs and provides a platform to address problems relevant to postdocs.

## Cost-analysis tool for electronics manufacturers

_2005_

Conception of a new software to analyse and manage costs for electronics
manufacturers (project & product visualisation, resources management).

## 3D Renderer

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

