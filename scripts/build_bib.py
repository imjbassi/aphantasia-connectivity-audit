import json, sys, urllib.parse, urllib.request, pathlib

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
UA = {"User-Agent": "aphantasia-audit-build/1.0 (mailto:build@example.org)"}
OUT = pathlib.Path("refs.bib")

DOIS = {
    "milton2021": "10.1093/texcom/tgab035",
    "liu2025": "10.1016/j.cortex.2025.01.013",
    "monzel2024": "10.7554/eLife.94916",
    "keogh2018": "10.1016/j.cortex.2017.10.012",
    "keogh2020": "10.7554/eLife.50232",
    "keogh2024": "10.1016/j.neures.2024.01.008",
    "wicken2021": "10.1098/rspb.2021.0267",
    "kay2022": "10.7554/eLife.72484",
    "dupont2024": "10.1093/braincomms/fcae072",
    "dupont2024b": "10.1162/jocn_a_02084",
    "montabes2024": "10.1016/j.cub.2024.09.008",
    "chang2025": "10.1016/j.cub.2024.12.012",
    "megla2025": "10.1093/cercor/bhaf192",
    "boere2025": "10.1038/s41598-025-27735-x",
    "takamura2026": "10.7554/eLife.111728.1",
    "noble2026": "10.1016/j.neuropsychologia.2025.109322",
    "tian2025": "10.1101/2025.08.01.668040",
    "zeman2010": "10.1016/j.neuropsychologia.2009.08.024",
    "zeman2015": "10.1016/j.cortex.2015.05.019",
    "jin2024": "10.3390/vision8030056",
    "bartolomeo2026": "10.1146/annurev-vision-110425-105103",
    "lorenzatti2026": "10.1016/j.neuropsychologia.2026.109431",
    "mckilliam2025": "10.1016/j.concog.2025.103924",
    "scholz2025": "10.1016/j.cub.2025.05.009",
    "liubartolomeo2025": "10.1016/j.tics.2025.05.012",
    "marks1973": "10.1111/j.2044-8295.1973.tb01322.x",
    "spagna2021": "10.1016/j.neubiorev.2020.12.029",
    "simonsohn2015": "10.1177/0956797614567341",
    "rouder2009": "10.3758/pbr.16.2.225",
    "vanbuckhave2026": "10.1111/psyp.70298",
    "fulford2018": "10.1016/j.cortex.2017.09.014",
}


def cr(doi):
    url = "https://api.crossref.org/works/" + urllib.parse.quote(doi, safe="")
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40) as r:
        return json.load(r)["message"]


def tidy(s):
    return (
        (s or "")
        .replace("&amp;", "&")
        .replace("{", "")
        .replace("}", "")
        .replace("  ", " ")
        .strip()
    )


def bib(key, m):
    auth = m.get("author", [])
    names = []
    for a in auth:
        fam = tidy(a.get("family", ""))
        giv = tidy(a.get("given", ""))
        if fam:
            names.append(f"{fam}, {giv}" if giv else fam)
    fields = []
    title = tidy((m.get("title") or [""])[0])
    container = tidy((m.get("container-title") or [""])[0])
    year = str((m.get("issued", {}).get("date-parts") or [[None]])[0][0])
    typ = m.get("type", "journal-article")
    fields.append(("author", " and ".join(names)))
    fields.append(("year", year))
    fields.append(("title", title))
    if typ in ("posted-content", "preprint"):
        fields.append(("howpublished", container or "Preprint"))
    else:
        fields.append(("journal", container))
    for f, src in (("volume", m.get("volume")), ("number", m.get("issue")), ("pages", m.get("page"))):
        if src:
            fields.append((f, tidy(src)))
    fields.append(("doi", tidy(m.get("DOI", ""))))
    body = ",\n".join(f"  {k} = {{{v}}}" for k, v in fields if v)
    entry_type = "article" if typ not in ("posted-content", "preprint") else "misc"
    return f"@{entry_type}{{{key},\n{body}\n}}\n"


chunks = []
for key, doi in DOIS.items():
    try:
        m = cr(doi)
        chunks.append(bib(key, m))
        print(f"ok   {key:18s} {tidy((m.get('title') or [''])[0])[:70]}")
    except Exception as exc:  # noqa: BLE001
        print(f"FAIL {key:18s} {doi} {type(exc).__name__}")

# Entries Crossref does not hold.
MANUAL = """
@misc{wuyu2026,
  author = {Wu, Tingting and Yu, Qing},
  year = {2026},
  title = {A cortical hierarchical mechanism for subjective visual experience during working memory},
  howpublished = {bioRxiv preprint},
  doi = {10.64898/2026.04.08.717338},
  note = {Preprint, not peer reviewed}
}
"""
chunks.append(MANUAL)
OUT.write_text("\n".join(chunks), encoding="utf-8")
print(f"\nwrote {OUT} ({len(chunks)} blocks)")
