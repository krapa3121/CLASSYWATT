def calculate_controls(room, settings, occupancy):
    """Calculate lighting and HVAC states with occupancy interlocks."""

    capacity = room["capacity"]
    occupied = occupancy > 0

    daylight = max(0, float(settings["daylight_lux"]))
    target = max(1, float(settings["target_lux"]))

    min_b = int(settings["min_brightness"])
    max_b = int(settings["max_brightness"])

    # Daylight-aware lighting.
    needed = round((target - daylight) / target * 100)
    needed = max(0, min(100, needed))

    brightness = (
        max(min_b, min(max_b, needed))
        if occupied else 0
    )

    light_state = "ON" if occupied else "OFF"

    if settings["projection_mode"] and occupied:
        brightness = 25 if settings["projection_lighting"] == "Dim" else 0
        light_state = "ON" if brightness > 0 else "OFF"

    # Manual light override works only while the room is occupied.
    if occupied:
        if settings["manual_light_override"] == "Force ON":
            light_state = "ON"
            brightness = int(settings["manual_brightness"])
        elif settings["manual_light_override"] == "Force OFF":
            light_state = "OFF"
            brightness = 0

    # HVAC control: occupancy always takes priority.
    temperature = float(settings.get("temperature_c", 29))
    fan_threshold = float(settings.get("fan_threshold_c", 26))
    ac_threshold = float(settings.get("ac_threshold_c", 30))

    mode = settings.get("hvac_mode", "Auto")
    requested = settings.get("manual_hvac_override", "Auto")

    if not occupied:
        hvac = "OFF"

    elif mode == "Manual":
        # Only one requested mode is accepted.
        hvac = requested if requested in ("Fan", "AC", "OFF") else "OFF"

    else:
        # Automatic mode uses temperature, not sunlight.
        if temperature >= ac_threshold:
            hvac = "AC"
        elif temperature >= fan_threshold:
            hvac = "Fan"
        else:
            hvac = "OFF"

    # A single exclusive HVAC state prevents simultaneous activation.
    fan_status = "ON" if hvac == "Fan" else "OFF"
    ac_status = "ON" if hvac == "AC" else "OFF"

    return {
        "light_state": light_state,
        "brightness": max(0, min(100, brightness)),
        "hvac_mode": hvac,
        "fan_status": fan_status,
        "ac_status": ac_status,
        "projection_status": (
            "ON" if settings["projection_mode"] else "OFF"
        ),
        "screen_status": (
            "CLOSED"
            if settings["projection_mode"]
            and settings["projection_screen_supported"]
            else "SIMULATED / NOT CONNECTED"
        ),
        "capacity_alert": occupancy > capacity,
        "available_seats": max(0, capacity - occupancy),
        "occupied": occupied,
    }
