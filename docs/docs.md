# Information extraction from Novel food opinions

Two main classes:

**JATS Opinion** 
- encompass the formal parts of the opinion, abstract the inner structure of the opinions into common interface
- it will abstract the formal things about the article: DOI, Title, EFSA Question, adoption date, publication date,
URL, authors(panels)
- also it will abstract the different headings from different types of opinion and match them to the same structure

**Opinion** 
- the scientific opinion itself, it will accept JATS opinion in constructor
- it will have subclass for each category, which will contain the category specific information
- it will extract NF Name, Applicant, Country of origin, NF code, type of mandate, regulation, outcome,
common name, trade names, food form
- also proposed uses + target population
- availability of ADME studies
- allergenicity 
- food category -- for FOODS 
- for **Microorganisms**: type, genus, species, strain, QPS(?)
- for **Plants**: type, common name, botanical name, genus, species, part used
- for **Animals**: genus, species, subspecies, part used
- for **Cell or Tissue**: genus, species, cell type
- for **Chemicals**: common name, IUPAC name, CAS notation, SMILES, molecular formula, InChi


#### TASKS
1. create summary df containing - EFSA Q number, do we have full jats file or not, do we have jats file at all, what report version is this -- DATA STATE DATAFRAME, reflect the special opinions that have to be separated to two and the ones that have to be merged 
2. create the JATS Opinion and extract all the informations
3. obtain TEI files of those Opinions that we dont have a fulltext for


#### Extraction rules


Adoption date

traditional food - nemají adopted, místo toho mají X
front - notes -fn-group - v nejake z nich je Adopted
group6 - ADOPTED: in fn-group 
<fn id="efs26305-note-1203" xml:lang="en">
<p>Adopted: 22 October 2020</p>
</fn>

**QUESTION NUMBER**

question number je taky v jedne fn-group
<fn id="efs26305-note-1002" xml:lang="en">
<p>
<bold>Question number:</bold>
EFSA‐Q‐2019‐00448
</p>
</fn>


ve formátu group 2 je to až někde úplně dole:
v body -> pak najít sekci s tímto titlem

<sec id="efs28416-sec-0024" xml:lang="en">
<title>QUESTION NUMBER</title>
<p xml:lang="en">EFSA‐Q‐2020‐00491</p>
</sec>