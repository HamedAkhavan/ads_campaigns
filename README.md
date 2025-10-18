# Campaign Challenge

:wave: Welcome to an exciting challenge!

Get ready to dive into the world of advertisement campaigns! Your
mission is to create the backend logic that will smartly serve
advertisement banners for various websites owned by a multi-national
advertisement company. The magic lies in selecting the right banners
based on their revenue performance, and that's where your
data-crunching skills will shine.

<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-refresh-toc -->

**Table of Contents**

- [Campaign Challenge](#campaign-challenge)
- [:pencil: What You'll Be Doing](#pencil-what-youll-be-doing)
  - [Business Rules](#business-rules)
  - [Implementation \& Testing](#implementation--testing)
  - [Ready for Prime Time](#ready-for-prime-time)
- [:gift: Your Data Playground](#gift-your-data-playground)
  - [Clicks Table](#clicks-table)
  - [Conversions Table](#conversions-table)
  - [Running the Project](#running-the-project)
- [:trophy: How to Win](#trophy-how-to-win)

<!-- markdown-toc end -->

# :pencil: What You'll Be Doing

Here's what you'll be working on. We've broken down the business rules
into a checklist to guide you through the challenge. Let’s get
started!

## Business Rules

The logic you implement will determine which banners to show based on
their conversion performance within a campaign. To make it clearer:

- `X` represents the number of banners with conversions within a given
  campaign.

Here are the rules:

| Scenario             | What to Do                                                                                                                            | Checklist |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------- | --------- |
| **X >= 10**          | Show the top 10 banners based on revenue within that campaign.                                                                        | [ ]       |
| **X in range(5,10)** | Show the top X banners based on revenue within that campaign.                                                                         | [ ]       |
| **X in range(1,5)**  | Show 5 banners: X banners based on revenue, supplemented by banners with the most clicks within that campaign.                        | [ ]       |
| **X == 0**           | Show the top 5 banners based on clicks within that campaign. If there are fewer than 5, fill the remaining slots with random banners. | [ ]       |

## Implementation & Testing

| Task                    | Description                                                                                                                                                           | Checklist |
| ----------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------- |
| **Implement the Logic** | Your primary goal is to implement the logic that’s currently throwing a `NotImplementedError`. Feel free to introduce additional helper functions or tests as needed. | [ ]       |
| **Test Your Work**      | Ensure your implementation is rock-solid by writing and running tests. All tests should pass before you consider the task complete.                                   | [ ]       |

## Ready for Prime Time

| Task                                 | Description                                                                                                                                         | Checklist |
| ------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------- | --------- |
| **Follow the Coding Style**          | Stick to the coding style guidelines—this will help keep your code clean, consistent, and easy to maintain.                                         | [ ]       |
| **Implement Linting**                | Add linting to catch any sneaky errors and keep the code up to standard.                                                                            | [ ]       |
| **Pass CI Checks**                   | Ensure your project runs smoothly in the Continuous Integration (CI) pipeline, passing all checks and tests.                                        | [ ]       |
| **Refactor & Document**              | If you hit a roadblock with the existing design, don’t sweat it, refactor the code and document your solution. It’s all part of the process!        | [ ]       |
| **Create an Architecture Schematic** | Use [draw.io](https://www.draw.io) to create a schematic of the architecture you suggest for deploying the project. Include a link to your diagram. | [ ]       |
| **Record an Architecture Video**     | Record a video where you describe the architecture you’ve suggested, explaining why you chose it and how it fits the project’s needs.               | [ ]       |

# :gift: Your Data Playground

You’ll be working with data stored in a
[SQLite](https://www.sqlite.org/index.html) database located in
`campaign.db`. Here’s what you’ll find inside:

## Clicks Table

| Column Name | Data Type |
| ----------- | --------- |
| click_id    | INTEGER   |
| banner_id   | INTEGER   |
| campaign_id | INTEGER   |
| quarter     | INTEGER   |

## Conversions Table

| Column Name   | Data Type |
| ------------- | --------- |
| conversion_id | INTEGER   |
| click_id      | INTEGER   |
| revenue       | REAL      |
| quarter       | INTEGER   |

## Running the Project

Make sure you have [DevEnv](https://devenv.sh/getting-started/)
installed. Then you can easily run the project:

```sh
devenv shell # to enter the isolated environment

pytest # Make all of them pass!
```

# :trophy: How to Win

You're done when:

- All the checks and tests pass.
- The code meets our style guidelines.
- The project is up and running perfectly on CI.
- You’ve created and shared your architecture schematic and
  accompanying video.

Most importantly, have fun with it! We can’t wait to see what you come
up with. :four_leaf_clover: Good luck!
