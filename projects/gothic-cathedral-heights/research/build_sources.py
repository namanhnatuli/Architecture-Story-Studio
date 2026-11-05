"""Build research/sources.json (python3 research/build_sources.py research/sources.json): every excerpt is
verified verbatim (whitespace-normalised) against the downloaded source text in research/snapshots/
(git-ignored; files, URLs and SHA256 in research/source_snapshots.json). French excerpts are quoted in
French; the claim text gives the English meaning the film uses."""
import hashlib
import json
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
S = Path(os.environ.get("GOTHIC_SOURCE_SNAPSHOTS", HERE / "snapshots"))
TEXT = {
    "SRC_MIT_BLOCK_2005": "pdf/block_SMArchS_2005.txt",
    "SRC_ISSMGE_BEAUVAIS_1": "pdf/beauvais_issmge_part1.txt",
    "SRC_ISSMGE_BEAUVAIS_2": "pdf/beauvais_issmge_part2.txt",
    "SRC_CU_AMIENS_REVOLUTION": "web/amiens/p_gothic-structural-revolution.txt",
    "SRC_CU_AMIENS_POINTED_ARCH": "web/amiens/p_pointed-arch.txt",
    "SRC_CU_AMIENS_GEOMETRY": "web/amiens/p_dynamic-geometry.txt",
    "SRC_CU_AMIENS_CARPENTERS": "web/amiens/detail_work-carpenters.txt",
    "SRC_CU_AMIENS_MASONS": "web/amiens/p_detail_work-masons.txt",
    "SRC_CU_AMIENS_UPPER_NAVE": "web/amiens/detail_amiens-cathedral-0.txt",
    "SRC_CU_AMIENS_TRIFORIUM_CHAIN": "web/amiens/p_node_3012.txt",
    "SRC_CU_AMIENS_ETEXT_1": "web/amiens/node_3418.txt",
    "SRC_CU_AMIENS_ETEXT_4": "web/amiens/etext_4.txt",
    "SRC_CU_AMIENS_ETEXT_11": "web/amiens/etext_11.txt",
    "SRC_CU_AMIENS_ETEXT_17": "web/amiens/etext_17.txt",
    "SRC_CU_AMIENS_ETEXT_18": "web/amiens/etext_18.txt",
    "SRC_CU_SAINT_DENIS": "web/columbia_stdenis.txt",
    "SRC_BNF_ARC_BRISE": "web/bnf/arc_brise.txt",
    "SRC_BNF_ARCS_BOUTANTS": "web/bnf/arcs_boutants.txt",
    "SRC_BNF_SAINT_DENIS": "web/bnf/saint_denis.txt",
    "SRC_FM_TIMBERT_SAINT_DENIS": "web/bnf/france_memoire_stdenis.txt",
    "SRC_ABC_HISTORY": "web/beauvais/history_en.txt",
    "SRC_ABC_THRUST": "web/beauvais/from-romanesque-to-gothic-art-the-thrust-revolution.txt",
    "SRC_ABC_FRENCH_ART": "web/beauvais/french-art-known-as-gothic.txt",
    "SRC_ABC_DESCRIPTION": "web/beauvais/description-of-the-cathedral.txt",
}
texts = {k: (S / v).read_text(encoding="utf-8") for k, v in TEXT.items()}


def _pat(word):
    out = ""
    for ch in word:
        if ch in "'’‘":
            out += "['’‘]"
        elif ch in '"“”':
            out += '["“”]'
        else:
            out += re.escape(ch)
    return out


def find(src, excerpt):
    """The source's own wording of the excerpt, whitespace-normalised (SystemExit when absent)."""
    m = re.search(r"\s+".join(_pat(w) for w in excerpt.split()), texts[src])
    if not m:
        raise SystemExit(f"NOT FOUND in {src}: {excerpt[:80]}")
    return re.sub(r"\s+", " ", m.group(0))


CU = "Columbia University Media Center for Art History, 'Life of a Cathedral: Notre-Dame of Amiens' (Stephen Murray et al.)"
CU_URL = "https://projects.mcah.columbia.edu/amiens-arthum/"
HTML = "HTML downloaded 2026-11-05; text extracted (scripts/styles and tags stripped, entities unescaped, whitespace collapsed); every excerpt matched verbatim."
ABC = ("Association Beauvais Cathédrale (ABC), the cathedral's heritage association; a secondary, non-peer-reviewed source "
       "that cites Stephen Murray and French reference works. Used with confidence 'medium' and, where it gives figures, "
       "beside the other sources.")


def cu(sid, title, path, kind="university teaching website (Columbia University)"):
    return {"id": sid, "title": f"{title} ({CU})", "publisher": "Columbia University Media Center for Art History",
            "kind": kind, "edition": "web project, copyright 2017", "url": CU_URL + path, "accessed": "2026-11-05",
            "verification": HTML, "license": "Quoted for research/citation only."}


