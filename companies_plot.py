import pandas as pd
import matplotlib.pyplot as plt

# Load the data
data = pd.read_csv('companies.txt', sep='\t')

# Create the left panel scatterplot
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

ax1.scatter(data['Sales'], data['MarketValue'])
ax1.set_xlabel('Sales')
ax1.set_ylabel('MarketValue')
ax1.set_title('Scatterplot of MarketValue vs Sales')

# Create the right panel scatterplot with log-log scales
ax2.scatter(data['Sales'], data['MarketValue'])
ax2.set_xlabel('Sales')
ax2.set_ylabel('MarketValue')
ax2.set_title('Scatterplot of MarketValue vs Sales (log-log scales)')
ax2.set_xscale('log')
ax2.set_yscale('log')

plt.show()