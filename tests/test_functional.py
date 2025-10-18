"""All functional tests for the advertisement campaign module.

We are using a single file given the size of this project. However,
feel free to start splitting the tests, if you feel it is necessary.

"""

import sqlite3
from datetime import UTC, datetime

import pytest

from ads_campaigns.utils import get_hours_quarter
from ads_campaigns.views import get_all_banners, get_campaign

pytestmark = pytest.mark.campaign


@pytest.mark.dependency(name="s1")
def test_all_banners():
    """Test there is at least one banner."""
    assert len(get_all_banners()) > 0


@pytest.mark.dependency(name="s2", depends=["s1"])
def test_all_banners_5_banner_per_campaign():
    """Test there is at least 5 banners per campaign."""
    banners = get_all_banners()
    campaigns = {b.campaign for b in banners}

    for campaign in campaigns:
        campaign_banners = [b for b in banners if b.campaign == campaign]
        assert (
            len(campaign_banners) >= 5
        ), f"Campaign {campaign} has less than 5 banners"


@pytest.mark.dependency(name="s3", depends=["s2"])
def test_all_banners_has_no_duplicates():
    """Test there are no duplicate banners."""
    banners = get_all_banners()

    assert len(banners) == len(set(banners))


@pytest.mark.dependency(name="s4", depends=["s3"])
def test_all_banners_quarter():
    """Test all banners have a valid quarter."""
    banners = get_all_banners()

    assert not [b.quarter for b in banners if b.quarter not in range(1, 5)]


@pytest.mark.dependency(name="s5", depends=["s4"])
@pytest.mark.parametrize("campaign", range(1, 50))
def test_campaign(campaign):
    """The number of returned banners is at least 5."""
    assert len(get_campaign(campaign)) >= 5


@pytest.mark.dependency(name="s6", depends=["s5"])
@pytest.mark.parametrize("campaign", range(1, 50))
def test_campaign_correct_id(campaign):
    """All banners belong to the requested campaign."""
    banners = get_campaign(campaign)
    assert not [b.campaign for b in banners if b.campaign != campaign]


@pytest.mark.dependency(name="s7", depends=["s6"])
@pytest.mark.parametrize("campaign", range(1, 50))
def test_campaign_no_duplicates(campaign):
    """There are no duplicate banners."""
    banners = get_campaign(campaign)
    assert len(banners) == len(set(banners))


@pytest.mark.dependency(name="s8", depends=["s7"])
@pytest.mark.parametrize("campaign", range(1, 50))
def test_campaign_check_order(campaign):
    """The banners doesn't have the same order in different requests."""
    set_1 = get_campaign(campaign)
    set_2 = get_campaign(campaign)

    assert set_1 != set_2


@pytest.mark.dependency(name="s9", depends=["s8"])
@pytest.mark.parametrize("campaign", range(1, 50))
def test_campaign_quarter(campaign):
    """All banners belong to the current quarter."""
    current_quarter = get_hours_quarter()
    banners = get_campaign(campaign)

    assert not [b.quarter for b in banners if b.quarter != current_quarter]


@pytest.mark.dependency(name="s10", depends=["s9"])
def test_x_minimum_10():
    """Top banners by revenue.

    When X >= 10: Show top 10 banners based on revenue within a
    given campaign.

    X: the number of banners with conversions within a campaign.

    """
    # Query to find a campaign with at least 10 banners with conversions

    current_quarter = get_hours_quarter(datetime.now(UTC))
    conn = sqlite3.connect("src/ads_campaigns/campaign.db")
    cursor = conn.cursor()

    # Find campaigns with 10+ banners with conversions
    query = """
    SELECT c.campaign_id, COUNT(DISTINCT c.banner_id) as banner_count
    FROM clicks c
    JOIN conversions conv ON c.click_id = conv.click_id
    WHERE c.quarter = ?
    GROUP BY c.campaign_id
    HAVING banner_count >= 10
    LIMIT 1
    """

    cursor.execute(query, (current_quarter,))
    result = cursor.fetchone()

    if result:
        campaign_id = result[0]
        banners = get_campaign(campaign_id)

        # Should return exactly 10 banners
        assert len(banners) == 10, f"Expected 10 banners, got {len(banners)}"

        # Verify they are ordered by revenue
        query = """
        SELECT c.banner_id, SUM(conv.revenue) as total_revenue
        FROM clicks c
        JOIN conversions conv ON c.click_id = conv.click_id
        WHERE c.campaign_id = ? AND c.quarter = ?
        GROUP BY c.banner_id
        ORDER BY total_revenue DESC
        LIMIT 10
        """

        cursor.execute(query, (campaign_id, current_quarter))
        expected_banners = cursor.fetchall()
        expected_banner_ids = [b[0] for b in expected_banners]

        # Check that we got the top 10 revenue banners (order may vary due to shuffling)
        actual_banner_ids = {b.banner for b in banners}
        assert actual_banner_ids == set(
            expected_banner_ids[:10]
        ), "Did not get the top 10 revenue banners"

    conn.close()