SOURCES = [
    {"id": "SRC_MIT_BLOCK_2005", "title": "Equilibrium Systems: Studies in Masonry Structure (S.M.Arch.S. thesis), Philippe Block",
     "publisher": "Massachusetts Institute of Technology, Department of Architecture (supervisor: John A. Ochsendorf)",
     "kind": "university thesis (structural engineering of historic masonry)", "edition": "June 2005",
     "url": "http://web.mit.edu/masonry/papers/block_SMArchS_2005.pdf", "accessed": "2026-11-05",
     "verification": "PDF downloaded 2026-11-05 (1.2 MB) from the MIT Masonry Research Group publications page; text extracted with pdftotext (reading order); every excerpt matched verbatim (whitespace-normalised).",
     "notes": "Summarises Jacques Heyman's limit-analysis view of masonry (The Stone Skeleton, 1995); the film attributes these ideas to engineers who study historic masonry.",
     "license": "Quoted for research/citation only."},
    {"id": "SRC_ISSMGE_BEAUVAIS_1", "title": "Cathédrale de Beauvais : les accidents structurels des XIIIe et XVIe siècles eurent-ils une origine géotechnique ? Partie 1 : contexte historique et naturel (J.-D. Vernhes, P. Renault, Y. Zotna)",
     "publisher": "Proceedings of the XVIII European Conference on Soil Mechanics and Geotechnical Engineering (ECSMGE 2024, Lisbon); ISSMGE Online Library",
     "kind": "peer-reviewed conference paper (open access, CC BY-NC-ND 4.0); authors from UniLaSalle Beauvais, BMI and the regional historic-monuments conservation (Amiens)",
     "edition": "2024", "url": "https://www.issmge.org/uploads/publications/51/126/1039_C_cathdrale_de_beauvais_les_accidents_structurels_de.pdf",
     "accessed": "2026-11-05",
     "verification": "PDF downloaded 2026-11-05; text extracted with pdftotext (reading order, not -layout: the paper has two columns); every excerpt matched verbatim. French text; the claim gives the English meaning.",
     "license": "CC BY-NC-ND 4.0; quoted for research/citation."},
    {"id": "SRC_ISSMGE_BEAUVAIS_2", "title": "Cathédrale de Beauvais : les accidents structurels des XIIIe et XVIe siècles eurent-ils une origine géotechnique ? Partie 2 : accidents structurels et rôle de la géotechnique (J.-D. Vernhes, P. Renault, Y. Zotna)",
     "publisher": "Proceedings of the XVIII ECSMGE 2024 (DOI 10.1201/9781003431749-378); ISSMGE Online Library",
     "kind": "peer-reviewed conference paper (open access, CC BY-NC-ND 4.0)", "edition": "2024",
     "url": "https://www.issmge.org/uploads/publications/51/126/1040_C_cathdrale_de_beauvais_les_accidents_structurels_de.pdf",
     "accessed": "2026-11-05",
     "verification": "PDF downloaded 2026-11-05; text extracted with pdftotext (reading order); every excerpt matched verbatim. French text with an English abstract.",
     "license": "CC BY-NC-ND 4.0; quoted for research/citation."},
    cu("SRC_CU_AMIENS_REVOLUTION", "The Gothic Structural Revolution", "gothic-structural-revolution.html"),
    cu("SRC_CU_AMIENS_POINTED_ARCH", "The Pointed Arch", "pointed-arch.html"),
    cu("SRC_CU_AMIENS_GEOMETRY", "Dynamic Geometry", "dynamic-geometry.html"),
    cu("SRC_CU_AMIENS_CARPENTERS", "The Work of the Carpenters", "detail/work-carpenters.html"),
    cu("SRC_CU_AMIENS_MASONS", "The Work of the Masons, First Phase c.1220-25", "detail/work-masons.html"),
    cu("SRC_CU_AMIENS_UPPER_NAVE", "Amiens Cathedral, upper nave, north (image essay)", "detail/amiens-cathedral-0.html"),
    cu("SRC_CU_AMIENS_TRIFORIUM_CHAIN", "Amiens Cathedral (Ascent): triforium passage and iron chain", "node/3012.html"),
    cu("SRC_CU_AMIENS_ETEXT_1", "E-Text 1: Introduction to Amiens Cathedral, by Stephen Murray", "node/3418.html"),
    cu("SRC_CU_AMIENS_ETEXT_4", "E-Text 4: Entering the Cathedral, by Stephen Murray", "e-text-4.html"),
    cu("SRC_CU_AMIENS_ETEXT_11", "E-Text 11: Presence of the Clergy, by Stephen Murray", "e-text-11.html"),
    cu("SRC_CU_AMIENS_ETEXT_17", "E-Text 17: Forces in the Cathedral, by Stephen Murray", "e-text-17.html"),
    cu("SRC_CU_AMIENS_ETEXT_18", "E-Text 18: Gothic as One of the Three Great Architectural Revolutions, by Stephen Murray", "e-text-18.html"),
    {"id": "SRC_CU_SAINT_DENIS", "title": "Saint-Denis (Paris and its monuments teaching map)",
     "publisher": "Columbia University (CCNMTL)", "kind": "university teaching website",
     "edition": "web page, undated", "url": "https://ccnmtl.columbia.edu/projects/paris_map/buildings/stdenis/1300.html",
     "accessed": "2026-11-05", "verification": HTML, "license": "Quoted for research/citation only."},
    {"id": "SRC_BNF_ARC_BRISE", "title": "Arc brisé et voûte sur croisée d'ogive (Passerelles, dossier 'La cathédrale Notre-Dame de Chartres')",
     "publisher": "Bibliothèque nationale de France, BnF Essentiels / Passerelles", "kind": "national library educational resource",
     "edition": "web page", "url": "https://passerelles.essentiels.bnf.fr/fr/article/8fc27d60-6dd7-4cbd-88c3-8d8a50988db4-arc-brise-et-voute-sur-croisee-ogive",
     "accessed": "2026-11-05", "verification": HTML + " French text; the claim gives the English meaning.", "license": "Quoted for research/citation only."},
    {"id": "SRC_BNF_ARCS_BOUTANTS", "title": "Les arcs-boutants (Passerelles, dossier 'La cathédrale Notre-Dame de Chartres')",
     "publisher": "Bibliothèque nationale de France, BnF Essentiels / Passerelles", "kind": "national library educational resource",
     "edition": "web page", "url": "https://passerelles.essentiels.bnf.fr/fr/article/6e7cfc7d-da13-4d81-bb7c-c85c1698aa76-arcs-boutants",
     "accessed": "2026-11-05", "verification": HTML + " French text; the claim gives the English meaning.", "license": "Quoted for research/citation only."},
    {"id": "SRC_BNF_SAINT_DENIS", "title": "La naissance du style gothique à Saint-Denis (Passerelles)",
     "publisher": "Bibliothèque nationale de France, BnF Essentiels / Passerelles", "kind": "national library educational resource",
     "edition": "web page", "url": "https://passerelles.essentiels.bnf.fr/fr/chronologie/construction/55e1a07f-e1e6-47e3-a690-ef8c003c9159-basilique-saint-denis/article/3038d0ed-badc-47e6-a520-5c8b6caeeca8-naissance-style-gothique-saint-denis",
     "accessed": "2026-11-05", "verification": HTML + " French text.", "license": "Quoted for research/citation only."},
    {"id": "SRC_FM_TIMBERT_SAINT_DENIS", "title": "L'abbatiale de Saint-Denis et les débuts de l'architecture gothique, by Arnaud Timbert (professor of medieval art history, Université de Picardie Jules Verne)",
     "publisher": "France Mémoire", "kind": "commemorations programme article by a university art historian",
     "edition": "web page", "url": "https://www.france-memoire.fr/labbatiale-de-saint-denis-et-les-debuts-de-larchitecture-gothique/",
     "accessed": "2026-11-05", "verification": HTML + " French text.", "license": "Quoted for research/citation only."},
    {"id": "SRC_ABC_HISTORY", "title": "History of Beauvais Cathedral", "publisher": "Association Beauvais Cathédrale (cathedrale-beauvais.fr)",
     "kind": "heritage association web page", "edition": "web page, copyright 2026",
     "url": "https://cathedrale-beauvais.fr/en/history-of-beauvais-cathedral/", "accessed": "2026-11-05",
     "verification": HTML, "notes": ABC, "license": "Quoted for research/citation only."},
    {"id": "SRC_ABC_THRUST", "title": "From Romanesque to Gothic art: the thrust revolution", "publisher": "Association Beauvais Cathédrale (cathedrale-beauvais.fr)",
     "kind": "heritage association web page (cites BnF Essentiels, Larousse, France Mémoire)", "edition": "web page, consulted sources dated 2026",
     "url": "https://cathedrale-beauvais.fr/en/from-romanesque-to-gothic-art-the-thrust-revolution/", "accessed": "2026-11-05",
     "verification": HTML, "notes": ABC, "license": "Quoted for research/citation only."},
    {"id": "SRC_ABC_FRENCH_ART", "title": "French art, known as 'Gothic', in Beauvais", "publisher": "Association Beauvais Cathédrale (cathedrale-beauvais.fr)",
     "kind": "heritage association web page", "edition": "web page",
     "url": "https://cathedrale-beauvais.fr/en/french-art-known-as-gothic/", "accessed": "2026-11-05",
     "verification": HTML, "notes": ABC, "license": "Quoted for research/citation only."},
    {"id": "SRC_ABC_DESCRIPTION", "title": "Description of the cathedral", "publisher": "Association Beauvais Cathédrale (cathedrale-beauvais.fr)",
     "kind": "heritage association web page", "edition": "web page",
     "url": "https://cathedrale-beauvais.fr/en/description-of-the-cathedral/", "accessed": "2026-11-05",
     "verification": HTML, "notes": ABC, "license": "Quoted for research/citation only."},
]


