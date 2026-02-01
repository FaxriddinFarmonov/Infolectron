def calculate_score(game, correct_count, total):
    ratio = correct_count / total
    return int(game.max_score * ratio)
