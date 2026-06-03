# AI Experiment Summary

- Matches per AI: 100
- Seed: 42
- Player strategy: `balanced`
- Map: `fixed_lane`

| AI Profile | Win % | AI HP Avg | Damage to Player Base | Resource Eff | Attack Avg | Defense Avg | Main Lane | Decision ms Avg |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| random_balanced | 3.0 | 323.9 | 20.0 | 0.004 | 94.3 | 9.6 | 0 | 0.0491 |
| rule_based_balanced | 0.0 | 256.4 | 39.6 | 0.009 | 89.1 | 1.2 | 0 | 0.0160 |
| heuristic_defensive | 46.0 | 390.1 | 97.8 | 0.021 | 83.3 | 9.2 | 2 | 0.2640 |
| heuristic_balanced | 48.0 | 393.0 | 104.2 | 0.022 | 100.0 | 5.0 | 2 | 0.2381 |
| heuristic_aggressive | 17.0 | 356.2 | 104.3 | 0.022 | 97.6 | 4.9 | 2 | 0.2721 |

## Notes

- `Damage to Player Base` only counts base damage after metric cleanup.
- `Resource Eff` = AI base damage dealt / AI resource spent.
- The scripted player is a controlled test opponent, not a human-level player.
