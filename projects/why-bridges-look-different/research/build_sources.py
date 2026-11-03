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
# The M6 pilot is a test fixture since the M7 cleanup (docs/production/CLEANUP_REPORT.md).
M6 = json.loads((ROOT / "tests/fixtures/legacy_projects/bridge-load-explained/research/sources.json").read_text())
m6_src = {s["id"]: s for s in M6["sources"]}
m6_ex = {(e["source_id"], e["excerpt"]) for c in M6["claims"] for e in c["evidence"]}

raw = (S / "nchrp/nchrp.txt").read_text()
pages = [(m.start(), m.group(1)) for m in re.finditer(r"^\s{20,}(\d-\d{1,3})\s*$", raw, re.M)]
texts = {
    "SRC_NCHRP_CONTEXT": raw,
    "SRC_ASCE_BOLLMAN": (S / "web/asce_bollman.txt").read_text(),
    "SRC_YALE_PHYSICS": (S / "web/yale_6.txt").read_text(),
    # M8: the archived FHWA PDF carries an "Archived" watermark; fhwa.txt drops its stray fragments
    # (lines that are only "Ar", "ch", "i", "ve" or "d"), see research/source_snapshots.json
    "SRC_FHWA_BRIDGE_TYPES": (S / "fhwa/fhwa.txt").read_text(),
    "SRC_FHWA_PENOBSCOT": (S / "web/fhwa_14067_003.txt").read_text(),   # M8.1
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
    {"id": "SRC_FHWA_BRIDGE_TYPES", "title": "Steel Bridge Design Handbook: Selecting the Right Bridge Type (Publication No. FHWA-IF-12-052, Vol. 5)",
     "publisher": "U.S. Department of Transportation, Federal Highway Administration",
     "kind": "federal engineering handbook", "edition": "November 2012",
     "url": "https://www.fhwa.dot.gov/bridge/steel/pubs/if12052/volume05.pdf",
     "archived_url": "https://web.archive.org/web/2017id_/https://www.fhwa.dot.gov/bridge/steel/pubs/if12052/volume05.pdf",
     "accessed": "2026-10-31",
     "verification": "The FHWA URL no longer serves the file (HTTP 404) and the ROSAP copy refuses automated access (HTTP 403); the PDF was downloaded on 2026-10-31 from the Internet Archive capture of the FHWA URL (5.8 MB), text extracted with pdftotext -layout, the archive watermark fragments removed; every excerpt matched verbatim (whitespace-normalised). Superseded by FHWA-HIF-16-002 (2015) and AISC (2022); quoted as a 2012 FHWA statement.",
     "license": "U.S. federal government work; quoted for research/citation."},
    {"id": "SRC_FHWA_PENOBSCOT", "title": "Dynamic Properties of Stay Cables on the Penobscot Narrows Bridge (FHWA-HRT-14-067), Chapter 3: Experimental Procedures",
     "publisher": "U.S. Department of Transportation, Federal Highway Administration (Turner-Fairbank Highway Research Center)",
     "kind": "federal research report", "edition": "September 2014",
     "url": "https://www.fhwa.dot.gov/publications/research/infrastructure/structures/bridge/14067/003.cfm", "accessed": "2026-11-03",
     "verification": "HTML downloaded 2026-11-03; text extracted (tags stripped, entities unescaped, whitespace collapsed); every excerpt matched verbatim.",
     "license": "U.S. federal government work; quoted for research/citation."},
    {"id": "SRC_HAER_GOLDENGATE", "title": "Golden Gate Bridge, Spanning mouth of San Francisco Bay, San Francisco, CA (HAER CA-31)",
     "publisher": "Historic American Engineering Record, National Park Service; Library of Congress (item ca1355)",
     "kind": "federal documentation record (photographs)", "edition": "colour photograph 1984 (Jet Lowe)",
     "url": "https://www.loc.gov/pictures/item/ca1355.color.570641c", "accessed": "2026-11-03",
     "verification": "Photograph and LOC source link from the Wikimedia Commons file page (licence templates PD-USGov-NPS, HABS-source); loc.gov blocks automated access.",
     "license": "Public domain (work of the U.S. National Park Service / HAER)."},
    {"id": "SRC_HAER_BROOKLYN", "title": "Brooklyn Bridge, Spanning East River between Park Row, Manhattan and Sands Street, Brooklyn, New York, NY (HAER NY-18)",
     "publisher": "Historic American Engineering Record, National Park Service; Library of Congress (item ny1234)",
     "kind": "federal documentation record (photographs)", "edition": "colour transparency before November 1982 (unknown photographer; scanned by Jet Lowe)",
     "url": "https://www.loc.gov/pictures/item/ny1234.color.570577c", "accessed": "2026-10-31",
     "verification": "Photograph and LOC source link from the Wikimedia Commons file page (licence templates PD-USGov-NPS, HABS-source); loc.gov blocks automated access.",
     "license": "Public domain (work of the U.S. National Park Service / HAER)."},
    {"id": "SRC_HAER_QUEENSBORO", "title": "Queensboro Bridge, Spanning East River and Blackwell's Island, New York, NY (HAER NY-19)",
     "publisher": "Historic American Engineering Record, National Park Service; Library of Congress (item ny0326)",
     "kind": "federal documentation record (photographs)", "edition": "photograph 1991 (Jet Lowe)",
     "url": "https://www.loc.gov/pictures/item/ny0326.photos.348966p", "accessed": "2026-10-31",
     "verification": "Photograph and LOC source link from the Wikimedia Commons file page (licence templates PD-USGov-NPS, HABS-source); loc.gov blocks automated access.",
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
F = "SRC_FHWA_BRIDGE_TYPES"
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
    # ---- M8: the long-span families (NCHRP 25-25(15) 3.1, 3.5, 3.7; FHWA-IF-12-052 vol. 5) ----
    claim("CLM_750", "A cantilever is like an arm held straight out from the shoulder, or a diving board: a beam supported at one end and unsupported at the other; cantilever bridges are a modified form of beam bridge.",
          [(N, "3.7 Cantilevers", "If you hold your arm straight out from your shoulder, it is acting as a cantilever."),
           (N, "3.7 Cantilevers", "Cantilever bridges are a modified form of beam bridge. A cantilever is essentially a beam that is unsupported at one end but supported at the other, like diving boards.")],
          ["cantilever"], ["cantilever_arm"], "Cantilever model assembling on the wide site"),
    claim("CLM_751", "A cantilevered truss bridge consists of anchor arms supported by piers and a suspended span supported by the arms.",
          [(N, "3.1 Trusses", "A cantilevered truss bridge consists of anchor arms supported by piers, and a suspended span that is supported by the anchor arms."),
           (N, "3.7 Cantilevers", "the counterbalanced cantilever with the arms supporting a simple suspended span")],
          ["cantilever"], ["anchor_arm", "cantilever_arm", "suspended_span"], "Cantilever model: anchor arms, cantilever arms, suspended span labelled"),
    claim("CLM_752", "The cantilever was developed to make bridges longer, to cross wide rivers and deep gorges; it made longer spans and wider clearance beneath possible.",
          [(N, "3.7 Cantilevers", "The cantilever was developed to solve the problem of increasing the length of the bridge to enable crossing wide bodies of water like the Ohio and Mississippi rivers, or wide and deep gorges like the Niagara Gorge"),
           (N, "3.7 Cantilevers", "This configuration made longer spans possible and wider clearance beneath.")],
          ["cantilever"], [], "The wide crossing (illustrative)"),
    claim("CLM_753", "A cantilever can be built outward from its towers without falsework blocking the channel below; the suspended span is then lifted into place.",
          [(N, "3.7 Cantilevers", "One great advantage of a cantilever is that it can be built outwards from the towers without falsework to block the channel below. Then the suspended span can be lifted into place.")],
          ["cantilever"], ["suspended_span"], "Exploded cantilever: the suspended span lifts out and returns"),
    claim("CLM_754", "In the United States, cantilever bridges date from the 1880s to the 1960s and were one of the standard types for intermediate to longer spans.",
          [(N, "3.7 Cantilevers", "The cantilever bridge in the U.S. dates from the 1880s to the 1960s and is one of the standard bridge types for intermediate to longer spans")],
          ["cantilever"], [], "Timeline band"),
    claim("CLM_755", "In the two decades before 2005, cable-stayed bridges began to supplant cantilevers because they are visually appealing and sometimes more economical.",
          [(N, "3.7 Cantilevers", "In the last twenty years, however, cable-stayed suspension bridges have begun to supplant cantilevers because they are visually appealing and sometimes more economical.")],
          ["cantilever", "cable_stayed"], [], "Timeline / economics card",
          assumptions="'The last twenty years' is read from the report's 2005 date (about 1985-2005); the report calls them 'cable-stayed suspension bridges'."),
    claim("CLM_756", "The Queensboro Bridge over the East River in New York City was the longest cantilever in the United States when completed in 1909.",
          [(N, "3.7 Cantilevers", "The Queensboro Bridge over the East River in New York City was the longest cantilever in the United States when completed in 1909.")],
          ["cantilever"], [], "HAER photograph of the Queensboro Bridge"),
    claim("CLM_757", "Beam and arch bridges of steel or reinforced concrete had limited spans, not exceeding 200 to 300 feet; the cantilever provided an alternative, and also avoided the costly anchorages a suspension bridge requires.",
          [(N, "3.7 Cantilevers", "It provided alternatives to beam and arch bridges, which had limited spans not exceeding 200 to 300 feet when constructed of steel or reinforced concrete."),
           (N, "3.7 Cantilevers", "The cantilever also eliminated the high cost of building anchorages required by the other long span bridge type, suspension bridges, thus saving money and materials.")],
          ["cantilever", "beam", "arch", "suspension"], [], "Comparison / span card"),
    claim("CLM_760", "The deck of a suspension bridge hangs from vertical suspenders attached to cables in tension, which pass over towers in compression.",
          [(N, "3.5 Suspension", "The deck of a suspension bridge is hung from vertical suspenders that are affixed to ropes, chains, eyebars or cables that are in tension, passing over towers that are in compression.")],
          ["suspension"], ["main_cable", "hanger", "tower"], "Suspension model: hangers, cables (tension) and towers (compression) marked"),
    claim("CLM_761", "The ends of a suspension bridge's main cables are anchored in large masses of stone or concrete, or directly into bedrock.",
          [(N, "3.5 Suspension", "Usually the ends of the cables are anchored in large masses of stone or concrete"),
           (F, "2.6 Suspension Bridges", "The ends of the main suspension cables are anchored either into large counterweights or directly into bedrock at the ends of the structure.")],
          ["suspension"], ["anchorage"], "Anchorages on the banks"),
    claim("CLM_762", "The main cables run along the outer edges of the bridge, draped over the towers where they rest in saddles, and vertical cables connect them to the ends of transverse floor beams.",
          [(F, "2.6 Suspension Bridges", "The main cables typically are located at the outside edges of the bridge and are draped over the towers where they rest in saddles."),
           (F, "2.6 Suspension Bridges", "The superstructure is generally supported at relatively short intervals by vertical cables that connect at the ends of transverse floorbeams.")],
          ["suspension"], ["main_cable", "hanger"], "Suspension model geometry"),
    claim("CLM_763", "Suspension bridges are particularly suited to spanning great distances; their towers are much shorter than a cable-stayed bridge's, and they become economical for very long spans.",
          [(N, "3.5 Suspension", "Suspension bridges are particularly suited for spanning great distances"),
           (F, "2.6 Suspension Bridges", "Suspension bridges, whose towers are significantly shorter than those required for cable-stayed bridges, become economical for very long spans.")],
          ["suspension", "cable_stayed"], ["tower", "pylon"], "Suspension vs cable-stayed side by side (tower heights)"),
    claim("CLM_764", "Two towers, cables and suspenders, anchorages and a stiffening truss are the character-defining features of a suspension bridge.",
          [(N, "3.5 Suspension", "The plan involved two towers, cables and suspenders, anchorages and a stiffening truss - the character-defining features of a suspension bridge.")],
          ["suspension"], ["tower", "main_cable", "hanger", "anchorage", "stiffening_truss"], "Brooklyn Bridge photograph; the model's parts"),
    claim("CLM_765", "A suspension deck is very light for its span and can be very flexible, so a stiffening truss is commonly provided under the deck against wind and earthquake loading.",
          [(F, "2.6 Suspension Bridges", "Suspension bridge superstructures are generally very light relative to the span length which leads to structures that may be very flexible."),
           (F, "2.6 Suspension Bridges", "it is common to provide a lateral stiffening truss under the deck to avoid excessive excitement of the superstructure under wind or seismic loadings.")],
          ["suspension"], ["stiffening_truss"], "Stiffening truss highlighted"),
    claim("CLM_766", "Ellet's Wheeling bridge (1849) spanned 1,010 feet and was the longest bridge in the world for many years; Roebling's Cincinnati-Covington bridge (1867) had a 1,057-foot main span, the longest clear span in the world when completed.",
          [(N, "3.5 Suspension", "He quickly turned his full attention to the Wheeling Bridge, which was completed in 1849. Spanning 1,010 feet, this was the longest bridge in the world for many years after its completion"),
           (N, "3.5 Suspension", "Officially opened on January 1, 1867, this bridge has a main span of 1,057 feet. It had the longest clear span of any bridge in the world when completed")],
          ["suspension"], [], "Span scale card (sourced values only)"),
    claim("CLM_767", "At one time a great number of suspension bridges of very modest span were built across the United States, because of the type's basic simplicity and ease of erection.",
          [(N, "3.5 Suspension", "At one time, however, a great number of suspension bridges of very modest span length were built across the country due to the type’s basic simplicity and ease of erection.")],
          ["suspension"], [], "Not a story of progress (timeline / conclusion)"),
    claim("CLM_768", "The Brooklyn Bridge was completed in 1883; few suspension bridges built since the Roeblings' time can claim to stand entirely clear of its shadow.",
          [(N, "3.7 Cantilevers", "Washington Roebling for the Brooklyn Bridge (1883)"),
           (N, "3.5 Suspension", "Few suspension bridges in the world built since the time of the Roeblings can claim to stand entirely clear of the shadow cast by the Brooklyn Bridge.")],
          ["suspension"], [], "HAER photograph of the Brooklyn Bridge",
          assumptions="'Few ... stand entirely clear of the shadow' is the report's assessment; the narration attributes it ('one report')."),
    claim("CLM_770", "Cable-stayed bridges rely on high-strength steel cables; the stay cables are inclined from the towers to edge girders at or below the deck.",
          [(F, "2.5 Cable-Stayed", "Cable-Stayed bridges rely on high strength steel cables as major structural elements. The stay cables are inclined from the supporting towers to edge girders at or below the deck elevation.")],
          ["cable_stayed"], ["stay_cable", "pylon"], "Cable-stayed model: stays and towers labelled"),
    claim("CLM_771", "Cable-stayed bridge towers are generally very tall, their height set by the span; the flattest stays should not be less than about 22 degrees from the horizontal.",
          [(F, "2.5 Cable-Stayed", "Generally the towers are very tall with the height determined as a function of the span length."),
           (F, "2.5 Cable-Stayed", "The flattest cable angle should not be less than about 22 degrees with the horizontal.")],
          ["cable_stayed"], ["pylon", "stay_cable"], "Tall pylons; the model's flattest stay is about 29 degrees"),
    claim("CLM_772", "Once the towers are complete, a cable-stayed deck can be built without falsework towers, by a balanced cantilever method proceeding away from the towers until the spans close.",
          [(F, "4.4 Cable-Stayed Bridges", "Once the towers are completed, the cable-stayed superstructures can be constructed without falsework towers, which can provide significant benefits over navigable waterways. The construction uses a balanced cantilever method proceeding away from the towers until the spans can be closed.")],
          ["cable_stayed"], ["deck_segment", "stay_cable"], "Exploded cable-stayed model: the deck segments return outward from the towers"),
    claim("CLM_773", "The stay cables also compress the edge girders along their length; the compression adds up toward the towers.",
          [(F, "2.5 Cable-Stayed", "The compressive forces are additive from the end of the longest cables toward the towers. In most cases the edge girder design is not controlled by bending but by the compressive forces imparted by the stay cables")],
          ["cable_stayed"], ["deck_segment"], "Conceptual compression arrows along the deck toward a tower (no magnitudes)"),
    claim("CLM_774", "In the United States, cable-stayed bridges become very cost competitive for main spans over 750 feet, and almost all bridges with main spans over 1,000 feet built since 1980 have been cable-stayed.",
          [(F, "3.0 Economics", "In the U.S., cable-stayed bridges become very cost competitive for main span lengths over 750 feet. Almost all bridges with main span lengths in excess of 1000 feet built in the U.S. since 1980 have been cable-stayed structures.")],
          ["cable_stayed"], [], "Long-span economics card (sourced values only)"),
    claim("CLM_775", "Before 1970, suspension bridges were considered the most economical solution for spans over about 1,200 feet; with cable-stayed technology, suspension bridges do not become economical until main spans approach 3,000 feet.",
          [(F, "3.0 Economics", "Prior to 1970, it was generally considered that suspension bridges provided the most economical solution for span lengths in excess of about 1200 feet. With the development of cable-stayed bridge technology, suspension bridges do not become economical until the main span length approaches 3000 feet.")],
          ["suspension", "cable_stayed"], [], "Long-span economics card"),
    claim("CLM_776", "Cable-stayed bridges are more versatile than suspension bridges: they offer more possible configurations, and their towers do not need good rock near the surface.",
          [(F, "3.0 Economics", "They are more versatile than suspension bridges in that they offer more possible configurations and towers can be constructed in less than optimal foundation conditions because having good rock near the surface is not a requirement.")],
          ["cable_stayed", "suspension"], [], "Comparison"),
    claim("CLM_777", "Welded plate girders, a form of beam, are currently the most common type of steel bridge.",
          [(F, "3.0 Economics", "Welded plate girders are currently the most common type of steel bridge.")],
          ["beam"], [], "Conclusion: not a story of progress", assumptions="A 2012 FHWA statement about steel bridges."),
    # ---- M8.1: the long-span families in the factors, decisions and conclusion chapters ----
    claim("CLM_780", "America's first metal suspension bridges hung from iron chains; chain bridges tended to fail after only a few years, critics felt the design was only as good as its weakest link, and metal cables answered that fear.",
          [(N, "3.5 Suspension", "In 1801, James Finley (1756-1828), a justice of the peace and judge in Fayette County, Pennsylvania, constructed the first metal suspension bridge in the United States"),
           (N, "3.5 Suspension", "Although forty or more chain bridges were built according to Finley\u2019s 1808 patent, they tended to fail after only a few years of use. Some critics felt that the Finley design was only as good as the weakest link in one of the chains. This fear was addressed by the introduction of metal cables.")],
          ["suspension"], ["main_cable"], "Main cables highlighted; NOTE on chains and cables"),
    claim("CLM_781", "Cable-stayed and suspension bridges both rely on high-strength steel cables as major structural elements.",
          [(F, "2.5 Cable-Stayed", "Cable-Stayed bridges rely on high strength steel cables as major structural elements."),
           (F, "2.6 Suspension Bridges", "suspension bridges rely on high-strength cables as major structural elements.")],
          ["suspension", "cable_stayed"], ["main_cable", "stay_cable"], "Main cables highlighted"),
    claim("CLM_782", "A cantilever's superstructure can adjust if a pier or abutment sinks, where a continuous beam may fail; with unstable soil a common problem, this was a significant breakthrough.",
          [(N, "3.7 Cantilevers", "the members did not have the inherent deficiency of the continuous beam or girder developing indiscernible internal stresses and possibly failing should one of the piers or abutments subside. Unstable soil conditions plagued foundation, pier, and abutment design, so the ability of a bridge\u2019s superstructure to adjust should one of the piers or abutments sink, was a significant design breakthrough.")],
          ["cantilever"], ["pier"], "Cantilever model, main piers labelled"),
    claim("CLM_783", "In 1940 the four-month-old Tacoma Narrows suspension bridge collapsed in only moderately high winds; the event led to intense research on wind, and later suspension bridges followed new standards for truss-stiffened spans.",
          [(N, "2.2", "In 1940, the four-month old Tacoma Narrows Bridge over Puget Sound collapsed due to the forces of the wind on the suspension structure. The event led to intense research on the dynamics of the effects of wind in large structures."),
           (N, "2.2", "were based on substantial research that produced new formulae and standards"),
           (F, "2.6 Suspension Bridges", "The structure collapsed due to the harmonic frequency set up during a period of only moderately high winds.")],
          ["suspension"], ["stiffening_truss"], "Stiffening truss highlighted; no collapse is shown",
          assumptions="Narrated as a historical event; the film shows no collapse or destruction."),
    claim("CLM_784", "For steel bridges, welded plate girders are applicable from about 90 feet to over 500 feet.",
          [(F, "3.0 Economics", "Applicable in span lengths from approximately 90 feet to over 500 feet they provide a versatile choice for the designer.")],
          ["beam"], [], "Span-range card (sourced values only)"),
    claim("CLM_785", "Steel trusses are generally not cost-effective below about 450 feet, and the practical upper limit for simple-span trusses is about 750 feet; continuous or cantilever trusses span considerably farther.",
          [(F, "3.0 Economics", "Trusses are generally not cost-effective for span lengths under 450 feet."),
           (F, "3.0 Economics", "The practical upper limit for simple span trusses is approximately 750 feet while continuous trusses begin to be cost-effective when the span length exceeds 550 feet. Continuous or cantilever trusses can span considerably longer distances than simple span trusses.")],
          ["truss", "cantilever"], [], "Span-range card"),
    claim("CLM_786", "Arches have been used for spans from about 200 to 1,800 feet worldwide, and cable-stayed bridges built with main spans from under 200 feet to nearly 3,000 feet.",
          [(F, "3.0 Economics", "Arches have been used for span lengths from approximately 200 feet up to 1800 feet worldwide."),
           (F, "3.0 Economics", "Cable-stayed bridges have been constructed with main span lengths less than 200 feet and extending up to nearly 3000 feet.")],
          ["arch", "cable_stayed"], [], "Span-range card"),
    claim("CLM_787", "Erecting a suspension bridge is specialised: installing the main cables needs expertise very few contractors have, and construction often takes a long time.",
          [(F, "4.5 Suspension Bridges", "Erection of suspension bridges is relatively specialized. The installation of the main suspender cables requires expertise that very few contractors possess."),
           (F, "4.5 Suspension Bridges", "The time to construct a suspension bridge is often relatively long as well.")],
          ["suspension"], ["main_cable", "anchorage"], "Suspension model, anchorages and cables highlighted"),
    claim("CLM_788", "Cable-stayed bridges are becoming more common worldwide, one significant reason being that their erection methods have become better understood.",
          [(F, "4.4 Cable-Stayed Bridges", "Cable-stayed bridges are becoming more common worldwide. One significant reason for this is that the erection methods required for cable-stayed bridges have become better understood over the past 25 years.")],
          ["cable_stayed"], [], "Cable-stayed model"),
    claim("CLM_789", "Roebling's 1855 suspension bridge across the Niagara Gorge carried railway traffic, but railroad executives doubted suspension bridges could bear heavy trains; the bridge needed substantial repairs, was declared inadequate in 1890, and 133 years passed before the next railway suspension bridge.",
          [(N, "3.5 Suspension", "who won the contract to build the second suspension bridge, and the first railroad bridge, across the Niagara Gorge. Completed in 1855"),
           (N, "3.5 Suspension", "railroad company executives were not convinced that suspension bridges were capable of bearing the live loads imposed on them by heavy rail traffic. Their skepticism was not unjustified because the Niagara Bridge needed substantial repair in 1877 and 1880, and was declared inadequate in 1890. It would be 133 years before the next suspension bridge designed for railway traffic was built")],
          ["suspension"], [], "Suspension model with 'Illustrative model, not the Niagara bridge'"),
    claim("CLM_790", "Cantilevers were first used by the railroads; a cantilever is inherently rigid, so heavy locomotives pulling trains are no threat to a properly designed one.",
          [(N, "3.7 Cantilevers", "Cantilevers first were used by the railroads"),
           (N, "3.7 Cantilevers", "Another is that it is inherently rigid so that heavy locomotives pulling trains of cars are no threat to the structure if properly designed.")],
          ["cantilever"], ["cantilever_truss"], "Cantilever model highlighted"),
    claim("CLM_791", "In 1877 the world's longest cantilever was built for the Cincinnati Southern Railroad over the 275-foot-deep Kentucky River gorge at Dixville.",
          [(N, "3.7 Cantilevers", "In 1877, American engineer C. Shaler Smith, Baltimore Bridge Company, and Louis Frederic Gustav Bouscaren, chief railroad engineer, built the world\u2019s longest cantilever for the Cincinnati Southern Railroad over the 275-foot deep Kentucky River gorge at Dixville.")],
          ["cantilever"], [], "Cantilever model with 'Illustrative model, not the Kentucky River bridge'"),
    claim("CLM_792", "The Golden Gate Bridge opened in San Francisco in May 1937 and stood as the world's longest span for twenty-seven years.",
          [(N, "2.2", "In May 1937, the Golden Gate Bridge opened in San Francisco. For twenty-seven years, the bridge stood as the world\u2019s longest span")],
          ["suspension"], [], "HAER photograph of the Golden Gate Bridge"),
    claim("CLM_793", "The Penobscot Narrows Bridge in Maine is a cable-stayed bridge with a 1,161-foot main span, supported by two 430-foot concrete pylons with 40 stay cables each; it was opened in December 2006, 42 months from conception, and its west pylon has a public observatory at the top.",
          [("SRC_FHWA_PENOBSCOT", "Chapter 3, The test bridge", "The Penobscot Narrows Bridge is a 2,120 ft (646 m) long cable-stayed bridge that carries U.S. Route 1 over the Penobscot River connecting Verona Island to Prospect in Maine."),
           ("SRC_FHWA_PENOBSCOT", "Chapter 3, The test bridge", "has a main span of 1,161 ft (354 m)"),
           ("SRC_FHWA_PENOBSCOT", "Chapter 3, The test bridge", "The bridge spans are supported by two 430-ft (131.1-m) tall concrete pylons, each containing 40 stay cables."),
           ("SRC_FHWA_PENOBSCOT", "Chapter 3, The test bridge", "spanned a mere 42 months from conception to completion; construction was started in 2004 and the bridge was opened to traffic on December 30, 2006."),
           ("SRC_FHWA_PENOBSCOT", "Chapter 3, The test bridge", "A unique feature of the west pylon, Pier 1, is the public observatory, accessible by elevator, located at its top.")],
          ["cable_stayed"], [], "Cable-stayed model with 'Illustrative model, not the Penobscot Narrows Bridge'"),
    claim("CLM_747", "Stone arch bridges were popular where good stone was available locally, yet some states with abundant stone built few of them.",
          [(N, "3.2.1 Stone Arch", "stone arch bridges were popular in Kansas for many reasons, a major one being that the stone was often available locally."),
           (N, "3.2.1 Stone Arch", "despite an abundance of stone in various forms through the state and an indigenous tradition of masonry construction, stone bridges were never built in abundance in Michigan.")],
          ["arch"], [], "Materials/site panel"),
]

# The owner's editorial decision (a human record, never written by this script) is applied on top.
approval_path = Path(sys.argv[1]).parent / "editorial_approval.json"
approval = json.loads(approval_path.read_text()) if approval_path.is_file() else None
revision = json.loads((Path(__file__).resolve().parents[1] / "script/narration.template.json").read_text())["revision"]["version"]
if approval and approval.get("narration_revision") != revision:
    # documented invalidation: an approval covers the narration revision it was given for
    print(f"editorial approval of narration {approval.get('narration_revision')} does not cover {revision}: NOT applied")
    approval = None
if approval:
    import hashlib
    texts_sha = approval.get("claims_text_sha256", {})
    for c in CLAIMS:
        if c["id"] in approval["claims"] and texts_sha.get(c["id"], hashlib.sha256(c["text"].encode()).hexdigest()) \
                != hashlib.sha256(c["text"].encode()).hexdigest():
            print(f"{c['id']}: claim text changed since the approval; approval NOT applied")
            continue
        if c["id"] in approval["claims"]:
            c["review_status"] = "EDITORIALLY_APPROVED"
            c["caveat"] = (f"Editorially approved {approval['approved_on']} for narration "
                           f"{approval['narration_revision']}; illustrative models, conceptual forces only.")
            c["editorial_approval"] = {k: approval[k] for k in ("approved_by", "approved_on", "narration_revision", "basis")}

out = {"note": "Evidence registry for 'Why Bridges Don't All Look the Same'. CLM_701-714 restate the M6 claims (verified 2026-10-28) under new ids; CLM_720-747 were added in M7, CLM_750-777 (long-span families) in M8. Every excerpt was matched verbatim against the downloaded source text (research/build_sources.py). "
               + (f"{len(approval['claims'])} narrated claims editorially approved by {approval['approved_by']} on {approval['approved_on']} (research/editorial_approval.json)."
                  if approval else "Nothing here is editorially approved."),
       "sources": SOURCES, "claims": CLAIMS}
Path(sys.argv[1]).write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
print(len(SOURCES), "sources", len(CLAIMS), "claims")
