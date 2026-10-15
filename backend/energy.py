import pandas as pd
import numpy as np

def energy_summary(room, controls, settings):
    hours = float(settings["hours_per_day"])
    light_kw = settings["light_watts"] * (controls["brightness"] / 100) / 1000
    fan_kw = settings["fan_watts"] * room["fans"] / 1000 if controls["hvac_mode"] == "Fan" else 0
    ac_kw = settings["ac_watts"] / 1000 if controls["hvac_mode"] == "AC" else 0
    projector_kw = settings["projector_watts"] / 1000 if settings["projection_mode"] else 0
    optimized = (light_kw + fan_kw + ac_kw + projector_kw) * hours
    baseline = (settings["baseline_light_watts"] + settings["baseline_fan_watts"] + settings["baseline_ac_watts"]) / 1000 * hours
    saved = max(0, baseline - optimized)
    cost = optimized * float(settings["electricity_rate"])
    return {"optimized_kwh": optimized, "baseline_kwh": baseline, "saved_kwh": saved,
            "savings_pct": saved / baseline * 100 if baseline else 0, "cost_rupees": cost,
            "waste_kwh": max(0, baseline - optimized)}

def weekly_report(room, settings):
    # Reproducible illustrative data for demo; replace with database/meter readings for real reporting.
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    baseline = np.array([18.2, 19.0, 17.6, 20.1, 18.8, 8.2, 6.0])
    optimized = baseline * np.array([0.78, 0.72, 0.75, 0.69, 0.74, 0.80, 0.82])
    rate = float(settings["electricity_rate"])
    return pd.DataFrame({
        "Day": days,
        "Baseline kWh (demo)": baseline.round(2),
        "Optimized kWh (demo)": optimized.round(2),
        "Wastage avoided kWh (demo)": (baseline - optimized).round(2),
        "Baseline cost ₹ (demo)": (baseline * rate).round(2),
        "Optimized cost ₹ (demo)": (optimized * rate).round(2),
        "Savings ₹ (demo)": ((baseline - optimized) * rate).round(2),
    })
