"""
Population vs. GDP Growth Visualization (2014–2023)

Description:
-------------
This script visualizes the relationship between the total population and GDP growth rate in a scatter plot 
for the years 2014 to 2023. It combines male and female population data to compute total population values 
and maps them against corresponding annual GDP growth percentages.

Main Functionalities:
---------------------
- Calculates total population by summing male and female populations per year.
- Plots a scatter chart of total population vs. GDP growth rate.
- Annotates each data point with the year and its GDP value.
- Computes and plots a linear trendline using NumPy for visual regression analysis.
- Calculates the Pearson correlation coefficient between population and GDP growth.
- Displays the correlation value on the chart title and prints it in the console.

Intended Use:
-------------
Useful for analyzing potential trends or correlations between demographic growth and economic performance over a 10-year period.
"""
import matplotlib.pyplot as plt
import numpy as np

# Data for 2014-2023
years = list(range(2014, 2024))  # 2014 to 2023

# Population Data (Male + Female in millions)
male_population = [52.1, 52.84, 53.49, 54.12, 54.71, 55.3, 55.91, 56.42, 56.85, 57.31]
female_population = [51.67, 52.48, 53.24, 54.0, 54.75, 55.51, 56.18, 56.68, 57.12, 57.58]
total_population = [m + f for m, f in zip(male_population, female_population)]  # Sum of male and female

# GDP Growth Rate (%)
gdp_growth = [6.3, 6.3, 7.1, 6.9, 6.3, 6.1, -9.5, 5.7, 7.6, 5.5]  # 2014 to 2023

# Scatter plot
plt.figure(figsize=(8, 5))
plt.scatter(total_population, gdp_growth, color='purple', marker='o', label='Data Points')

# Add GDP values and years beside each point
for i, txt in enumerate(gdp_growth):
    label = f"{years[i]}: {txt:.1f}%"  # Format "Year: GDP%"
    plt.annotate(label, (total_population[i], gdp_growth[i]), textcoords="offset points", xytext=(5,5), ha='left', fontsize=9, color='black')

# Trendline
m, b = np.polyfit(total_population, gdp_growth, 1)  # Linear regression (y = mx + b)
trendline = np.polyval([m, b], total_population)  # Compute y-values

plt.plot(total_population, trendline, color='black', linestyle='dashed', label='Trendline')

# Correlation Coefficient
correlation = np.corrcoef(total_population, gdp_growth)[0, 1]

# Labels and Title
plt.xlabel('Total Population (millions)')
plt.ylabel('GDP Growth Rate (%)')
plt.title(f'Population Growth vs. GDP Growth (2014-2023)\nCorrelation: {correlation:.2f}')
plt.legend()
plt.grid()

# Show the plot
plt.show()

# Print correlation coefficient
print(f"Correlation Coefficient (r-value): {correlation:.2f}")
