"""M5 narrative-to-visual planning (pure Python, no bpy, no network, no LLM at runtime).

  beats.py      narrative beat contract (schemas/narrative_beats.schema.json): load, validate, timing, evidence
  intents.py    visual intent taxonomy -> visual strategies; rule-based intent check
  vocabulary.py concepts (config/visual_vocabulary.json) -> families / semantic roles
  catalog.py    asset index: M4 library specs + legacy house/roof states (compatibility adapter)
  resolver.py   architecture asset resolution (REUSE / GENERATE / ADAPT / NEW / BLOCKED)
  mapper.py     narrative component concepts -> semantic component ids of a resolved asset
  camera.py     camera director: modes -> existing presets, continuity groups, visibility
  timing.py     provisional and audio-locked beat timing; minimum template durations
  planner.py    beats -> visual execution plan (schemas/visual_plan.schema.json)
  validate.py   plan validation (actionable errors)
  compiler.py   plan -> states.json + storyboard.json for the existing deterministic engine
  coverage.py   per-beat visual coverage report

The planning intelligence (choosing intents and concepts for a script) is the author's
(Claude Code / a human) and is written into the beats file; everything from there on is
deterministic, so a plan is reproducible without calling a model again.
"""
PLANNER_VERSION = "1.0.0"
