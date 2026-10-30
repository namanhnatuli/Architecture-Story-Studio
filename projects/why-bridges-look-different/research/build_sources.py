"""Build research/sources.json (python3 research/build_sources.py research/sources.json): every excerpt is verified
verbatim (whitespace-normalised) against the downloaded source text; NCHRP locators get the
printed page number. M6 excerpts (ODOT/FHWA/SCI/Yale) were verified on 2026-10-28 and are
re-checked against the M6 ledger text."""
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
# Local snapshots of the downloaded sources (not committed; see research/source_snapshots.json):
#   M7_SOURCE_SNAPSHOTS=<dir with nchrp/nchrp.txt, web/asce_bollman.txt, web/yale_6.txt>
S = Path(os.environ.get("M7_SOURCE_SNAPSHOTS", Path(__file__).resolve().parent / "snapshots"))
M6 = json.loads((ROOT / "projects/bridge-load-explained/research/sources.json").read_text())
m6_src = {s["id"]: s for s in M6["sources"]}
m6_ex = {(e["source_id"], e["excerpt"]) for c in M6["claims"] for e in c["evidence"]}

raw = (S / "nchrp/nchrp.txt").read_text()
pages = [(m.start(), m.group(1)) for m in re.finditer(r"^\s{20,}(\d-\d{1,3})\s*$", raw, re.M)]
texts = {
    "SRC_NCHRP_CONTEXT": raw,
    "SRC_ASCE_BOLLMAN": (S / "web/asce_bollman.txt").read_text(),
    "SRC_YALE_PHYSICS": (S / "web/yale_6.txt").read_text(),
}


def _pat(word):
    out = ""
    for ch in word:
        if ch in "'\u2019\u2018":
            out += "['\u2019\u2018]"
        elif ch in '"\u201c\u201d':
            out += '["\u201c\u201d]'
        else:
            out += re.escape(ch)
    return out


def find(src, excerpt):
    """(page locator or None, the source's own wording of the excerpt, whitespace-normalised)."""
    t = texts[src]
    m = re.search(r"\s+".join(_pat(w) for w in excerpt.split()), t)
    if not m:
        raise SystemExit(f"NOT FOUND in {src}: {excerpt[:80]}")
    exact = re.sub(r"\s+", " ", m.group(0))
    if src == "SRC_NCHRP_CONTEXT":
        page = next((p for pos, p in pages if pos > m.start()), "?")
        return f"p. {page}", exact
    return None, exact


