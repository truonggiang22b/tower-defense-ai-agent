# AI Experiment Summary

- Matches per AI: 8
- Seed: 42
- Player strategy: `balanced`
- Map: `fixed_lane`

| AI Profile | Win % | AI HP Avg | Damage to Player Base | Resource Eff | Attack Avg | Defense Avg | Main Lane | Decision ms Avg |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| random_balanced | 0.0 | 298.1 | 17.5 | 0.004 | 95.1 | 8.4 | 1 | 0.0681 |
| rule_based_balanced | 0.0 | 248.1 | 49.0 | 0.011 | 85.5 | 2.9 | 0 | 0.0278 |
| heuristic_defensive | 62.5 | 402.5 | 121.0 | 0.025 | 91.2 | 3.8 | 2 | 0.3416 |
| heuristic_balanced | 25.0 | 335.6 | 124.2 | 0.026 | 101.1 | 4.4 | 2 | 0.3069 |
| heuristic_aggressive | 0.0 | 236.2 | 124.2 | 0.027 | 121.0 | 0.0 | 1 | 0.2575 |

## Notes

- `Damage to Player Base` only counts base damage after metric cleanup.
- `Resource Eff` = AI base damage dealt / AI resource spent.
- The scripted player is a controlled test opponent, not a human-level player.
