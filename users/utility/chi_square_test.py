from django.conf import settings
import pandas as pd
from scipy import stats


def start_chi():
    rslt = []
    path = settings.MEDIA_ROOT + "\\" + "CentralIndia.csv"
    df = pd.read_csv(path)

    required_columns = ['Gender', 'Age Group', 'Occupation']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        return [f"Missing required columns: {', '.join(missing_columns)}"]

    gender_distribution = df['Gender'].value_counts(normalize=True) * 100
    rslt.append(f"Gender Distribution (%):\n{gender_distribution.to_string()}")

    age_group_distribution = df['Age Group'].value_counts(normalize=True) * 100
    rslt.append(f"Age Group Distribution (%):\n{age_group_distribution.to_string()}")

    occupation_distribution = df['Occupation'].value_counts(normalize=True) * 100
    rslt.append(f"Occupation Distribution (%):\n{occupation_distribution.to_string()}")

    contingency_table = pd.crosstab(df['Gender'], df['Occupation'])
    chi2_stat, p_val, dof, expected = stats.chi2_contingency(contingency_table)

    rslt.append(f"Chi-square Statistic: {chi2_stat:.4f}")
    rslt.append(f"P-value: {p_val:.4f}")
    rslt.append(f"Degrees of Freedom: {dof}")
    rslt.append(f"Expected Frequencies:\n{expected}")

    alpha = 0.05
    if p_val < alpha:
        rslt.append("There is a significant association between Gender and Occupation (reject the null hypothesis).")
    else:
        rslt.append("There is no significant association between Gender and Occupation (fail to reject the null hypothesis).")
    return rslt