SOURCES = [
    dict(m6_src["SRC_ODOT_MBI"]), dict(m6_src["SRC_FHWA_CBM"]), dict(m6_src["SRC_FHWA_PBES_GLOSSARY"]),
    dict(m6_src["SRC_FHWA_PBES_CH2"]), dict(m6_src["SRC_SCI_TRUSSES"]),
    dict(m6_src["SRC_YALE_PHYSICS"], verification="Pages re-fetched 2026-10-29 (units/2001/5/01.05.08/6); excerpts matched verbatim."),
    {"id": "SRC_NCHRP_CONTEXT", "title": "A Context for Common Historic Bridge Types (NCHRP Project 25-25, Task 15)",
     "publisher": "Transportation Research Board / National Cooperative Highway Research Program; prepared by Parsons Brinckerhoff and Engineering and Industrial Heritage",
     "kind": "national research report (historic context study, AASHTO/FHWA-sponsored)", "edition": "October 2005",
     "url": "https://onlinepubs.trb.org/onlinepubs/archive/notesdocs/25-25(15)_FR.pdf", "accessed": "2026-10-29",
     "verification": "PDF downloaded 2026-10-29 (11.1 MB), text extracted with pdftotext -layout; every excerpt matched verbatim (whitespace-normalised); page = printed report page.",
     "notes": "The cover carries the standard NCHRP 'privileged document' legend; the final report is publicly posted by TRB. Quoted for research and citation only.",
     "license": "Quoted for research/citation only."},
    {"id": "SRC_ASCE_BOLLMAN", "title": "Bollman Truss Bridge (Historic Civil Engineering Landmark)", "publisher": "American Society of Civil Engineers",
     "kind": "professional engineering society landmark page", "edition": "web page, accessed 2026-10-29",
     "url": "https://www.asce.org/about-civil-engineering/history-and-heritage/historic-landmarks/bollman-truss-bridge", "accessed": "2026-10-29",
     "verification": "HTML downloaded 2026-10-29; excerpts matched verbatim. Note: the page gives 1852 for the present bridge (moved 1882); other records give c. 1869, so the film does not state the construction year.",
     "license": "Quoted for research/citation only."},
    {"id": "SRC_HAER_CARROLLTON", "title": "Baltimore & Ohio Railroad, Carrollton Viaduct, Spanning Gwynn's Falls near Carroll Park, Baltimore (HAER MD-9)",
     "publisher": "Historic American Engineering Record, National Park Service; Library of Congress Prints & Photographs (item md0908)",
     "kind": "federal documentation record (photographs)", "edition": "photographs 1970-1971 (William E. Barrett)",
     "url": "https://www.loc.gov/item/md0908/", "accessed": "2026-10-29",
     "verification": "loc.gov blocks automated access (HTTP 403); the photograph and its LOC source link (hhh.md0908/photos.086090p) were taken from the Wikimedia Commons file page, licence template PD-USGov-NPS.",
     "license": "Public domain (work of the U.S. National Park Service / HAER)."},
    {"id": "SRC_HAER_PROMONTORY", "title": "Promontory Route Railroad Trestles, Trestle 790B, Corinne vicinity, Box Elder County, Utah (HAER UT-64)",
     "publisher": "Historic American Engineering Record, National Park Service; Library of Congress (item ut0393)",
     "kind": "federal documentation record (photographs)", "edition": "documentation compiled after 1968",
     "url": "https://www.loc.gov/pictures/item/ut0393.photos.367543p", "accessed": "2026-10-29",
     "verification": "Photograph and LOC source link from the Wikimedia Commons file page (PD-USGov-NPS); loc.gov itself returned HTTP 403 to automated access.",
     "license": "Public domain (work of the U.S. National Park Service / HAER)."},
    {"id": "SRC_HAER_BOLLMAN", "title": "Baltimore & Ohio Railroad, Bollman Truss Bridge, Spanning Little Patuxent River, Savage, Howard County, MD (HAER MD-1)",
     "publisher": "Historic American Engineering Record, National Park Service; Library of Congress (item md0583)",
     "kind": "federal documentation record (photographs)", "edition": "photograph 1970 (William E. Barrett)",
     "url": "https://www.loc.gov/pictures/item/md0583.photos.082178p", "accessed": "2026-10-29",
     "verification": "Photograph and LOC source link from the Wikimedia Commons file page (PD-USGov-NPS); loc.gov returned HTTP 403 to automated access.",
     "license": "Public domain (work of the U.S. National Park Service / HAER)."},
    {"id": "SRC_HAER_HUMPBACK", "title": "Humpback Covered Bridge, spanning Dunlap Creek, Covington, VA (HAER VA, Survey va0239)",
     "publisher": "Historic American Engineering Record, National Park Service; Library of Congress (item va0239)",
     "kind": "federal documentation record (photographs)", "edition": "photograph 1971 (Jack E. Boucher)",
     "url": "https://www.loc.gov/pictures/item/va0239.photos.161261p", "accessed": "2026-10-29",
     "verification": "Photograph and LOC source link from the Wikimedia Commons file page (PD-USGov-NPS); loc.gov returned HTTP 403 to automated access.",
     "license": "Public domain (work of the U.S. National Park Service / HAER)."},
]


def m6(cid):
    return next(c for c in M6["claims"] if c["id"] == cid)


