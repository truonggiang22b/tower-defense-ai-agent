# AI Experiment Summary

- Matches per AI: 10
- Seed: 42
- Player strategy: `early_attacker`
- Map: `fixed_lane`

| AI Profile | Win % | AI HP Avg | Damage to Player Base | Resource Eff | Attack Avg | Defense Avg | Main Lane | Decision ms Avg |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| random_balanced | 100.0 | 198.0 | 500.0 | 0.129 | 76.4 | 8.6 | 0 | 0.0659 |
| rule_based_balanced | 100.0 | 230.0 | 378.4 | 0.118 | 47.3 | 9.0 | 0 | 0.0144 |
| heuristic_defensive | 100.0 | 149.0 | 500.0 | 0.154 | 85.0 | 0.0 | 0 | 0.1688 |
| heuristic_balanced | 100.0 | 149.0 | 500.0 | 0.154 | 85.0 | 0.0 | 0 | 0.1734 |
| heuristic_aggressive | 100.0 | 149.0 | 500.0 | 0.154 | 85.0 | 0.0 | 0 | 0.1913 |

## Notes

- `Damage to Player Base` only counts base damage after metric cleanup.
- `Resource Eff` = AI base damage dealt / AI resource spent.
- The scripted player is a controlled test opponent, not a human-level player.