def claim(cid, text, evidence, applies, comps, visual, assumptions="", scope=None, confidence="high"):
    ev = [{"source_id": s, "locator": loc, "excerpt": find(s, ex)} for s, loc, ex in evidence]
    return {"id": cid, "text": text, "source_ids": sorted({e["source_id"] for e in ev}), "review_status": "SOURCE_VERIFIED",
            "confidence": confidence, "evidence": ev, "assumptions": assumptions or "None beyond the quoted wording.",
            "applies_to": applies, "components": comps, "intended_visual": visual,
            "scope": scope or "qualitative; illustrative models; no forces, stresses, loads or safety factors beyond quoted facts",
            "caveat": "Not editorially approved."}


B, I1, I2 = "SRC_MIT_BLOCK_2005", "SRC_ISSMGE_BEAUVAIS_1", "SRC_ISSMGE_BEAUVAIS_2"
AT, AH = "SRC_ABC_THRUST", "SRC_ABC_HISTORY"
CLAIMS = [
    # ---- the cathedrals and their heights
    claim("CLM_101", "Work on the Gothic cathedral of Amiens began in 1220, after a disastrous fire; its main roof was not finished until about 1310.",
          [("SRC_CU_AMIENS_ETEXT_1", "E-Text 1, paragraph 2", "beginning in 1220 with the start of work on a new cathedral after a disastrous fire"),
           ("SRC_CU_AMIENS_MASONS", "First Phase, c.1220-25", "An inscription on the south transept façade records that the foundation stone was laid in 1220"),
           ("SRC_CU_AMIENS_ETEXT_1", "E-Text 1, paragraph 2", "The main roof was not finished until c.1310.")],
          ["amiens"], [], "Timeline band 1220-1310"),
    claim("CLM_102", "The high vault of Amiens Cathedral rises more than 42 metres (Columbia's Amiens project gives 43.3 m); Beauvais is a few metres higher.",
          [("SRC_CU_AMIENS_UPPER_NAVE", "Amiens Cathedral, upper nave, north", "Amiens at 43.3 meters is a little lower than Beauvais at 46m."),
           (AH, "Around 1260, the choir is completed", "Its vault rises to nearly 47 m, 4 m higher than Amiens.")],
          ["amiens", "beauvais"], ["high_vault"], "Height comparison card (sourced values only)",
          assumptions="Published heights differ: Columbia gives Amiens 43.3 m and Beauvais 46 m; the Beauvais association gives Beauvais nearly 47 m and 4 m more than Amiens. The film says only 'more than 42 metres' for Amiens, which all of these support.",
          confidence="medium"),
    claim("CLM_103", "Beauvais Cathedral has the highest vaults built in the Middle Ages; it suffered two famous structural accidents, in the choir in 1284 and at the transept crossing in 1573.",
          [(I1, "Abstract (English)", "Saint Peter’s cathedral in Beauvais (France) has the highest vaults ever built during the Middle Ages. It was affected by two famous structural accidents, in the choir in 1284, and later at the transept crossing, in 1573.")],
          ["beauvais"], ["high_vault"], "Beauvais section, height card"),
    claim("CLM_104", "The choir vault of Beauvais rises nearly 47 metres; published figures differ (46 m, 46.7 m, nearly 47 m, above 48 m).",
          [(AH, "Around 1260, the choir is completed", "Its vault rises to nearly 47 m, 4 m higher than Amiens. It is the tallest Gothic stone vault in the world."),
           ("SRC_ABC_DESCRIPTION", "The choir", "The choir has the tallest vault of any Gothic choir: 46.7 m."),
           ("SRC_ABC_FRENCH_ART", "The 13th century", "Its choir vaults rise above 48 metres"),
           ("SRC_CU_AMIENS_UPPER_NAVE", "Amiens Cathedral, upper nave, north", "Amiens at 43.3 meters is a little lower than Beauvais at 46m.")],
          ["beauvais"], ["high_vault"], "Height card with the note 'published figures differ'",
          assumptions="The figures disagree, even within one association's pages (nearly 47 m, 46.7 m, above 48 m; Columbia: 46 m). The narration says 'nearly forty-seven metres' and the card notes that published figures range from about 46 to 48 m.",
          confidence="medium"),
    claim("CLM_105", "Gothic architecture first appeared in France in the 1140s; Beauvais marks its high point.",
          [(I1, "1 Introduction", "Elle marque l’apogée de ce style architectural qui a vu le jour en France dans les années 1140.")],
          ["beauvais"], [], "Timeline", assumptions="'Elle' is Beauvais Cathedral (the preceding sentence)."),
    claim("CLM_106", "The eastern arm of a cathedral is commonly called the choir; the long body of the building is crossed by a cross-arm, the transept, and the piers where they meet are the crossing piers.",
          [("SRC_CU_AMIENS_ETEXT_11", "E-Text 11", "The eastern arm of the cathedral is commonly called the choir"),
           ("SRC_CU_AMIENS_ETEXT_4", "E-Text 4", "the long, boat-like body of the cathedral is intersected by a cross-arm or transept")],
          ["all"], ["choir", "transept"], "Terms named in the narration, shown on a plan card",
          assumptions="E-Text 11 adds that the term is 'something of a misnomer' because the choir proper is where the clergy sat; the film uses the common meaning. 'Crossing piers' is the term used in CLM_190."),
    # ---- how masonry stands (MIT, after Heyman)
    claim("CLM_110", "Medieval master builders used geometrical rules developed through centuries of trial and error, scaling up proven proportions for larger elements; they had no knowledge of material properties or allowable stresses, yet many of their buildings still stand.",
          [(B, "1.1 Introduction, p. 9", "The master builders of the Middle Ages were able to use geometrical rules, developed through centuries of trial and error, to build structural elements by scaling up the same proportions for new larger elements [Huerta 2004]. In those days, there was no knowledge of material properties or allowable stresses."),
           (B, "1.1 Introduction, p. 9", "Yet, many of these architectural marvels are still standing in a state of equilibrium.")],
          ["all"], [], "Geometry card: one proportion scaled up"),
    claim("CLM_111", "Engineers analysing historic masonry assume it has no tensile strength; stone has little or no tensile capacity, so a masonry structure collapses if it cannot contain a line of thrust in compression.",
          [(B, "1.1 Introduction, p. 9", "masonry has no tensile strength; it can resist infinite compression; and no sliding will occur within the masonry."),
           (B, "3.2, p. 19", "Stone has no or very little tensile capacity, so, the structure would collapse if it cannot contain a thrust line in compression.")],
          ["all"], [], "2D diagram: an arch, squeeze (compression) vs pull (tension)",
          assumptions="These are the analysis assumptions of limit analysis (Heyman), stated as such: 'infinite compression' is not narrated."),
    claim("CLM_112", "Masonry structures usually fail through instability rather than lack of material strength; stresses are typically only a fraction of the stone's crushing capacity, and unlike problems in elasticity, stability problems can be scaled.",
          [(B, "1.1 Introduction, p. 9", "In most cases, masonry structures fail due to instability rather than a lack of material strength [Heyman 1995]. Stresses in masonry structures are typically only a fraction of the crushing capacity of the stone. Therefore, rigid block models with the same proportions as the structures are good models to understand their stability. Unlike problems in elasticity, stability problems can be scaled.")],
          ["all"], [], "Small model and large model with the same proportions"),
    claim("CLM_113", "The line of thrust is the path of the compressive force through the stone; a masonry structure in pure compression is in equilibrium only if a line of thrust can be found that lies entirely within the masonry; if no such line can be found, it collapses.",
          [(B, "1.1 Introduction, p. 9", "This is a theoretical line, which represents the path of the resultants of the compressive forces through the stone structure. For a pure compression structure to be in equilibrium with the applied loads there must be a line of thrust that lies entirely within the section."),
           (B, "3.2, p. 19", "if a line that fits within the arch’s profile for the given loading can no longer be found, then the arch will collapse.")],
          ["all"], ["arch_ring"], "2D diagram: a conceptual thrust line inside an arch (no magnitudes)"),
    claim("CLM_114", "In 1675 Robert Hooke wrote that the rigid arch stands as a hanging chain hangs, inverted ('As hangs the flexible line, so but inverted will stand the rigid arch').",
          [(B, "Preface, p. 7", "written by Robert Hooke (1635-1703) in 1675"),
           (B, "Preface, footnote 1", "As hangs the flexible line, so but inverted will stand the rigid arch, translation by Heyman [1995].")],
          ["all"], [], "2D diagram: hanging chain flipped into an arch"),
    # ---- thrust and the Romanesque answer
    claim("CLM_120", "A vault does not only press down: it also pushes outward, like a bow being bent; this outward push is called thrust.",
          [(AT, "The Romanesque problem", "A vault, whatever its shape, does not simply press downward: it also pushes outward, like a bow being bent."),
           (AT, "What is “thrust”?", "In structural mechanics, thrust is the horizontal component of the force exerted by a vault or an arch on its support.")],
          ["all"], ["vault"], "Romanesque section: outward push at the springing", confidence="medium"),
    claim("CLM_121", "Medieval builders knew about thrust: an Amiens document calls the thrust in the arcade arches 'boutture'.",
          [("SRC_CU_AMIENS_POINTED_ARCH", "The Pointed Arch", "A contemporary document reveals that the builders were well aware of the existence of \"thrust\" in the arcade arches--it is termed boutture.")],
          ["amiens"], [], "NOTE on the thrust arrows",
          assumptions="'Contemporary' refers to the late-medieval Amiens context of the paragraph (the 1497 crisis); the film says only that builders knew about thrust."),
    claim("CLM_122", "Romanesque builders vaulted their churches in heavy masonry; its considerable outward thrust forced them to thicken the supports and outer walls, stiffened by buttresses, so windows stayed small and interiors were dark.",
          [("SRC_CU_AMIENS_REVOLUTION", "Antithesis (Romanesque)", "Since the heavy masonry of the vaulting creates considerable outward thrust it has been necessary to thicken the main supports (no longer columns but compound piers) and outer walls which are stiffened by shallow buttresses. Windows are small. The interior is now dark"),
           (AT, "The Romanesque problem", "In Romanesque architecture, this oblique thrust is spread along the entire length of the wall, which must therefore be thick and pierced with only small openings to remain stable.")],
          ["romanesque"], ["wall", "barrel_vault", "buttress"], "Romanesque section: thick wall, barrel vault, small windows"),
    claim("CLM_123", "Gothic builders stopped fighting the thrust of vaults with wall thickness and learned to channel it, through the pointed arch, the ribbed vault and the flying buttress.",
          [(AT, "Introduction", "master builders stopped fighting the thrust of vaults with sheer wall thickness. They learned to channel it instead. Three technical innovations made this revolution possible: the pointed arch, the ribbed vault, and the flying buttress."),
           ("SRC_CU_AMIENS_ETEXT_18", "E-Text 18", "This revolution is made possible through the use of pointed arches and lightweight rib vaults, but above all by the creation of rigid peripheral supports ( culées) from which flying buttresses can be launched to support the high vaults.")],
          ["gothic"], [], "Three tools card"),
    # ---- the pointed arch
    claim("CLM_130", "A pointed arch is formed by two arcs of a circle meeting at a point; it exerts less sideways thrust than a round arch, which allows it to be raised much higher.",
          [(AT, "Innovation No. 1", "the pointed arch is formed by two arcs of a circle meeting at a point."),
           ("SRC_BNF_ARC_BRISE", "Arc brisé et voûte sur croisée d’ogive", "Il a pour avantage d’exercer des poussées latérales réduites, ce qui permet de l’élever nettement plus haut."),
           ("SRC_CU_AMIENS_REVOLUTION", "Synthesis (Gothic)", "The pointed arch. Appropriated from Islamic sources and applied to reduce outward thrust.")],
          ["gothic"], ["pointed_arch"], "Round vs pointed arch, same span (qualitative arrows, no magnitudes)"),
    claim("CLM_131", "The pointed arch was not born with Gothic: examples appear in Burgundian Romanesque architecture, at the rebuilding of the abbey of Cluny around 1088, and Columbia's Amiens project says it was appropriated from Islamic sources; at Saint-Denis it was used systematically with the other Gothic innovations.",
          [(AT, "Innovation No. 1", "The pointed arch was not born with Gothic art: examples already appear in Burgundian Romanesque architecture, notably on the rebuilding site of the abbey of Cluny (Cluny III), around 1088. It was at the abbey of Saint-Denis, under Abbot Suger between 1130 and 1144, that it was used systematically and combined with the other Gothic innovations."),
           ("SRC_CU_AMIENS_REVOLUTION", "Synthesis (Gothic)", "The pointed arch. Appropriated from Islamic sources")],
          ["gothic"], ["pointed_arch"], "Timeline note", confidence="medium"),
    claim("CLM_132", "Unlike a round arch, a pointed arch can span bays of different widths while keeping the same height at its crown, a valuable asset for keeping complex vaults regular.",
          [(AT, "Innovation No. 1", "unlike the round arch, the pointed arch allows bays of different widths to be spanned while keeping the same keystone height — a valuable asset for regularising complex vaults.")],
          ["gothic"], ["pointed_arch"], "2D diagram: narrow and wide pointed arches with level crowns; the round arches cannot",
          assumptions="Geometric property also shown on the card: a semicircular arch's rise is half its span.", confidence="medium"),
    claim("CLM_133", "Columbia's Amiens project says that, following Hooke's hanging-chain principle, the pointed arch is closer to a catenary than the round arch and so is more efficient; a round arch pushes outward at its base and, if its supports spread, sags and cracks.",
          [("SRC_CU_AMIENS_POINTED_ARCH", "The Pointed Arch", "the line of force in an arch will follow the line of a catenary arch--like a hanging chain"),
           ("SRC_CU_AMIENS_POINTED_ARCH", "The Pointed Arch", "Since the pointed arch comes closer to the round arch to a catenary curve it is more efficient."),
           ("SRC_CU_AMIENS_POINTED_ARCH", "The Pointed Arch", "the line of force in the masonry of a rounded arch: it will want to push outwards as \"thrust\" at the base of the arch. As the supports open outward the arch begins to sag, cracking on the inside surface at its crown and on the exterior surface at its haunch.")],
          ["gothic"], ["pointed_arch"], "Hanging chain card",
          assumptions="The first sentence is garbled on the page; it is read as 'closer than the round arch to a catenary curve'. The page calls Hooke an 18th-century physicist; Hooke wrote in 1675 (CLM_114), so the film takes the date from the MIT source.",
          confidence="medium"),
    # ---- the rib vault
    claim("CLM_140", "In a ribbed vault two pointed arches cross diagonally over each bay and gather the vault's load onto four points, the corner piers: the vault's thrust goes to piers rather than to walls.",
          [(AT, "Innovation No. 2", "two pointed arches cross diagonally above each bay, gathering the vault’s load onto four precise points — the corner piers."),
           ("SRC_BNF_SAINT_DENIS", "Une nouvelle conception de la spiritualité", "Elle dirige les poussées de la voûte sur des piliers, et non plus sur des murs")],
          ["gothic"], ["rib", "pier", "vault_web"], "Rib vault plan: diagonal ribs to four piers"),
    claim("CLM_141", "How quadripartite vaults stand has been debated for centuries; engineers following Jacques Heyman assume the main ribs bring the forces down to the buttresses, with the web between them acting as a series of parallel arches.",
          [(B, "3.6 Gothic quadripartite vault, p. 23", "The structural behavior of the quadripartite vault has been the focus of debate for centuries."),
           (B, "3.6 Gothic quadripartite vault, p. 23", "We use the assumptions made by Heyman that the main ribs bring down the forces to the buttresses and the web is considered to be a collection of parallel arches spanning between the cross ribs")],
          ["gothic"], ["rib", "vault_web"], "Rib vault: web strips as small arches"),
    claim("CLM_142", "Ribbed vaults appear at Durham Cathedral in England as early as 1093, before the Gothic style itself; the rib vault also has Islamic, Roman and Byzantine sources.",
          [(AT, "Innovation No. 2", "The very first ribbed vaults appear as early as 1093 at Durham Cathedral in England — even before the birth of the Gothic style itself."),
           ("SRC_CU_AMIENS_REVOLUTION", "Synthesis (Gothic)", "The ribbed vault. Also from Islamic, Roman and Byzantine sources")],
          ["gothic"], ["rib"], "Timeline note",
          assumptions="The association calls Durham's vaults 'the very first ribbed vaults'; Columbia names earlier Islamic, Roman and Byzantine sources, so the film says only 'as early as 1093' for Durham.",
          confidence="medium"),
    claim("CLM_143", "Because the vault's load is gathered onto piers, the walls between them no longer carry it: they can be thinned and opened with wide windows. It is the combination of the three devices that answers thrust.",
          [(AT, "Innovation No. 2", "Direct consequence: between the piers, the walls no longer carry any load. They can be thinned, hollowed out, and eventually replaced with wide glazed openings."),
           ("SRC_BNF_ARC_BRISE", "La voûte sur croisée d’ogive", "Les murs perdent ainsi leur rôle de soutien, et peuvent être percés de larges ouvertures."),
           (AT, "From load-bearing wall to stone skeleton", "Taken separately, the pointed arch, the ribbed vault and the flying buttress are each only a partial answer to the problem of thrust. Combined, they form a complete system")],
          ["gothic"], ["clerestory_window", "pier"], "Wall between piers turns to glass"),
    # ---- the flying buttress
    claim("CLM_150", "Even reduced, the sideways thrust of the vaults remains a threat to the stability of the whole building, so it still has to be resisted.",
          [("SRC_BNF_ARCS_BOUTANTS", "Les arcs-boutants", "Ces structures sont plus légères mais toujours présentes, car les poussées latérales, même réduites, demeurent une menace pour la stabilité de l’ensemble."),
           (AT, "Innovation No. 3", "The ribbed vault concentrates thrust onto piers, but that thrust still has to be contained somewhere.")],
          ["gothic"], ["flying_buttress"], "Thrust arrow at the top of the pier"),
    claim("CLM_151", "In Gothic buildings, the Romanesque buttresses became flying buttresses: supports set away from the wall and hollowed into arches.",
          [("SRC_BNF_ARCS_BOUTANTS", "Les arcs-boutants", "Pour contrer les poussées exercées sur les murs par les voûtes, les églises romanes les renforcent par des contreforts, renforts de maçonnerie en saillie accolés au mur extérieur."),
           ("SRC_BNF_ARCS_BOUTANTS", "Les arcs-boutants", "Dans les édifices gothiques, les contreforts deviennent des arcs-boutants, comme des contreforts éloignés de la paroi et évidés en arc.")],
          ["gothic", "romanesque"], ["flying_buttress", "buttress"], "Romanesque buttress -> flying buttress"),
    claim("CLM_152", "A flying buttress picks up the thrust where it leaves the vault, carries it across the aisle roof and down to a massive pier buttress, often topped with a pinnacle whose weight helps stabilise the thrust.",
          [(AT, "Innovation No. 3", "this external arch picks up the thrust at the point where it leaves the vault, carries it across the aisle roof, and channels it down to a massive pier buttress, often topped with a pinnacle that weighs it down to better stabilise the thrust.")],
          ["gothic"], ["flying_buttress", "pier_buttress", "pinnacle"], "Gothic section: conceptual thrust path through the flyer (no magnitudes)",
          confidence="medium"),
    claim("CLM_153", "Columbia's Amiens project describes the exterior supports (culées) as if the outer wall had been cut into segments, each turned 90 degrees, to give rigid supports for the flying buttresses that hold up the high vaults.",
          [("SRC_CU_AMIENS_REVOLUTION", "Synthesis (Gothic)", "It is as if the outer wall (labeld F) has been broken into segments, each of which is rotated 90 degrees to provide rigid transverse supports for exposed arches (flying buttresses) which support the high vaults.")],
          ["gothic"], ["pier_buttress", "flying_buttress"], "Wall segments rotate into buttress piers"),
    claim("CLM_154", "The first flying buttresses were used to consolidate Romanesque churches that threatened to collapse; at Chartres they were part of the original plans; at Notre-Dame de Paris the flyers around the east end look almost like a giant external skeleton.",
          [("SRC_BNF_ARCS_BOUTANTS", "Les arcs-boutants", "Les premiers arcs-boutants ont été utilisés pour consolider les églises romanes qui menaçaient de s’effondrer."),
           ("SRC_BNF_ARCS_BOUTANTS", "Les arcs-boutants", "C’est lors de la construction de la cathédrale de Chartres que les arcs-boutants sont intégrés pour la première fois dans les plans d’origine"),
           ("SRC_BNF_ARCS_BOUTANTS", "Les arcs-boutants", "À Notre-Dame de Paris, les immenses arcs-boutants aériens qui soutiennent l’abside évoquent presque un gigantesque squelette externe !"),
           (AT, "Innovation No. 3", "at Notre-Dame de Paris, systematic buttressing was put in place around 1180.")],
          ["gothic"], ["flying_buttress"], "Flyers card / photographs (rights to be cleared)",
          assumptions="The BnF page says Chartres was the first time ('pour la première fois'). The film drops 'first' and says only 'part of the original plans': flying buttresses at Notre-Dame around 1180 are earlier, and whether those were planned from the start is a question the sources here do not settle."),
    claim("CLM_155", "According to France's national library, the slanting timber props that builders used while constructing vaults were made permanent in stone in Gothic architecture.",
          [("SRC_BNF_ARCS_BOUTANTS", "Les arcs-boutants", "Les étais extérieurs obliques en bois utilisés par les maîtres ouvriers dans la construction des voûtes sont ainsi pérennisés et intégrés en pierre dans la structure de l’architecture gothique.")],
          ["gothic"], ["flying_buttress"], "Timber prop -> stone flyer",
          assumptions="An explanation given by the BnF educational page; the film attributes it ('according to France's national library')."),
    claim("CLM_156", "Flying buttresses allowed builders to create tall, slender, light-filled structures; the first had been used about eighty years before Amiens' upper nave (1230s), and builders learned to exploit them to build ever taller cathedrals.",
          [("SRC_CU_AMIENS_UPPER_NAVE", "Amiens Cathedral, upper nave, north", "These are \"flying buttresses\" (arcs boutants) that allowed the builders to create such tall, slender, light-filled stuctures. The first flying buttresses had been deployed some eighty years earlier and builders learned how to exploit them to achieve cathedrals that were ever taller."),
           ("SRC_CU_AMIENS_UPPER_NAVE", "Amiens Cathedral, upper nave, north", "The upper nave was built by Master Thomas de Cormont in the 1230s.")],
          ["gothic", "amiens"], ["flying_buttress"], "Flyers on the model; NOTE 'Illustrative model, not Amiens'"),
    claim("CLM_157", "Flying buttresses also carry away rainwater from the roof; at Beauvais the flyers are double, the upper arch channelling rainwater.",
          [("SRC_BNF_ARCS_BOUTANTS", "Les arcs-boutants", "Les arcs-boutants servent aussi à l’évacuation de l’eau de pluie tombée sur le toit."),
           ("SRC_ABC_FRENCH_ART", "The double flying buttresses", "In Beauvais, unlike in Amiens, the system is double: the lower arch absorbs the vault’s thrust, while the upper arch channels rainwater down to the base of the roof.")],
          ["gothic", "beauvais"], ["flying_buttress"], "NOTE on the flyer", confidence="medium"),
    # ---- light: Saint-Denis and Chartres
    claim("CLM_160", "At the abbey church of Saint-Denis, Abbot Suger built a west front with rib vaults and pointed arches between 1130 and 1140, then a new choir between 1140 and 1144 in which the pointed arch is used throughout, the vaults are all ribbed and monumental stained-glass windows fill the walls.",
          [("SRC_FM_TIMBERT_SAINT_DENIS", "paragraph 2", "Entre 1130 et 1140, l’abbé Suger (1122-1151) choisit de greffer sur la nef carolingienne de son abbatiale un massif de façade* voûté d’ogives* et structuré par des arcs brisés*. Puis, entre 1140 et 1144, il érigea un chevet*"),
           ("SRC_FM_TIMBERT_SAINT_DENIS", "Au-dessus de la crypte", "Ici, l’arc brisé est généralisé (fenêtres, arcs formerets* et doubleaux*), l’emploi de la voûte d’ogives est exclusif, les supports appareillés sont supplantés par des colonnes monolithes, les murs intermédiaires des chapelles sont élidés et, enfin, des vitraux monumentaux dématérialisent l’ensemble.")],
          ["saint_denis"], [], "Saint-Denis choir: photograph (rights to be cleared) or plan diagram"),
    claim("CLM_161", "Columbia's teaching map calls Suger's choir at Saint-Denis, dedicated in 1144, the first fully Gothic structure; for Suger, light was a sign or bridge to the divine.",
          [("SRC_CU_SAINT_DENIS", "Significance and Basic Concepts", "The choir of Abbot Suger was the first fully gothic structure. For Suger light functioned as a sign or bridge to the divine."),
           ("SRC_CU_SAINT_DENIS", "Building Campaigns", "This Choir was built in new, gothic style and dedicated in 1144.")],
          ["saint_denis"], [], "Light through the windows"),
    claim("CLM_162", "Chartres Cathedral keeps about 2,500 square metres of stained glass, most of it original.",
          [("SRC_BNF_ARCS_BOUTANTS", "Notre-Dame de Chartres (image caption)", "La cathédrale Notre-Dame de Chartres est la cathédrale gothique la plus représentative, la plus complète et la mieux conservée avec son dallage orné d’un labyrinthe, plus de 600 sculptures et 2 500 m2 de vitraux pour la plupart d’origine.")],
          ["chartres"], ["clerestory_window"], "Stained-glass card"),
    claim("CLM_163", "Historians disagree on how new Gothic was: Columbia's Amiens project follows Viollet-le-Duc in calling it an entire revolution in the art of building, while the art historian Arnaud Timbert argues that there was no revolution and no Gothic break, but a creative proposal rooted in continuity; Suger's crypt still relies almost entirely on groin vaults and round arches.",
          [("SRC_CU_AMIENS_REVOLUTION", "The Gothic Structural Revolution", "Following Viollet-le-Duc's premise of Gothic understood as \"An Entire Revolution in the Art of Building.\""),
           ("SRC_FM_TIMBERT_SAINT_DENIS", "conclusion", "C’est pourquoi il n’y a pas de « révolution » et, donc, de rupture gothique, mais une proposition créative inscrite dans la permanence."),
           ("SRC_FM_TIMBERT_SAINT_DENIS", "La crypte", "La voûte d’arêtes et l’arc en plein cintre y sont employés de manière quasi exclusive."),
           (I1, "1 Introduction", "Eugène Viollet-le-Duc, connu pour son œuvre de restauration de Notre-Dame de Paris au XIXe siècle")],
          ["gothic", "saint_denis"], [], "Two-voice card: 'revolution' vs 'continuity'"),
    # ---- how they built: geometry, templates, centering, carpenters
    claim("CLM_170", "At Amiens the site was set out by stretching ropes pegged to the ground and forming squares with right-angled corners; templates for piers, windows and vaults were drawn with straight-edge and compass.",
          [("SRC_CU_AMIENS_GEOMETRY", "1. Ease and Security of Construction", "The templates necessary for manufacturing the elements of multiple piers, windows and vaults were designed with straight-edge and compass."),
           ("SRC_CU_AMIENS_GEOMETRY", "1. Ease and Security of Construction", "Plotting the site began with the stretching of ropes pegged to the ground. Spatial control was achieved through the formation of squares whose perfect right-angled corners were achieved through the application of a Pythagorean triangle or through an optical surveying instrument.")],
          ["amiens"], [], "Plan card: ropes, pegs and squares"),
    claim("CLM_171", "The Gothic skeleton relies on lining up the thrust of each arch with the buttress that supports it: there is little room for error.",
          [("SRC_CU_AMIENS_GEOMETRY", "1. Ease and Security of Construction", "The skeletal structure of Gothic relies upon the correct alignment of the thrust of an arch with the support of a buttress--there is little room for error.")],
          ["gothic"], ["flying_buttress", "pier_buttress"], "Thrust path meets the buttress"),
    claim("CLM_172", "Arches were usually drawn full size on the ground and divided into voussoirs; a wooden template was made for each voussoir, and the stones were laid on wooden centering, removed once the mortar had set (at Amiens after a couple of months or so).",
          [("SRC_BNF_ARCS_BOUTANTS", "Des modèles en bois pour les tailleurs de pierre", "La forme des arcs est généralement tracée au sol à l’échelle 1, puis divisée en segments qui correspondent aux voussoirs , pierres qui vont constituer l’arc, surmonté par la \"clé de voûte\". Des gabarits en bois sont préparés aux dimensions de chaque voussoir : ils servent de modèle aux tailleurs de pierre. Les voussoirs sont ensuite disposés sur une armature de cintres en bois que l’on retire une fois le mortier pris."),
           ("SRC_CU_AMIENS_ETEXT_17", "E-Text 17", "All concave surfaces (arches, vaults) were formed over rigid wooden centering : the carefully-cut stones were laid up with a thin layer of mortar, left in place for a period (a couple of months or so) and then the formwork was removed.")],
          ["all"], ["voussoir", "centering"], "Arch assembled on centering, then the centering lowered"),
    claim("CLM_173", "Carpenters built the scaffolding, the wooden formwork for the vaults and the lifting gear, and tied the upper piers with wooden (later iron) ties to stop the arches pushing them over.",
          [("SRC_CU_AMIENS_CARPENTERS", "Working with the masons", "The carpenters built scaffolding to provide access and temporary support; tying the upper piers with wooden (later, iron) ties to prevent them from being pushed over by the arches; wooden formwork for the vaults; lifting gear.")],
          ["all"], ["centering"], "Construction card (no people, no machinery shown)"),
    # ---- Beauvais
    claim("CLM_180", "In 1225 a fire damaged the Romanesque choir of Beauvais; Bishop Milon de Nanteuil decided to rebuild it after the greatest buildings of his time, in the French (Gothic) style.",
          [(I1, "2.1.1 Avant 1225", "En 1225, un incendie endommageait le chœur roman. L’évêque Milon de Nanteuil décida alors de le reconstruire en s’inspirant des plus grandes réalisations de son époque, dans le style français (gothique, alors rayonnant)")],
          ["beauvais"], [], "Beauvais timeline"),
    claim("CLM_181", "In the 1250s, with the arcades and triforium finished, Bishop Guillaume de Grès apparently decided to go beyond the originally planned proportions, adding a few metres (about five) to the upper windows and so to the vaults; the clergy could use the new choir from 1272.",
          [(I1, "2.1.2 1225-1340", "Dans les années 1250, les deux premiers niveaux de construction étant achevés (grandes arcades et triforium), l’évêque Guillaume de Grès décida apparemment pour le troisième et dernier étage de l’édifice de sortir des proportions prévues originellement en ajoutant quelques mètres (de l’ordre de cinq) aux fenêtres hautes et donc aux voûtes. En 1272, le nouveau chœur put être occupé par le clergé")],
          ["beauvais"], ["clerestory_window", "high_vault"], "Section: the upper storey grows by about five metres",
          assumptions="'Apparemment': the paper presents the decision as probable, and the film says 'apparently'."),
    claim("CLM_182", "On 29 November 1284, twelve years after the choir came into use, part of the vaults of the choir's straight bays collapsed; Viollet-le-Duc called it the last limit that the building of the great 13th-century churches could reach; the repairs ended in 1340, and Stephen Murray notes that the choir took longer to repair than to build.",
          [(I1, "2.1.2 1225-1340", "Le 29 novembre 1284, durant cette nouvelle phase de chantier, des voûtains des travées droites du chœur, les plus vulnérables, s’effondrèrent"),
           (I1, "2.1.2 1225-1340", "« la dernière limite à laquelle la construction des grandes églises du XIIIe s. ait pu arriver »"),
           (I1, "2.1.2 1225-1340", "chantier qui s’en suivi s’acheva en 1340. « On mit donc plus de temps à réparer le chœur qu’à le construire » (Murray, 2000)."),
           (I2, "2.1 Cause d’après les sources", "la durée de stabilité de 12 ans des parties hautes")],
          ["beauvais"], ["high_vault"], "The collapse is told, not shown: the section with the straight bays outlined",
          assumptions="The film shows no collapse or destruction; it says 'in 1284' (the association gives 'a Friday in November 1284')."),
    claim("CLM_183", "Why the 1284 vaults fell is still debated: explanations include monolithic colonnettes and settling mortar breaking flying buttresses, gusts of wind setting the buttress system resonating, and slow differential settlement of the foundations; the 2024 study finds no geotechnical cause and argues that raising the vaults by several metres, against proven proportions, made the upper structure too flexible.",
          [(I2, "2.1 Cause d’après les sources", "Il existe trois types d’interprétations pour expliquer l’effondrement partiel de voûtes du chœur en 1284, deux en partie haute de l’édifice, une en fondation."),
           (I2, "2.1 Cause d’après les sources", "Il s’agit pour la première de la rupture de colonnettes monolithes solidaires d’une maçonnerie appareillée dont les mortiers auraient progressivement tassé, provoquant la rupture d’arcs-boutants"),
           (I2, "2.1 Cause d’après les sources", "La deuxième invoque la mise en résonnance du système culée/arc-boutant au même endroit"),
           (I2, "2.1 Cause d’après les sources", "causée par un vent en rafale"),
           (I2, "2.1 Cause d’après les sources", "La troisième suggère l’existence d’un tassement différentiel lent dans les fondations"),
           (I2, "2.2 Origine géotechnique en 1284?", "un raidissement généralisé des parties hautes atteintes. Elles s’étaient avérées trop souples, non pas en soi, mais en raison de la décision"),
           (I2, "2.2 Origine géotechnique en 1284?", "en cours de chantier de surélever de plusieurs mètres les voûtes de la cathédrale. Cette décision dû être prise au mépris des dimensions choisies pour les parties sous-jacentes, des proportions éprouvées"),
           (I2, "Abstract (English)", "We here show that nothing appears to justify a geotechnical origin in the 1284 collapse."),
           (I2, "2.2 Origine géotechnique en 1284?", "Ainsi, nous ne souscrivons pas à l’hypothèse d’une origine géotechnique dans l’accident de 1284.")],
          ["beauvais"], ["flying_buttress", "high_vault"], "Three-explanations card (no collapse shown)",
          assumptions="The sentence on the raised vaults runs across a page break of the paper, so it is quoted in two excerpts. This is the authors' argument, not a settled result: the film attributes it to them. The association's view (CLM_184) is that a storm was the likely trigger."),
    claim("CLM_184", "The Beauvais association describes the flying buttresses twisting and breaking in November 1284 and thinks a storm was the likely trigger, since the very tall building is exposed to wind.",
          [(AH, "A first catastrophe", "On a Friday in November 1284, the flying buttresses twist and break, causing the collapse of the choir’s vault. The cathedral, being very tall, rises above the neighboring plateau and is highly exposed to wind. It was likely a storm that triggered this catastrophe.")],
          ["beauvais"], ["flying_buttress"], "Three-explanations card", confidence="medium"),
    claim("CLM_185", "After 1284 the Beauvais choir was rebuilt with new intermediate piers that divided its three straight bays into six, and its vaults became six-part (sexpartite).",
          [(AH, "The reconstruction", "As a precaution, the bays were subdivided with new, narrower intermediate piers. This changed the straight section of the choir from 3 to 6 bays."),
           ("SRC_ABC_DESCRIPTION", "The choir", "After the partial collapse of 1284, the choir was rebuilt in the 14th century with additional piers, and the vaults became six-part, as they remain today.")],
          ["beauvais"], ["pier"], "Plan diagram: three bays become six", confidence="medium"),
    claim("CLM_186", "In the 16th century Beauvais built a transept and then, instead of a nave, a lantern tower with a spire about 150 metres high, completed in 1569; the tower rested on four slender crossing piers with no buttressing to the west, where the nave had not been built, and it fell in 1573.",
          [(AH, "150 years later, work resumes", "Begun in May 1500, this masterpiece of the Flamboyant period took 50 long years to build."),
           (AH, "An oversized spire", "Instead of extending the cathedral with a nave — which would have stabilized the building — it was decided to build a lantern tower at the crossing of the transept"),
           (AH, "An oversized spire", "Completed in 1569, this tower, topped with a spire, reached 150 m. It collapsed four years later"),
           (I2, "3.1 Cause d’après les sources", "un défaut de contrebutement à l’ouest, où la nouvelle nef n’était pas encore construite. La tour tout entière portait sur les quatre piliers élancés de la croisée du transept"),
           (I1, "2.1.3 1499-1605", "un support de la tour lanterne s’effondra le jour de l’Ascension 1573, un 30 avril")],
          ["beauvais"], [], "Beauvais timeline; the fall is told, not shown",
          assumptions="'About 150 metres' is the association's figure for the tower with its spire; the film rounds it as 'about 150 metres'.", confidence="medium"),
    claim("CLM_187", "Beauvais Cathedral's Gothic nave was never built.",
          [(I1, "1 Introduction", "sa nef gothique n’a jamais été construite (Murray, 2000)"),
           (AH, "The cathedral remains unfinished", "work stopped at a nave reduced to a single bay")],
          ["beauvais"], [], "Beauvais plan: choir and transept only",
          assumptions="The paper says the Gothic nave was never built; the association says work stopped at a nave reduced to a single bay. The film says 'the great Gothic nave was never built', which both support."),
    # ---- Amiens: limits and repairs
    claim("CLM_190", "At Amiens the enlarged central bays began to fail: the crossing piers, burdened by a great central steeple, buckled, and an iron chain was installed between 1497 and 1500 to arrest the deformation; the chain still runs through the triforium and ties the crossing piers.",
          [("SRC_CU_AMIENS_ETEXT_1", "E-Text 1, paragraph 2", "the enlarged central bays began to fail; the main crossing piers, burdened with weight of a great central steeple buckled inward at arcade level and outward in their upper parts, threatening collapse.  This deformation was arrested through the installation (1497-1500) of an iron chain"),
           ("SRC_CU_AMIENS_TRIFORIUM_CHAIN", "Triforium passage, south side of nave", "On the pavement to the left runs the iron chain (actually a series of iron rods linked together) that runs the length of the nave and ties the crossing pier.")],
          ["amiens"], [], "Section: a conceptual chain in the triforium (no forces shown)",
          assumptions="'Still runs' rests on the present tense of Columbia's page (copyright 2017, with a note dated 2017)."),
    claim("CLM_191", "Stephen Murray writes that in the vaulted masonry of Amiens forces were at work that could push verticals out of plumb; within two centuries the crossing piers were threatening collapse.",
          [("SRC_CU_AMIENS_ETEXT_17", "E-Text 17", "Within the arched masonry forces were at play that were capable of destroying the rectitude of the edifice, pushing verticals out of plumb and threatening disaster."),
           ("SRC_CU_AMIENS_ETEXT_17", "E-Text 17", "Within two centuries the crossing piers were threatening collapse.")],
          ["amiens"], ["pier"], "Amiens NOTE"),
]