def claim(cid, text, evidence, applies, comps, visual, assumptions="", scope=None, confidence="high"):
    ev = []
    for src, locator, excerpt in evidence:
        if src in texts:
            page, excerpt = find(src, excerpt)
            if locator and locator.startswith("List of figures"):
                page = None   # front matter: the figure number is the locator
            if page and locator is None:
                locator = page
            elif page:
                locator = f"{locator}, {page}"
        elif (src, excerpt) not in m6_ex:
            raise SystemExit(f"{cid}: excerpt not in the verified M6 ledger: {excerpt[:60]}")
        ev.append({"source_id": src, "locator": locator, "excerpt": excerpt})
    return {"id": cid, "text": text, "source_ids": sorted({e["source_id"] for e in ev}), "review_status": "SOURCE_VERIFIED",
            "confidence": confidence, "evidence": ev, "assumptions": assumptions or "None beyond the quoted wording.",
            "applies_to": applies, "components": comps, "intended_visual": visual,
            "scope": scope or "qualitative; illustrative models; no member forces, capacities, stresses, safety factors or quantitative comparisons beyond quoted facts",
            "caveat": "Not editorially approved."}


def from_m6(cid, new_id, visual=None):
    c = m6(cid)
    return claim(new_id, c["text"], [(e["source_id"], e["locator"], e["excerpt"]) for e in c["evidence"]], c["applies_to"],
                 c["components"], visual or c["intended_visual"], c.get("assumptions", ""), c.get("scope"), c.get("confidence", "high"))


