import streamlit as st
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Fuzzy logic variables
temperature = ctrl.Antecedent(np.arange(16, 31, 1), 'temperature')
time_of_day = ctrl.Antecedent(np.arange(0, 24, 1), 'time_of_day')
setpoint = ctrl.Consequent(np.arange(16, 31, 1), 'setpoint')

# Membership functions
temperature['cold'] = fuzz.trimf(temperature.universe, [16, 16, 20])
temperature['cool'] = fuzz.trimf(temperature.universe, [18, 21, 24])
temperature['warm'] = fuzz.trimf(temperature.universe, [22, 25, 28])
temperature['hot'] = fuzz.trimf(temperature.universe, [26, 30, 30])

time_of_day['morning'] = fuzz.trimf(time_of_day.universe, [5, 8, 11])
time_of_day['afternoon'] = fuzz.trimf(time_of_day.universe, [12, 15, 18])
time_of_day['night'] = fuzz.trimf(time_of_day.universe, [19, 22, 24])

setpoint['cool'] = fuzz.trimf(setpoint.universe, [16, 18, 21])
setpoint['comfortable'] = fuzz.trimf(setpoint.universe, [20, 23, 26])
setpoint['warm'] = fuzz.trimf(setpoint.universe, [24, 27, 30])

# Fuzzy rules
rule1 = ctrl.Rule(temperature['cold'] & time_of_day['morning'], setpoint['warm'])
rule2 = ctrl.Rule(temperature['cool'] & time_of_day['afternoon'], setpoint['comfortable'])
rule3 = ctrl.Rule(temperature['warm'] & time_of_day['night'], setpoint['cool'])
rule4 = ctrl.Rule(temperature['hot'], setpoint['cool'])

# Control system
climate_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4])
climate_sim = ctrl.ControlSystemSimulation(climate_ctrl)

# Streamlit UI
st.title("Smart Temperature Controller")
st.write("Fuzzy logic-based temperature recommendation system")

current_temp = st.slider("Current Room Temperature (°C)", 16, 30, 22)
current_hour = st.slider("Current Hour of Day (0-23)", 0, 23, 14)

climate_sim.input['temperature'] = current_temp
climate_sim.input['time_of_day'] = current_hour
climate_sim.compute()

output_temp = climate_sim.output['setpoint']
st.success(f"Recommended Temperature Setpoint: {output_temp:.1f}°C")

# Basic future preference prediction
st.subheader("Next Likely Preference (Predicted)")

def predict_next(hour):
    if 5 <= hour < 12:
        return "warm"
    elif 12 <= hour < 18:
        return "comfortable"
    else:
        return "cool"

next_pref = predict_next(current_hour)
st.info(f"Predicted Preference Based on Time: {next_pref}")
