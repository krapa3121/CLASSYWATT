import streamlit as st
import pandas as pd

def _change_occupancy(key, delta):
    """Increase or decrease occupancy without exceeding classroom capacity."""
    st.session_state[key] = max(0, min(40, st.session_state[key] + delta))


def render_sidebar(defaults, rooms):
    st.sidebar.header("Smart Classroom Control Panel")

    room = st.sidebar.selectbox(
        "Select classroom",
        list(rooms),
        index=list(rooms).index(defaults["room"]),
    )

    settings = dict(defaults)
    settings["room"] = room
    capacity = rooms[room]["capacity"]

    # Manual occupancy controls, stored independently for each classroom.
    occupancy_key = f"occupancy_{room}"

    if occupancy_key not in st.session_state:
        st.session_state[occupancy_key] = min(
            capacity, int(defaults["simulated_occupancy"])
        )

    with st.sidebar.expander("Student Occupancy", expanded=True):
        st.caption(f"Capacity: {capacity} students")

        col1, col2 = st.columns(2)

        col1.button(
            "➖ Decrease",
            key=f"decrease_{room}",
            on_click=_change_occupancy,
            args=(occupancy_key, -1),
            disabled=st.session_state[occupancy_key] <= 0,
            use_container_width=True,
        )

        col2.button(
            "➕ Increase",
            key=f"increase_{room}",
            on_click=_change_occupancy,
            args=(occupancy_key, 1),
            disabled=st.session_state[occupancy_key] >= capacity,
            use_container_width=True,
        )

        st.slider(
            "Adjust student count",
            min_value=0,
            max_value=capacity,
            step=1,
            key=occupancy_key,
        )

        settings["occupancy_mode"] = "Simulator"
        settings["simulated_occupancy"] = st.session_state[occupancy_key]
        settings["camera_source"] = ""

        st.metric("Current students", settings["simulated_occupancy"])
        st.metric("Available seats", capacity - settings["simulated_occupancy"])

    with st.sidebar.expander("Daylight & Lighting", expanded=True):
        settings["daylight_lux"] = st.slider(
            "Natural daylight (lux)", 0, 1500,
            int(defaults["daylight_lux"]), 25
        )
        settings["target_lux"] = st.slider(
            "Target room brightness (lux)", 100, 1000,
            int(defaults["target_lux"]), 25
        )
        settings["min_brightness"] = st.slider(
            "Minimum light brightness (%)", 0, 50,
            int(defaults["min_brightness"])
        )
        settings["max_brightness"] = st.slider(
            "Maximum light brightness (%)", 50, 100,
            int(defaults["max_brightness"])
        )

        settings["projection_mode"] = st.toggle(
            "Projection mode", value=defaults["projection_mode"]
        )
        settings["projection_lighting"] = st.selectbox(
            "Projection lighting", ["Dim", "OFF"]
        )
        settings["projection_screen_supported"] = st.checkbox(
            "Screen controller connected (demo)",
            value=defaults["projection_screen_supported"],
        )
        settings["empty_delay_minutes"] = st.slider(
            "Empty-room OFF delay (minutes)", 1, 15,
            int(defaults["empty_delay_minutes"])
        )

    with st.sidebar.expander("Fan & AC Controls", expanded=True):
        settings["hvac_mode"] = st.radio(
            "Operating mode",
            ["Auto", "Manual"],
            horizontal=True,
        )

        settings["temperature_c"] = st.slider(
            "Room temperature (°C)", 20, 40,
            int(defaults.get("temperature_c", 29))
        )

        settings["fan_threshold_c"] = st.slider(
            "Fan activation temperature (°C)", 20, 35,
            int(defaults.get("fan_threshold_c", 26))
        )

        settings["ac_threshold_c"] = st.slider(
            "AC activation temperature (°C)", 21, 40,
            int(defaults.get("ac_threshold_c", 30))
        )

        if settings["hvac_mode"] == "Manual":
            settings["manual_hvac_override"] = st.radio(
                "Choose device to test",
                ["OFF", "Fan", "AC"],
                horizontal=True,
                help="Only one device can be selected at a time.",
            )
        else:
            settings["manual_hvac_override"] = "Auto"

        st.caption(
            "Safety rule: occupancy 0 forces both fan and AC OFF. "
            "Fan and AC cannot be ON together."
        )

    with st.sidebar.expander("Manual Light Override"):
        settings["manual_light_override"] = st.selectbox(
            "Light override", ["Auto", "Force ON", "Force OFF"]
        )
        settings["manual_brightness"] = st.slider(
            "Manual brightness (%)", 0, 100,
            int(defaults["manual_brightness"])
        )

    with st.sidebar.expander("Energy Settings"):
        settings["light_watts"] = st.number_input(
            "Light power (W)", 1, 2000, int(defaults["light_watts"])
        )
        settings["fan_watts"] = st.number_input(
            "Each fan power (W)", 1, 1000, int(defaults["fan_watts"])
        )
        settings["ac_watts"] = st.number_input(
            "AC power (W)", 1, 10000, int(defaults["ac_watts"])
        )
        settings["projector_watts"] = st.number_input(
            "Projector power (W)", 0, 3000,
            int(defaults["projector_watts"])
        )
        settings["hours_per_day"] = st.slider(
            "Daily operating hours", 1, 24,
            int(defaults["hours_per_day"])
        )
        settings["electricity_rate"] = st.number_input(
            "Electricity tariff (₹/kWh)", 1.0, 50.0,
            float(defaults["electricity_rate"]), 0.5
        )

    return settings

