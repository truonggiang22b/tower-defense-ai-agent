---
name: tower-defense-ai-tuning
description: Use when changing AI behavior, heuristic scoring, lane summaries, candidate generation, AI profiles, or difficulty in this tower defense project, and validate changes with simulation metrics.
---

# Tower Defense AI Tuning

Use this skill for work in:

- `src/ai/ai_agent.py`
- `src/ai/heuristic_evaluator.py`
- AI-related parts of `src/models/game_state.py`
- simulation or logging code needed to measure AI changes

This repo's intended AI path is rule-based plus heuristic plus greedy selection. Treat that as the default target, not advanced learning systems.

## First Reads

- `docs_tower_defense_ai_project/02 - Mô hình hóa AI và thiết kế ra quyết định.md`
- `docs_tower_defense_ai_project/03 - Thuật toán AI và đánh đổi.md`
- `README.md`
- `src/ai/ai_agent.py`
- `src/ai/heuristic_evaluator.py`
- `src/simulation/simulation.py`
- `src/systems/game_logger.py`

## Tuning Workflow

1. State the hypothesis in one line.
Example: "Heuristic AI overbuilds and attacks too late because defense rewards dominate."
2. Find the narrowest place to change.
3. Prefer small, explainable edits:
- candidate action generation
- lane summary features
- thresholds
- profile weights
- action-specific scoring
4. Keep `RandomAI` and `RuleBasedAI` as baselines.
5. Run simulation and compare before and after.
6. Summarize outcome with metrics, not only impression.

## Default Metrics

Use the project's existing outputs first:

- AI win rate
- end-match AI base HP
- resource efficiency
- action mix: attack, defense, economy
- decision time average and max

Relevant files:

- `src/simulation/simulation.py`
- `src/systems/game_logger.py`
- `logs/`

## Guardrails

- Do not remove the baseline AIs.
- Do not add opaque "magic" bonuses without a readable rationale.
- Do not claim improvement from one or two anecdotal matches.
- Do not jump to GA, RL, minimax, or lookahead unless the user explicitly asks.
- If you change summary features or action semantics, update logger and simulation expectations too.

## Validation Commands

Start with a targeted run, then compare:

```powershell
python simulate.py heuristic balanced
python simulate.py heuristic defensive
python simulate.py heuristic aggressive
python simulate.py --compare
```

If results are noisy, increase match count by editing the simulation invocation or code in a minimal, reversible way.

## Reporting Format

When closing the task, report:

- what changed
- which AI profiles were tested
- before/after metrics if available
- any remaining tradeoff, such as stronger offense but lower AI survivability
