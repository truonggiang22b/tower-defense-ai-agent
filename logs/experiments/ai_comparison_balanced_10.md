# AI Experiment Summary

- Matches per AI: 10
- Seed: 42
- Player strategy: `balanced`
- Map: `fixed_lane`

| AI Profile | Win % | AI HP Avg | Damage to Player Base | Resource Eff | Attack Avg | Defense Avg | Main Lane | Decision ms Avg |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| random_balanced | 0.0 | 309.5 | 16.1 | 0.004 | 95.3 | 8.5 | 1 | 0.0397 |
| rule_based_balanced | 0.0 | 255.5 | 48.8 | 0.011 | 86.2 | 2.5 | 0 | 0.0117 |
| heuristic_defensive | 70.0 | 388.5 | 120.8 | 0.025 | 84.6 | 9.4 | 2 | 0.2029 |
| heuristic_balanced | 70.0 | 392.0 | 123.4 | 0.026 | 103.3 | 4.1 | 2 | 0.2040 |
| heuristic_aggressive | 30.0 | 354.0 | 123.4 | 0.026 | 99.5 | 5.0 | 2 | 0.2346 |

## Notes

- `Damage to Player Base` only counts base damage after metric cleanup.
- `Resource Eff` = AI base damage dealt / AI resource spent.
- The scripted player is a controlled test opponent, not a human-level player.
