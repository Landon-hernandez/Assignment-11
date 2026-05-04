# module11-assignment.py
# Module 11 Assignment: Data Visualization with Matplotlib
# SunCoast Retail Visual Analysis

# Import required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Welcome message
print("=" * 60)
print("SUNCOAST RETAIL VISUAL ANALYSIS")
print("=" * 60)

# ----- USE THE FOLLOWING CODE TO CREATE SAMPLE DATA (DO NOT MODIFY) -----
np.random.seed(42)

# Generate dates for 8 quarters (Q1 2022 - Q4 2023)
quarters = pd.date_range(start='2022-01-01', periods=8, freq='Q')
quarter_labels = ['Q1 2022', 'Q2 2022', 'Q3 2022', 'Q4 2022',
                 'Q1 2023', 'Q2 2023', 'Q3 2023', 'Q4 2023']

locations = ['Tampa', 'Miami', 'Orlando', 'Jacksonville']
categories = ['Electronics', 'Clothing', 'Home Goods', 'Sporting Goods', 'Beauty']

quarterly_data = []
for quarter_idx, quarter in enumerate(quarters):
    for location in locations:
        for category in categories:
            base_sales = np.random.normal(loc=100000, scale=20000)
            seasonal_factor = 1.3 if quarter.quarter == 4 else (0.8 if quarter.quarter == 1 else 1.0)
            location_factor = {'Tampa': 1.0, 'Miami': 1.2, 'Orlando': 0.9, 'Jacksonville': 0.8}[location]
            category_factor = {'Electronics': 1.5, 'Clothing': 1.0, 'Home Goods': 0.8, 'Sporting Goods': 0.7, 'Beauty': 0.9}[category]
            growth_factor = (1 + 0.05/4) ** quarter_idx
            sales = base_sales * seasonal_factor * location_factor * category_factor * growth_factor
            sales *= np.random.normal(loc=1.0, scale=0.1)
            ad_spend = (sales ** 0.7) * 0.05 * np.random.normal(loc=1.0, scale=0.2)
            quarterly_data.append({
                'Quarter': quarter,
                'QuarterLabel': quarter_labels[quarter_idx],
                'Location': location,
                'Category': category,
                'Sales': round(sales, 2),
                'AdSpend': round(ad_spend, 2),
                'Year': quarter.year
            })

# Customer data
customer_data = []
total_customers = 2000
age_params = {
    'Tampa': (45, 15),
    'Miami': (35, 12),
    'Orlando': (38, 14),
    'Jacksonville': (42, 13)
}

for location in locations:
    mean_age, std_age = age_params[location]
    customer_count = int(total_customers * {'Tampa': 0.3, 'Miami': 0.35, 'Orlando': 0.2, 'Jacksonville': 0.15}[location])
    ages = np.random.normal(loc=mean_age, scale=std_age, size=customer_count)
    ages = np.clip(ages, 18, 80).astype(int)
    for age in ages:
        if age < 30:
            category_preference = np.random.choice(categories, p=[0.3, 0.3, 0.1, 0.2, 0.1])
        elif age < 50:
            category_preference = np.random.choice(categories, p=[0.25, 0.2, 0.25, 0.15, 0.15])
        else:
            category_preference = np.random.choice(categories, p=[0.15, 0.1, 0.35, 0.1, 0.3])
        base_amount = np.random.gamma(shape=5, scale=20)
        price_tier = np.random.choice(['Budget', 'Mid-range', 'Premium'], p=[0.3, 0.5, 0.2])
        tier_factor = {'Budget': 0.7, 'Mid-range': 1.0, 'Premium': 1.8}[price_tier]
        purchase_amount = base_amount * tier_factor
        customer_data.append({
            'Location': location,
            'Age': age,
            'Category': category_preference,
            'PurchaseAmount': round(purchase_amount, 2),
            'PriceTier': price_tier
        })

# Create DataFrames
sales_df = pd.DataFrame(quarterly_data)
customer_df = pd.DataFrame(customer_data)
sales_df['Quarter_Num'] = sales_df['Quarter'].dt.quarter
sales_df['AdSpend'] = sales_df['AdSpend'].replace(0, 1e-6)
sales_df['SalesPerDollarSpent'] = sales_df['Sales'] / sales_df['AdSpend']

# ---------------- Visualization Functions ----------------

# 1. Time Series: Overall quarterly sales
def plot_quarterly_sales_trend():
    agg = sales_df.groupby('QuarterLabel', sort=False)['Sales'].sum().reindex(quarter_labels)
    fig, ax = plt.subplots(figsize=(9,5))
    ax.plot(agg.index, agg.values, marker='o', linewidth=2)
    ax.set_title('Total Quarterly Sales (All Locations & Categories)')
    ax.set_xlabel('Quarter')
    ax.set_ylabel('Total Sales (USD)')
    ax.grid(True, linestyle='--', alpha=0.6)
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig

