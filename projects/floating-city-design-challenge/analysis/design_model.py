"""Transparent concept-stage calculations for SCN_FLOATCITY_COASTAL_01 (stdlib only).

    python3 analysis/design_model.py            # writes analysis/results.json and analysis/RESULTS.md

Every input comes from concept/scenario_contract.json (DESIGN_ASSUMPTION) or a sourced constant (claim id).
Every output is a CALCULATED_ESTIMATE for an idealised rectangular concrete box in still water.

This model does NOT and cannot certify: structural safety, dynamic stability, large-angle or damage stability to any
rule, mooring adequacy, storm survivability, hydro-elastic response, occupant comfort or environmental compliance.
Those need site data and marine-engineering analysis (concept/ENGINEERING_RESEARCH.md, section 8).
"""
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
CONTRACT = HERE.parent / "concept" / "scenario_contract.json"

RHO_SEA = 1025.0        # kg/m3, CLM_004 (design value)
RHO_CANAL = 1000.0      # kg/m3, fresh water rounded from 998 at 20 C (CLM_008)
RHO_CONCRETE = 2400.0   # kg/m3, CLM_008
G = 9.81                # m/s2, CLM_004


def hull_concrete_m3(L, B, H, slab, wall, spacing, bulkhead):
    """Concrete volume of a closed box pontoon: top and bottom slabs, perimeter walls, internal bulkhead grid."""
    slabs = 2 * L * B * slab
    inner_h = H - 2 * slab
    walls = 2 * (L + B) * inner_h * wall
    nx = max(0, math.ceil(L / spacing) - 1)          # bulkheads across the length
    ny = max(0, math.ceil(B / spacing) - 1)
    bulkheads = (nx * B + ny * L) * inner_h * bulkhead
    return {"slabs": slabs, "walls": walls, "bulkheads": bulkheads, "total": slabs + walls + bulkheads,
            "compartments": (nx + 1) * (ny + 1)}


def platform(L=40.0, B=40.0, H=4.0, slab=0.25, wall=0.25, spacing=10.0, bulkhead=0.2, cover=0.4, storeys=3,
             storey_h=3.0, dead=0.6, variable=0.25, finishes=0.2, rho=RHO_SEA):
    """Masses (t), centres of gravity above keel (m), draft, freeboard and small-angle stability of one box platform."""
    conc = hull_concrete_m3(L, B, H, slab, wall, spacing, bulkhead)
    deck = L * B
    floor = deck * cover * storeys
    items = {   # name: (tonnes, KG above keel in m)
        "hull_concrete": (conc["total"] * RHO_CONCRETE / 1000, H / 2),             # symmetric box shell: G at mid-depth
        "deck_finishes": (deck * finishes, H + 0.1),
        "buildings_dead": (floor * dead, H + storeys * storey_h / 2),
        "variable_on_floors": (floor * variable, H + storeys * storey_h / 2),
        "variable_on_open_deck": (deck * (1 - cover) * variable, H + 0.5),
    }
    M = sum(m for m, _ in items.values())
    KG = sum(m * z for m, z in items.values()) / M
    T = M * 1000 / (rho * deck)                   # Archimedes: M = rho * L * B * T
    KB = T / 2
    BM = B ** 2 / (12 * T)                        # It / volume = (L B^3 / 12) / (L B T)
    GM = KB + BM - KG
    return {"inputs": {"L_m": L, "B_m": B, "H_m": H, "cover": cover, "storeys": storeys, "dead_t_m2": dead,
                       "variable_t_m2": variable, "finishes_t_m2": finishes, "rho_kg_m3": rho},
            "concrete_m3": {k: round(v, 1) for k, v in conc.items()},
            "mass_t": {k: round(m, 1) for k, (m, _) in items.items()} | {"total": round(M, 1)},
            "areal_mass_t_m2": round(M / deck, 3), "gross_floor_area_m2": round(floor, 1),
            "draft_m": round(T, 3), "freeboard_m": round(H - T, 3), "displaced_volume_m3": round(M * 1000 / rho, 1),
            "KB_m": round(KB, 3), "BM_m": round(BM, 2), "KG_m": round(KG, 3), "GM_m": round(GM, 2),
            "compartments": conc["compartments"]}


