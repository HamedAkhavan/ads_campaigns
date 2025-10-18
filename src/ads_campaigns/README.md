# Campaign Challenge

:wave: Welcome to this challenge!

You will be creating the backend logic to serve advertisement banners for one of many websites owned by a multi-national advertisement company.
The magic is picking banners based on their revenue performance, and this is exactly where your understanding of data crunching comes to play.

## :pencil: Business Rules

The business rules are all based on the number of banners with conversion within a given campaign. So, to be precise:
`X: the nummber of banners with conversions within a campaign`

Here are the rules:

| Scenario         | Business Rule                                                                                                                                       |
| ---------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| X >= 10          | Show the top 10 banners based on revenue within that campaign                                                                                       |
| X in range(5,10) | Show the top X banners based on revenue within that campaign                                                                                        |
| X in range(1,5)  | Show 5 banners, consisting of the X banners based on revenue within that campaign, supplemented by banners with the most clicks in that campaign    |
| X == 0           | Show the top 5 banners based on clicks within that campaign. If the number of banners with clicks is less than 5, supplement it with random banners |

## :runner: How to Get Started

Please carefully read the "How To" sections in the [README.md](../../../README.md) first.

Your goal is to implement the logic and tests that are throwing a `NotImplementedError`. How you approach this is completely up to you.
You are welcome to introduce additional (helper) functions, tests, and use packages as you see fit.

The data for this challenge is located in [campaign.db](campaign.db), which is a [SQLite](https://www.sqlite.org/index.html) database.
The tables have the following schemas:

Clicks

| name        | type    |
| ----------- | ------- |
| click_id    | INTEGER |
| banner_id   | INTEGER |
| campaign_id | INTEGER |
| quarter     | INTEGER |

Conversions

| name          | type    |
| ------------- | ------- |
| conversion_id | INTEGER |
| click_id      | INTEGER |
| revenue       | REAL    |
| quarter       | INTEGER |

## :trophy: When are you Done?

We consider the challenge as completed once all the checks and tests pass.

:four_leaf_clover: Best of luck!
