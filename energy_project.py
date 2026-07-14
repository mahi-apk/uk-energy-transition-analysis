# ============================================
# UK ENERGY TRANSITION — TIME-SERIES ANALYSIS
# Sector: Energy / Renewables
# Data: Global Data on Sustainable Energy (2000-2020), filtered to UK
# Tools: pandas, numpy, matplotlib
# ============================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ============================================
# LAYER 1: LOAD & CLEAN DATA
# ============================================

df = pd.read_csv("sustainable_data.csv")

# Filter to the UK
uk = df[df["Entity"] == "United Kingdom"]

# Keep and rename the columns we need
uk = uk[["Year",
         "Electricity from fossil fuels (TWh)",
         "Electricity from renewables (TWh)"]]
uk = uk.rename(columns={
    "Year": "year",
    "Electricity from fossil fuels (TWh)": "fossil_fuels_twh",
    "Electricity from renewables (TWh)": "renewables_twh"
})

# Check for missing values
print("Missing values:\n", uk.isnull().sum())

# Create a datetime index from the year
uk["date"] = pd.to_datetime(uk["year"], format="%Y")
uk = uk.set_index("date")

print(f"\nCleaned data: {uk.shape[0]} years ({uk['year'].min()}-{uk['year'].max()})")

# ============================================
# LAYER 2: TIME-SERIES ANALYSIS
# ============================================

uk["renewables_pct_growth"] = uk["renewables_twh"].pct_change() * 100
uk["total_twh"] = uk["renewables_twh"] + uk["fossil_fuels_twh"]
uk["renewable_share_pct"] = (uk["renewables_twh"] / uk["total_twh"]) * 100
uk["renewables_3yr_avg"] = uk["renewables_twh"].rolling(window=3).mean()

share_2000 = uk.loc["2000-01-01", "renewable_share_pct"]
share_2020 = uk.loc["2020-01-01", "renewable_share_pct"]
points_increased = share_2020 - share_2000
avg_annual_growth = uk["renewables_pct_growth"].mean()
fastest_growth_year = uk["renewables_pct_growth"].idxmax().year

print("\n=== ENERGY TRANSITION SUMMARY ===")
print(f"Renewable share in 2000: {share_2000:.1f}%")
print(f"Renewable share in 2020: {share_2020:.1f}%")
print(f"Renewable share increased by {points_increased:.1f} percentage points")
print(f"Average annual renewable growth: {avg_annual_growth:.1f}%")
print(f"Year renewables grew fastest: {fastest_growth_year}")

# ============================================
# LAYER 3: VISUALISATION
# ============================================

# Chart 1 — Transition crossover
plt.figure(figsize=(11, 6))
plt.plot(uk.index, uk["renewables_twh"],
         color="#2ca02c", linewidth=2.5, marker="o", label="Renewables")
plt.plot(uk.index, uk["fossil_fuels_twh"],
         color="#8c564b", linewidth=2.5, marker="o", label="Fossil Fuels")
plt.fill_between(uk.index, uk["renewables_twh"], uk["fossil_fuels_twh"],
                 alpha=0.1, color="grey")
plt.xlabel("Year", fontsize=11)
plt.ylabel("Generation (TWh)", fontsize=11)
plt.title("The UK Energy Transition (2000-2020)", fontsize=14, fontweight="bold")
plt.legend(fontsize=11)
plt.grid(alpha=0.3)
plt.savefig("uk_energy_transition.png", dpi=150, bbox_inches="tight")
plt.close()
print("\nSaved: uk_energy_transition.png")

# Chart 2 — Renewable share with 50% milestone
plt.figure(figsize=(11, 6))
plt.plot(uk.index, uk["renewable_share_pct"],
         color="#2ca02c", linewidth=2.5, marker="o", label="Renewable Share")
plt.axhline(y=50, color="red", linestyle="--", alpha=0.6, label="50% Milestone")
plt.xlabel("Year", fontsize=11)
plt.ylabel("Renewable Share (%)", fontsize=11)
plt.title("Renewables as a Share of UK Generation", fontsize=14, fontweight="bold")
plt.legend(fontsize=11)
plt.grid(alpha=0.3)
plt.savefig("uk_renewable_share.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved: uk_renewable_share.png")

# ============================================
# LAYER 4: FORECAST (fitted on 2010-2020 for realism)
# ============================================
# NOTE: Fitting on the full 2000-2020 range underestimates recent growth,
# because renewables were near-flat 2000-2010 then accelerated after 2011.
# We therefore fit the trend on 2010-2020 only, giving a realistic projection.

recent = uk.loc["2010-01-01":"2020-01-01"].copy()
recent["year_num"] = range(len(recent))

slope, intercept = np.polyfit(recent["year_num"], recent["renewables_twh"], 1)

print("\n=== FORECAST (2010-2020 trend) ===")
print(f"Recent slope: {slope:.2f} TWh/year")
print(f"Interpretation: since 2010, UK renewables grew ~{slope:.1f} TWh per year.\n")

future_nums = range(len(recent), len(recent) + 5)
forecast_values = [slope * n + intercept for n in future_nums]
forecast_dates = pd.date_range(start="2021-01-01", periods=5, freq="YS")

for date, value in zip(forecast_dates, forecast_values):
    print(f"{date.year}: {value:.1f} TWh")

# Forecast chart
plt.figure(figsize=(11, 6))
plt.plot(uk.index, uk["renewables_twh"],
         color="#2ca02c", linewidth=2.5, marker="o", label="Historical")
plt.plot(forecast_dates, forecast_values,
         color="#ff7f0e", linewidth=2.5, linestyle="--", marker="s", label="Forecast (2021-2025)")
plt.xlabel("Year", fontsize=11)
plt.ylabel("Renewables (TWh)", fontsize=11)
plt.title("UK Renewables: History and 5-Year Forecast", fontsize=14, fontweight="bold")
plt.legend(fontsize=11, loc="upper left")
plt.grid(alpha=0.3)
plt.savefig("uk_renewables_forecast.png", dpi=150, bbox_inches="tight")
plt.close()
print("\nSaved: uk_renewables_forecast.png")

# ============================================
# ANALYSIS CAVEAT
# ============================================
print("\n=== FORECAST CAVEAT ===")
print("This is a linear projection based on the 2010-2020 trend. It assumes")
print("growth continues at the same rate and does not account for grid capacity")
print("limits, policy changes, or technology shifts. Treat as directional")
print("guidance, not precise prediction.")
