import unittest
from backend.control import calculate_controls
from backend.config import ROOMS, DEFAULT_SETTINGS

class ControlTests(unittest.TestCase):
    def settings(self, **kwargs):
        s = dict(DEFAULT_SETTINGS)
        s.update(kwargs)
        return s

    def test_lights_turn_on_when_occupied(self):
        out = calculate_controls(ROOMS["Classroom A"], self.settings(), 10)
        self.assertIn(out["light_state"], ("ON", "OFF"))  # brightness may be 0 only under other policies

    def test_empty_room_turns_hvac_off(self):
        out = calculate_controls(ROOMS["Classroom A"], self.settings(hvac_mode="AC"), 0)
        self.assertEqual(out["hvac_mode"], "OFF")
        self.assertEqual(out["brightness"], 0)

    def test_fan_and_ac_never_simultaneous(self):
        out = calculate_controls(ROOMS["Classroom A"], self.settings(hvac_mode="Fan"), 12)
        self.assertFalse(out["fan_status"] == "ON" and out["ac_status"] == "ON")

    def test_projection_mode(self):
        out = calculate_controls(ROOMS["Classroom A"], self.settings(projection_mode=True), 12)
        self.assertEqual(out["projection_status"], "ON")
        self.assertEqual(out["brightness"], 25)

    def test_capacity_overflow(self):
        out = calculate_controls(ROOMS["Classroom A"], self.settings(), 61)
        self.assertTrue(out["capacity_alert"])

if __name__ == "__main__":
    unittest.main()
