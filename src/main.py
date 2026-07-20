"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

try:
    from .recommender import load_songs, recommend_songs
except ImportError:
    from recommender import load_songs, recommend_songs


HIGH_ENERGY_POP = {"genre": "pop", "mood": "happy", "energy": 0.8}
CHILL_LOFI = {"genre": "lofi", "mood": "chill", "energy": 0.4}
DEEP_INTENSE_ROCK = {"genre": "rock", "mood": "intense", "energy": 0.9}
RANKING_MODE = "balanced"


def print_recommendation_table(recommendations, mode: str) -> None:
    print(f"\nTop recommendations ({mode} mode):\n")
    header = f"{'Rank':<4} {'Title':<22} {'Artist':<16} {'Score':>6}  Reasons"
    print(header)
    print("-" * len(header))

    for rank, rec in enumerate(recommendations, start=1):
        song, score, explanation = rec
        reasons = explanation.replace(", ", " | ")
        title = str(song['title'])[:22]
        artist = str(song['artist'])[:16]
        print(f"{rank:<4} {title:<22} {artist:<16} {score:>6.2f}  {reasons}")


def main() -> None:
    songs = load_songs("data/songs.csv") 

    # Starter example profile
    user_prefs = HIGH_ENERGY_POP

    recommendations = recommend_songs(user_prefs, songs, k=5, ranking_mode=RANKING_MODE)

    print_recommendation_table(recommendations, RANKING_MODE)


if __name__ == "__main__":
    main()
