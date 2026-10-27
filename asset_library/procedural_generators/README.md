# Procedural generators

Generators are code, kept with the engine so render caches track them (`tools/render_cache.py`, category `engine`):

| Family / variant | Generator | Spec examples |
|---|---|---|
| `site/river_crossing` | `engine/arch/families/site.py: river_crossing` | `architecture/sites/site_river_crossing_24.json` |
| `bridge/timber_beam` | `engine/arch/families/bridge.py: timber_beam` | `architecture/bridges/bridge_timber_beam_01.json` |
| `bridge/stone_arch` | `engine/arch/families/bridge.py: stone_arch` | `bridge_stone_arch_03.json`, `bridge_stone_arch_05.json` |
| `bridge/steel_truss` | `engine/arch/families/bridge.py: steel_truss` | `bridge_steel_truss_pratt_01.json`, `bridge_steel_truss_warren_01.json` |

Registry, parameter ranges and validation: `engine/arch/assets.py` (`FAMILIES`). Generator version:
`engine.arch.GENERATOR_VERSION`. How to add a family: `docs/m4/M4_ARCHITECTURE_MODELING.md` §7.
