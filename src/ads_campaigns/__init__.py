"""Campaign module.

The responsibilities of this module, is to load the campaign
information, transform it based on the required business logic, and
serve it with the following conditions:

| A Scenario       |Requirements                                                       |
| X >= 10          |Show the top 10 banners based on revenue within that campaign      |
| X in range(5, 10)|Show the top x banners based on revenue within that campaign       |
| X in range(1, 5) |Your collection of banners should consist of 5 banners, containing:|
|                  |- the top x banners based on revenue within that campaign          |
|                  |- banners with the most clicks within that campaign                |
| X == 0           |Show the top 5 banners based on clicks. If the banners with clicks |
|                  |is less than 5 within that campaign, then you should add a         |
|                  |set of random banners to make up a collection of 5 unique banners  |

"""
