from django.core.cache import cache

class LessonViewService:
    @staticmethod
    def increase_view(lesson_id: str):
        key = f"lesson:view:{lesson_id}"

        # agar key yo‘q bo‘lsa → 0 qilib qo‘yamiz
        if cache.get(key) is None:
            cache.set(key, 0)

        cache.incr(key)

    @staticmethod
    def get_views(lesson_id: str) -> int:
        key = f"lesson:view:{lesson_id}"
        return cache.get(key, 0)
