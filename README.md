# 📊 Marketing Campaign Analytics Dashboard

## 🚀 Project Overview
This project is an interactive analytics dashboard built using **Streamlit** and **Python**. It provides insights into a retail company's marketing campaigns, customer demographics, and spending patterns. The goal is to assist management in identifying the most profitable customer segments and improving campaign acceptance rates.

## ❓ Problem Statement
A retail company has run multiple marketing campaigns but lacks a consolidated view of the results. Management needs to answer key business questions:
* Which customer segments have the highest response rates?
* How do spending patterns vary by age, income, and marital status?
* Which product categories perform best across different demographics?

## 🛠️ Tech Stack
* **Language:** Python
* **Dashboard Framework:** Streamlit
* **Data Manipulation:** Pandas
* **Visualization:** Plotly Express, Matplotlib, Seaborn
* **Data Source:** `marketing_campaign_data.csv` (2,240 rows, 28 columns)

## 📂 Key Features & Insights
* **Dynamic Filtering:** Filter data by Country, Education Level, and Marital Status via the sidebar.
* **KPI Metrics:** Real-time calculation of Total Customers, Average Income, Total Spend, and Average Campaigns Accepted.
* **Feature Engineering:**
    * **Age:** Calculated from `Year_Birth`.
    * **Total_Spend:** Aggregated spend across all 6 product categories (Wines, Fruits, Meat, Fish, Sweets, Gold).
    * **Tenure:** Calculated days since enrollment (`Dt_Customer`).
* **Visualizations:**
    * **Campaign Acceptance:** Bar charts showing conversion rates for Campaigns 1-5 and the final response.
    * **Spending Analysis:** Pie charts for product mix and scatter plots for Income vs. Spend analysis.
    * **Customer Segmentation:** Histograms and box plots analyzing Age and Income distributions.

## ⚙️ How to Run Locally

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YOUR-USERNAME/marketing-campaign-analytics.git](https://github.com/YOUR-USERNAME/marketing-campaign-analytics.git)
    cd marketing-campaign-analytics
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the Streamlit app:**
    ```bash
    streamlit run app.py
    ```

## 📄 Data Dictionary (Key Fields)
* `Response`: 1 if customer accepted the offer in the last campaign, 0 otherwise.
* `Income`: Customer's yearly household income.
* `MntWines`, `MntMeatProducts`, etc.: Amount spent on specific categories in the last 2 years.
* `NumWebPurchases`, `NumStorePurchases`: Number of purchases made through specific channels.

## 🔮 Future Improvements
* Implement Machine Learning (Clustering) to automatically group similar customers.
* Add predictive modeling to forecast campaign acceptance probabilities.

---
*Created by [Your Name]*
