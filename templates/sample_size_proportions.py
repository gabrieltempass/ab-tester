# Import the libraries
import math
from statsmodels.stats.proportion import proportion_effectsize
from statsmodels.stats.power import tt_ind_solve_power

# Define the parameters
control_conversion = {{ control_conversion }}
sensitivity = {{ sensitivity }}
alternative = "{{ alternative }}"
confidence_level = {{ confidence_level }}
power = {{ power }}
control_ratio = {{ control_ratio }}
treatment_ratio = {{ treatment_ratio }}

# Calculate the sample size
if alternative == "smaller":
    sensitivity *= -1
treatment_conversion = control_conversion * (1 + sensitivity)
effect_size = proportion_effectsize(
    treatment_conversion,
    control_conversion
)
alpha = 1 - confidence_level
ratio = treatment_ratio / control_ratio
control_sample = math.ceil(tt_ind_solve_power(
    effect_size=effect_size,
    alpha=alpha,
    power=power,
    ratio=ratio,
    alternative=alternative
))
treatment_sample = math.ceil(control_sample * ratio)

# Show the result
print("Sample size")
print(f"Control: {control_sample:,}")
print(f"Treatment: {treatment_sample:,}")
print(f"Total: {(control_sample + treatment_sample):,}")