def list_angle_deg(w_t, d_m, W_t, GM_m):
    """Small-angle list from moving w a distance d sideways: tan(theta) = w d / (W GM) (CLM_009)."""
    return math.degrees(math.atan(w_t * d_m / (W_t * GM_m)))


def lost_buoyancy_draft_increase(L, B, T, s):
    """One s x s compartment flooded to the outside water level (permeability 1, walls ignored): the lost volume s^2 T
    is regained by sinking dT over the remaining waterplane LB - s^2 (lost-buoyancy method, simplified)."""
    return s * s * T / (L * B - s * s)


def main():
    c = json.loads(CONTRACT.read_text(encoding="utf-8"))["fields"]
    g = c["module_geometry_assumptions"]["value"]
    L, B = g["platform_A_m"]
    base = dict(L=L, B=B, H=g["hull_depth_m"], slab=g["slab_thickness_m"], wall=g["wall_thickness_m"],
                spacing=g["bulkhead_spacing_m"], bulkhead=g["bulkhead_thickness_m"], cover=g["building_cover_fraction"],
                storeys=g["storeys"], storey_h=g["storey_height_m"], variable=g["variable_load_t_per_m2"],
                finishes=g["deck_finishes_t_per_m2"])
    lo, mid, hi = g["building_dead_load_t_per_m2_floor"]
    A = platform(**base, dead=mid)
    out = {"scenario_id": "SCN_FLOATCITY_COASTAL_01", "class": "CALCULATED_ESTIMATE",
           "limits": "Idealised rectangular box in still water; small-angle hydrostatics only. Not a stability, strength, "
                     "mooring, storm, comfort or hydro-elastic assessment.",
           "constants": {"rho_sea": RHO_SEA, "rho_canal": RHO_CANAL, "rho_concrete": RHO_CONCRETE, "g": G,
                         "sources": {"rho_sea": "CLM_004", "rho_canal": "CLM_008 (998 at 20 C, rounded)",
                                     "rho_concrete": "CLM_008", "g": "CLM_004"}}}
    # 1. what one tonne asks of the water
    out["displaced_per_tonne_m3"] = {"sea": round(1000 / RHO_SEA, 4), "canal": round(1000 / RHO_CANAL, 4)}
    # 2. the real anchor: the heaviest Schoonschip home (CLM_013), canal water
    sch = {}
    for m in (340, 350):
        v = m * 1000 / RHO_CANAL
        sch[f"{m}_t"] = {"displaced_m3": round(v, 1), "equivalent_cube_side_m": round(v ** (1 / 3), 2)}
    out["schoonschip_heaviest_home"] = sch
    # 2b. the 'clay boat' (CLM_002): the hull's concrete as one solid block vs shaped as the hollow box (hull only, no buildings)
    v = A["concrete_m3"]["total"]
    out["clay_boat"] = {"concrete_m3": v, "solid_cube_side_m": round(v ** (1 / 3), 2),
                        "solid_density_vs_sea": round(RHO_CONCRETE / RHO_SEA, 2),
                        "hollow_box_draft_hull_only_m": round(v * RHO_CONCRETE / (RHO_SEA * L * B), 3),
                        "note": "Same concrete: a solid block is 2.3 times denser than sea water and sinks; as a 40 x 40 x 4 m box it floats."}
    # 3. Design A platform at three building dead loads
    out["design_A"] = {"mid": A, "dead_load_low": platform(**base, dead=lo), "dead_load_high": platform(**base, dead=hi)}
    # 4. sensitivity: what an added storey or an added tonne does to the draft
    W = A["mass_t"]["total"]
    plus = platform(**dict(base, storeys=base["storeys"] + 1), dead=mid)
    out["sensitivity"] = {
        "draft_per_100_t_added_cm": round(100 * 1000 / (RHO_SEA * L * B) * 100, 2),
        "extra_storey": {"mass_added_t": round(plus["mass_t"]["total"] - W, 1),
                         "draft_increase_cm": round((plus["draft_m"] - A["draft_m"]) * 100, 1),
                         "KG_rise_m": round(plus["KG_m"] - A["KG_m"], 2), "GM_after_m": plus["GM_m"]},
        "hull_concrete_share_of_mass": round(A["mass_t"]["hull_concrete"] / W, 3),
    }
    # 5. small-angle list when 100 t (e.g. a crowd or stored goods, assumption) moves 15 m off centre
    out["list_example"] = {"w_t": 100, "d_m": 15, "W_t": W, "GM_m": A["GM_m"],
                           "list_deg": round(list_angle_deg(100, 15, W, A["GM_m"]), 3),
                           "note": "Small-angle relation only; wind, waves and large angles need a GZ curve (CLM_006)."}
    # 6. why compartments: one flooded 10 m x 10 m cell (simplified lost buoyancy)
    s = g["bulkhead_spacing_m"]
    dT = lost_buoyancy_draft_increase(L, B, A["draft_m"], s)
    out["one_compartment_flooded"] = {"cell_m": s, "draft_increase_m": round(dT, 3),
                                      "freeboard_after_m": round(A["freeboard_m"] - dT, 3),
                                      "note": "Simplified, level sinkage only (an off-centre cell also causes list); no damage-stability rule is checked."}
    # 7. narrow vs wide: same displacement, different beam -> BM (why wide platforms are 'stiff', CLM_007)
    out["beam_comparison"] = {f"B_{b}m": {"BM_m": round(b * b / (12 * A["draft_m"]), 2)} for b in (10, 20, 40, 80)}
    # 8. city scale under GFA-per-resident assumptions
    pop = c["proposed_population"]["value"]
    gfa_per_A = A["gross_floor_area_m2"]
    city = {}
    for per in g["gross_floor_area_per_resident_m2"]:
        gfa = pop * per
        deck = gfa / (base["cover"] * base["storeys"])
        n = math.ceil(deck / (L * B))
        city[f"{per}_m2_per_resident"] = {
            "gross_floor_area_m2": gfa, "deck_area_m2": round(deck), "deck_area_ha": round(deck / 1e4, 1),
            "deck_m2_per_resident": round(deck / pop, 1), "platforms_40x40": n,
            "residents_per_platform": round(gfa_per_A / per), "displacement_t": round(n * W, -3),
            "displacement_range_t_by_dead_load": [round(n * out["design_A"]["dead_load_low"]["mass_t"]["total"], -3),
                                                  round(n * out["design_A"]["dead_load_high"]["mass_t"]["total"], -3)]}
    out["city_scale"] = city
    # 8a. residents per platform by storeys (40 m2 of floor per resident): the district goes back to three storeys
    out["residents_by_storeys"] = {f"{side}m_{st}_storeys": round(platform(**dict(base, L=side, B=side, storeys=st), dead=mid)["gross_floor_area_m2"] / 40)
                                   for side in (40, 60) for st in (3, 4)}
    # 8b. big or many: module size vs number of modules and connections for the mid case (40 m2 GFA per resident)
    deck_mid = city["40_m2_per_resident"]["deck_area_m2"]
    trade = {}
    for side in (40, 60, 80, 100):
        p = platform(**dict(base, L=side, B=side), dead=mid)
        n = math.ceil(deck_mid / (side * side))
        k = math.ceil(math.sqrt(n))
        rows_ = math.ceil(n / k)
        joints = (k - 1) * rows_ + (rows_ - 1) * k        # shared edges in a k x rows grid (upper bound when the last row is short)
        trade[f"{side}m"] = {"modules": n, "shared_edges_in_grid_max": joints, "module_mass_t": p["mass_t"]["total"],
                             "residents_per_module": round(p["gross_floor_area_m2"] / 40), "draft_m": p["draft_m"]}
    out["module_size_tradeoff"] = {"deck_area_m2": deck_mid, "by_side": trade,
                                   "note": "Fewer, larger modules mean fewer connections but heavier units to build, launch and tow, "
                                           "and a larger share of the response becomes flexible (hydro-elastic, CLM_042/CLM_053). "
                                           "Counts only; no loads."}
    # 8c. design revisions the story uses
    deeper = platform(**dict(base, H=4.5), dead=hi)
    two, four = platform(**dict(base, storeys=2), dead=mid), platform(**dict(base, storeys=4), dead=mid)
    # one continuous branch (owner review 2026-11-08): 3 storeys -> add a 4th -> deepen the hull, mid dead load throughout
    four_deep = platform(**dict(base, storeys=4, H=4.5), dead=mid)
    out["storey_branch"] = {
        "dead_load_t_m2": mid,
        "steps": [
            {"step": "3 storeys, hull 4.0 m", "mass_t": A["mass_t"]["total"], "draft_m": A["draft_m"], "freeboard_m": A["freeboard_m"]},
            {"step": "4 storeys, hull 4.0 m", "mass_t": four["mass_t"]["total"], "draft_m": four["draft_m"], "freeboard_m": four["freeboard_m"]},
            {"step": "4 storeys, hull 4.5 m", "mass_t": four_deep["mass_t"]["total"], "draft_m": four_deep["draft_m"],
             "freeboard_m": four_deep["freeboard_m"]}],
        "extra_concrete_for_deeper_hull_t": round(four_deep["mass_t"]["hull_concrete"] - four["mass_t"]["hull_concrete"], 1),
        "extra_concrete_share_of_hull": round((four_deep["mass_t"]["hull_concrete"] - four["mass_t"]["hull_concrete"]) / four["mass_t"]["hull_concrete"], 3),
        "note": "Same dead load in every step; only the storeys, then the hull depth, change."}
    # 8b'. the same small-angle list for the state the story shows while it tilts (B11: four storeys, hull 4.5 m)
    W4 = four_deep["mass_t"]["total"]
    out["list_example_shown_state"] = {"state": "4 storeys, hull 4.5 m (end of the storey branch)", "w_t": 100, "d_m": 15,
                                       "W_t": W4, "GM_m": four_deep["GM_m"],
                                       "list_deg": round(list_angle_deg(100, 15, W4, four_deep["GM_m"]), 3),
                                       "note": "The film's B11 shows this state; list_example is the three-storey case. Both are "
                                               "about 0.4 degrees and below half a degree."}
    out["revisions"] = {
        "A_prime_deeper_hull_heavy_buildings": {"hull_depth_m": 4.5, "draft_m": deeper["draft_m"], "freeboard_m": deeper["freeboard_m"],
                                                "vs_4m_hull_freeboard_m": out["design_A"]["dead_load_high"]["freeboard_m"],
                                                "extra_concrete_t": round(deeper["mass_t"]["hull_concrete"] - out["design_A"]["dead_load_high"]["mass_t"]["hull_concrete"], 1)},
        "B_neighbours_2_vs_4_storeys": {"draft_2_storeys_m": two["draft_m"], "draft_4_storeys_m": four["draft_m"],
                                        "deck_level_step_m": round(four["draft_m"] - two["draft_m"], 3),
                                        "note": "Two platforms floating independently. Once they are joined, the joint forces change "
                                                "the equilibrium of both, so this step is not what a rigid link would see; it only shows "
                                                "that different loads add a demand on the connection. The design chooses hinged walkways."},
    }
    # 8d. district C at the chosen module size (standard residential modules only)
    side = g["district_module_m"][0]
    mod = platform(**dict(base, L=side, B=side), dead=mid)
    n = math.ceil(deck_mid / (side * side))
    out["district_C"] = {"module_m": side, "modules": n, "deck_area_m2": n * side * side,
                         "module_mass_t": mod["mass_t"]["total"], "module_draft_m": mod["draft_m"],
                         "residents_per_module": round(mod["gross_floor_area_m2"] / 40),
                         "joints_max": trade[f"{side}m"]["shared_edges_in_grid_max"],
                         "standard_modules_displacement_t": round(n * mod["mass_t"]["total"], -3),
                         "excludes": ["service and port platforms", "breakwater", "link-span bridges", "moorings and piles",
                                      "utility plants and networks"],
                         "gfa_per_resident_m2": {"total": 40, **g["gross_floor_area_split_mid_m2"]}}
    # 8e. how the district's 93 modules are used (illustrative allocation, owner review of the L5 excerpt): every module
    # keeps the same footprint, storeys and loads, so every module floats at the same draft; only the use changes
    split = g["gross_floor_area_split_mid_m2"]
    gfa = mod["gross_floor_area_m2"]
    alloc = {"home": 66, "mixed": 6, "service": n - 66 - 6}
    mixed_home_share = (base["storeys"] - 1) / base["storeys"]   # mixed: shops and services on the ground floor, homes above
    homes_m2 = alloc["home"] * gfa + alloc["mixed"] * gfa * mixed_home_share
    services_m2 = alloc["service"] * gfa + alloc["mixed"] * gfa * (1 - mixed_home_share)
    residents = homes_m2 / split["homes"]
    out["district_C_allocation"] = {
        "modules": alloc, "module_gross_floor_area_m2": gfa, "mixed_home_share": round(mixed_home_share, 3),
        "homes_m2": round(homes_m2), "services_m2": round(services_m2),
        "residents_at_homes_m2_each": round(residents), "services_m2_per_resident": round(services_m2 / residents, 2),
        "service_types": {"school": 3, "clinic": 1, "community_shops_offices": alloc["service"] - 4},
        "note": "Illustrative allocation: 66 home modules alone give 9,504 residents at 30 m2 each; six mixed modules on the "
                "flanks near the shore (shops and services below, homes on the two upper floors) bring it to about 10,000 "
                "with about 10 m2 of services each. Parks are the open decks (60 percent of every deck), not extra modules."}
    # 9. published reference points (for scale only)
    busan_m2 = 15.5 * 4046.8564224                   # CLM_031 (acres -> m2)
    out["reference_points"] = {
        "oceanix_busan_proposed": {"platform_area_m2": round(busan_m2), "people": 12000,
                                   "m2_per_person": round(busan_m2 / 12000, 1),
                                   "note": "Design figures; 12,000 is residents and visitors (CLM_031); not comparable to a residents-only ratio."},
        "ruzzo_2026_functional_module": {"module_area_m2": 300 * 300, "inhabitants": 3000,
                                         "m2_per_inhabitant": round(300 * 300 / 3000, 1),
                                         "note": "Square ~300 m module, ~1,500 inhabitants per triangular half (CLM_057); excludes barrier and special modules."},
        "large_scale_threshold_ha": 20, "large_scale_threshold_source": "CLM_040",
        "ruzzo_energy_per_inhabitant_MWh_yr": {"total": round(470.3e3 / 50000, 2),
                                               "excluding_food_production": round(470.3e3 * (1 - 0.475) / 50000, 2),
                                               "note": "Third-party concept estimate for an autonomous offshore city (CLM_058); context only, not used in narration."},
    }
    # 10. link-span bridge slope over the water-level range (tide/surge + loading)
    rng = c["tidal_and_water_level_range"]["value"]
    variable_t = A["mass_t"]["variable_on_floors"] + A["mass_t"]["variable_on_open_deck"]
    draft_swing = variable_t * 1000 / (RHO_SEA * L * B)          # empty vs fully loaded (variable loads only)
    out["link_span"] = {f"{lb}_m_bridge": {"max_slope_deg_each_way": round(math.degrees(math.atan((rng / 2 + draft_swing / 2) / lb)), 1)}
                        for lb in (15, 25, 40)}
    out["link_span"]["water_level_range_m"] = rng
    out["link_span"]["draft_swing_empty_to_full_m"] = round(draft_swing, 3)
    out["link_span"]["water_level_only"] = {f"{lb}_m_bridge": {"max_slope_deg_each_way": round(math.degrees(math.atan((rng / 2) / lb)), 1)}
                                            for lb in (15, 25, 40)}
    out["link_span"]["hinge_assumption"] = ("Shore hinge at the middle of the combined range (water level plus loading), so the "
                                            "bridge tilts the same amount up and down.")
    out["link_span"]["note"] = "Platform end follows the water and the loading. Accessibility limits are not checked."
    (HERE / "results.json").write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    write_md(out)
    print(f"WROTE {HERE / 'results.json'} and RESULTS.md: Design A draft {A['draft_m']} m, freeboard {A['freeboard_m']} m, "
          f"GM {A['GM_m']} m (idealised box)")
    return out


