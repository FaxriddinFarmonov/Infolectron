from django.core.cache import cache

SESSION_KEY = "game_session:{user_id}:{game_id}"


def start_game_session(user_id, game_id, duration):
    key = SESSION_KEY.format(user_id=user_id, game_id=game_id)

    cache.set(
        key,
        {
            "score": 0,
            "started": True,
        },
        timeout=duration
    )


def get_game_session(user_id, game_id):
    key = SESSION_KEY.format(user_id=user_id, game_id=game_id)
    return cache.get(key)


def end_game_session(user_id, game_id):
    key = SESSION_KEY.format(user_id=user_id, game_id=game_id)
    cache.delete(key)

