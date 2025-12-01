
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from typing import List

from matplotlib.axes import Axes
from matplotlib.figure import Figure

# Ensure outputs directory exists
os.makedirs("outputs/charts", exist_ok=True)

# Load cleaned data
df = pd.read_csv("cleaned_survey.csv") # type: ignore

# 1. Descriptive statistics
stats_summary = df.describe(include='all')
with open("outputs/stats_results.txt", "w") as f:
    f.write(str(stats_summary))
    
# 2. Likert scale columns
# ensure likert_cols is a Sequence[str] so indexing returns a DataFrame
likert_cols: List[str] = [col for col in df.columns if col.startswith("q7_")]
# take an explicit copy to avoid SettingWithCopy warnings and give a clear DataFrame type
df_likert: pd.DataFrame = df[likert_cols].copy()
# Boxplot for Likert distribution
fig, ax = plt.subplots(figsize=(10, 6))
sns.boxplot(data=df_likert, ax=ax)
ax.set_title("Likert Scale Distribution")
ax.set_ylabel("Score (1-5)")
fig.savefig("outputs/charts/likert_distribution.png")
plt.close(fig)

# Correlation heatmap
corr = df_likert.corr()
plt.figure(figsize=(8, 6))
sns.heatmap(corr, annot=True, cmap="coolwarm", vmin=0, vmax=1)
plt.title("Correlation Heatmap of Likert Items")
plt.savefig("outputs/charts/likert_correlation_heatmap.png")
plt.close()

# 3. Years of experience vs confidence
experience_map: dict[str, float] = {
    "Less than 1 year": 0.5,
    "1-3 years": 2.0,
    "4-7 years": 5.5,
    "8-15 years": 11.5,
    "16+ years": 18.0,
}
df['years_numeric'] = df['q3'].map(experience_map)

plt.figure(figsize=(8, 6))
sns.scatterplot(x=df['years_numeric'], y=df['q7_1'])
plt.title("Years of Experience vs Confidence (Q7_1)")
plt.xlabel("Years of Experience")
plt.ylabel("Confidence Score")
plt.savefig("outputs/charts/experience_vs_confidence.png")
plt.close()

print("Analysis complete! Check outputs/charts and stats_results.txt")
