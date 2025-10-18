"""This module hosts the business logic of the application."""

import random
import sqlite3
from datetime import UTC, datetime

from .settings import DB_PATH
from .types import Banner
from .utils import get_hours_quarter


class DBConnection:
    """Database connection context manager."""

    def __init__(self):
        """Init."""
        self.conn = None

    def __enter__(self):
        """Enter."""
        self.conn = sqlite3.connect(DB_PATH)
        self.conn.row_factory = sqlite3.Row
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit."""
        if self.conn:
            self.conn.close()


class BannerSelectorSQL:
    """Retrieve Banners from DB."""

    def __init__(self, connection: sqlite3.Connection):
        """Init."""
        self.con = connection
        self.cur = connection.cursor()

    def _execute_query(self, query: str, params: tuple = ()) -> list[sqlite3.Row]:
        self.cur.execute(query, params)
        return [row for row in self.cur.fetchall()]

    @property
    def current_quarter(self):
        """Get current quarter of the hour."""
        return get_hours_quarter(datetime.now(UTC))

    def _get_top_by_revenue(
        self, campaign_id: int, n: int, exclude: list[int]
    ) -> list[sqlite3.Row]:
        """Returns top N banners by revenue, excluding specified banners."""
        placeholders = ",".join("?" for _ in exclude)
        query = f"""
            SELECT
                c.banner_id,
                COUNT(c.click_id) as clicks,
                c.campaign_id,
                c.quarter
            FROM Conversions conv
            JOIN Clicks c ON conv.click_id = c.click_id
            WHERE c.campaign_id = ? AND c.quarter = ?
            AND c.banner_id NOT IN ({placeholders})
            GROUP BY c.banner_id
            ORDER BY SUM(conv.revenue) DESC
            LIMIT ?
        """
        params = (campaign_id, self.current_quarter, *exclude, n)
        return self._execute_query(query, params)

    def _get_top_by_clicks(
        self, campaign_id: int, n: int, exclude: list[int]
    ) -> list[sqlite3.Row]:
        """Returns top N banners by click count, excluding specified banners."""
        placeholders = ",".join("?" for _ in exclude)
        query = f"""
            SELECT
                banner_id,
                COUNT(click_id) as clicks,
                campaign_id,
                quarter,
            FROM Clicks
            WHERE campaign_id = ? AND c.quarter = ?
            AND banner_id NOT IN ({placeholders})
            GROUP BY banner_id
            ORDER BY COUNT(click_id) DESC
            LIMIT ?
        """
        params = (campaign_id, self.current_quarter, *exclude, n)
        return self._execute_query(query, params)

    def _get_random_banners(
        self, campaign_id: int, n: int, exclude: list[int]
    ) -> list[sqlite3.Row]:
        """Returns N random banners, excluding specified banners."""
        placeholders = ",".join("?" for _ in exclude)
        query = f"""
            SELECT
                DISTINCT banner_id,
                COUNT(click_id) as clicks,
                campaign_id,
                quarter,
            FROM Clicks
            WHERE campaign_id = ? AND c.quarter = ?
            AND banner_id NOT IN ({placeholders})
            ORDER BY RANDOM()
            LIMIT ?
        """
        params = (campaign_id, self.current_quarter, *exclude, n)
        return self._execute_query(query, params)

    def get_campaign_banners(
        self, campaign_id: int, seen_banners: list[int] = []
    ) -> list[Banner]:
        """Determines which banners to show for a campaign based on business rules."""
        exclude_banners = seen_banners if seen_banners else [-1]
        final_banners = []

        # Calculate X (number of banners with conversions)
        query_x = """
            SELECT COUNT(DISTINCT c.banner_id)
            FROM Conversions conv
            JOIN Clicks c ON conv.click_id = c.click_id
            WHERE c.campaign_id = ? AND c.quarter = ?
        """
        self.cur.execute(query_x, (campaign_id, self.current_quarter))
        X = self.cur.fetchone()[0]

        # Apply Business Rules
        if X >= 10:
            final_banners = self._get_top_by_revenue(campaign_id, 10, exclude_banners)

        elif 5 <= X < 10:
            final_banners = self._get_top_by_revenue(campaign_id, X, exclude_banners)

        elif 1 <= X < 5:
            revenue_banners = self._get_top_by_revenue(campaign_id, X, exclude_banners)
            final_banners.extend(revenue_banners)

            needed = 5 - len(final_banners)
            if needed > 0:
                current_exclude = exclude_banners + [
                    row["banner_id"] for row in final_banners
                ]
                click_banners = self._get_top_by_clicks(
                    campaign_id, needed, current_exclude
                )
                final_banners.extend(click_banners)

        else:  # X == 0
            click_banners = self._get_top_by_clicks(campaign_id, 5, exclude_banners)
            final_banners.extend(click_banners)

            needed = 5 - len(final_banners)
            if needed > 0:
                current_exclude = exclude_banners + [
                    row["banner_id"] for row in final_banners
                ]
                random_banners = self._get_random_banners(
                    campaign_id, needed, current_exclude
                )
                final_banners.extend(random_banners)

        banners = [
            Banner(
                id=row["banner_id"],
                click=row["clicks"] if "clicks" in row else 0,
                banner=row["banner_id"],
                campaign=row["campaign_id"],
                quarter=row["quarter"],
            )
            for row in final_banners
        ]
        random.shuffle(banners)
        return banners

    def get_all_banners(self):
        """Retrieve all available banners from DB."""
        query = """
        SELECT DISTINCT
            c.banner_id as id,
            COUNT(c.click_id) as click,
            c.banner_id as banner,
            c.campaign_id as campaign,
            c.quarter
        FROM clicks c
        GROUP BY c.banner_id, c.campaign_id, c.quarter
        """

        rows = self._execute_query(query)

        return [
            Banner(
                id=row["id"],
                click=row["click"],
                banner=row["banner"],
                campaign=row["campaign"],
                quarter=row["quarter"],
            )
            for row in rows
        ]


def get_all_banners() -> list[Banner]:
    """Return all banners from the database.

    Returns:
        list[Banner]: List of all banners with their click counts and campaign info
    """
    with DBConnection() as conn:
        banner_selector = BannerSelectorSQL(conn)
        banners = banner_selector.get_all_banners()
    return banners


def get_campaign(campaign: int, seen_banners: list[int] = []) -> list[Banner]:
    """Return banners for a campaign according to business rules.

    Returns:
        list[Banner]: List of all banners with their click counts and campaign info
    """
    with DBConnection() as conn:
        banner_selector = BannerSelectorSQL(conn)
        banners = banner_selector.get_campaign_banners(campaign, seen_banners)
    return banners
