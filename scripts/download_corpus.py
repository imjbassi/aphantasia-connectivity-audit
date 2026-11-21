"""Download the obtainable source papers for the verification pass."""
import pathlib, sys, urllib.request, json

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
UA = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"
}
OUT = pathlib.Path("pdfs")
OUT.mkdir(exist_ok=True)

EPMC_XML = {
    "milton2021": "PMC8186241",
    "monzel2024": "PMC11426968",
    "keogh2020": "PMC7200162",
    "wicken2021": "PMC7944105",
    "kay2022": "PMC9018072",
    "dupont2024": "PMC10957132",
    "megla2025": "PMC11463508",
    "boere2025": "PMC12711949",
}

PDFS = {
    "keogh2018.pdf": "https://www.gwern.net/doc/psychology/vision/2018-keogh.pdf",
    "jin2024.pdf": "https://www.mdpi.com/2411-5150/8/3/56/pdf",
    "takamura2026.pdf": "https://elifesciences.org/reviewed-preprints/111728.pdf",
    "tian2025.pdf": "https://www.biorxiv.org/content/10.1101/2025.08.01.668040v1.full.pdf",
    "wuyu2026.pdf": "https://www.biorxiv.org/content/10.64898/2026.04.08.717338v1.full.pdf",
    "noble2025_preprint.pdf": "https://www.biorxiv.org/content/10.1101/2025.05.25.655911v1.full.pdf",
}

ok, fail = [], []

for key, pmcid in EPMC_XML.items():
    url = f"https://www.ebi.ac.uk/europepmc/webservices/rest/{pmcid}/fullTextXML"
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
            data = r.read()
        (OUT / f"{key}.xml").write_bytes(data)
        ok.append(f"{key}.xml ({len(data)//1024} KB)")
    except Exception as exc:  # noqa: BLE001
        fail.append(f"{key}: {type(exc).__name__}")

for name, url in PDFS.items():
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=90) as r:
            data = r.read()
        if not data.startswith(b"%PDF"):
            fail.append(f"{name}: not a pdf ({data[:20]!r})")
            continue
        (OUT / name).write_bytes(data)
        ok.append(f"{name} ({len(data)//1024} KB)")
    except Exception as exc:  # noqa: BLE001
        fail.append(f"{name}: {type(exc).__name__}")

print("DOWNLOADED:")
for x in ok:
    print("  +", x)
print("FAILED:")
for x in fail:
    print("  -", x)
