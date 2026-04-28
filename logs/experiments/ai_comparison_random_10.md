# AI Experiment Summary

- Matches per AI: 10
- Seed: 42
- Player strategy: `random`
- Map: `fixed_lane`

| AI Profile | Win % | AI HP Avg | Damage to Player Base | Resource Eff | Attack Avg | Defense Avg | Main Lane | Decision ms Avg |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| random_balanced | 0.0 | 299.4 | 47.2 | 0.010 | 92.2 | 10.9 | 0 | 0.1177 |
| rule_based_balanced | 0.0 | 206.8 | 153.6 | 0.042 | 61.3 | 7.5 | 0 | 0.0345 |
| heuristic_defensive | 0.0 | 117.3 | 107.0 | 0.023 | 110.2 | 4.5 | 0 | 0.5205 |
| heuristic_balanced | 0.0 | 88.7 | 124.0 | 0.027 | 121.0 | 0.0 | 0 | 0.5160 |
| heuristic_aggressive | 0.0 | 87.2 | 107.0 | 0.023 | 121.0 | 0.0 | 0 | 0.3762 |

## Notes

- `Damage to Player Base` only counts base damage after metric cleanup.
- `Resource Eff` = AI base damage dealt / AI resource spent.
- The scripted player is a controlled test opponent, not a human-level player.
