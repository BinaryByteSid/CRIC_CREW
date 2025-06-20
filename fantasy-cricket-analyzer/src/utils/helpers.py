def normalize_scores(scores):
    max_score = max(scores)
    return [score / max_score for score in scores]

def weight_scores(scores, weights):
    return sum(score * weight for score, weight in zip(scores, weights))

def calculate_average(scores):
    return sum(scores) / len(scores) if scores else 0

def filter_players_by_threshold(players, threshold):
    return [player for player in players if player['score'] >= threshold]