N = "SRC_NCHRP_CONTEXT"
CLAIMS = [
    from_m6("CLM_601", "CLM_701"), from_m6("CLM_602", "CLM_702"), from_m6("CLM_603", "CLM_703"), from_m6("CLM_604", "CLM_704"),
    from_m6("CLM_605", "CLM_705"), from_m6("CLM_606", "CLM_706"), from_m6("CLM_607", "CLM_707"), from_m6("CLM_608", "CLM_708"),
    from_m6("CLM_609", "CLM_709"), from_m6("CLM_610", "CLM_710"), from_m6("CLM_611", "CLM_711"), from_m6("CLM_612", "CLM_712"),
    from_m6("CLM_613", "CLM_713"), from_m6("CLM_614", "CLM_714"),
    claim("CLM_720", "Timber stringer (beam) bridges are a very old type that dates back to the origins of bridge building.",
          [(N, "3.3.1 Timber Stringer", "Wood stringer (or beam) bridges are a very old type of design that dates back to the origins of bridge building.")],
          ["beam"], ["stringer"], "Timber beam model; no historical reconstruction"),
    claim("CLM_721", "Because of their simplicity and readily available wood, timber beam bridges were still built long after wood trusses stopped being competitive, and today they are built on low-traffic rural roads, private roads, forests and parks.",
          [(N, "3.3.1 Timber Stringer", "Long after wood truss bridges had ceased to be competitive with metal truss bridges for use in short spans in the nineteenth century, timber beam bridges were still being built. Because of the structure's simplicity and readily available material (wood), the timber beam has endured to the present day"),
           (N, "3.3.1 Timber Stringer", "Today, these structures are built on low-trafficked, rural backcountry roads, private roads, or in national forests and parks.")],
          ["beam"], ["stringer"], "Timber beam model; caption 'Illustrative model'"),
    claim("CLM_722", "Many early timber bridges had relatively short spans.",
          [(N, "2.2 (North Dakota, quoted)", "Most were built of timber with relatively short spans.")],
          ["beam"], ["trestle_bent"], "Timber model: several short spans on bents",
          assumptions="The quoted passage describes early bridges west of the Mississippi (North Dakota); used only as 'many early timber bridges had relatively short spans'."),
    claim("CLM_723", "Falsework (temporary supports, built by carpenters) is erected to support a stone arch during construction, and the masonry is laid by skilled masons.",
          [(N, "3.2.1 Stone Arch", "the skills necessary for erection of falsework to support arch construction (carpentry) and for the laying of stones (masonry) were commonly found within the local labor pool")],
          ["arch"], ["arch_ring"], "2D diagram: arch ring on temporary falsework (conceptual)"),
    claim("CLM_724", "Stone arch bridges were generally more expensive to build than timber bridges, but were favoured for heavily travelled routes or important locations; elsewhere the lower cost of timber offset its lack of permanence.",
          [(N, "3.2.1 Stone Arch", "Stone arch bridges were generally more expensive to build than were timber bridges, but their use for roads and highways was favored for heavily traveled routes or locations of high visibility and importance; otherwise, the cost savings of timber bridges tended to offset their relative lack of permanence.")],
          ["arch", "beam"], ["arch_ring"], "2D comparison panel: cost vs permanence (qualitative, no numbers)"),
    claim("CLM_725", "Where durability and permanence were required, stone was the preferred bridge material over wood.",
          [(N, "3.2.1 Stone Arch", "Stone and wood were often the most readily available building materials for bridges long before fabricated metal was introduced towards the middle of the nineteenth century, and of the two, stone was by far the preferred choice where durability and permanence were required.")],
          ["arch"], ["arch_ring"], "Comparison panel"),
    claim("CLM_726", "Arch bridges need materials that are strong under compression, such as stone, concrete or steel.",
          [("SRC_YALE_PHYSICS", "unit 01.05.08, section 6", "When selecting a building material for an arch bridge, engineers must consider only materials that are strong under compression. These materials include stone, concrete, or steel.")],
          ["arch"], ["arch_ring"], "Materials panel", confidence="medium",
          assumptions="Educational secondary source (teacher curriculum unit); used for the general principle only."),
    claim("CLM_727", "The Pratt truss was patented in 1844; its original form combined vertical timber members in compression with diagonal iron rods in tension, a principle used well into the twentieth century in all-steel trusses.",
          [(N, "2.2", "In 1844, Thomas and Caleb Pratt patented the Pratt Truss, which reversed the Howe system and incorporated vertical timber members in compression and diagonal iron rods in tension, a “combination” structure. The structural principle in this design was used well into the twentieth century when all parts were made in steel.")],
          ["truss"], ["truss_web"], "Pratt pattern highlighted (no member colouring)",
          assumptions="Historical design description of the 1844 patent; the film does not mark the model's members as in tension or compression."),
    claim("CLM_728", "The Warren truss was patented in 1848 by James Warren and Willoughby Monzani, with alternating diagonals.",
          [(N, "2.2", "the Warren truss was patented by two British engineers, James Warren and Willoughby Monzani. This truss design had alternating diagonals in either tension or compression")],
          ["truss"], ["truss_web"], "Warren pattern on the shared chords (illustrative variant without verticals)",
          assumptions="The model's Warren variant has no verticals; the film says only that the diagonals alternate."),
    claim("CLM_729", "From mid-century, fabricating shops formed, drilled and test-assembled truss members and shipped them to the bridge site; by 1860 railroads relied almost exclusively on such prefabricated parts.",
          [(N, "2.2 'Foundries and Fabricators'", "These shops formed bridge members, drilled the members and assembled and connected the truss members, before packaging and shipping them to the bridge site. By 1860, the railroads were almost exclusively relying on these private concerns to fill their bridge needs with pre-fabricated parts.")],
          ["truss"], ["truss_members"], "Exploded truss (members as separate prefabricated pieces)"),
    claim("CLM_730", "Through trusses carry heavier loads than pony trusses and are longer in span, some approaching 400 feet.",
          [(N, "3.1 Trusses", "Through trusses are designed to carry heavier traffic loads than the pony truss and are longer in span, some approaching 400 feet.")],
          ["truss"], ["truss_members"], "Span scale panel (sourced values only)"),
    claim("CLM_731", "Simple king post trusses spanned only very short distances, up to about 30 feet.",
          [(N, "3.1.1 King Post", "Simple king post trusses were used only to span very short distances up to about 30 feet")],
          ["truss"], ["truss_members"], "Span scale panel"),
    claim("CLM_732", "The 220-foot span Cabin John Aqueduct Bridge (1864) was the longest arch bridge in the world until 1905.",
          [(N, "3.2.1 Stone Arch", "America’s greatest stone arch is the 220-foot span Cabin John Aqueduct Bridge (1864) over Cabin John Creek in suburban Maryland outside Washington, DC. It was the longest arch bridge in the world until 1905.")],
          ["arch"], ["arch_ring"], "Span scale panel"),
    claim("CLM_733", "Many timber truss bridges were covered by a roof and siding to protect them from the weather.",
          [(N, "3.1.1 King Post", "the most common extant king post truss bridges are covered by a roof and siding to protect them from the weather")],
          ["truss"], ["truss_members"], "HAER photograph of the Humpback Covered Bridge",
          assumptions="Stated for king post trusses; the film says 'many timber truss bridges'."),
    claim("CLM_734", "Wooden bridges were vulnerable to decay.",
          [("SRC_ASCE_BOLLMAN", "main text", "Replacing wooden bridges, which were cumbersome to build and vulnerable to decay")],
          ["beam", "truss"], [], "Materials panel"),
    claim("CLM_735", "Wrought iron was valued as a material strong equally in tension and in compression (Plowden, quoted in NCHRP).",
          [(N, "2.2", "realized that a great advantage would be gained by the substitution of wrought iron [for cast iron], a material strong equally in tension and in compression")],
          ["truss"], ["truss_members"], "Materials panel", assumptions="A historian's characterisation (David Plowden) quoted in the report."),
    claim("CLM_736", "Viaducts and trestles were the engineering solution for keeping a railway line nearly straight and level where a valley was too deep and wide for embankments, because engines have limited traction.",
          [(N, "3.6 Trestles and Viaducts", "both have design attributes that were generated by the need of railroad engineers to maintain easy gradients, especially when crossing deep ravines or depressions, to compensate for the limited traction of railroad engines."),
           (N, "3.6 Trestles and Viaducts", "“Viaducts and trestles were the engineering solution for maintaining a nearly straight and horizontal line where the depth and width of the valley or gorge rendered embankments impracticable.”")],
          ["all"], [], "2D diagram: valley profile with a level line on piers (schematic)"),
    claim("CLM_737", "A trestle is a succession of towers of steel, timber or reinforced concrete supporting short spans.",
          [(N, "3.6 Trestles and Viaducts", "a trestle consists of a succession of towers of steel, timber, or reinforced concrete, supporting short spans")],
          ["beam"], ["trestle_bent"], "Timber model bents highlighted"),
    claim("CLM_738", "Stone arch construction declined with the spread of metal truss bridges, fewer skilled masons and reinforced concrete, then briefly revived in the Great Depression.",
          [(N, "3.2.1 Stone Arch", "Increased use of metal truss bridges on highways from the late 1800s into the early twentieth century, coupled with a decrease in the number of skilled masons, and advancements in reinforced concrete construction technology in the early decades of the twentieth century, led to a decline in stone arch bridge construction. A brief resurgence in construction of this type occurred during the Great Depression")],
          ["arch"], ["arch_ring"], "Timeline card"),
    claim("CLM_739", "The Carrollton Viaduct, completed in 1829 across Gwynn's Falls west of Baltimore, was built of about 12,000 granite blocks; the 312-foot bridge has an 80-foot arch over the waterway.",
          [(N, "2.2", "The first major engineered railroad bridge was the Carrollton Viaduct, completed in 1829 across Gwynn’s Falls, west of Baltimore City. Constructed of approximately 12,000 granite blocks, the 312-foot long bridge featured an 80-foot arch over the waterway.")],
          ["arch"], ["arch_ring"], "HAER photograph of the Carrollton Viaduct"),
    claim("CLM_740", "The Carrollton Viaduct is the earliest stone arch railroad bridge built in the United States and, as of 2005, the world's oldest stone railroad span still in service; it is a National Historic Landmark.",
          [(N, "3.6 Trestles and Viaducts", "The earliest stone arch railroad bridge built in the United States, and the world’s oldest stone railroad span still in service, is the Carrollton Viaduct over Gwynn’s Falls on the old B & O Railroad line near Baltimore, Maryland. Completed in 1829, this National Historic Landmark")],
          ["arch"], [], "HAER photograph", assumptions="'Still in service' is as of the 2005 report; the film attributes it to the report."),
    claim("CLM_741", "Railroads needed more sophisticated designs and durable materials for the heavy loads of railcars; in the East they built massive stone viaducts.",
          [(N, "2.2", "The railroad companies revolutionized bridge design, as they required more sophisticated designs and durable materials for carrying the heavy loads of the railcars."),
           (N, "2.2", "In the east, the railroads built massive high and/or long stone viaducts along the Baltimore and Ohio (B&O) Railroad.")],
          ["arch"], [], "Arch model with 'Illustrative model' note"),
    claim("CLM_742", "Western bridge builders generally used timber because of the pressure to open new railroads quickly and economically, and because timber was abundant and cheap.",
          [(N, "2.2", "While stone was often used in the East, timber was generally used by the western bridge builders because of the pressure to quickly and economically get new railroads on line, and timber was generally abundant and cheap.")],
          ["beam"], [], "HAER photograph of the Promontory trestle; schematic map"),
    claim("CLM_743", "Promontory Route Railroad Trestle 790B (1872), near Corinne in Box Elder County, Utah, was built by the Central Pacific Railroad Company.",
          [(N, "List of figures, 3-106", "Promontory Route Railroad Trestles 790B (1872), Corinne vicinity, Box Elder County, Utah. This nineteenth century structure was built by the Central Pacific Railroad Company.")],
          ["beam"], [], "HAER photograph"),
    claim("CLM_744", "The Bollman truss design, patented in 1852, was one of the first to use iron exclusively in all essential structural elements and could be built relatively quickly and inexpensively while providing the long-lasting qualities of metal.",
          [("SRC_ASCE_BOLLMAN", "main text", "patented in 1852 and one of the first to use iron exclusively in all essential structural elements"),
           ("SRC_ASCE_BOLLMAN", "main text", "the Bollman Truss Bridge could be built relatively quickly and inexpensively, while providing the long-lasting qualities associated with metal.")],
          ["truss"], [], "HAER photograph of the Bollman truss at Savage"),
    claim("CLM_745", "The Bollman Truss Bridge at Savage, Maryland, is the only remaining example of a patented design used extensively on the Baltimore & Ohio and other railroads.",
          [("SRC_ASCE_BOLLMAN", "main text", "The Bollman Truss Bridge is the only remaining example of a patented design that was used extensively on the Baltimore & Ohio and other railroads.")],
          ["truss"], [], "HAER photograph"),
    claim("CLM_746", "The Humpback Covered Bridge (1857), spanning Dunlap Creek, is an example of a multiple king post truss used for a covered bridge.",
          [(N, "List of figures, 3-5", "Humpback Covered Bridge (1857), Humpback Bridge spanning Dunlap")],
          ["truss"], [], "HAER photograph", assumptions="Only the name, date and crossing are narrated."),
    claim("CLM_747", "Stone arch bridges were popular where good stone was available locally, yet some states with abundant stone built few of them.",
          [(N, "3.2.1 Stone Arch", "stone arch bridges were popular in Kansas for many reasons, a major one being that the stone was often available locally."),
           (N, "3.2.1 Stone Arch", "despite an abundance of stone in various forms through the state and an indigenous tradition of masonry construction, stone bridges were never built in abundance in Michigan.")],
          ["arch"], [], "Materials/site panel"),
]