def render_dashboard(room_name, room, occupancy, camera_status, camera_note, settings, controls, summary):
    st.subheader(f"🏫 {room_name} • Live status")
    if controls["capacity_alert"]:
        st.error(f"⚠️ Capacity exceeded: {occupancy} people for capacity {room['capacity']}.")
    elif camera_status == "CAMERA ERROR":
        st.warning("Camera/sensor failure: occupancy is unknown. Dashboard is showing a safe fallback value of 0; verify the room manually.")
    else:
        st.success(f"Occupancy source: {camera_status} • {camera_note}")
    a,b,c,d = st.columns(4)
    a.metric("👥 Occupancy", f"{occupancy} people")
    b.metric("🪑 Room capacity", f"{room['capacity']} people")
    c.metric("🟢 Available seats", controls["available_seats"])
    d.metric("☀️ Daylight", f"{settings['daylight_lux']} lux")
    st.markdown("### Device control status")
    x1,x2,x3,x4 = st.columns(4)
    x1.metric("💡 Classroom light", controls["light_state"], f"{controls['brightness']}% brightness")
    x2.metric("🌀 Fans (2)", controls["fan_status"])
    x3.metric("❄️ AC (1)", controls["ac_status"])
    x4.metric("🎬 Projection", controls["projection_status"])
    if controls["screen_status"] == "CLOSED":
        st.info("Projection screen: CLOSED (simulated status; no motor hardware command sent).")
    else:
        st.caption("Projection screen: simulated / controller not connected.")
    if occupancy == 0:
        st.info(f"Empty-room lighting delay configured: {settings['empty_delay_minutes']} min. This prototype displays the policy but does not persist a timer between reruns; use backend scheduler/state for production.")
    st.markdown("### ⚡ Energy estimate")
    e1,e2,e3,e4 = st.columns(4)
    e1.metric("Optimized usage", f"{summary['optimized_kwh']:.2f} kWh")
    e2.metric("Baseline usage", f"{summary['baseline_kwh']:.2f} kWh")
    e3.metric("Estimated saved", f"{summary['saved_kwh']:.2f} kWh", f"{summary['savings_pct']:.1f}%")
    e4.metric("Estimated cost", f"₹{summary['cost_rupees']:.2f}")
    st.caption("Estimates use configured power ratings and daily hours, not actual meter readings.")

def render_weekly_report(df):
    st.subheader("📊 Weekly energy, wastage & cost report")
    st.caption("Illustrative demo dataset — replace with real logs or smart-meter readings for an evidence-based report.")
    c1,c2 = st.columns(2)
    with c1:
        st.markdown("**Power consumption (kWh)**")
        st.line_chart(df.set_index("Day")[["Baseline kWh (demo)", "Optimized kWh (demo)"]])
        st.markdown("**Energy wastage avoided (kWh)**")
        st.bar_chart(df.set_index("Day")[["Wastage avoided kWh (demo)"]])
    with c2:
        st.markdown("**Weekly electricity cost (₹)**")
        st.line_chart(df.set_index("Day")[["Baseline cost ₹ (demo)", "Optimized cost ₹ (demo)"]])
        st.markdown("**Savings (₹)**")
        st.bar_chart(df.set_index("Day")[["Savings ₹ (demo)"]])
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.download_button("⬇️ Download weekly report CSV", df.to_csv(index=False).encode("utf-8"), "weekly_energy_report_demo.csv", "text/csv")

def render_recommendations(items):
    st.subheader("🤖 Energy-saving recommendations")
    st.caption("Rule-based recommendations for the prototype; not a trained AI model.")
    for i, item in enumerate(items, 1):
        st.markdown(f"**{i}.** {item}")
