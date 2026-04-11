import matplotlib.pyplot as plt
 
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
 
# --- Line Plot: Daily Website Visitors ---
days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
visitors = [150, 200, 180, 220, 300, 250, 180]
 
ax1.plot(days, visitors, marker='o', color='steelblue', linewidth=2)
ax1.set_title('Daily Website Visitors')
ax1.set_xlabel('Day of Week')
ax1.set_ylabel('Number of Visitors')
ax1.grid(True, linestyle='--', alpha=0.5)
 
# --- Bar Chart: Product Sales by Category ---
categories = ['Electronics', 'Clothing', 'Food', 'Books']
sales = [45000, 32000, 28000, 15000]
colors = ['steelblue', 'salmon', 'mediumseagreen', 'orchid']
 
ax2.bar(categories, sales, color=colors)
ax2.set_title('Product Sales by Category')
ax2.set_xlabel('Category')
ax2.set_ylabel('Sales (USD)')
ax2.grid(axis='y', linestyle='--', alpha=0.5)
 
plt.tight_layout()
plt.show()