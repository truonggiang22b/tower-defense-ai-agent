# AI Experiment Summary

- Matches per AI: 10
- Seed: 42
- Player strategy: `defensive`
- Map: `fixed_lane`

| AI Profile | Win % | AI HP Avg | Damage to Player Base | Resource Eff | Attack Avg | Defense Avg | Main Lane | Decision ms Avg |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| random_balanced | 40.0 | 424.5 | 43.1 | 0.009 | 92.2 | 11.6 | 1 | 0.0623 |
| rule_based_balanced | 0.0 | 283.5 | 83.2 | 0.018 | 92.0 | 0.0 | 0 | 0.0192 |
| heuristic_defensive | 100.0 | 475.0 | 62.0 | 0.013 | 74.1 | 6.9 | 0 | 0.4162 |
| heuristic_balanced | 100.0 | 465.0 | 62.0 | 0.013 | 96.4 | 3.0 | 0 | 0.3311 |
| heuristic_aggressive | 0.0 | 363.5 | 59.1 | 0.013 | 103.3 | 4.9 | 1 | 0.2514 |

## Notes

- `Damage to Player Base` only counts base damage after metric cleanup.
- `Resource Eff` = AI base damage dealt / AI resource spent.
- The scripted player is a controlled test opponent, not a human-level player.
