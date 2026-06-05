# Premier League Home vs Away Analysis(Premier League 2025/26)


## What is this?

A data analysis project that compares Premier League teams' home and away performance using WhoScored ratings.

## What I did

1. Cleaned and merged home/away data from WhoScored
2. Calculated rating difference: `Home_Rating - Away_Rating`
3. Classified teams into: Home Dominant / Balanced / Away Dominant
4. Visualized the results with a bar chart

## Results

- **Burnley** is the most home-reliant team (+0.24)
- **Tottenham & Chelsea** have away advantage (-0.11, -0.02)
- **Crystal Palace** is perfectly balanced (0.00)
- 17 out of 20 teams perform better at home

![Home vs Away Difference](images/home_away_rating_diff.png)

## How to run

```bash
pip install -r requirements.txt
jupyter notebook notebook.ipynb