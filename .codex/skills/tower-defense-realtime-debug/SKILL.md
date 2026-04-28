---
name: tower-defense-realtime-debug
description: Use when debugging gameplay bugs in this tower defense project, especially issues in the game loop, action execution, combat, movement, cooldowns, resource spending, or mismatches between simulation and UI behavior.
---

# Tower Defense Realtime Debug

Use this skill when the problem is behavioral rather than architectural: towers not firing, units not dying, resources going negative, AI taking invalid actions, matches never ending, or UI behavior disagreeing with simulation.

## First Reads

- `README.md`
- `src/engine/game_engine.py`
- `src/models/game_state.py`
- the subsystem closest to the symptom:
  - `src/systems/combat_system.py`
  - `src/systems/unit_manager.py`
  - `src/systems/tower_manager.py`
  - `src/systems/resource_manager.py`
  - `src/systems/game_logger.py`
  - `src/ai/ai_agent.py`

## Debug Order

1. Reproduce the bug with the smallest scenario possible.
2. Prefer headless reproduction before UI reproduction.
3. Locate the owning layer.
4. Add narrow instrumentation if the cause is unclear.
5. Fix the smallest correct layer.
6. Re-run the exact reproduction path.

## Reproduction Strategy

Prefer these in order:

1. `python simulate.py ...`
2. targeted engine-level reasoning through `GameEngine.update()` and `execute_action()`
3. interactive `python main.py` only when the bug is input or rendering specific

Useful checks:

- action chosen but not executed
- resource deducted twice or not at all
- unit removed late or never
- tower cooldown never resets
- game over condition never triggers
- logger output disagrees with actual state changes

## Symptom Map

- Invalid AI action or odd prioritization: `src/ai/ai_agent.py`, `src/ai/heuristic_evaluator.py`
- Resource or affordability issues: `src/systems/resource_manager.py`, `GameEngine.execute_action`
- Spawn, movement, or arrival bugs: `src/systems/unit_manager.py`
- Damage, kills, or base HP bugs: `src/systems/combat_system.py`
- Match lifecycle or timing bugs: `src/engine/game_engine.py`
- Metrics mismatch: `src/systems/game_logger.py`

## Guardrails

- Do not start by rewriting UI for a logic bug.
- Do not patch over a timing bug with arbitrary constants unless you can justify them.
- Remove or minimize temporary debug noise before finishing.
- Validate the real failure mode after the fix; a clean compile is not enough.

## Minimal Validation

```powershell
python simulate.py heuristic balanced
python -m py_compile main.py simulate.py
```

If the bug only appears in interactive mode, say that explicitly and note what was or was not verified headlessly.
