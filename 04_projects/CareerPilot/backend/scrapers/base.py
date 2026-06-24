from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class ScrapedJob:
    platform: str
    platform_job_id: str
    url: str
    title: str
    company: str
    location: str
    description: str
    requirements: str = ""
    is_remote: bool = False
    is_easy_apply: bool = False
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    salary_currency: str = "INR"
    posted_at: Optional[datetime] = None
    raw_data: dict = field(default_factory=dict)


class BaseScraper(ABC):
    platform: str = ""

    @abstractmethod
    async def scrape(
        self,
        search_queries: list[str],
        location: str = "",
        max_jobs: int = 100,
        lookback_days: int = 3,
    ) -> list[ScrapedJob]:
        ...

    def deduplicate(self, jobs: list[ScrapedJob]) -> list[ScrapedJob]:
        seen: set[str] = set()
        unique = []
        for job in jobs:
            key = f"{job.platform}:{job.platform_job_id}"
            if key not in seen:
                seen.add(key)
                unique.append(job)
        return unique
