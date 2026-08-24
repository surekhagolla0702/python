def calculate_kpis(df):
    total_applications = len(df)

    default_customers = 0
    non_default_customers = 0
    default_rate = 0

    if "TARGET" in df.columns:
        default_customers = (df["TARGET"] == 1).sum()
        non_default_customers = (df["TARGET"] == 0).sum()

        if total_applications > 0:
            default_rate = (
                default_customers / total_applications
            ) * 100

    avg_income = 0
    avg_credit = 0
    avg_annuity = 0
    avg_age = 0

    if "AMT_INCOME_TOTAL" in df.columns:
        avg_income = df["AMT_INCOME_TOTAL"].mean()

    if "AMT_CREDIT" in df.columns:
        avg_credit = df["AMT_CREDIT"].mean()

    if "AMT_ANNUITY" in df.columns:
        avg_annuity = df["AMT_ANNUITY"].mean()

    if "AGE_YEARS" in df.columns:
        avg_age = df["AGE_YEARS"].mean()

    return {
        "total_applications": total_applications,
        "default_customers": default_customers,
        "non_default_customers": non_default_customers,
        "default_rate": default_rate,
        "avg_income": avg_income,
        "avg_credit": avg_credit,
        "avg_annuity": avg_annuity,
        "avg_age": avg_age,
    }
