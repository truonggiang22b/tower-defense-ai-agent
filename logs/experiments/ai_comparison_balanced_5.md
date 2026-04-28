# AI Experiment Summary

- Matches per AI: 5
- Seed: 42
- Player strategy: `balanced`
- Map: `fixed_lane`

| AI Profile | Win % | AI HP Avg | Damage to Player Base | Resource Eff | Attack Avg | Defense Avg | Main Lane | Decision ms Avg |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| random_balanced | 0.0 | 304.0 | 14.4 | 0.003 | 94.2 | 9.2 | 1 | 0.1481 |
| rule_based_balanced | 0.0 | 250.0 | 51.2 | 0.011 | 85.8 | 3.0 | 0 | 0.0328 |
| heuristic_defensive | 0.0 | 363.0 | 28.0 | 0.006 | 90.0 | 3.0 | 1 | 0.4345 |
| heuristic_balanced | 0.0 | 263.0 | 28.0 | 0.006 | 108.0 | 2.2 | 1 | 0.3500 |
| heuristic_aggressive | 0.0 | 239.0 | 28.0 | 0.006 | 121.0 | 0.0 | 1 | 0.3503 |

## Notes

- `Damage to Player Base` only counts base damage after metric cleanup.
- `Resource Eff` = AI base damage dealt / AI resource spent.
- The scripted player is a controlled test opponent, not a human-level player.
