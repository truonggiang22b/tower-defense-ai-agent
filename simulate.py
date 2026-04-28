"""
CLI entry point for headless AI simulations and experiment exports.
"""
import sys

from src.simulation.simulation import (
    run_comparison,
    run_experiment_suite,
    run_simulation,
)


def main():
    n = 20
    seed = 42
    player_strategy = "balanced"

    for i, arg in enumerate(sys.argv):
        if arg in ("-n", "--num") and i + 1 < len(sys.argv):
            n = int(sys.argv[i + 1])
        elif arg == "--seed" and i + 1 < len(sys.argv):
            seed = int(sys.argv[i + 1])
        elif arg == "--player" and i + 1 < len(sys.argv):
            player_strategy = sys.argv[i + 1]

    if "--experiment" in sys.argv:
        run_experiment_suite(num_matches=n, seed=seed, player_strategy=player_strategy)
        return

    if "--compare" in sys.argv or "-c" in sys.argv:
        run_comparison(num_matches=n, seed=seed, player_strategy=player_strategy)
        return

    ai_type = "heuristic"
    profile = "balanced"
    for arg in sys.argv[1:]:
        if arg in ("random", "rule_based", "heuristic"):
            ai_type = arg
        elif arg in ("defensive", "aggressive", "balanced"):
            profile = arg

    run_simulation(
        ai_type,
        profile,
        num_matches=n,
        seed=seed,
        verbose=True,
        player_strategy=player_strategy,
    )


if __name__ == "__main__":
    main()
