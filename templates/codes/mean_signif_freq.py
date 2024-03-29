# Import the libraries
import random
import numpy as np
import pandas as pd
{% if i.method == "t-test" %}
from statsmodels.stats.weightstats import ttest_ind
{% elif i.method == "Z-test" %}
from statsmodels.stats.weightstats import ztest
{% endif %}

# Load the CSV file
df = pd.read_csv("{{ i.file.name }}")

# Define the parameters
alternative = "{{ i.alternative }}"
confidence = {{ i.confidence }}
alpha = 1 - confidence

# Calculate the observed difference
control_mean = df[df["{{ i.alias['Group'] }}"] == "{{ i.alias['Control'] }}"]["{{ i.alias['Measurement'] }}"].mean()
treatment_mean = df[df["{{ i.alias['Group'] }}"] == "{{ i.alias['Treatment'] }}"]["{{ i.alias['Measurement'] }}"].mean()
observed_diff = treatment_mean - control_mean

# Get the control and treatment measurements
control_measurements = df[df["{{ i.alias['Group'] }}"] == "{{ i.alias['Control'] }}"]["{{ i.alias['Measurement'] }}"]
treatment_measurements = df[df["{{ i.alias['Group'] }}"] == "{{ i.alias['Treatment'] }}"]["{{ i.alias['Measurement'] }}"]

# Calculate the p-value
{% if i.method == "t-test" %}
tstat, p_value, dof = ttest_ind(
    treatment_measurements,
    control_measurements,
    alternative=alternative
)
{% elif i.method == "Z-test" %}
tstat, p_value = ztest(
    treatment_measurements,
    control_measurements,
    alternative=alternative
)
{% endif %}

# Show the result
if p_value <= alpha:
    outcome = "is"
else:
    outcome = "is not"
if round(p_value, 4) < 0.0001:
    value = "< 0.0001"
else:
    value = f"= {p_value:.4f}"
print(f"The difference {outcome} statistically significant, with a p-value {value}.")