# 2. Multi-line chart by location
def plot_location_sales_comparison():
    grouped = sales_df.groupby(['QuarterLabel', 'Location'])['Sales'].sum().unstack('Location').reindex(quarter_labels)
    fig, ax = plt.subplots(figsize=(10,6))
    markers = ['o', 's', 'D', '^']
    for i, loc in enumerate(grouped.columns):
        ax.plot(grouped.index, grouped[loc], marker=markers[i%len(markers)], linewidth=2, label=loc)
    ax.set_title('Quarterly Sales by Location')
    ax.set_xlabel('Quarter')
    ax.set_ylabel('Sales (USD)')
    ax.legend(title='Location')
    ax.grid(True, linestyle='--', alpha=0.5)
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig

# 3. Category performance grouped bar
def plot_category_performance_by_location():
    recent_label = sales_df['QuarterLabel'].iloc[-1]
    subset = sales_df[sales_df['QuarterLabel'] == recent_label]
    pivot = subset.groupby(['Category','Location'])['Sales'].sum().unstack('Location').reindex(categories)
    fig, ax = plt.subplots(figsize=(10,6))
    n_cat, n_loc = len(pivot.index), len(pivot.columns)
    x = np.arange(n_cat)
    width = 0.75 / n_loc
    offsets = (np.arange(n_loc) - (n_loc-1)/2) * width
    for i, loc in enumerate(pivot.columns):
        ax.bar(x + offsets[i], pivot[loc].values, width=width, label=loc)
    ax.set_xticks(x)
    ax.set_xticklabels(pivot.index, rotation=30)
    ax.set_title(f'Product Category Performance by Location - {recent_label}')
    ax.set_ylabel('Sales (USD)')
    ax.legend(title='Location')
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    return fig

# 4. Stacked bar chart
def plot_sales_composition_by_location():
    pivot = sales_df.groupby(['Location','Category'])['Sales'].sum().unstack('Category').fillna(0)
    pct = pivot.div(pivot.sum(axis=1), axis=0) * 100
    fig, ax = plt.subplots(figsize=(9,6))
    bottoms = np.zeros(len(pct))
    for cat in categories:
        ax.bar(pct.index, pct[cat], bottom=bottoms, label=cat)
        bottoms += pct[cat].values
    ax.set_title('Sales Composition by Category (Percentage) — By Location')
    ax.set_ylabel('Percent of Sales (%)')
    ax.legend(title='Category', bbox_to_anchor=(1.02, 1))
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    return fig

# 5. Scatter Ad Spend vs Sales
def plot_ad_spend_vs_sales():
    x = sales_df['AdSpend'].values
    y = sales_df['Sales'].values
    fit_func = np.poly1d(np.polyfit(x, y, 1))
    preds = fit_func(x)
    residuals = y - preds
    outlier_idx = np.argsort(np.abs(residuals))[-3:]
    fig, ax = plt.subplots(figsize=(9,6))
    ax.scatter(x, y, alpha=0.6, label='Quarter-Category Observations')
    ax.plot(np.sort(x), fit_func(np.sort(x)), color='red', linewidth=2, label='Best-fit line')
    for idx in outlier_idx:
        ax.annotate(f"{sales_df.iloc[idx]['Location']}, {sales_df.iloc[idx]['Category']}",
                    (x[idx], y[idx]), xytext=(8,8), textcoords='offset points', ha='left', fontsize=8,
                    arrowprops=dict(arrowstyle='->', lw=0.7))
    ax.set_xscale('log')
    ax.set_title('Ad Spend vs Sales (per quarter-category)')
    ax.set_xlabel('Ad Spend (USD) - log scale')
    ax.set_ylabel('Sales (USD)')
    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.4)
    plt.tight_layout()
    return fig

# 6. Sales per $ ad spend over time
def plot_ad_efficiency_over_time():
    agg = sales_df.groupby('QuarterLabel')['SalesPerDollarSpent'].mean().reindex(quarter_labels)
    fig, ax = plt.subplots(figsize=(9,5))
    ax.plot(agg.index, agg.values, marker='o', linewidth=2)
    ax.set_title('Average Sales per Dollar Spent on Advertising (By Quarter)')
    ax.set_xlabel('Quarter')
    ax.set_ylabel('Average Sales per $ Spent')
    ax.grid(True, linestyle='--', alpha=0.6)
    hi_idx, lo_idx = np.nanargmax(agg.values), np.nanargmin(agg.values)
    ax.annotate(f"Highest: {agg.values[hi_idx]:.1f}", (agg.index[hi_idx], agg.values[hi_idx]), xytext=(0,10), textcoords='offset points', ha='center', fontsize=9)
    ax.annotate(f"Lowest: {agg.values[lo_idx]:.1f}", (agg.index[lo_idx], agg.values[lo_idx]), xytext=(0,-15), textcoords='offset points', ha='center', fontsize=9)
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig

