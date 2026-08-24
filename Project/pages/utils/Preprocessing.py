import pandas as pd

def preprocess_data(df):
    df = df.copy()

    # Convert negative age days to age in years
    if "DAYS_BIRTH" in df.columns:
        df["AGE_YEARS"] = (-df["DAYS_BIRTH"]) / 365.25

    # Convert negative employment days to years
    if "DAYS_EMPLOYED" in df.columns:
        df["EMPLOYMENT_YEARS"] = df["DAYS_EMPLOYED"].replace(365243, pd.NA)
        df["EMPLOYMENT_YEARS"] = (-df["EMPLOYMENT_YEARS"]) / 365.25

    # Income-to-credit ratio
    if "AMT_INCOME_TOTAL" in df.columns and "AMT_CREDIT" in df.columns:
        df["INCOME_CREDIT_RATIO"] = (
            df["AMT_INCOME_TOTAL"] / df["AMT_CREDIT"]
        )

    # Annuity burden
    if "AMT_ANNUITY" in df.columns and "AMT_INCOME_TOTAL" in df.columns:
        df["ANNUITY_BURDEN"] = (
            df["AMT_ANNUITY"] / df["AMT_INCOME_TOTAL"]
        )

    return df
