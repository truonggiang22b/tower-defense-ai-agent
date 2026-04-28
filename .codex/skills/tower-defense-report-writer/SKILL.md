---
name: tower-defense-report-writer
description: Use when drafting report sections, experiment summaries, demo scripts, or slide content for this tower defense AI project based on the project documents, source code, and logged results.
---

# Tower Defense Report Writer

Use this skill when the user wants writing output rather than code changes, especially for:

- report sections
- experiment summaries
- result analysis
- demo scripts
- slide outlines
- conclusions and limitations

## First Reads

Choose only the files needed for the section being written.

Core references:

- `docs_tower_defense_ai_project/00 - Phân tích tổng hợp đề tài.md`
- `docs_tower_defense_ai_project/05 - Thực nghiệm, chỉ số và đánh giá.md`
- `docs_tower_defense_ai_project/07 - Mục lục báo cáo và checklist demo.md`
- `README.md`

Implementation references when needed:

- `src/models/game_state.py`
- `src/engine/game_engine.py`
- `src/ai/ai_agent.py`
- `src/ai/heuristic_evaluator.py`
- `src/simulation/simulation.py`
- `src/systems/game_logger.py`
- `logs/*.json`

## Writing Workflow

1. Identify the target artifact.
Examples: chapter 6, experiment section, 3-minute demo script, 10-slide outline.
2. Collect only evidence already present in docs, code, or logs.
3. Separate:
- implemented facts
- inferred interpretation
- future work
4. Write in academic, concrete language.
5. Keep claims aligned with actual implementation.

## Project-Specific Rules

- Present the project as an academic simulation, not a production game.
- Emphasize state modeling, action design, heuristic logic, and evaluation.
- Do not oversell graphics or UI polish.
- Do not describe advanced algorithms as if they were implemented unless the code proves it.
- When summarizing results, prefer project metrics over vague judgments.

## Preferred Evidence

For technical sections, anchor statements in:

- module boundaries from `README.md`
- AI pipeline from `src/ai/ai_agent.py` and `src/ai/heuristic_evaluator.py`
- evaluation metrics from `src/systems/game_logger.py`
- batch workflow from `src/simulation/simulation.py`
- quantitative outputs from `logs/`

## Useful Output Shapes

Common deliverables this skill should produce well:

- concise subsection draft
- full report chapter outline
- table-ready metric summary
- bullet script for oral demo
- slide-by-slide content skeleton
- conclusion with strengths, limitations, and future work

## Guardrails

- Do not invent numbers.
- Do not state that A*, minimax, GA, or RL were implemented unless verified in code.
- Do not draw conclusions from feelings when logs or metrics are available.
- If data is missing, say what is missing and what can still be concluded.
- Prefer short, direct Vietnamese academic prose unless the user asks for English.
