def recommendations(occupancy, settings, controls, summary):
    tips = []
    if occupancy == 0:
        tips.append("Room is empty: keep lights, fans and AC off. Verify occupancy before relying on automation.")
    if settings["daylight_lux"] >= settings["target_lux"]:
        tips.append("Daylight meets the target: keep artificial lighting at its minimum useful brightness.")
    elif occupancy > 0:
        tips.append("Daylight is below target: increase lighting only enough to meet the configured illumination target.")
    if settings["projection_mode"]:
        tips.append("Projection mode is active: use the lowest comfortable brightness and check screen visibility.")
    if controls["hvac_mode"] == "AC":
        tips.append("AC mode is active: keep doors/windows closed where appropriate and use a reasonable setpoint.")
    elif controls["hvac_mode"] == "Fan":
        tips.append("Fan mode is active: prefer fans when conditions are comfortable enough to avoid AC.")
    if summary["savings_pct"] < 15:
        tips.append("Potential improvement: review operating hours and device wattage assumptions; connect meter data for better estimates.")
    tips.append("For production AI, train recommendations on historical occupancy, weather, lux and smart-meter data; current tips are rule-based, not an AI model.")
    return tips
