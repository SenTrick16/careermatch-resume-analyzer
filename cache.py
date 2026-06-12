from datetime import datetime, timedelta
import hashlib


class AnalysisCache:
    def __init__(self):
        self.cache = {}

    def generate_key(self, resume: str, job_desc: str) -> str:
        """
        Generate unique cache key from resume and job description
        """
        combined = f"{resume}|{job_desc}"
        return hashlib.md5(combined.encode()).hexdigest()

    def get(self, key: str):
        """
        Get cached result if it exists and is not expired
        """
        if key in self.cache:
            timestamp, result = self.cache[key]

            # Cache valid for 1 hour
            if datetime.now() - timestamp < timedelta(hours=1):
                return result

            # Remove expired cache
            del self.cache[key]

        return None

    def set(self, key: str, value):
        """
        Store result in cache
        """
        self.cache[key] = (
            datetime.now(),
            value
        )

    def clear(self):
        """
        Clear all cached results
        """
        self.cache.clear()

    def size(self):
        """
        Return number of cached items
        """
        return len(self.cache)