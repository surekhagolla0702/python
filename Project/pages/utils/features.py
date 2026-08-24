import pandas as pd

def create_features(df):
    df = df.copy()

    # Age in years
    if "DAYS_BIRTH" in df.columns:
        df["AGE_YEARS"] = abs(df["DAYS_BIRTH"]) / 365

    # Employment years
    if "DAYS_EMPLOYED" in df.columns:
        employed_days = df["DAYS_EMPLOYED"].replace(365243, pd.NA)
        df["EMPLOYMENT_YEARS"] = abs(employed_days) / 365

    # Credit-to-income ratio
    if "AMT_CREDIT" in df.columns and "AMT_INCOME_TOTAL" in df.columns:
        df["CREDIT_TO_INCOME"] = (
            df["AMT_CREDIT"] / df["AMT_INCOME_TOTAL"]
        )

    # Annuity-to-income ratio
    if "AMT_ANNUITY" in df.columns and "AMT_INCOME_TOTAL" in df.columns:
        df["ANNUITY_TO_INCOME"] = (
            df["AMT_ANNUITY"] / df["AMT_INCOME_TOTAL"]
        )

    # Credit-to-goods ratio
    if "AMT_CREDIT" in df.columns and "AMT_GOODS_PRICE" in df.columns:
        df["CREDIT_TO_GOODS"] = (
            df["AMT_CREDIT"] / df["AMT_GOODS_PRICE"]
        )

    # Average external credit score
    score_columns = [
        "EXT_SOURCE_1",
        "EXT_SOURCE_2",
        "EXT_SOURCE_3"
    ]

    available_scores = [
        col for col in score_columns if col in df.columns
    ]

    if available_scores:
        df["AVERAGE_EXTERNAL_SCORE"] = df[available_scores].mean(axis=1)

    return df
