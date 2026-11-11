"""Authoring source of "Could We Build an Entire City That Floats?" (revision c-r2, locked by the owner).

    python3 projects/floating-city-design-challenge/script/story.py

writes script/narration.json, script/visual_beats.json and script/chapters.json from the chapters and beats below, so
narration and visual beats always carry the same sentences. Every fact or interpretation beat cites claims from
research/sources.json:
  - external sources (ESTABLISHED_FACT, SPECULATIVE_PROPOSAL, UNVERIFIED);
  - the Studio's own calculation, analysis/RESULTS.md (CALCULATED_ESTIMATE, CLM_101-109);
  - the scenario contract, concept/SCENARIO_CONTRACT.md (DESIGN_ASSUMPTION, CLM_121-125).
Numbers from the Studio's calculation are always said as illustrative ("in this illustrative design", "about").

Revision c-r2 (owner review of c-r1, 2026-11-08): B03/B40 shorter on the status of OCEANIX Busan (the architects'
page lists it "In Design"); B12 goes back to the three-story design before scaling up; B23 names the loading behind
the bridge slope; B15-B16 become one evolving diagram.

The owner locked c-r2 and approved its claims (2026-11-08, review/OWNER_APPROVALS.json): the sentences below are
locked and must not change. Production layer L4 (review/PRODUCTION_PLAN.md): the visuals of every beat live in
script/visuals.py (3D SEQUENCE steps timed by the narration's words, 2D cards) and override the brief visual fields
written here at the script stage.
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

CHAPTERS = [
    ("C1", "Could We Actually Do This?", "The finished district; the design problem; one real precedent and one proposal; take it apart."),
    ("C2", "The First Problem: Making Buildings Float", "How it floats; what added load does and one fix; floating is not the whole problem."),
    ("C3", "Why One Platform Isn't a City", "Different loads and connections; how many platforms; bigger or more."),
    ("C4", "The Water Never Stays Still", "Relative motion, what residents feel, bending; site and layout as the first fixes."),
    ("C5", "Keeping the City in Place", "Piles and water level, hinged bridges, mooring lines in deeper water, the seabed."),
    ("C6", "A City Needs More Than Buildings", "Power, wastewater and services: a floating city stays tied to land."),
    ("C7", "What Would Actually Make This Difficult?", "Offshore counterfactual: waves, moorings, links, autonomy as an extra choice, a different hull; maintenance, ecology, water rights, cost."),
    ("C8", "Could We Really Build It?", "Verdict in three tiers; what the arithmetic does and does not show; call to action; credits."),
]

BEATS = []


def beat(chapter, bid, kind, intent, sentences, claims=(), strategy=None, goal="", concepts=(), complexity="MEDIUM", label=None):
    BEATS.append({"chapter": chapter, "id": bid, "kind": kind, "intent": intent, "sentences": list(sentences),
                  "claims": list(claims),
                  "visual": {"strategy": strategy, "visual_goal": goal, "required_concepts": list(concepts),
                             "expected_complexity": complexity, **({"label": label} if label else {})}})


CONCEPT_MOTION = "Conceptual motion visualization — not a hydrodynamic simulation"
DISTRICT = ["floating_district", "bay_site"]
PLATFORM = ["floating_platform", "platform_hull", "bulkhead", "bay_site"]

# C1 ----------------------------------------------------------------------------------------------------------------
beat("C1", "B01", "framing", "INTRODUCE_ARCHITECTURE", [
    "10,000 people, with homes, schools, a clinic, parks, and streets to walk along.",
    "And not one of them is standing on land."],
    strategy="HOLD", goal="Establishing aerial of the finished illustrative district in a sheltered bay; NOTE 'Illustrative design'",
    concepts=DISTRICT, complexity="HIGH")
beat("C1", "B02", "framing", "SHOW_CONTEXT", [
    "Could we design a city like this, one that floats, stays where we put it, and keeps working?",
    "Let's treat it as a design problem, and solve it one step at a time."],
    strategy="HOLD", goal="Slow push-in on the district; no claim on screen", concepts=DISTRICT, complexity="HIGH")
beat("C1", "B03", "fact", "SHOW_CONTEXT", [
    "Floating neighborhoods are not science fiction.",
    "In Amsterdam, a floating neighborhood called Schoonschip is home to 46 households, a little over 100 people.",
    "Much larger designs exist on paper.",
    "One, for 12,000 people off the coast of Busan in South Korea, was unveiled in 2022,",
    "and when we checked in November 2026, its architects still listed it as in design."],
    claims=["CLM_010", "CLM_011", "CLM_030", "CLM_031", "CLM_034", "CLM_057"],
    strategy="CARD", goal="Scale card: Schoonschip (built, ~100 people; schematic unless a licensed photo is approved), "
                         "OCEANIX Busan (proposed 2022; 'architects' project page, Nov 2026: In Design')",
    complexity="LOW")
beat("C1", "B04", "framing", "EXPLAIN_STRUCTURE", [
    "So let's take our city apart,",
    "and build it back, one problem at a time."],
    strategy="SEQUENCE", goal="The district comes apart layer by layer (breakwater, moorings, utilities, buildings, platforms) "
                              "until one empty platform remains", concepts=DISTRICT, complexity="HIGH")

# C2 ----------------------------------------------------------------------------------------------------------------
beat("C2", "B05", "fact", "EXPLAIN_STRUCTURE", [
    "Problem one: how does something this heavy float at all?",
    "Take a block of concrete.",
    "As a solid lump, it sinks: concrete is more than twice as dense as seawater.",
    "Shape the same concrete into a hollow box, 40 meters on each side, and it floats."],
    claims=["CLM_002", "CLM_008", "CLM_101"],
    strategy="COMPARE_SIDE_BY_SIDE", goal="Section: the hull's concrete as a solid block on the seabed beside the same "
                                          "concrete as a floating box (draft from analysis)", concepts=PLATFORM)
beat("C2", "B06", "fact", "EXPLAIN_STRUCTURE", [
    "It floats because it pushes water out of the way, and the water it pushes aside weighs as much as the platform.",
    "Every ton we add needs roughly one more cubic meter of water pushed aside."],
    claims=["CLM_001", "CLM_102"],
    strategy="HOLD_HIGHLIGHT", goal="Cutaway below the waterline: the displaced volume glows (prototype P1)", concepts=PLATFORM)
beat("C2", "B07", "fact", "SHOW_CONTEXT", [
    "Real floating homes work exactly this way.",
    "The Schoonschip houses stand on concrete floats.",
    "The heaviest weighs around 340 to 350 metric tons,",
    "so it pushes aside roughly as many cubic meters of canal water: a cube about 7 meters on each side."],
    claims=["CLM_012", "CLM_013", "CLM_103"],
    strategy="CARD", goal="House on its float beside a 7 m cube of water (schematic, labelled; 'two builders' figures')",
    complexity="LOW")
beat("C2", "B08", "fact", "EXPLAIN_STRUCTURE", [
    "Our first platform, in this illustrative design, carries four blocks of three-story homes.",
    "Altogether it weighs about 4,800 tons, and floats about 3 meters deep.",
    "And here's the surprise: more than half of that weight is the concrete hull itself."],
    claims=["CLM_104"],
    strategy="EXPLODE", goal="Layers lift apart (homes, deck finishes, hull) with their share of the mass; label 'illustrative'",
    concepts=PLATFORM)
beat("C2", "B09", "fact", "EXPLAIN_DESIGN_CHANGE", [
    "Now add a fourth story.",
    "The platform settles about a third of a meter deeper,",
    "and the freeboard, the part of the hull above the water, shrinks from about a meter to about 70 centimeters."],
    claims=["CLM_003", "CLM_105"],
    strategy="HIGHLIGHT_REPLACE_HIGHLIGHT", goal="Close-up of the draft gauge: the fourth storey arrives, the platform sinks "
                                                 "by the calculated amount (prototype P2b; new SINK step)", concepts=PLATFORM)
beat("C2", "B10", "fact", "EXPLAIN_DESIGN_CHANGE", [
    "One fix is to make the hull half a meter deeper.",
    "That adds about 100 tons of concrete, 4% more,",
    "and brings the freeboard back to about a meter and 15 centimeters.",
    "Lighter buildings would be another way."],
    claims=["CLM_105"],
    strategy="HIGHLIGHT_REPLACE_HIGHLIGHT", goal="Same camera: the extra half metre of hull appears below, the deck rises to "
                                                 "the calculated freeboard (same branch as B09)", concepts=PLATFORM)
beat("C2", "B11", "fact", "EXPLAIN_STRUCTURE", [
    "Will it tip over?",
    "Move 100 tons out toward the edge, and in this example the platform tilts by less than half a degree.",
    "But a small tilt under a shifted load tells us very little about how it will move in waves.",
    "Floating is only the first problem."],
    claims=["CLM_009", "CLM_106"],
    strategy="HOLD", goal="A 100 t load slides to the edge; the platform tilts by the calculated small angle (no G, B, M symbols)",
    concepts=PLATFORM)

# C3 ----------------------------------------------------------------------------------------------------------------
beat("C3", "B12", "fact", "EXPLAIN_DESIGN_CHANGE", [
    "Let's go back to the three-story version. A platform like this holds about 50 people.",
    "For 10,000, we need a lot of them.",
    "So why not simply join them all into one enormous slab?"],
    claims=["CLM_108"],
    strategy="ASSEMBLE_IN", goal="The platform returns to three stories and its original hull (the fourth story and the extra hull "
                                 "fade), then copies of it arrive around a small basin", concepts=["floating_platform", "bay_site"])
beat("C3", "B13", "fact", "EXPLAIN_DESIGN_CHANGE", [
    "Look at two identical platforms carrying different buildings, one with two stories and one with four.",
    "Floating on their own, their decks would sit about 66 centimeters apart in height.",
    "So different loads add a demand on whatever connects them.",
    "In this design, the walkways between platforms are hinged, so they can follow the difference.",
    "Adding ballast to even out the decks would be another option."],
    claims=["CLM_107"],
    strategy="HIGHLIGHT_REPLACE_HIGHLIGHT", goal="Side elevation: two decks at different heights; a hinged walkway spans them "
                                                 "(no part shown as failing)", concepts=["floating_platform", "walkway_connector"])
beat("C3", "B14", "fact", "SHOW_COMPONENT", [
    "Connections are where engineers expect trouble.",
    "A 2026 research agenda lists stress concentrations on connectors among the challenges of large floating developments.",
    "One concept study links its modules flexibly, and spaces them far enough apart not to collide, because on flexible moorings they are expected to move sideways quite a lot."],
    claims=["CLM_042", "CLM_056"],
    strategy="CLOSEUP_HIGHLIGHT", goal="Close-up of a joint: gap, hinged walkway, flexible utility link (conceptual geometry)",
    concepts=["walkway_connector", "utility_line"])
beat("C3", "B15", "fact", "SHOW_CONTEXT", [
    "How many platforms would 10,000 people need?",
    "Say each resident needs about 40 square meters of floor: thirty for their home, and ten for a share of schools, shops and services.",
    "That's about thirty-three hectares of platform:",
    "about 200 platforms like our first one, with hundreds of connections between them."],
    claims=["CLM_124", "CLM_108"],
    strategy="CARD", goal="One plan diagram (continues into B16): 40 m cells appear until ~33 ha are covered; the joints between "
                          "cells light up as they are counted (label 'illustrative')", complexity="LOW")
beat("C3", "B16", "fact", "COMPARE_VARIANTS", [
    "Bigger platforms mean fewer connections.",
    "At 100 meters on a side, 34 would do,",
    "but each would weigh about 30,000 tons, to build, launch and tow.",
    "Even the Schoonschip floats were too big for the dry docks of traditional houseboat builders, and were cast on the quay instead.",
    "Our district uses 60-meter platforms with three-story homes, 93 of them: a middle choice for this illustration, not an optimum."],
    claims=["CLM_108", "CLM_014", "CLM_125"],
    strategy="CARD", goal="Same diagram as B15: the cells regroup into 100 m modules (fewer joints, mass per module shown), "
                          "then settle on 60 m; no second table", complexity="LOW")

# C4 ----------------------------------------------------------------------------------------------------------------
beat("C4", "B17", "framing", "EXPLAIN_CAUSE_EFFECT", [
    "And all of this sits on water that never keeps still.",
    "Each platform rises and falls on its own, and every gap and hinge between them has to cope."],
    strategy="HOLD", goal=f"Five platforms move out of phase; gaps open and close; label '{CONCEPT_MOTION}' (new CONCEPT_MOTION)",
    concepts=["floating_platform", "walkway_connector"], label=CONCEPT_MOTION)
beat("C4", "B18", "fact", "SHOW_CONTEXT", [
    "People living on the water feel it.",
    "Floating homes in the Netherlands can rock in storms, or when large cruise ships pass,",
    "and one Amsterdam resident feels it most on her upper floor."],
    claims=["CLM_022"],
    strategy="CARD", goal="Floating home section; upper floor marked; source line (Yale E360, 2021)", complexity="LOW")
beat("C4", "B19", "fact", "EXPLAIN_STRUCTURE", [
    "Very large platforms don't only move. They bend,",
    "and predicting exactly how is still an open research problem."],
    claims=["CLM_053"],
    strategy="CARD", goal="Long platform drawn flexing; 'exaggerated, conceptual'", complexity="LOW")
beat("C4", "B20", "fact", "SHOW_CONTEXT", [
    "So the first fix is where you build.",
    "A 2026 concept study looks for sea areas with limited fetch, near a gulf, a strait or an archipelago, where waves stay moderate.",
    "That's why our city sits in a sheltered bay, connected to an existing city on shore."],
    claims=["CLM_050", "CLM_121"],
    strategy="CARD", goal="Two schematic bays: sheltered vs open; the district placed in the sheltered one", complexity="LOW")
beat("C4", "B21", "fact", "EXPLAIN_DESIGN_CHANGE", [
    "The second fix is the layout.",
    "Following one concept study, homes go in the middle, and functions that can tolerate more motion form the outer ring.",
    "Where the bay opens to the sea, a breakwater reduces the waves.",
    "But a floating breakwater may not be enough against longer waves from the open sea, and how much wave energy passes behind one is still hard to predict."],
    claims=["CLM_055", "CLM_051", "CLM_052"],
    strategy="SEQUENCE", goal="Top view to three-quarter: inner homes glow, outer ring, breakwater arrives on the open side; "
                              "NOTE 'reduces waves, does not remove storm risk'", concepts=DISTRICT + ["breakwater"], complexity="HIGH")

# C5 ----------------------------------------------------------------------------------------------------------------
beat("C5", "B22", "fact", "SHOW_COMPONENT", [
    "Something also has to hold the city in place.",
    "Floating homes in the Netherlands are fixed to the shore, often resting against steel poles."],
    claims=["CLM_020"],
    strategy="SEQUENCE", goal="Water surface visible, then ghosted in a second step; piles glow (prototype P4)",
    concepts=["mooring_pile", "floating_platform", "bay_site"])
beat("C5", "B23", "fact", "EXPLAIN_CAUSE_EFFECT", [
    "Water levels rise and fall, and a floating platform rises and falls with them, sliding along its poles.",
    "In our scenario, the water level can change by about 2 meters,",
    "so the bridges to shore need hinges: including changes in loading, the slope of a 25-meter bridge changes by about 3 degrees either way."],
    claims=["CLM_041", "CLM_122", "CLM_109"],
    strategy="SEQUENCE", goal="Elevation: water rises, platform slides up its piles, the link-span turns on its shore hinge "
                              "(new RISE/SINK step); on screen: '2 m water level + loading, assumed; shore hinge at mid-range'", concepts=["mooring_pile", "link_span", "floating_platform"])
beat("C5", "B24", "fact", "EXPLAIN_DESIGN_CHANGE", [
    "Further out, the water is deeper, and piles give way to mooring lines anchored in the seabed.",
    "Deeper water means longer lines, deeper anchors, and higher costs.",
    "The seabed itself shapes the design, and the bill."],
    claims=["CLM_055", "CLM_054"],
    strategy="REPLACE", goal="Underwater, water ghosted: piles replaced by mooring lines toward deeper seabed; "
                             "NOTE 'Conceptual mooring — not sized'", concepts=["mooring_line", "anchor", "bay_site"])

# C6 ----------------------------------------------------------------------------------------------------------------
beat("C6", "B25", "framing", "EXPLAIN_STRUCTURE", [
    "So it floats, and it stays put. But is it a city yet?",
    "Fade out the buildings, and the city's other half appears."],
    strategy="SEQUENCE", goal="Buildings ghost; utility networks appear along the bridges", concepts=DISTRICT + ["utility_line"],
    complexity="HIGH")
beat("C6", "B26", "fact", "SHOW_CONTEXT", [
    "Power first: at Schoonschip, 46 households share a single connection to the national grid,",
    "with solar panels, a battery in every house, and a smart grid between them.",
    "Floating doesn't mean off-grid."],
    claims=["CLM_016"],
    strategy="CARD", goal="Many homes, one cable to shore (schematic)", complexity="LOW")
beat("C6", "B27", "fact", "SHOW_COMPONENT", [
    "Wastewater is separated there too: gray water from showers and washing machines, black water from toilets.",
    "Connecting floating homes to sewers on land takes extra infrastructure, such as waterproof cables and pumps.",
    "In our city, wastewater is pumped ashore along the bridges, and drinking water comes back the same way."],
    claims=["CLM_017", "CLM_023", "CLM_123"],
    strategy="CLOSEUP_HIGHLIGHT", goal="One platform: grey and black lines, a pump, the line along the bridge", concepts=["utility_line", "link_span"])
beat("C6", "B28", "fact", "SHOW_COMPONENT", [
    "Transport, fire and medical services, and food all follow the same logic.",
    "A large floating development has to connect sewage, power and roads to land, or develop alternatives of its own,",
    "and our city connects."],
    claims=["CLM_043"],
    strategy="SEQUENCE", goal="Boat landings, two routes to land from each platform, rescue-boat berth glow in turn",
    concepts=DISTRICT + ["access_route"], complexity="HIGH")

# C7 ----------------------------------------------------------------------------------------------------------------
beat("C7", "B29", "framing", "SHOW_CONTEXT", [
    "Everything so far assumed sheltered water close to a city.",
    "So what happens if we tow it out to sea?"],
    strategy="HOLD", goal="Small 3D district on an open sea (counterfactual); label 'Counterfactual'", concepts=["floating_district", "open_sea_site"])
beat("C7", "B30", "fact", "EXPLAIN_CAUSE_EFFECT", [
    "Longer waves arrive, and a floating breakwater may not be enough against them.",
    "Below the surface, the seabed drops away, so mooring lines get longer and anchors deeper."],
    claims=["CLM_051", "CLM_054"],
    strategy="SEQUENCE", goal="Same open-sea scene: long conceptual swell passes the breakwater (labelled); water ghosts, "
                              "lines lengthen to a deeper seabed", concepts=["breakwater", "mooring_line", "open_sea_site"], label=CONCEPT_MOTION)
beat("C7", "B31", "fact", "EXPLAIN_CAUSE_EFFECT", [
    "Further from shore, cables, pipes and supply ships can still reach the city,",
    "but every link becomes longer and more exposed."],
    claims=["CLM_043", "CLM_051"],
    strategy="HOLD_HIGHLIGHT", goal="The links to shore stretch across open water and glow", concepts=["utility_line", "open_sea_site"])
beat("C7", "B32", "fact", "EXPLAIN_CAUSE_EFFECT", [
    "And if we also asked the city to supply itself, as one 2026 offshore concept does,",
    "it would need its own systems for energy, water and food.",
    "In that study, growing food alone accounts for nearly half of the city's estimated energy use."],
    claims=["CLM_058"],
    strategy="CARD", goal="An added condition: three systems appear; 'one concept study's estimate'", complexity="LOW")
beat("C7", "B33", "fact", "COMPARE_VARIANTS", [
    "That study also uses a different kind of hull:",
    "semi-submersible platforms, with the deck raised above the sea on columns, behind a floating barrier.",
    "Offshore isn't the same city moved further out. It's a different design."],
    claims=["CLM_062"],
    strategy="COMPARE_SIDE_BY_SIDE", goal="3D: our box pontoon beside a column-stabilised module (schematic, labelled 'concept study')",
    concepts=["floating_platform", "semi_submersible_module"])
beat("C7", "B34", "fact", "SHOW_COMPONENT", [
    "Some difficulties remain wherever we build.",
    "Concrete in seawater needs watching: chlorides can corrode the steel reinforcement,",
    "and, according to a 2026 study, there are no dedicated standards for floating cities yet."],
    claims=["CLM_059"],
    strategy="CLOSEUP_HIGHLIGHT", goal="Hull surface, inspection zone glows (no damage shown)", concepts=["platform_hull"])
beat("C7", "B35", "fact", "SHOW_CONTEXT", [
    "Large floating developments change the light, shade and water movement beneath them, effects that researchers say still need study,",
    "and they expect the impact on local ecology to be far larger than that of small developments."],
    claims=["CLM_044"],
    strategy="HOLD", goal="Underwater view: the district's shadow on the seabed (EEVEE shadow, illustrative)", concepts=DISTRICT)
beat("C7", "B36", "fact", "SHOW_CONTEXT", [
    "And who gets to use the water?",
    "How districts like this fit into planning law is not yet known,",
    "and researchers warn they could end up serving the wealthy, and fencing off water that used to be public."],
    claims=["CLM_045", "CLM_046"],
    strategy="COMPARE_SIDE_BY_SIDE", goal="Two waterfront edges: public path vs fenced edge", concepts=["floating_platform", "access_route"])
beat("C7", "B37", "fact", "SUMMARIZE_DIFFERENCES", [
    "And what would it cost?",
    "We do not yet have a reliable cost estimate for this design. The one published framework we found is preliminary, and covers only flotation and energy.",
    "Compared with land, floating structures can follow the water level, and can be moved or reused,",
    "but they trade a fixed foundation for moorings, connections and ongoing maintenance."],
    claims=["CLM_063", "CLM_041", "CLM_054", "CLM_042", "CLM_059"],
    strategy="CARD", goal="Two columns: what floating gives, what it costs (no numbers)", complexity="LOW")

# C8 ----------------------------------------------------------------------------------------------------------------
beat("C8", "B38", "framing", "SUMMARIZE_DIFFERENCES", [
    "From one platform to a district, every part we added answers a question we had to ask."],
    strategy="DETAIL_THEN_OVERVIEW", goal="Platform A alone, then beside district C; one label per added system",
    concepts=["floating_platform", "floating_district"], complexity="HIGH")
beat("C8", "B39", "fact", "SUMMARIZE_DIFFERENCES", [
    "So, could we build an entire city that floats?",
    "Small floating neighborhoods, connected to the shore in sheltered water, already exist."],
    claims=["CLM_010", "CLM_011", "CLM_016"],
    strategy="CARD", goal="Verdict tier 1 of 3 (elements appear with the words)", complexity="LOW")
beat("C8", "B40", "interpretation", "SUMMARIZE_DIFFERENCES", [
    "A connected district for 10,000 people, in a sheltered bay, built step by step, may be possible under the right conditions.",
    "But how very large platforms bend, how their connections hold up, and what they would cost are still open questions.",
    "And the one project of that size we checked is still listed as in design."],
    claims=["CLM_121", "CLM_053", "CLM_042", "CLM_063", "CLM_034"],
    strategy="CARD", goal="Verdict tier 2 of 3", complexity="LOW")
beat("C8", "B41", "interpretation", "SUMMARIZE_DIFFERENCES", [
    "A city far out at sea, especially one that has to supply itself, remains much more speculative."],
    claims=["CLM_051", "CLM_058", "CLM_062"],
    strategy="CARD", goal="Verdict tier 3 of 3", complexity="LOW")
beat("C8", "B42", "interpretation", "SUMMARIZE_DIFFERENCES", [
    "Our arithmetic shows what it takes for a platform to float.",
    "Whether a whole district works depends on the site, and on every other system we added."],
    claims=["CLM_104", "CLM_121"],
    strategy="HOLD", goal="Closing aerial of the district (re-uses the opening scene)", concepts=DISTRICT, complexity="HIGH")
beat("C8", "B43", "framing", "SHOW_CONTEXT", [
    "Which structure should we explain next?",
    "Suggest a topic in the comments.",
    "And if you enjoyed this film, please like it and subscribe."],
    strategy="CARD", goal="Closing call to action with self-drawn icons (comment, like, subscribe, bell) as each is asked; "
                          "no platform logo or trademark", complexity="LOW")
beat("C8", "B44", "framing", "SHOW_CONTEXT", [
    "Thank you for watching.",
    "The sources are listed in the description."],
    strategy="CARD", goal="Credits; AI-voice disclosure; 'Models are illustrative, not engineering designs'", complexity="LOW")


def main():
    narration = json.loads((HERE / "narration.template.json").read_text())
    narration["beats"] = [{"id": b["id"], "kind": b["kind"], "claim_ids": b["claims"], "sentences": b["sentences"]}
                          for b in BEATS]
    (HERE / "narration.json").write_text(json.dumps(narration, indent=2, ensure_ascii=False) + "\n")
    doc = {"schema": "narrative_beats/1", "project_id": "floating-city-design-challenge",
           "title": "Could We Build an Entire City That Floats?", "status": "INTERNAL_REVIEW_DRAFT", "timing_mode": "AUDIO_LOCKED",
           "publication": {"restriction": "INTERNAL_ONLY",
                           "reason": "Revision c-r2, locked by the owner with its claims approved (2026-11-08); visuals in "
                                     "internal production, not approved for publication."},
           "beats": []}
    from visuals import VISUALS, note   # production layer L4: the visuals of every beat
    # full review (2026-11-11): chapters 2-8 open with their numbered title (one source: CHAPTERS), as in the reference film
    firsts = {next(b["id"] for b in BEATS if b["chapter"] == cid): (k, title)
              for k, (cid, title, _) in enumerate(CHAPTERS, 1) if k > 1}
    missing = [b["id"] for b in BEATS if b["id"] not in VISUALS]
    if missing:
        raise SystemExit(f"no visual in script/visuals.py for {missing}")
    for b in BEATS:
        v = dict(VISUALS[b["id"]])
        entry = {"beat_id": b["id"], "chapter": b["chapter"], "kind": b["kind"], "narrative_intent": b["intent"],
                 "claim_ids": b["claims"], "narration": " ".join(b["sentences"]),
                 "visual_goal": v.pop("visual_goal"), "required_concepts": v.pop("required_concepts"),
                 "expected_complexity": v.pop("expected_complexity")}
        entry.update(v)
        if b["id"] in firsts:
            k, title = firsts[b["id"]]
            entry["annotations"] = [note(f"{b['id']}_ch", f"{k} \u00b7 {title}", 0, until=1 if len(b["sentences"]) > 1 else None,
                                         position="TOP_LEFT")] + list(entry.get("annotations") or [])
        doc["beats"].append(entry)
    (HERE / "visual_beats.json").write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
    chapters = {"schema": "chapters/1", "project_id": "floating-city-design-challenge",
                "chapters": [{"id": cid, "title": title, "purpose": purpose,
                              "beat_ids": [b["id"] for b in BEATS if b["chapter"] == cid]}
                             for cid, title, purpose in CHAPTERS]}
    (HERE / "chapters.json").write_text(json.dumps(chapters, indent=2, ensure_ascii=False) + "\n")
    words = sum(len(s.split()) for b in BEATS for s in b["sentences"])
    print(f"{len(CHAPTERS)} chapters, {len(BEATS)} beats, {sum(len(b['sentences']) for b in BEATS)} sentences, {words} words")


if __name__ == "__main__":
    main()
