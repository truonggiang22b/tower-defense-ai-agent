# Asset pipeline

The game can run without external image files because `src/ui/assets.py` creates procedural fallbacks.

To replace a fallback with a real bitmap asset, add files with these names:

- `assets/icons/tower_fast.png`
- `assets/icons/tower_heavy.png`
- `assets/icons/tower_balanced.png`
- `assets/icons/unit_fast.png`
- `assets/icons/unit_tank.png`
- `assets/icons/unit_swarm.png`
- `assets/bases/player_base.png`
- `assets/bases/ai_base.png`

Recommended constraints:

- Use transparent PNG for icons and bases.
- Do not include text inside bitmap assets.
- Keep icons readable at 24-40 px.
- Keep base sprites readable around 92x132 px.
