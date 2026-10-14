
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# ------------------------------------------
# 1. CREATE OUTPUT FOLDER
# ------------------------------------------

output_folder = Path("output")
output_folder.mkdir(exist_ok=True)

# ------------------------------------------
# 2. LOAD DATASET
# ------------------------------------------

df = pd.read_csv("tour_enquiries.csv")

print("=" * 45)
print("GROWFINIX TASK 3")
print("CUSTOMER DEMOGRAPHIC ANALYSIS")
print("=" * 45)

print("\nFirst five records:")
print(df.head())

print("\nTotal rows and columns:")
print(df.shape)

# ------------------------------------------
# 3. CHECK MISSING VALUES
# ------------------------------------------

print("\nMissing values in each column:")
print(df.isnull().sum())

# ------------------------------------------
# 4. CLEAN DATA
# ------------------------------------------

df = df.drop_duplicates()

df["Destination"] = df["Destination"].astype("string").str.strip()
df["Age"] = pd.to_numeric(df["Age"], errors="coerce")
df["Income"] = pd.to_numeric(df["Income"], errors="coerce")

df = df.dropna(subset=["Destination", "Age", "Income"])
df = df[df["Destination"] != ""]

df = df[
    (df["Age"] > 0) &
    (df["Income"] >= 0)
].copy()

print("\nTotal records after cleaning:", len(df))

# ------------------------------------------
# 5. CREATE AGE GROUPS
# ------------------------------------------

df["Age Group"] = pd.cut(
    df["Age"],
    bins=[0, 18, 30, 45, 60, float("inf")],
    labels=[
        "Under 18",
        "18-30",
        "31-45",
        "46-60",
        "Above 60"
    ]
)

# ------------------------------------------
# 6. CREATE INCOME BRACKETS
# ------------------------------------------

df["Income Bracket"] = pd.cut(
    df["Income"],
    bins=[-1, 25000, 50000, 75000, float("inf")],
    labels=[
        "Up to 25,000",
        "25,001-50,000",
        "50,001-75,000",
        "Above 75,000"
    ]
)

# ------------------------------------------
# 7. ANALYZE POPULAR DESTINATIONS
# ------------------------------------------

destination_counts = df["Destination"].value_counts()

print("\nPopular Travel Destinations:")
print(destination_counts)

print("\nMost popular destination:")
if not destination_counts.empty:
    print(destination_counts.index[0])
    print("Number of enquiries:", destination_counts.iloc[0])

# ------------------------------------------
# 8. ANALYZE CUSTOMER AGE GROUPS
# ------------------------------------------

age_counts = df["Age Group"].value_counts(sort=False)

print("\nCustomers by Age Group:")
print(age_counts)

# ------------------------------------------
# 9. ANALYZE CUSTOMER INCOME BRACKETS
# ------------------------------------------

income_counts = df["Income Bracket"].value_counts(sort=False)

print("\nCustomers by Income Bracket:")
print(income_counts)

# ------------------------------------------
# 10. SAVE ANALYSIS RESULTS
# ------------------------------------------

df.to_csv(
    output_folder / "cleaned_enquiries.csv",
    index=False
)

destination_counts.to_csv(
    output_folder / "destination_summary.csv",
    header=["Number of Enquiries"]
)

age_counts.to_csv(
    output_folder / "age_group_summary.csv",
    header=["Number of Customers"]
)

income_counts.to_csv(
    output_folder / "income_summary.csv",
    header=["Number of Customers"]
)

# ------------------------------------------
# 11. CHART 1: POPULAR DESTINATIONS
# ------------------------------------------

plt.figure(figsize=(8, 5))

destination_counts.plot(kind="bar")

plt.title("Most Popular Travel Destinations")
plt.xlabel("Destination")
plt.ylabel("Number of Enquiries")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(
    output_folder / "popular_destinations.png",
    dpi=300
)

plt.close()

print("\nPopular destinations chart saved.")

# ------------------------------------------
# 12. CHART 2: CUSTOMER AGE HISTOGRAM
# ------------------------------------------

plt.figure(figsize=(8, 5))

plt.hist(
    df["Age"],
    bins=8,
    edgecolor="black"
)

plt.title("Customer Age Distribution")
plt.xlabel("Age")
plt.ylabel("Number of Customers")
plt.tight_layout()

plt.savefig(
    output_folder / "age_histogram.png",
    dpi=300
)

plt.close()

print("Age histogram saved.")

# ------------------------------------------
# 13. CHART 3: CUSTOMER INCOME BRACKETS
# ------------------------------------------

plt.figure(figsize=(9, 5))

income_counts.plot(kind="bar")

plt.title("Customers by Income Bracket")
plt.xlabel("Monthly Income (Rs.)")
plt.ylabel("Number of Customers")
plt.xticks(rotation=25)
plt.tight_layout()

plt.savefig(
    output_folder / "income_brackets.png",
    dpi=300
)

plt.close()

print("Income bracket chart saved.")

# ------------------------------------------
# 14. FINAL STATUS
# ------------------------------------------

print("\n" + "=" * 45)
print("SUCCESS! TASK 3 ANALYSIS COMPLETED.")
print("=" * 45)

print("\nCheck the output folder for:")
print("- cleaned_enquiries.csv")
print("- destination_summary.csv")
print("- age_group_summary.csv")
print("- income_summary.csv")
print("- popular_destinations.png")
print("- age_histogram.png")
print("- income_brackets.png")
