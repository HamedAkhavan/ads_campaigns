"""Settings module for the ads_campaigns package.

This module contains configuration settings and parameters for the ads_campaigns
package, including defaults, environment variables, and other customizable
options that control the behavior of the application.

The settings can be modified directly or through environment variables to customize
the package's functionality according to specific requirements.

Note:
    All settings should be documented and have appropriate default values.

"""

DB_PATH = (
    "src/ads_campaigns/campaign.db"  # Can be set via environment variable if needed
)
