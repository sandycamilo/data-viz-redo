# Life Expectancy: U.S. States vs. the World

**Live chart:** https://sandycamilo.github.io/data-viz-redo/

A redesign of the New York Times chart "Life Expectancy in U.S. States and Select Countries," created for a data visualization assignment on storytelling with data.


## What changed from the original
- **Ranked dot plot instead of a beeswarm.** In the original beeswarm, life expectancy was shown vertically, while each bubble's left-to-right position was only spacing to keep bubbles from overlapping. Readers naturally read horizontal position as data, so places on opposite sides, like Alaska and Maryland, appeared different even when their values were nearly the same. The redesign places life expectancy on a single horizontal axis and ranks all 76 places from highest to lowest, each on its own labeled row, so every position on the chart now reflects an actual value.

- **Purposeful color with a key.** The story compares U.S. states with wealthy countries, so those two groups get strong, contrasting colors: blue for wealthy countries and orange for U.S. states. This contrast helps readers separate the two groups at a glance as they move through the ranking. Other countries are shown in gray so they provide context without competing for attention. The original used pale pink and mint with similar lightness and no legend, which made the groups hard to tell apart and left readers to figure out what each color meant.

- **Annotation instead of guesswork.** The original chart had no annotations, so readers had to scan dozens of bubbles and work out the comparison on their own. The redesign adds a light blue shaded band covering the full range of wealthy countries (80.6 to 84.8 years), labeled at the top in the same blue as the wealthy-country dots. The band gives readers a clear benchmark: anything inside it matches wealthy-country levels, and anything to the left falls short. A callout in the U.S. state color sits right beside Hawaii's dot and explains that Hawaii, the top U.S. state, only ties Germany, the lowest wealthy country, while the other 49 states fall below it. Placing the explanation exactly where the reader's eye lands makes the takeaway hard to miss and shows that the gap isn't caused by a few struggling states, since even the best state only reaches the bottom of the wealthy group.

- **Decluttered and interactive.** The original filled the space with dashed gridlines, large overlapping bubbles, and abbreviated labels, giving every element equal visual weight. The redesign removes the gridlines and extra marks, leaving a clean space where the ranking and the wealthy-country band stand out. 


## Data
Values were estimated from the original chart. U.S. data are for people born in 2020; international data are for 2021.

**Sources:** National Center for Health Statistics; United Nations.

**Original chart:** "What's Going On in This Graph? | Life Expectancy." The Learning Network, *The New York Times*, Jan. 15, 2026.
https://www.nytimes.com/2026/01/15/learning/whats-going-on-in-this-graph-jan-21-2026.html

The graph originally appeared in N. Kristof, "How Do We Fix the Scandal That Is American Health Care?" *The New York Times* (Opinion), Aug. 16, 2023.


## Run it yourself
```
pip install pandas plotly
python life_expectancy_dot_plot.py
```
