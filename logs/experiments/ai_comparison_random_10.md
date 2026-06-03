# AI Experiment Summary

- Matches per AI: 10
- Seed: 42
- Player strategy: `random`
- Map: `fixed_lane`

| AI Profile | Win % | AI HP Avg | Damage to Player Base | Resource Eff | Attack Avg | Defense Avg | Main Lane | Decision ms Avg |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| random_balanced | 0.0 | 299.4 | 47.2 | 0.010 | 92.2 | 10.9 | 0 | 0.0644 |
| rule_based_balanced | 0.0 | 206.8 | 153.6 | 0.042 | 61.3 | 7.5 | 0 | 0.0184 |
| heuristic_defensive | 0.0 | 99.2 | 128.0 | 0.028 | 113.7 | 2.4 | 0 | 0.2727 |
| heuristic_balanced | 0.0 | 88.7 | 134.0 | 0.029 | 121.0 | 0.0 | 0 | 0.2422 |
| heuristic_aggressive | 0.0 | 165.2 | 140.8 | 0.030 | 110.1 | 4.0 | 0 | 0.2440 |

## Notes

- `Damage to Player Base` only counts base damage after metric cleanup.
- `Resource Eff` = AI base damage dealt / AI resource spent.
- The scripted player is a controlled test opponent, not a human-level player.