@pytest.mark.dependency(name="s11", depends=["s10"])
def test_x_5_to_10():
    """Top banners counting less than 10.

    When X is between 5 to 10: Show the Top x banners based on
    revenue within that campaign.

    X: the number of banners with conversions within a campaign.

    """
    current_quarter = get_hours_quarter(datetime.now(UTC))
    conn = sqlite3.connect("src/ads_campaigns/campaign.db")
    cursor = conn.cursor()

    # Find campaigns with 5-10 banners with conversions
    query = """
    WITH campaign_conversions AS (
        SELECT c.campaign_id, COUNT(DISTINCT c.banner_id) as banner_count
        FROM clicks c
        JOIN conversions conv ON c.click_id = conv.click_id
        WHERE c.quarter = ?
        GROUP BY c.campaign_id
        HAVING banner_count BETWEEN 5 AND 9
    )
    SELECT campaign_id, banner_count
    FROM campaign_conversions
    LIMIT 1
    """

    cursor.execute(query, (current_quarter,))
    result = cursor.fetchone()

    if result:
        campaign_id, expected_count = result
        banners = get_campaign(campaign_id)

        # Should return exactly X banners
        assert (
            len(banners) == expected_count
        ), f"Expected {expected_count} banners, got {len(banners)}"

        # Verify they are ordered by revenue
        query = """
        SELECT c.banner_id, SUM(conv.revenue) as total_revenue
        FROM clicks c
        JOIN conversions conv ON c.click_id = conv.click_id
        WHERE c.campaign_id = ? AND c.quarter = ?
        GROUP BY c.banner_id
        ORDER BY total_revenue DESC
        """

        cursor.execute(query, (campaign_id, current_quarter))
        expected_banners = cursor.fetchall()
        expected_banner_ids = [b[0] for b in expected_banners[:expected_count]]

        # Check that we got the top X revenue banners (order may vary due to shuffling)
        actual_banner_ids = {b.banner for b in banners}
        assert actual_banner_ids == set(
            expected_banner_ids
        ), "Did not get the correct top revenue banners"

    conn.close()


