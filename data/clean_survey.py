
import pandas as pd

# 1. Load the CSV file
file_path = "data/capstone_project.csv"
df: pd.DataFrame = pd.read_csv(file_path, skiprows=[1, 2])  # type: ignore # Skip extra header rows

# 2. Drop unnecessary columns
drop_cols = [
    "IPAddress", "RecipientLastName", "RecipientFirstName", "RecipientEmail",
    "ExternalReference", "LocationLatitude", "LocationLongitude",
    "DistributionChannel", "UserLanguage", "Q_RecaptchaScore"
]
df.drop(columns=drop_cols, inplace=True, errors="ignore")

# 3. Remove preview/incomplete responses
df = df[(df["Status"] != "Survey Preview") & (df["Finished"] == True)]

# 4. Standardize column names
df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

# 5. Fix typos in Likert responses
typo_replacements: dict[str, str] = {"Nuetral": "Neutral", "Srongly Disagree": "Strongly Disagree"}
df.replace(typo_replacements, inplace=True) # type: ignore

# 6. Convert date columns to datetime
df["startdate"] = pd.to_datetime(df["startdate"], errors="coerce")
df["enddate"] = pd.to_datetime(df["enddate"], errors="coerce")

# 7. Optional: Convert Likert scale to numeric
likert_map = {
    "Strongly Disagree": 1,
    "Disagree": 2,
    "Neutral": 3,
    "Agree": 4,
    "Strongly Agree": 5
}
for col in df.columns:
    if col.startswith("q7_"):  # Likert questions
        df[col] = df[col].map(likert_map)

# 8. Save cleaned file
cleaned_path = "cleaned_survey.csv"
df.to_csv(cleaned_path, index=False)

print(f"Cleaning complete! Saved as {cleaned_path}")
