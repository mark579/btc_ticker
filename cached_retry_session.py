from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from requests_cache import CachedSession


class CachedRetrySession:
    def __init__(self, cache_name, expire_after,
                 total_retries, backoff_factor):
        self.retry_strategy = Retry(
            total=total_retries,
            backoff_factor=backoff_factor,
        )
        self.adapter = HTTPAdapter(max_retries=self.retry_strategy)
        self.http = CachedSession(cache_name, expire_after=expire_after)
        self.http.mount("https://", self.adapter)
        self.http.mount("http://", self.adapter)

    def get_session(self):
        return self.http