# The owner's editorial decision (a human record, never written by this script) is applied on top.
approval_path = Path(sys.argv[1]).parent / "editorial_approval.json"
approval = json.loads(approval_path.read_text()) if approval_path.is_file() else None
revision = json.loads((HERE.parent / "script/narration.template.json").read_text())["revision"]["version"]
if approval and approval.get("narration_revision") != revision:
    print(f"editorial approval of narration {approval.get('narration_revision')} does not cover {revision}: NOT applied")
    approval = None
if approval:
    texts_sha = approval.get("claims_text_sha256", {})
    for c in CLAIMS:
        if c["id"] not in approval["claims"]:
            continue
        if texts_sha.get(c["id"]) != hashlib.sha256(c["text"].encode()).hexdigest():
            print(f"{c['id']}: claim text changed since the approval; approval NOT applied")
            continue
        c["review_status"] = "EDITORIALLY_APPROVED"
        c["caveat"] = f"Editorially approved {approval['approved_on']} for narration {approval['narration_revision']}."
        c["editorial_approval"] = {k: approval[k] for k in ("approved_by", "approved_on", "narration_revision", "basis")}

out = {"note": "Evidence registry for 'How Gothic Cathedrals Reached Impossible Heights'. Every excerpt was matched verbatim "
               "against the downloaded source text (research/build_sources.py; snapshots listed in research/source_snapshots.json). "
               + (f"{len(approval['claims'])} narrated claims editorially approved by {approval['approved_by']} on {approval['approved_on']}."
                  if approval else "Nothing here is editorially approved."),
       "sources": SOURCES, "claims": CLAIMS}
Path(sys.argv[1]).write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
print(len(SOURCES), "sources", len(CLAIMS), "claims")
