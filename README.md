# UK Energy Transition — Time-Series Analysis

Analysing two decades of real UK electricity generation data (2000–2020) to quantify the shift from fossil fuels to renewables, with a 5-year forecast.

## Problem

The UK has undergone one of the fastest energy transitions in the world. This project quantifies that shift using real government-sourced data: how fast have renewables grown, when did they overtake fossil fuels, and where are they heading?

## Approach

1. **Data cleaning** — filtered a global energy dataset to the UK, selected and renamed the relevant columns, checked for missing values, and built a datetime index for time-series analysis.
2. **Time-series analysis** — calculated year-on-year growth, renewable share of total generation, and a 3-year rolling average.
3. **Visualisation** — produced a crossover chart (renewables vs fossil fuels), a renewable-share chart with a 50% milestone line, and a forecast chart.
4. **Forecasting** — fitted a linear trend on the 2010–2020 period (the modern growth era) to project renewable generation through 2025.

## Key Findings

- Renewables grew from **3.4% of UK generation in 2000 to 51.4% in 2020** — a 47.9 percentage-point shift.
- Average annual renewable growth was **14.3%**, with the fastest single-year jump in **2011**.
- Since 2010, renewables have grown ~10.8 TWh per year; projecting this forward suggests ~185 TWh by 2025.

## A Note on the Forecast

A linear trend fitted across the full 2000–2020 range underestimates recent growth, because renewables were near-flat from 2000–2010 before accelerating after 2011. The forecast is therefore fitted on **2010–2020 only**, giving a realistic projection. This is a linear model — it assumes constant growth and does not account for grid capacity limits, policy changes, or technology shifts. It is directional guidance, not precise prediction.

## Tools

Python, pandas, NumPy, Matplotlib

## Files

| File | Description |
|------|-------------|
| `energy_project.py` | Full analysis pipeline |
| `uk_energy_transition.png` | Renewables vs fossil fuels crossover |
| `uk_renewable_share.png` | Renewable share of generation |
| `uk_renewables_forecast.png` | Historical trend + 5-year forecast |

## Data

[Global Data on Sustainable Energy (2000–2020) — Kaggle](https://www.kaggle.com/datasets/anshtanwar/global-data-on-sustainable-energy), filtered to the UK.

## How to Run

```
pip install pandas numpy matplotlib
python energy_project.py
```