def write_md(o):
    A = o["design_A"]["mid"]
    lo, hi = o["design_A"]["dead_load_low"], o["design_A"]["dead_load_high"]
    s = o["sensitivity"]
    rows = ["# Kết quả mô hình tính khái niệm (CALCULATED_ESTIMATE)", "",
            "Sinh bởi `analysis/design_model.py` từ `concept/scenario_contract.json`. Hộp bê tông chữ nhật lý tưởng, nước lặng, "
            "góc nghiêng nhỏ. **Không** đánh giá an toàn kết cấu, ổn định động hay ổn định khi hư hỏng theo quy chuẩn, neo, bão, "
            "dao động đàn hồi thủy lực hay tiện nghi.", "",
            "## 1. Một tấn đòi bao nhiêu nước",
            f"- Nước biển 1.025 kg/m³: {o['displaced_per_tonne_m3']['sea']} m³ mỗi tấn; nước kênh 1.000 kg/m³: {o['displaced_per_tonne_m3']['canal']} m³.",
            f"- Nhà nặng nhất ở Schoonschip (340–350 t, CLM_013) chiếm chỗ {o['schoonschip_heaviest_home']['340_t']['displaced_m3']}–"
            f"{o['schoonschip_heaviest_home']['350_t']['displaced_m3']} m³ nước kênh, tức một khối lập phương cạnh khoảng "
            f"{o['schoonschip_heaviest_home']['340_t']['equivalent_cube_side_m']}–{o['schoonschip_heaviest_home']['350_t']['equivalent_cube_side_m']} m.", "",
            f"- 'Thuyền đất sét' (CLM_002): {o['clay_boat']['concrete_m3']} m³ bê tông của thân phao, nếu đúc đặc là khối lập phương cạnh "
            f"{o['clay_boat']['solid_cube_side_m']} m, đặc hơn nước biển {o['clay_boat']['solid_density_vs_sea']} lần, chìm; làm thành hộp 40 × 40 × 4 m "
            f"thì nổi với mớn nước {o['clay_boat']['hollow_box_draft_hull_only_m']} m (chưa có nhà).", "",
            "## 2. Phao A (40 × 40 m, sâu 4 m, nhà 3 tầng phủ 40%)",
            "| Tải tĩnh nhà (t/m² sàn) | Khối lượng (t) | t/m² mặt sàn phao | Mớn nước (m) | Mạn khô (m) | KG (m) | BM (m) | GM (m) |",
            "|---|---|---|---|---|---|---|---|"]
    for name, p in (("thấp", lo), ("giữa", A), ("cao", hi)):
        rows.append(f"| {p['inputs']['dead_t_m2']} ({name}) | {p['mass_t']['total']} | {p['areal_mass_t_m2']} | {p['draft_m']} | "
                    f"{p['freeboard_m']} | {p['KG_m']} | {p['BM_m']} | {p['GM_m']} |")
    rows += ["", f"- Bê tông thân phao chiếm {round(s['hull_concrete_share_of_mass'] * 100)}% khối lượng (phương án giữa): "
                 f"{A['mass_t']['hull_concrete']} t trong {A['mass_t']['total']} t.",
             f"- Thêm 100 t: mớn nước tăng {s['draft_per_100_t_added_cm']} cm. Thêm một tầng: +{s['extra_storey']['mass_added_t']} t, "
             f"mớn nước +{s['extra_storey']['draft_increase_cm']} cm, KG +{s['extra_storey']['KG_rise_m']} m.",
             f"- Dời 100 t ra cách tâm 15 m: nghiêng khoảng {o['list_example']['list_deg']}° (công thức góc nhỏ, CLM_009).",
             f"- Một ô {o['one_compartment_flooded']['cell_m']} × {o['one_compartment_flooded']['cell_m']} m ngập: phao chìm thêm "
             f"{o['one_compartment_flooded']['draft_increase_m']} m (mạn khô còn {o['one_compartment_flooded']['freeboard_after_m']} m; "
             "chỉ tính chìm đều, không xét nghiêng).", "",
             "## 3. Rộng hay hẹp (cùng mớn nước)", "| Bề rộng | BM = B²/(12T) |", "|---|---|"]
    for k, v in o["beam_comparison"].items():
        rows.append(f"| {k[2:]} | {v['BM_m']} m |")
    rows += ["", "Phao càng rộng so với mớn nước thì BM càng lớn: ổn định ban đầu không phải bài toán khó của phao rộng. "
                 "Cái giá là phao 'cứng' (CLM_007), bám theo mặt nước; vấn đề chuyển sang sóng, mối nối và tiện nghi.", "",
             "## 4. Quy mô 10.000 người (theo giả định diện tích sàn mỗi người)",
             "| m² sàn/người | Diện tích mặt phao | m² mặt phao/người | Số phao 40 × 40 | Người/phao | Lượng chiếm nước (t) |", "|---|---|---|---|---|---|"]
    for k, v in o["city_scale"].items():
        rows.append(f"| {k.split('_')[0]} | {v['deck_area_ha']} ha | {v['deck_m2_per_resident']} | {v['platforms_40x40']} | "
                    f"{v['residents_per_platform']} | {v['displacement_t']:,.0f} ({v['displacement_range_t_by_dead_load'][0]:,.0f}–"
                    f"{v['displacement_range_t_by_dead_load'][1]:,.0f}) |")
    r = o["reference_points"]
    rows += ["", f"- Mốc so sánh: OCEANIX Busan (đề xuất) {r['oceanix_busan_proposed']['m2_per_person']} m² mặt phao mỗi người "
                 "(12.000 là cư dân và khách); module của Ruzzo 2026: "
                 f"{r['ruzzo_2026_functional_module']['m2_per_inhabitant']} m² mỗi người. Ngưỡng 'quy mô lớn' 20 ha (CLM_040).", "",
             "## 5. Phao lớn hay nhiều phao (33,3 ha, 40 m² sàn mỗi người)",
             "| Cạnh phao | Số phao | Số cạnh chung tối đa (mối nối) | Khối lượng một phao (t) | Người/phao |", "|---|---|---|---|---|"]
    for k, v in o["module_size_tradeoff"]["by_side"].items():
        rows.append(f"| {k} | {v['modules']} | {v['shared_edges_in_grid_max']} | {v['module_mass_t']:,.0f} | {v['residents_per_module']} |")
    rows += ["", "Chỉ là phép đếm, không có tải trọng. Phao to: ít mối nối nhưng nặng khi đúc, hạ thủy và kéo, và phần phản ứng "
                 "uốn theo sóng lớn hơn (CLM_042, CLM_053).", "",
             "## 6. Cầu nối bờ", f"Dải mực nước {o['link_span']['water_level_range_m']} m (giả định) cộng dao động mớn nước khi phao rỗng và đầy "
             f"({o['link_span']['draft_swing_empty_to_full_m']} m); khớp trên bờ đặt ở giữa dải tổng:"]
    rows += [f"- Cầu {k.split('_')[0]} m: dốc tối đa khoảng {v['max_slope_deg_each_way']}° mỗi chiều."
             for k, v in o["link_span"].items() if k.endswith("_bridge")]
    rows += ["", "Chỉ tính dải mực nước (không tính thay đổi tải), khớp ở giữa dải:"]
    rows += [f"- Cầu {k.split('_')[0]} m, chỉ mực nước: dốc tối đa khoảng {v['max_slope_deg_each_way']}° mỗi chiều."
             for k, v in o["link_span"]["water_level_only"].items()]
    rs = o["residents_by_storeys"]
    rows += ["", "## 6b. Số người mỗi phao theo số tầng (40 m² sàn mỗi người)",
             f"- Phao 40 m: 3 tầng {rs['40m_3_storeys']} người, 4 tầng {rs['40m_4_storeys']} người; "
             f"phao 60 m: 3 tầng {rs['60m_3_storeys']} người, 4 tầng {rs['60m_4_storeys']} người. "
             "Quận dùng nhà 3 tầng (phương án gốc), không dùng phương án 4 tầng của nhánh sửa."]
    sb, dc = o["storey_branch"], o["district_C"]
    rows += ["", "## 8. Nhánh thêm tầng (một nhánh liên tục, tải tĩnh nhà 0,6 t/m² sàn ở mọi bước)",
             "| Bước | Khối lượng (t) | Mớn nước (m) | Mạn khô (m) |", "|---|---|---|---|"]
    rows += [f"| {st['step']} | {st['mass_t']} | {st['draft_m']} | {st['freeboard_m']} |" for st in sb["steps"]]
    rows += [f"", f"Thân sâu thêm 0,5 m tốn thêm {sb['extra_concrete_for_deeper_hull_t']} t bê tông "
                  f"({round(sb['extra_concrete_share_of_hull'] * 100, 1)}% bê tông thân phao).", "",
             f"## 9. Quận C với phao {dc['module_m']} m (chỉ các phao tiêu chuẩn)",
             f"- {dc['modules']} phao, {round(dc['deck_area_m2'] / 1e4, 1)} ha, khoảng {dc['residents_per_module']} người mỗi phao, "
             f"tới {dc['joints_max']} cạnh chung; mỗi phao khoảng {dc['module_mass_t']:,.0f} t (mớn nước {dc['module_draft_m']} m).",
             f"- Lượng chiếm nước của các phao tiêu chuẩn: khoảng {dc['standard_modules_displacement_t']:,.0f} t. **Không gồm:** "
             + ", ".join(dc["excludes"]) + ".",
             f"- 40 m² sàn mỗi người = {dc['gfa_per_resident_m2']['homes']} m² nhà ở + {dc['gfa_per_resident_m2']['schools_clinic_shops_services']} m² "
             "trường học, phòng khám, cửa hàng, dịch vụ (giả định)."]
    al, ls = o["district_C_allocation"], o["list_example_shown_state"]
    rows += ["", "## 10. Phân bổ 93 phao của quận (minh họa)",
             f"- {al['modules']['home']} phao nhà ở, {al['modules']['mixed']} phao hỗn hợp (tầng trệt dịch vụ, hai tầng trên nhà ở), "
             f"{al['modules']['service']} phao dịch vụ ({al['service_types']['school']} trường học, {al['service_types']['clinic']} phòng khám, "
             f"{al['service_types']['community_shops_offices']} nhà cộng đồng, cửa hàng, văn phòng). Mọi phao cùng diện tích chiếm đất, "
             "số tầng và tải, nên cùng mớn nước.",
             f"- Nhà ở {al['homes_m2']:,} m² → khoảng {al['residents_at_homes_m2_each']:,} người ở mức 30 m²/người; dịch vụ "
             f"{al['services_m2']:,} m², khoảng {al['services_m2_per_resident']} m² mỗi người. Công viên là phần sàn trống (60% mỗi phao).",
             "", "## 11. Góc nghiêng của trạng thái mà B11 chiếu",
             f"- {ls['state']}: dời {ls['w_t']} t ra cách tâm {ls['d_m']} m → nghiêng khoảng {ls['list_deg']}° "
             f"(bản 3 tầng: {o['list_example']['list_deg']}°)."]
    rv = o["revisions"]
    a2, b2 = rv["A_prime_deeper_hull_heavy_buildings"], rv["B_neighbours_2_vs_4_storeys"]
    rows += ["", "## 7. Các lần sửa thiết kế mà câu chuyện dùng",
             f"- A′: thân sâu 4,5 m với nhà nặng (0,9 t/m²): thêm {a2['extra_concrete_t']} t bê tông, mớn nước {a2['draft_m']} m, "
             f"mạn khô {a2['freeboard_m']} m (thân 4 m: {a2['vs_4m_hull_freeboard_m']} m).",
             f"- B: hai phao giống nhau, nhà 2 tầng và 4 tầng: mớn nước {b2['draft_2_storeys_m']} m và {b2['draft_4_storeys_m']} m; "
             f"mặt sàn lệch nhau {b2['deck_level_step_m']} m."]
    (HERE / "RESULTS.md").write_text("\n".join(rows) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
