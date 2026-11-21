# Reduced frontoparietal–visual connectivity in aphantasia: an audit of the imaging evidence and its citation record

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.24415812.svg)](https://doi.org/10.5281/zenodo.24415812)

Archived: v1.0.0, concept DOI 10.5281/zenodo.24415812, version DOI 10.5281/zenodo.24415813.

Data and code accompanying the manuscript. Author: Jaiveer Bassi (independent researcher).

This repository contains the extraction sheet, the citation-coding sheet, and the scripts used to
compute the power figures, verify the extracted values against source papers, and build the
bibliography. No new empirical data were collected.

## Contents

```
data/
  extraction_studies.csv       one row per study: sampling, group definition, safeguards, data sharing
  extraction_connectivity.csv  one row per connectivity analysis: state, seed/target, N, result, correction
  citation_coding.csv          coded citing sentences for the sources checked against full text
scripts/
  make_figs.py                 regenerates Figure 1 (power) and Figure 2 (citation patterns)
  verify.py                    token-level checks of table values against downloaded texts
  download_corpus.py           downloads open-access sources (Europe PMC XML, PDFs)
  resolve_refs.py              resolves DOIs via Europe PMC / Crossref
  build_bib.py                 builds refs.bib from Crossref metadata
  requirements.txt             Python dependencies
```

## Status of the data

The `verified_against` column records, for each row, whether the value was checked against the
full text, a preprint version, the abstract only, or not at all. At the time of deposition:

- 16 of the 19 studies were checked against a full text: 9 in the version of record
  (Boere 2025; Dupont 2024; Kay 2022; Keogh & Pearson 2018 and 2020; Liu 2025; Milton 2021;
  Monzel 2024; Montabes de la Cruz 2024) and 7 in a preprint or reviewed-preprint version
  (Chang 2025; Megla 2025; Noble 2026; Takamura 2026; Tian 2025; Wicken 2021; Wu & Yu 2026);
- 1 was checked in abstract only (Keogh & Pearson 2024);
- 2 could not be retrieved (Zeman et al. 2010; Fulford et al. 2018).

Rows that could not be checked are reproduced from published abstracts and are flagged so that
anyone reusing the sheet knows their status. Where a value was taken from a preprint rather than
the version of record, the `verified_against` column says so, because the two can differ.

`citation_coding.csv` covers the citing sources for which the citing passage could be retrieved
and checked (Milton 2021, Liu 2025, Boere 2025, Megla 2025) plus two marked as not retrievable
(Wu & Yu 2026; Jin 2024). The aggregate counts in Table 5 of the manuscript also include four
further sources that are not in this sheet; completing those rows is outstanding work.
## Reproducing the figures

```bash
python -m pip install -r scripts/requirements.txt
python scripts/make_figs.py      # writes figs/fig1_power.pdf and figs/fig2_citation.pdf
```

The power calculations use a two-sample t-test with two-sided alpha = .05 and the noncentral t
distribution. The values printed to stdout should match Table 4 of the manuscript
(1.32, 1.06, 0.99, 0.68).

## Verification

`scripts/verify.py` downloads nothing and needs the source texts in a `pdfs/` directory, which
`scripts/download_corpus.py` populates for open-access items. It prints, for each study, whether
the tokens for each claimed value appear in the retrieved text. It is a screening tool: token
presence does not establish that a value was interpreted correctly, which is why the manuscript
reports row-by-row outcomes in Appendix C.

## Licence

- Data (`data/*.csv`): CC BY 4.0.
- Code (`scripts/*`): MIT.

## Citation

Bassi, J. (2026). *Reduced frontoparietal–visual connectivity in aphantasia: an audit of the
imaging evidence and its citation record*. Manuscript in preparation.
