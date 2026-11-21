"""Row-by-row verification of the manuscript's tables against downloaded sources."""
import re, sys, pathlib
import fitz

sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def load(name):
    p = pathlib.Path("pdfs") / name
    if p.suffix == ".xml":
        t = p.read_text(encoding="utf-8", errors="replace")
        t = re.sub(r"<[^>]+>", " ", t)
    elif p.suffix == ".pdf":
        doc = fitz.open(p)
        t = "\n".join(pg.get_text() for pg in doc)
    else:
        t = p.read_text(encoding="utf-8", errors="replace")
    return re.sub(r"\s+", " ", t)


CACHE = {}


def text(key):
    if key not in CACHE:
        CACHE[key] = load(f"{key}.xml" if pathlib.Path("pdfs", f"{key}.xml").exists() else f"{key}.pdf")
    return CACHE[key]


CHECKS = {
    "milton2021": [
        ("N 24/25/20", ["24 aphantasic", "25 hyperphantasic", "20 mid-range"]),
        ("total 69", ["69 participants", "n = 69"]),
        ("VVIQ 16-23", ["16", "23"]),
        ("VVIQ 75-80", ["75", "80"]),
        ("mid-range 55-60", ["55", "60"]),
        ("IQ p=.008", ["0.008", ".008"]),
        ("EXTEND", ["EXTEND"]),
        ("1.5T 8 min", ["8 min", "1.5"]),
        ("no control>aphant", ["no region", "not different"]),
        ("BA10 hippocampus", ["BA10", "hippocampus"]),
        ("BA8 DAN", ["BA8", "dorsal attention"]),
        ("hyper > aphant prefrontal", ["hyperphantasic"]),
        ("p<.001 FDR", ["0.001", "FDR"]),
        ("data considered individually", ["considered individually"]),
    ],
    "monzel2024": [
        ("14 vs 16", ["14", "16"]),
        ("means 16.6 / 62.9", ["16.6", "62.9"]),
        ("TR 2 s, 190 vols", ["2 s", "190"]),
        ("3.5 mm", ["3.5"]),
        ("no rest hipp-visual diff", ["no significant", "resting-state"]),
        ("t(28)=2.65", ["2.65"]),
        ("p=.006", ["0.006"]),
        ("SVC k=10", ["small volume", "10"]),
        ("no frontal parietal test", ["frontal", "parietal"]),
        ("Dryad", ["Dryad"]),
    ],
    "kay2022": [
        ("18 vs 42", ["18", "42"]),
        ("ages 19.8 / 35.8", ["19.8", "35.8"]),
        ("VVIQ <32", ["32"]),
        ("rivalry 65%", ["65"]),
        ("BF10 > 1e6", ["BF10"]),
        ("Bonferroni", ["Bonferroni"]),
    ],
    "keogh2020": [
        ("no aphantasics", ["aphantasia"]),
        ("tDCS", ["tDCS"]),
        ("Monte Carlo / FDR", ["Monte Carlo", "FDR"]),
    ],
    "dupont2024": [
        ("14 vs 14", ["14"]),
        ("17 enrolled", ["17"]),
        ("2 SD outliers", ["standard deviation", "SD"]),
        ("VVIQ <=23", ["23"]),
        ("VMIQ-2", ["VMIQ"]),
        ("d=0.89", ["0.89"]),
        ("OSF", ["OSF"]),
    ],
    "megla2025": [
        ("twins", ["twins"]),
        ("VVIQ 24 / 47", ["24", "47"]),
        ("p=.010", ["0.010", ".010"]),
        ("motion censoring", ["censoring", "motion"]),
        ("handedness", ["handedness"]),
    ],
    "boere2025": [
        ("62 vs 59", ["62", "59"]),
        ("VVIQ <=32", ["32"]),
        ("P300", ["P300"]),
        ("OSF qdz8m", ["qdz8m", "OSF"]),
        ("eta2 .37", ["0.37", ".37"]),
    ],
    "keogh2018": [
        ("15 vs 209", ["209", "15"]),
        ("mean VVIQ 19", ["19"]),
        ("Mann-Whitney U=914", ["914"]),
        ("t(14)=.68 chance", ["0.68", ".68"]),
    ],
    "jin2024": [
        ("65 studies", ["65"]),
        ("quality rubric", ["quality"]),
        ("Milton contrast", ["Milton"]),
    ],
    "liu2025": [
        ("10 vs 10", ["10 aphantasic", "10 typical"]),
        ("VVIQ 16 vs 55", ["16", "55"]),
        ("F 21.98", ["21.98"]),
        ("cluster mean 13.70", ["13.70"]),
        ("V1 seeds null", ["V1"]),
        ("no pre-registration", ["pre-regist", "preregist"]),
        ("Fig S10 five of ten", ["Fig. S10", "Figure S10"]),
        ("frontoparietal in abstract", ["frontoparietal"]),
    ],
}

for study, checks in CHECKS.items():
    print(f"\n=== {study} ===")
    try:
        t = text(study)
    except Exception as exc:  # noqa: BLE001
        print(f"  !! cannot load: {type(exc).__name__}")
        continue
    print(f"  ({len(t)//1000}k chars)")
    for label, tokens in checks:
        hits = [tok for tok in tokens if tok.lower() in t.lower()]
        status = "OK  " if len(hits) == len(tokens) else "MISS"
        print(f"  {status} {label:32s} found {hits} of {tokens}")
