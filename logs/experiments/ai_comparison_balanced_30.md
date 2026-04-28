# AI Experiment Summary

- Matches per AI: 30
- Seed: 42
- Player strategy: `balanced`
- Map: `fixed_lane`

| AI Profile | Win % | AI HP Avg | Damage to Player Base | Resource Eff | Attack Avg | Defense Avg | Main Lane | Decision ms Avg |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| random_balanced | 0.0 | 302.2 | 19.6 | 0.004 | 94.6 | 8.5 | 0 | 0.0974 |
| rule_based_balanced | 0.0 | 255.2 | 44.8 | 0.010 | 87.9 | 1.8 | 0 | 0.0322 |
| heuristic_defensive | 43.3 | 377.5 | 113.3 | 0.024 | 87.8 | 4.9 | 2 | 0.4135 |
| heuristic_balanced | 16.7 | 340.3 | 118.1 | 0.025 | 100.5 | 4.0 | 1 | 0.3652 |
| heuristic_aggressive | 0.0 | 248.3 | 118.1 | 0.026 | 121.0 | 0.0 | 1 | 0.2644 |

## Notes

- `Damage to Player Base` only counts base damage after metric cleanup.
- `Resource Eff` = AI base damage dealt / AI resource spent.
- The scripted player is a controlled test opponent, not a human-level player.
