---
name: tower-defense-experiment-eval
description: Use when running AI comparisons, analyzing batch simulations, summarizing logs, or preparing evaluation results for this tower defense project.
---

# Tower Defense Experiment Eval

Use this skill when the task is about evidence:

- compare `random`, `rule_based`, and `heuristic`
- summarize `logs/*.json`
- prepare experiment tables for the report
- verify whether an AI change actually improved behavior

## First Reads

- `docs_tower_defense_ai_project/05 - Thực nghiệm, chỉ số và đánh giá.md`
- `docs_tower_defense_ai_project/06 - Lộ trình, rủi ro và sản phẩm bàn giao.md`
- `README.md`
- `src/simulation/simulation.py`
- `src/systems/game_logger.py`

## Evaluation Workflow

1. Define the comparison clearly.
Example: baseline vs changed heuristic, or all AI profiles under the same seed.
2. Keep test conditions aligned:
- same seed
- same number of matches
- same opponent policy
- same map assumptions
3. Run the batch or comparison command.
4. Read generated summaries in `logs/`.
5. Report both outcomes and caveats.

## Default Commands

```powershell
python simulate.py random
python simulate.py rule_based
python simulate.py heuristic balanced
python simulate.py --compare
```

If you need a larger sample, prefer changing match count in one place and documenting it in the result.

## Metrics To Prefer

Use project-native metrics before inventing new ones:

- `winner`
- `match_duration`
- `player_base_hp_end`
- `ai_base_hp_end`
- `damage_to_player_base`
- `damage_to_ai_base`
- `resource_spent_ai`
- `resource_efficiency_ai`
- `ai_decision_time_avg_ms`
- `ai_attack_count`, `ai_defense_count`, `ai_economy_count`

These come from `GameLogger` records and batch outputs.

## Interpretation Rules

- Separate observed metrics from inference.
- Do not overclaim on small samples.
- If win rate improves but efficiency or survivability worsens, say so.
- Prefer compact tables and short conclusions over long prose.
- If simulation opponent behavior is simplistic, mention that limitation.

## Guardrails

- Do not mix code changes and experiment conclusions without rerunning the simulation.
- Do not compare runs with different seeds or match counts as if they were equivalent.
- Do not replace project metrics with ad hoc subjective judgments.