# 7. Customer age distribution
def plot_customer_age_distribution():
    fig, axs = plt.subplots(1, len(locations)+1, figsize=(16,4), sharey=True)
    axs[0].hist(customer_df['Age'], bins=15, alpha=0.8)
    mean_all, median_all = customer_df['Age'].mean(), customer_df['Age'].median()
    axs[0].axvline(mean_all, linestyle='--', label=f"Mean: {mean_all:.1f}")
    axs[0].axvline(median_all, linestyle=':', label=f"Median: {median_all:.1f}")
    axs[0].set_title('All Locations - Age Distribution')
    axs[0].set_xlabel('Age')
    axs[0].legend()
    for i, loc in enumerate(locations):
        ax = axs[i+1]
        subset = customer_df[customer_df['Location']==loc]
        ax.hist(subset['Age'], bins=12, alpha=0.85)
        m, md = subset['Age'].mean(), subset['Age'].median()
        ax.axvline(m, linestyle='--', label=f"Mean: {m:.1f}")
        ax.axvline(md, linestyle=':', label=f"Median: {md:.1f}")
        ax.set_title(f'{loc}')
        ax.set_xlabel('Age')
        ax.legend(fontsize=8)
    plt.tight_layout()
    return fig

# 8. Purchase by age group (fixed boxplot)
def plot_purchase_by_age_group():
    bins = [18, 30, 45, 60, 100]
    labels = ['18-30', '31-45', '46-60', '61+']
    customer_df['AgeGroup'] = pd.cut(customer_df['Age'], bins=bins, labels=labels, right=True)
    grouped = [customer_df[customer_df['AgeGroup']==lab]['PurchaseAmount'].values for lab in labels]
    fig, ax = plt.subplots(figsize=(8,6))
    ax.boxplot(grouped, labels=labels)
    ax.set_title('Purchase Amount by Age Group')
    ax.set_xlabel('Age Group')
    ax.set_ylabel('Purchase Amount (USD)')
    ax.grid(axis='y', linestyle='--', alpha=0.4)
    plt.tight_layout()
    return fig

# 9. Purchase amount distribution histogram
def plot_purchase_amount_distribution():
    fig, ax = plt.subplots(figsize=(8,5))
    ax.hist(customer_df['PurchaseAmount'], bins=30, alpha=0.85)
    ax.set_title('Distribution of Purchase Amounts')
    ax.set_xlabel('Purchase Amount (USD)')
    ax.set_ylabel('Count')
    ax.grid(axis='y', linestyle='--', alpha=0.4)
    plt.tight_layout()
    return fig

# 10. Sales by price tier (pie)
def plot_sales_by_price_tier():
    tier_sum = customer_df.groupby('PriceTier')['PurchaseAmount'].sum().reindex(['Budget','Mid-range','Premium'])
    fig, ax = plt.subplots(figsize=(6,6))
    explode = [0.05 if i==tier_sum.idxmax() else 0 for i in tier_sum.index]
    ax.pie(tier_sum.values, labels=tier_sum.index, autopct='%1.1f%%', startangle=140, explode=explode, wedgeprops={'edgecolor':'white'})
    ax.set_title('Sales Breakdown by Price Tier (Purchase Amount)')
    plt.tight_layout()
    return fig

# 11. Category market share pie
def plot_category_market_share():
    cat_sum = sales_df.groupby('Category')['Sales'].sum().reindex(categories)
    explode = [0.08 if cat_sum.idxmax()==cat else 0 for cat in cat_sum.index]
    fig, ax = plt.subplots(figsize=(7,7))
    ax.pie(cat_sum.values, labels=cat_sum.index, autopct='%1.1f%%', startangle=130, explode=explode, wedgeprops={'edgecolor':'white'})
    ax.set_title('Market Share by Product Category (All Sales)')
    plt.tight_layout()
    return fig

# 12. Location sales distribution pie
def plot_location_sales_distribution():
    loc_sum = sales_df.groupby('Location')['Sales'].sum().reindex(locations)
    fig, ax = plt.subplots(figsize=(6,6))
    ax.pie(loc_sum.values, labels=loc_sum.index, autopct='%1.1f%%', startangle=120, wedgeprops={'edgecolor':'white'})
    ax.set_title('Sales Distribution by Location')
    plt.tight_layout()
    return fig

