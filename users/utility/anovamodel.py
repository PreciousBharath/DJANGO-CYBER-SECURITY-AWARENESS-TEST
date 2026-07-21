from django.conf import settings
import pandas as pd
import numpy as np
from scipy import stats


def start_proccess():
    path = settings.MEDIA_ROOT + "\\" + "SocialServiceData.csv"
    data = pd.read_csv(path)
    result = []

    required_columns = ['Level of Background', 'Awareness about Cybercrime', 'Education Level', 'Ability to Deal with Cybercrime']
    missing_columns = [col for col in required_columns if col not in data.columns]
    if missing_columns:
        return "Missing required columns: " + ", ".join(missing_columns), ["Please verify the dataset columns."]

    features = data[['Level of Background', 'Awareness about Cybercrime', 'Education Level']]
    target = data['Ability to Deal with Cybercrime']

    # Convert to numeric where possible and keep a simple correlation-based summary.
    numeric_features = features.apply(pd.to_numeric, errors='coerce')
    numeric_target = pd.to_numeric(target, errors='coerce')
    clean_data = pd.concat([numeric_features, numeric_target], axis=1).dropna()

    if clean_data.empty:
        return "No valid numeric data found for analysis.", ["Please verify the dataset values."]

    X = clean_data[['Level of Background', 'Awareness about Cybercrime', 'Education Level']]
    y = clean_data['Ability to Deal with Cybercrime']

    # Compute a simple regression-style summary without statsmodels.
    x_matrix = np.column_stack([np.ones(len(X)), X.to_numpy()])
    coefficients, residuals, _, _ = np.linalg.lstsq(x_matrix, y.to_numpy(), rcond=None)
    fitted = x_matrix @ coefficients
    ss_res = np.sum((y.to_numpy() - fitted) ** 2)
    ss_tot = np.sum((y.to_numpy() - np.mean(y.to_numpy())) ** 2)
    r_squared = 1 - (ss_res / ss_tot) if ss_tot else 0.0

    for index, value in enumerate(coefficients):
        if index == 0:
            label = 'Intercept'
        else:
            label = X.columns[index - 1]
        result.append(f"{label}: Coefficient = {value:.3f}")

    result.append(f"R-squared = {r_squared:.4f}")

    if r_squared >= 0.5:
        result.append("Reject the null hypothesis: The selected variables explain a substantial part of the outcome.")
    else:
        result.append("Fail to reject the null hypothesis: The selected variables do not explain the outcome strongly enough.")

    summary = "<table><tr><th>Metric</th><th>Value</th></tr>" \
        + "<tr><td>R-squared</td><td>{:.4f}</td></tr>".format(r_squared) \
        + "<tr><td>Samples</td><td>{}</td></tr>".format(len(clean_data)) \
        + "</table>"
    return summary, result