# AI Experiment Summary

- Matches per AI: 20
- Seed: 42
- Player strategy: `balanced`
- Map: `fixed_lane`

| AI Profile | Win % | AI HP Avg | Damage to Player Base | Resource Eff | Attack Avg | Defense Avg | Main Lane | Decision ms Avg |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| random_balanced | 0.0 | 301.5 | 20.3 | 0.004 | 94.4 | 8.4 | 0 | 0.0781 |
| rule_based_balanced | 0.0 | 254.2 | 45.2 | 0.010 | 87.0 | 2.1 | 0 | 0.0347 |
| heuristic_defensive | 0.0 | 362.0 | 26.8 | 0.006 | 89.2 | 3.0 | 1 | 0.4758 |
| heuristic_balanced | 0.0 | 263.2 | 26.8 | 0.006 | 109.0 | 1.6 | 1 | 0.3609 |
| heuristic_aggressive | 0.0 | 244.2 | 26.8 | 0.006 | 121.0 | 0.0 | 1 | 0.3710 |

## Notes

- `Damage to Player Base` only counts base damage after metric cleanup.
- `Resource Eff` = AI base damage dealt / AI resource spent.
- The scripted player is a controlled test opponent, not a human-level player.
