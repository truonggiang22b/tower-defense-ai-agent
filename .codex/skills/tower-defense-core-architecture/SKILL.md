---
name: tower-defense-core-architecture
description: Use when changing gameplay architecture, data flow, or shared contracts in this tower defense project, especially around GameState, Action, GameEngine, AI integration, systems, or UI boundaries.
---

# Tower Defense Core Architecture

Use this skill when a request touches core gameplay structure rather than a one-off bug. Typical triggers: adding a mechanic, moving logic between modules, changing `GameState`, changing `Action` semantics, adding a new system, or refactoring code across `src/models`, `src/engine`, `src/systems`, `src/ai`, or `src/ui`.

## First Reads

Read only the files needed for the task, starting here:

- `docs_tower_defense_ai_project/README - Hướng dẫn bộ tài liệu.md`
- `docs_tower_defense_ai_project/04 - Kiến trúc hệ thống và mô hình dữ liệu.md`
- `README.md`
- `src/models/game_state.py`
- `src/engine/game_engine.py`

Then load the narrow module you are about to change.

## Core Contracts

Preserve these project rules unless the user explicitly asks to redesign them:

- `GameState` is the central source of truth.
- AI reads state and returns `Action`; it does not execute gameplay directly.
- `GameEngine` validates and executes actions, updates systems, and ends matches.
- `GameLogger` and simulation must remain compatible with gameplay changes.
- `UIManager` renders and forwards input; gameplay rules should stay out of UI code.
- The default project scope is fixed-lane MVP, not grid pathfinding.

If you must change a contract, update every dependent layer in the same pass:

- `src/models/game_state.py`
- `src/engine/game_engine.py`
- affected manager/system files
- `src/ai/ai_agent.py`
- `src/ai/heuristic_evaluator.py` if AI state features changed
- `src/systems/game_logger.py`
- `src/simulation/simulation.py`
- `README.md` if behavior or commands changed

## Working Pattern

1. Identify which layer owns the behavior.
2. Change the lowest correct layer first.
3. Keep public structures explicit and small.
4. Avoid duplicating state across engine, AI, and UI.
5. Re-run the narrowest validation that proves the contract still holds.

Ownership guide:

- `src/models/`: enums, configs, dataclasses, shared state shape
- `src/engine/`: tick order, AI step timing, action execution, match lifecycle
- `src/systems/`: movement, combat, resource spending, tower behavior, logging
- `src/ai/`: candidate generation, heuristics, AI profiles
- `src/ui/`: rendering and player controls only

## Architecture Guardrails

- Do not add RL, GA, minimax, or grid A* as a default path unless explicitly requested.
- Do not hide design problems inside UI code.
- Do not make AI mutate engine state directly.
- Do not add new mechanics without deciding whether they belong in `GameState`, `Action`, logs, and simulation.
- Prefer additive, explainable changes over large rewrites.

## Validation

Use the lightest command that covers the change:

```powershell
python simulate.py heuristic balanced
python simulate.py --compare
python -m py_compile main.py simulate.py
```

For architecture changes, validation is incomplete if simulation, logging, or action execution silently break.
