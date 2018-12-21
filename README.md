# Genetic-Report-Tool
This is a Flask/MongoDB web application that allows anybody to create a genetic "condition" report from their CSV-based raw genome export.

Simply upload your 23AndMe, Ancestry, Helix, Color, etc raw genome (in CSV format) to the uploader, and it will parse a database of SNPs (single nucleotide polymorphisms) and extract matches. 

**For example if I have the SNP:**

`rs28897696` with allele combination: `(A;A)` researchers are very confident that this mutation (combined with other factors of course), is likely be at high risk for breast/ovarian cancer according to the [NIH](https://www.ncbi.nlm.nih.gov/pubmed/17924331?dopt=Abstract)

The purpose of this repository is to show you what is happening under the hood. Want more information? Feel free to reach out.

You can see the live website [here](https://gene.meports.com)

### Installation

This Genetic Reporting Tool requires Python3 + and pip to run. 

Install the requirements before running:

```sh
$ pip install -r requirements.txt
```
Run the application:
```sh
$ python3 manage.py
```

### Data Reqiurements

The application requires a MongoDB connection. I've included a sample JSON for each MongoDB collection that the application relies on (a collection is analagous to tables in SQL):

**snps** Collection of SNPs:
```json
[{"foo":"bar"}]
```

**genes** Collection of gene combinations:
```json
[{"foo":"bar"}]
```

**reports** Generated reports:
```json
[{"foo":"bar"}]
```

**profiles** Colection of users that want their reports sent to them:
```json
[{"foo":"bar"}]
```

Simply spin up a MongoDB instance and add the above JSON to get a sense of how the application works. 

### Usage

1. Select your raw genome CSV source (23AndMe, Ancestry, Helix, etc.)
2. Click Upload!
3. Wait for the algorithm to run (via threading)
4. Review your results

### Future Enhancements

1. "Subscribe" to PubMed research that mentions gene mutations (SNP/Allele combinations) that your report contains


## Special Thanks:
1. @arvkevi for his contributions to [SNPY](https://github.com/superbobry/snpy) the SNP parser for Python and for meeting with me for random bioinformatics questions. 
2. Hacker News via [this post](https://news.ycombinator.com/item?id=18495201)

