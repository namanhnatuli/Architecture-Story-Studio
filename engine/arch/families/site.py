"""Site (shared base) generators: the context a structure stands in (pure Python)."""
from engine.arch import primitives as P
from engine.arch.semantic import Component

GROUND_Z = -0.38   # top of the environment ground plane (engine/scene.py build_environment)


def level_ground(p):
    """A plain paved plinth for a building: the shared base of one scene context."""
    return [Component(id="ground_plinth", type="GROUND", material="stone_dark", group="ground",
                      mesh=P.box((p["site_width_m"], p["site_length_m"], 0.2), (0.0, p["site_length_m"] / 2.0 - p["front_margin_m"], GROUND_Z - 0.1)),
                      layer=0, animation=("STATIC",))]


def river_crossing(p):
    """Two banks with vertical faces at x = +/- gap/2 and a water strip between them.

    Bank tops are at deck level so the road continues onto each bridge; the water
    surface sits at water_level_m. Every bridge variant spans exactly this gap."""
    gap, deck, width, bank, water = (p["gap_m"], p["deck_level_m"], p["site_width_m"], p["bank_length_m"],
                                     p["water_level_m"])
    comps = []
    for side, sign in (("left", -1), ("right", 1)):
        x_in, x_out = sign * gap / 2.0, sign * (gap / 2.0 + bank)
        comps.append(Component(
            id=f"bank_{side}", type="GROUND", material="earth_bank", group="banks",
            mesh=P.box((bank, width, deck - GROUND_Z), ((x_in + x_out) / 2.0, 0.0, (deck + GROUND_Z) / 2.0)),
            layer=0, animation=("STATIC",), bevel=0.08))
    comps.append(Component(
        id="water", type="WATER", material="water", group="water",
        mesh=P.box((gap, width, water - GROUND_Z), (0.0, 0.0, (water + GROUND_Z) / 2.0)),
        layer=0, animation=("STATIC",)))
    return comps
