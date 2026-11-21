"""Resolve the audit's sources to real bibliographic records (Europe PMC + Crossref)."""
import json, sys, time, urllib.parse, urllib.request, pathlib

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

UA = {"User-Agent": "aphantasia-audit-build/1.0 (mailto:build@example.org)"}
OUT = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path("refs.json")


def get_json(url, tries=3):
    for attempt in range(tries):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.load(r)
        except Exception as exc:  # noqa: BLE001
            if attempt == tries - 1:
                print(f"  ! {type(exc).__name__}: {exc} ({url[:80]})")
                return None
            time.sleep(2)


def europepmc(term):
    url = (
        "https://www.ebi.ac.uk/europepmc/webservices/rest/search?"
        + urllib.parse.urlencode(
            {"query": term, "format": "json", "resultType": "core", "pageSize": 3}
        )
    )
    d = get_json(url)
    if not d:
        return []
    out = []
    for r in d.get("resultList", {}).get("result", []):
        ji = r.get("journalInfo", {}) or {}
        out.append(
            {
                "title": (r.get("title") or "").rstrip("."),
                "authors": r.get("authorString") or "",
                "journal": ji.get("journal", {}).get("title") or r.get("journalTitle"),
                "year": r.get("pubYear"),
                "volume": ji.get("volume") or r.get("volume"),
                "issue": ji.get("issue"),
                "pages": r.get("pageInfo"),
                "doi": r.get("doi"),
                "pmid": r.get("pmid"),
                "pmcid": r.get("pmcid"),
                "type": "pubmed",
            }
        )
    return out


def crossref_doi(doi):
    d = get_json("https://api.crossref.org/works/" + urllib.parse.quote(doi, safe=""))
    if not d:
        return None
    m = d["message"]
    return {
        "title": ((m.get("title") or [""])[0] or "").rstrip("."),
        "authors": "; ".join(
            f"{a.get('family','')}, {a.get('given','')}" for a in m.get("author", [])
        ),
        "journal": (m.get("container-title") or [""])[0],
        "year": str((m.get("issued", {}).get("date-parts") or [[None]])[0][0]),
        "volume": m.get("volume"),
        "issue": m.get("issue"),
        "pages": m.get("page"),
        "doi": m.get("DOI"),
        "type": m.get("type"),
    }


def crossref_search(query, rows=4):
    url = (
        "https://api.crossref.org/works?"
        + urllib.parse.urlencode(
            {
                "query.bibliographic": query,
                "rows": rows,
                "select": "DOI,title,container-title,issued,author,volume,page,type",
            }
        )
    )
    d = get_json(url)
    if not d:
        return []
    out = []
    for m in d["message"]["items"]:
        out.append(
            {
                "title": ((m.get("title") or [""])[0] or "").rstrip("."),
                "authors": "; ".join(
                    f"{a.get('family','')}, {a.get('given','')}" for a in m.get("author", [])
                ),
                "journal": (m.get("container-title") or [""])[0],
                "year": str((m.get("issued", {}).get("date-parts") or [[None]])[0][0]),
                "volume": m.get("volume"),
                "pages": m.get("page"),
                "doi": m.get("DOI"),
                "type": m.get("type"),
            }
        )
    return out


PMC = {
    "milton2021": "PMC8186241",
    "megla2025": "PMC11463508",
    "boere2025": "PMC12711949",
    "wicken2021": "PMC7944105",
    "kay2022": "PMC9018072",
    "keogh2020": "PMC7200162",
    "dupont2024": "PMC10957132",
    "monzel2024": "PMC11426968",
}

DOIS = {
    "noble2026": "10.1016/j.neuropsychologia.2025.109322",
    "lorenzatti2026": "10.1016/j.neuropsychologia.2026.109431",
    "mckilliam2025": "10.1016/j.concog.2025.103924",
    "bartolomeo2026": "10.1146/annurev-vision-110425-105103",
    "monzel2024b": "10.7554/eLife.94916",
    "vanbuckhave2026": "10.1111/psyp.70298",
}

SEARCHES = {
    "liu2025": "aphantasia fusiform imagery prefrontal connectivity psychophysiological",
    "zeman2010": "Loss of imagery phenomenology with intact visuo-spatial task performance",
    "keogh2018": "The blind mind: No sensory visual imagery in aphantasia",
    "montabes2024": "aphantasia imagery sound visual experience blindfolded",
    "jin2024": "aphantasia systematic review of studies quality assessment",
    "takamura2026": "aphantasia white matter structural connectivity imagery network",
    "tian2025": "aphantasia visual imagery perception fMRI",
    "chang2025": "aphantasia binocular rivalry mental imagery vividness",
    "keogh2024": "aphantasia imagery vividness prevalence",
    "wicken2021b": "critical role of mental imagery in human emotion aphantasia",
}

found, searches = {}, {}

print("== Europe PMC (by PMC ID) ==")
for key, pmcid in PMC.items():
    hits = europepmc(f"PMCID:{pmcid}")
    if hits:
        found[key] = hits[0]
        h = hits[0]
        print(f"{key}: {h['title'][:78]} | {h['journal']} {h['year']};{h['volume']}:{h['pages']}")
    time.sleep(0.3)

print("\n== Crossref (known DOIs) ==")
for key, doi in DOIS.items():
    rec = crossref_doi(doi)
    if rec:
        found.setdefault(key, rec)
        print(f"{key}: {rec['title'][:78]} | {rec['journal']} {rec['year']}")
    time.sleep(0.3)

print("\n== Crossref searches (pick by eye) ==")
for key, q in SEARCHES.items():
    hits = crossref_search(q)
    searches[key] = hits
    print(f"\n{key}")
    for h in hits:
        print(f"   {h['year']} | {h['title'][:80]} | {h['journal'][:40]} | {h['doi']}")

OUT.write_text(json.dumps({"found": found, "searches": searches}, indent=1), encoding="utf-8")
print(f"\nwrote {OUT}")