# The owner's editorial decision (a human record, never written by this script) is applied on top.
approval_path = Path(sys.argv[1]).parent / "editorial_approval.json"
approval = json.loads(approval_path.read_text()) if approval_path.is_file() else None
if approval:
    for c in CLAIMS:
        if c["id"] in approval["claims"]:
            c["review_status"] = "EDITORIALLY_APPROVED"
            c["caveat"] = (f"Editorially approved {approval['approved_on']} for narration "
                           f"{approval['narration_revision']}; illustrative models, conceptual forces only.")
            c["editorial_approval"] = {k: approval[k] for k in ("approved_by", "approved_on", "narration_revision", "basis")}

out = {"note": "M7 evidence registry for 'Why Bridges Don't All Look the Same'. CLM_701-714 restate the M6 claims (verified 2026-10-28) under new ids; CLM_720+ are new. Every excerpt was matched verbatim against the downloaded source text (gen/build_sources.py). "
               + (f"{len(approval['claims'])} narrated claims editorially approved by {approval['approved_by']} on {approval['approved_on']} (research/editorial_approval.json)."
                  if approval else "Nothing here is editorially approved."),
       "sources": SOURCES, "claims": CLAIMS}
Path(sys.argv[1]).write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
print(len(SOURCES), "sources", len(CLAIMS), "claims")
