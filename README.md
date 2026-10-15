# CLASSYWATT ⚡
### Smart Classroom Automation & Energy Optimization — DSU Code Clash 2.0

**Smarter Classrooms. Greener Futures.**

CLASSYWATT is a Python-based Smart Classroom Automation and Energy Optimization system designed to monitor classroom occupancy, track room capacity, and optimize energy usage through intelligent control logic. It features an interactive Streamlit dashboard, computer-vision-based occupancy detection, equipment control simulation, and energy-saving analytics.

## Features

- **Occupancy monitoring:** Simulated occupancy or OpenCV HOG person detection using a local camera, video file, or authorized CCTV stream.
- **Capacity monitoring:** Displays occupancy, available seats, and capacity alerts.
- **Smart lighting:** Simulates occupancy-based lighting and daylight brightness compensation.
- **Equipment management:** Simulates fan, AC, light, and projection-screen status.
- **Energy optimization:** Estimates energy consumption, electricity costs, and potential savings.
- **Energy recommendations:** Rule-based suggestions for reducing unnecessary electricity usage.
- **Interactive dashboard:** Built with Streamlit, with configurable power ratings and electricity tariffs.
- **Reports and testing:** Demo charts, CSV export, and unit tests.

## Technology Stack

- Python 3.11
- Streamlit
- OpenCV
- NumPy
- Pandas
- Unittest

## Project Structure

```text
smart_classroom_automation/
├── app.py
├── requirements.txt
├── README.md
├── backend/
│   ├── __init__.py
│   ├── config.py
│   ├── control.py
│   ├── energy.py
│   ├── occupancy.py
│   └── recommendations.py
├── frontend/
│   ├── __init__.py
│   └── ui.py
└── tests/
    └── test_control.py
```

## Installation and Setup (Windows)

### 1. Clone the repository

```bash
git clone https://github.com/krapa3121/CLASSYWATT.git
cd CLASSYWATT
```

Alternatively, open your existing project folder in VS Code.

### 2. Create a Python environment

Using Anaconda Prompt:

```bash
conda create -n smartclass python=3.11 -y
conda activate smartclass
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Run the application

```bash
streamlit run app.py
```

Open the local URL displayed in your terminal, usually `http://localhost:8501`.

## Camera and Video Usage

1. Start with the simulator to verify the dashboard.
2. Select the camera or video occupancy source.
3. For a local webcam, use camera index `0` if supported.
4. For video files or CCTV, use an accessible source and follow your institution's authorization and privacy rules.

Camera support depends on the source, network, authentication, and supported video formats.

## Run Tests

From the project root:

```bash
python -m unittest discover -s tests -v
```

## Suggested Hackathon Demonstration

1. Show a classroom with simulated occupancy.
2. Increase occupancy beyond room capacity and demonstrate the alert.
3. Change simulated daylight levels and observe brightness compensation.
4. Toggle projection and HVAC modes.
5. Set occupancy to zero and demonstrate the equipment control policy.
6. Display energy and cost estimates.
7. Explain how occupancy-based automation can reduce unnecessary energy consumption.

## Important Prototype Limitations

- **Hardware control is simulated:** Physical lights, fans, AC units, and projection screens are not controlled without compatible hardware and implemented integrations.
- **Basic computer vision:** OpenCV HOG detection is a baseline and may miss people or produce inaccurate counts.
- **Simulated sensor values:** Daylight readings and demonstration energy reports are not actual sensor or meter readings.
- **Timer limitations:** The empty-room delay is a configurable policy, not a persistent production timer.
- **Recommendations:** The current recommendation engine is rule-based, not a trained AI model.

The application is a prototype intended for demonstration and further development. Real-world deployment requires authorized camera access, appropriate hardware integration, testing, and privacy safeguards.

## Future Enhancements

- Integrate authorized live occupancy tracking.
- Connect compatible IoT controllers for physical equipment automation.
- Add actual energy-meter and light-sensor readings.
- Store occupancy and energy history for analytics.
- Develop predictive energy optimization.

---

**CLASSYWATT — Smarter Classrooms. Greener Futures. ⚡**