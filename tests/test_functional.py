"""All functional tests for the advertisement campaign module.

We are using a single file given the size of this project. However,
feel free to start splitting the tests, if you feel it is necessary.

"""

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
    raise NotImplementedError("Please implement me!")


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
    raise NotImplementedError("Please implement me!")


@pytest.mark.dependency(name="s11", depends=["s10"])
def test_x_5_to_10():
    """Top banners counting less than 10.

    When X is between 5 to 10: Show the Top x banners based on
    revenue within that campaign.

    X: the number of banners with conversions within a campaign.

    """
    raise NotImplementedError("Please implement me!")


@pytest.mark.dependency(name="s12", depends=["s11"])
def test_x_less_than_5():
    """Top banners counting less than 5.

    When X is between 1 to 5: Your collection of banners should
    consist of 5 banners, containing: The top x banners based on
    revenue within that campaign and Banners with the most clicks
    within that campaign to make up a collection of 5 unique banners.

    X: the number of banners with conversions within a campaign.

    """
    raise NotImplementedError("Please implement me!")


@pytest.mark.dependency(name="s13", depends=["s12"])
def test_x_zero():
    """No banners with conversions.

    When X is zero: Show the top­5 banners based on clicks. If the
    number of banners with clicks is less than 5 within that campaign,
    then you should add random banners to make up a collection of 5
    unique banners.

    X: the number of banners with conversions within a campaign.

    """
    raise NotImplementedError("Please implement me!")
