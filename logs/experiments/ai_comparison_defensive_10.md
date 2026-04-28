# AI Experiment Summary

- Matches per AI: 10
- Seed: 42
- Player strategy: `defensive`
- Map: `fixed_lane`

| AI Profile | Win % | AI HP Avg | Damage to Player Base | Resource Eff | Attack Avg | Defense Avg | Main Lane | Decision ms Avg |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| random_balanced | 40.0 | 424.5 | 43.1 | 0.009 | 92.2 | 11.6 | 1 | 0.1100 |
| rule_based_balanced | 0.0 | 283.5 | 83.2 | 0.018 | 92.0 | 0.0 | 0 | 0.0352 |
| heuristic_defensive | 90.0 | 475.5 | 36.5 | 0.008 | 75.3 | 3.0 | 0 | 0.7648 |
| heuristic_balanced | 40.0 | 408.5 | 36.5 | 0.008 | 99.6 | 2.1 | 0 | 0.5280 |
| heuristic_aggressive | 0.0 | 284.0 | 36.5 | 0.008 | 121.0 | 0.0 | 1 | 0.3174 |

## Notes

- `Damage to Player Base` only counts base damage after metric cleanup.
- `Resource Eff` = AI base damage dealt / AI resource spent.
- The scripted player is a controlled test opponent, not a human-level player.