@pytest.mark.dependency(name="s12", depends=["s11"])
def test_x_less_than_5():
    """Top banners counting less than 5.

    When X is between 1 to 5: Your collection of banners should
    consist of 5 banners, containing: The top x banners based on
    revenue within that campaign and Banners with the most clicks
    within that campaign to make up a collection of 5 unique banners.

    X: the number of banners with conversions within a campaign.

    """
    current_quarter = get_hours_quarter(datetime.now(UTC))
    conn = sqlite3.connect("src/ads_campaigns/campaign.db")
    cursor = conn.cursor()

    # Find campaigns with 1-4 banners with conversions
    query = """
    WITH campaign_conversions AS (
        SELECT c.campaign_id, COUNT(DISTINCT c.banner_id) as banner_count
        FROM clicks c
        JOIN conversions conv ON c.click_id = conv.click_id
        WHERE c.quarter = ?
        GROUP BY c.campaign_id
        HAVING banner_count BETWEEN 1 AND 4
    )
    SELECT campaign_id, banner_count
    FROM campaign_conversions
    LIMIT 1
    """

    cursor.execute(query, (current_quarter,))
    result = cursor.fetchone()

    if result:
        campaign_id, conversion_count = result
        banners = get_campaign(campaign_id)

        # Should return exactly 5 banners
        assert len(banners) == 5, f"Expected 5 banners, got {len(banners)}"

        # Get banners with conversions ordered by revenue
        revenue_query = """
        SELECT c.banner_id, SUM(conv.revenue) as total_revenue
        FROM clicks c
        JOIN conversions conv ON c.click_id = conv.click_id
        WHERE c.campaign_id = ? AND c.quarter = ?
        GROUP BY c.banner_id
        ORDER BY total_revenue DESC
        """

        cursor.execute(revenue_query, (campaign_id, current_quarter))
        revenue_banners = cursor.fetchall()
        expected_revenue_banners = {b[0] for b in revenue_banners[:conversion_count]}

        # Verify all top revenue banners are included
        actual_banner_ids = {b.banner for b in banners}
        assert expected_revenue_banners.issubset(
            actual_banner_ids
        ), "Missing some top revenue banners"

        # Verify remaining banners are top by clicks
        remaining_count = 5 - conversion_count
        if remaining_count > 0:
            clicks_query = """
            SELECT c.banner_id, COUNT(*) as click_count
            FROM clicks c
            WHERE c.campaign_id = ? AND c.quarter = ?
                AND c.banner_id NOT IN (
                    SELECT DISTINCT c2.banner_id
                    FROM clicks c2
                    JOIN conversions conv ON c2.click_id = conv.click_id
                    WHERE c2.campaign_id = ? AND c2.quarter = ?
                )
            GROUP BY c.banner_id
            ORDER BY click_count DESC
            """

            cursor.execute(
                clicks_query,
                (campaign_id, current_quarter, campaign_id, current_quarter),
            )
            clicks_banners = cursor.fetchall()
            expected_clicks_banners = {b[0] for b in clicks_banners[:remaining_count]}

            # Get actual banners that aren't in the revenue set
            actual_clicks_banners = actual_banner_ids - expected_revenue_banners

            assert actual_clicks_banners.issubset(
                expected_clicks_banners
            ), "Did not get correct top-clicks banners"

    conn.close()


@pytest.mark.dependency(name="s13", depends=["s12"])
def test_x_zero():
    """No banners with conversions.

    When X is zero: Show the top­5 banners based on clicks. If the
    number of banners with clicks is less than 5 within that campaign,
    then you should add random banners to make up a collection of 5
    unique banners.

    X: the number of banners with conversions within a campaign.

    """
    current_quarter = get_hours_quarter(datetime.now(UTC))
    conn = sqlite3.connect("src/ads_campaigns/campaign.db")
    cursor = conn.cursor()

    # Find campaign with clicks but no conversions
    query = """
    SELECT DISTINCT c.campaign_id
    FROM clicks c
    WHERE c.quarter = ?
        AND c.campaign_id NOT IN (
            SELECT DISTINCT c2.campaign_id
            FROM clicks c2
            JOIN conversions conv ON c2.click_id = conv.click_id
            WHERE c2.quarter = ?
        )
    LIMIT 1
    """

    cursor.execute(query, (current_quarter, current_quarter))
    result = cursor.fetchone()

    if result:
        campaign_id = result[0]
        banners = get_campaign(campaign_id)

        # Should return exactly 5 banners
        assert len(banners) == 5, f"Expected 5 banners, got {len(banners)}"

        # Get banners ordered by clicks
        clicks_query = """
        SELECT c.banner_id, COUNT(*) as click_count
        FROM clicks c
        WHERE c.campaign_id = ? AND c.quarter = ?
        GROUP BY c.banner_id
        ORDER BY click_count DESC
        """

        cursor.execute(clicks_query, (campaign_id, current_quarter))
        clicks_banners = cursor.fetchall()

        if len(clicks_banners) >= 5:
            # If we have 5+ banners with clicks, verify we got top 5
            expected_banner_ids = {b[0] for b in clicks_banners[:5]}
            actual_banner_ids = {b.banner for b in banners}
            assert (
                actual_banner_ids == expected_banner_ids
            ), "Did not get top 5 banners by clicks"
        else:
            # If we have fewer than 5 banners with clicks, verify:
            # 1. All banners with clicks are included
            # 2. Random banners make up the difference
            banners_with_clicks = {b[0] for b in clicks_banners}
            actual_banner_ids = {b.banner for b in banners}

            assert banners_with_clicks.issubset(
                actual_banner_ids
            ), "Missing some banners with clicks"
            assert len(actual_banner_ids - banners_with_clicks) == 5 - len(
                banners_with_clicks
            ), "Wrong number of random banners added"

    conn.close()
