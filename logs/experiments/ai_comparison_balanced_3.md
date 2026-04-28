# AI Experiment Summary

- Matches per AI: 3
- Seed: 42
- Player strategy: `balanced`
- Map: `fixed_lane`

| AI Profile | Win % | AI HP Avg | Damage to Player Base | Resource Eff | Attack Avg | Defense Avg | Decision ms Avg |
|---|---:|---:|---:|---:|---:|---:|---:|
| random_balanced | 0.0 | 425.0 | 9.7 | 0.002 | 82.0 | 20.0 | 0.0683 |
| rule_based_balanced | 0.0 | 251.7 | 48.0 | 0.011 | 86.7 | 2.3 | 0.0217 |
| heuristic_defensive | 33.3 | 498.3 | 1.7 | 0.001 | 82.7 | 3.0 | 0.2670 |
| heuristic_balanced | 0.0 | 436.7 | 3.3 | 0.001 | 83.3 | 3.0 | 0.2757 |
| heuristic_aggressive | 0.0 | 360.0 | 3.3 | 0.001 | 118.0 | 3.0 | 0.2791 |

## Notes

- `Damage to Player Base` only counts base damage after metric cleanup.
- `Resource Eff` = AI base damage dealt / AI resource spent.
- The scripted player is a controlled test opponent, not a human-level player.