# 13. Comprehensive dashboard
def create_business_dashboard():
    quarterly_totals = sales_df.groupby('QuarterLabel')['Sales'].sum().reindex(quarter_labels)
    grouped_loc = sales_df.groupby(['QuarterLabel','Location'])['Sales'].sum().unstack('Location').reindex(quarter_labels)
    cat_sum = sales_df.groupby('Category')['Sales'].sum().reindex(categories)
    x, y = sales_df['AdSpend'].values, sales_df['Sales'].values
    fit_func = np.poly1d(np.polyfit(x, y, 1))

    fig, axs = plt.subplots(2,2, figsize=(14,10))
    # Top-left: quarterly total
    ax = axs[0,0]
    ax.plot(quarterly_totals.index, quarterly_totals.values, marker='o')
    ax.set_title('Total Quarterly Sales')
    ax.set_xlabel('Quarter')
    ax.set_ylabel('Sales (USD)')
    ax.grid(True, linestyle='--', alpha=0.4)
    ax.tick_params(axis='x', rotation=35)

    # Top-right: multi-line by location
    ax = axs[0,1]
    markers = ['o','s','D','^']
    for i, loc in enumerate(grouped_loc.columns):
        ax.plot(grouped_loc.index, grouped_loc[loc], marker=markers[i%len(markers)], label=loc)
    ax.set_title('Sales by Location (Quarterly)')
    ax.set_xlabel('Quarter')
    ax.set_ylabel('Sales (USD)')
    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.4)
    ax.tick_params(axis='x', rotation=35)

    # Bottom-left: pie category
    ax = axs[1,0]
    explode = [0.08 if cat_sum.idxmax()==cat else 0 for cat in cat_sum.index]
    ax.pie(cat_sum.values, labels=cat_sum.index, autopct='%1.1f%%', startangle=130, explode=explode, wedgeprops={'edgecolor':'white'})
    ax.set_title('Category Market Share')

    # Bottom-right: ad spend scatter
    ax = axs[1,1]
    ax.scatter(x, y, alpha=0.6)
    ax.plot(np.sort(x), fit_func(np.sort(x)), color='red', linewidth=2)
    ax.set_xscale('log')
    ax.set_title('Ad Spend vs Sales')
    ax.set_xlabel('Ad Spend (USD) - log scale')
    ax.set_ylabel('Sales (USD)')
    ax.grid(True, linestyle='--', alpha=0.4)

    plt.suptitle('SunCoast Retail — Business Dashboard', fontsize=16)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    return fig

# ---------------- Main Function ----------------
def main():
    print("\n" + "=" * 60)
    print("SUNCOAST RETAIL VISUAL ANALYSIS RESULTS")
    print("=" * 60)

    # Call and immediately show plots to avoid unused variable warnings
    plot_quarterly_sales_trend().show()
    plot_location_sales_comparison().show()
    plot_category_performance_by_location().show()
    plot_sales_composition_by_location().show()
    plot_ad_spend_vs_sales().show()
    plot_ad_efficiency_over_time().show()
    plot_customer_age_distribution().show()
    plot_purchase_by_age_group().show()
    plot_purchase_amount_distribution().show()
    plot_sales_by_price_tier().show()
    plot_category_market_share().show()
    plot_location_sales_distribution().show()
    create_business_dashboard().show()

    # Key business insights
    print("\nKEY BUSINESS INSIGHTS:")
    top_cat = sales_df.groupby('Category')['Sales'].sum().sort_values(ascending=False).idxmax()
    print(f"- Top product category by sales: {top_cat}")
    top_loc = sales_df.groupby('Location')['Sales'].sum().sort_values(ascending=False).idxmax()
    print(f"- Top performing location: {top_loc}")
    last_eff = sales_df.groupby('QuarterLabel')['SalesPerDollarSpent'].mean().iloc[-1]
    print(f"- Latest average sales per $ ad spend: {last_eff:.1f}")
    mean_ages = customer_df.groupby('Location')['Age'].mean().round(1).to_dict()
    print(f"- Mean customer ages by location: {mean_ages}")
    top_tier = customer_df.groupby('PriceTier')['PurchaseAmount'].sum().idxmax()
    print(f"- Most revenue from price tier: {top_tier}")

    print("\nRECOMMENDATIONS:")
    print("- Increase targeted electronics promotions in Miami and Tampa.")
    print("- Re-evaluate ad spend allocation; focus on quarters with higher ROI.")
    print("- Tailor product mixes by age demographics per location.")
    print("- Promote premium-tier products to lift average order value.")

if __name__ == "__main__":
    main()
