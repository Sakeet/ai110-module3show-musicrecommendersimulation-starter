import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file into a list of dictionaries."""
    print(f"Loading songs from {csv_path}...")

    songs: List[Dict] = []
    numeric_fields = {
        "id": int,
        "energy": float,
        "tempo_bpm": int,
        "valence": float,
        "danceability": float,
        "acousticness": float,
        "popularity": int,
        "release_year": int,
        "instrumentalness": float,
        "lyrical_intensity": float,
        "freshness": float,
    }

    with open(csv_path, newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            song: Dict = {}
            for key, value in row.items():
                if key in numeric_fields:
                    song[key] = numeric_fields[key](value)
                else:
                    song[key] = value
            songs.append(song)

    return songs

def _score_song_components(user_prefs: Dict, song: Dict) -> Tuple[float, List[str], Dict[str, float]]:
    """Score one song and return both the explanation and the component breakdown."""
    score = 0.0
    reasons: List[str] = []
    components: Dict[str, float] = {}

    user_genre = user_prefs.get("genre", user_prefs.get("favorite_genre", ""))
    user_mood = user_prefs.get("mood", user_prefs.get("favorite_mood", ""))
    target_energy = float(user_prefs.get("energy", user_prefs.get("target_energy", 0.0)))
    likes_acoustic = bool(user_prefs.get("likes_acoustic", False))

    song_genre = str(song.get("genre", ""))
    song_mood = str(song.get("mood", ""))

    genre_match = 1.0 if song_genre.lower() == str(user_genre).lower() and user_genre != "" else 0.0
    if genre_match:
        score += 1.0
        reasons.append("genre match (+1.0)")
    components["genre_match"] = genre_match

    mood_match = 1.0 if song_mood.lower() == str(user_mood).lower() and user_mood != "" else 0.0
    if mood_match:
        score += 1.0
        reasons.append("mood match (+1.0)")
    components["mood_match"] = mood_match

    song_energy = float(song.get("energy", 0.0))
    energy_similarity = max(0.0, 1.0 - abs(song_energy - target_energy))
    energy_points = energy_similarity * 4.0
    score += energy_points
    reasons.append(f"energy closeness (+{energy_points:.2f})")
    components["energy_points"] = energy_points

    song_acousticness = float(song.get("acousticness", 0.0))
    acoustic_bonus = song_acousticness * 0.5 if likes_acoustic else (1.0 - song_acousticness) * 0.5
    score += acoustic_bonus
    if likes_acoustic:
        reasons.append(f"acoustic preference (+{acoustic_bonus:.2f})")
    else:
        reasons.append(f"non-acoustic preference (+{acoustic_bonus:.2f})")
    components["acoustic_bonus"] = acoustic_bonus

    tempo_target = float(user_prefs.get("tempo_bpm", song.get("tempo_bpm", 0)))
    tempo_points = max(0.0, 1.0 - abs(float(song.get("tempo_bpm", 0)) - tempo_target) / 200.0) * 0.25
    score += tempo_points
    reasons.append(f"tempo closeness (+{tempo_points:.2f})")
    components["tempo_points"] = tempo_points

    valence_target = float(user_prefs.get("valence", song.get("valence", 0.0)))
    valence_points = max(0.0, 1.0 - abs(float(song.get("valence", 0.0)) - valence_target)) * 0.15
    score += valence_points
    reasons.append(f"valence closeness (+{valence_points:.2f})")
    components["valence_points"] = valence_points

    danceability_target = float(user_prefs.get("danceability", song.get("danceability", 0.0)))
    danceability_points = max(0.0, 1.0 - abs(float(song.get("danceability", 0.0)) - danceability_target)) * 0.15
    score += danceability_points
    reasons.append(f"danceability closeness (+{danceability_points:.2f})")
    components["danceability_points"] = danceability_points

    popularity_target = float(user_prefs.get("popularity", 50.0))
    popularity_points = max(0.0, 1.0 - abs(float(song.get("popularity", 50.0)) - popularity_target) / 100.0) * 0.08
    score += popularity_points
    reasons.append(f"popularity closeness (+{popularity_points:.2f})")
    components["popularity_points"] = popularity_points

    release_year_target = float(user_prefs.get("release_year", 2020.0))
    release_year_points = max(0.0, 1.0 - abs(float(song.get("release_year", 2020.0)) - release_year_target) / 20.0) * 0.08
    score += release_year_points
    reasons.append(f"release year closeness (+{release_year_points:.2f})")
    components["release_year_points"] = release_year_points

    instrumentalness_target = float(user_prefs.get("instrumentalness", 0.5))
    instrumentalness_points = max(0.0, 1.0 - abs(float(song.get("instrumentalness", 0.5)) - instrumentalness_target)) * 0.05
    score += instrumentalness_points
    reasons.append(f"instrumentalness closeness (+{instrumentalness_points:.2f})")
    components["instrumentalness_points"] = instrumentalness_points

    lyrical_intensity_target = float(user_prefs.get("lyrical_intensity", 0.5))
    lyrical_intensity_points = max(0.0, 1.0 - abs(float(song.get("lyrical_intensity", 0.5)) - lyrical_intensity_target)) * 0.05
    score += lyrical_intensity_points
    reasons.append(f"lyrical intensity closeness (+{lyrical_intensity_points:.2f})")
    components["lyrical_intensity_points"] = lyrical_intensity_points

    freshness_target = float(user_prefs.get("freshness", 0.5))
    freshness_points = max(0.0, 1.0 - abs(float(song.get("freshness", 0.5)) - freshness_target)) * 0.05
    score += freshness_points
    reasons.append(f"freshness closeness (+{freshness_points:.2f})")
    components["freshness_points"] = freshness_points

    components["score"] = score
    return score, reasons, components

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against the user preferences and explain why."""
    score, reasons, _ = _score_song_components(user_prefs, song)
    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5, ranking_mode: str = "balanced") -> List[Tuple[Dict, float, str]]:
    """Rank songs by score and return the top k recommendations."""
    scored_songs = []
    for song in songs:
        score, reasons, components = _score_song_components(user_prefs, song)
        scored_songs.append([song, score, ", ".join(reasons), components])

    ranked: List[Tuple[Dict, float, str]] = []
    artist_counts: Dict[str, int] = {}

    valid_modes = {"balanced", "genre_first", "energy_first"}
    if ranking_mode not in valid_modes:
        raise ValueError(f"Unknown ranking mode: {ranking_mode}")

    while scored_songs and len(ranked) < k:
        best_index = 0
        best_score = float("-inf")

        for index, item in enumerate(scored_songs):
            song, base_score, explanation, components = item
            artist = str(song.get("artist", ""))
            diversity_penalty = artist_counts.get(artist, 0) * 0.5
            adjusted_score = base_score - diversity_penalty

            if ranking_mode == "genre_first":
                adjusted_score += components.get("genre_match", 0.0) * 100.0
                adjusted_score += components.get("mood_match", 0.0) * 10.0
            elif ranking_mode == "energy_first":
                adjusted_score += components.get("energy_points", 0.0) * 100.0

            if adjusted_score > best_score:
                best_score = adjusted_score
                best_index = index

        song, base_score, explanation, components = scored_songs.pop(best_index)
        artist = str(song.get("artist", ""))
        diversity_penalty = artist_counts.get(artist, 0) * 0.5
        final_score = base_score - diversity_penalty

        if diversity_penalty > 0:
            explanation = f"{explanation}, artist diversity penalty (-{diversity_penalty:.2f})"

        ranked.append((song, final_score, explanation))
        artist_counts[artist] = artist_counts.get(artist, 0) + 1

    return ranked
