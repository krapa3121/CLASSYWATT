# Smart Classroom Automation & Energy Optimization — DSU Code Clash 2.0

A beginner-friendly Streamlit prototype for exactly three classrooms. Each room is configured with **2 fans, 1 AC, 1 light, and 1 projection screen**.

## Features
- Occupancy simulator or one-frame OpenCV HOG person detection from a local camera, video file, or authorized CCTV stream.
- Capacity and available-seat dashboard.
- Daylight lux simulator and brightness compensation.
- Projection mode with dim/OFF option and simulated screen status.
- Fan/AC interlock; HVAC is OFF when occupancy is zero.
- Manual light and HVAC overrides.
- Configurable power ratings, kWh/cost estimates, weekly demo charts and CSV export.
- Rule-based energy recommendations and unit tests.

## Important prototype limitations
- **Simulation only:** no physical device is controlled. A compatible controller (e.g. a supported relay/IoT gateway) and explicit integration code are required before real-world actuation.
- OpenCV's built-in HOG detector is a basic baseline, not production-grade people counting. It reads one frame per Streamlit rerun and may miss people or double-count detections. Test only with an authorized source.
- The five-minute empty-room delay is shown as a configurable policy but does not persist a real timer between reruns in this starter prototype. Add persistent state/scheduler before deploying.
- Lux is simulated; no actual sensor is queried.
- Weekly charts use illustrative demo data, not measured readings. The recommendation engine is rule-based rather than a trained AI model.
- A live CCTV URL may require authentication, network access, a supported codec, and permission from your institution.

## Folder structure
```text
smart_classroom_automation/
├── app.py
├── requirements.txt
├── README.md
├── backend/
│   ├── config.py
│   ├── occupancy.py
│   ├── control.py
│   ├── energy.py
│   └── recommendations.py
├── frontend/
│   └── ui.py
└── tests/
    └── test_control.py
```

## Windows setup using Anaconda Prompt
1. Extract the ZIP to a folder such as `Desktop\smart_classroom_automation`.
2. Open **Anaconda Prompt** and move into the extracted folder. Example:
   ```bat
   cd %USERPROFILE%\Desktop\smart_classroom_automation
   ```
3. Create an environment (Python 3.11 is recommended):
   ```bat
   conda create -n smartclass python=3.11 -y
   conda activate smartclass
   ```
   If you already have an environment with a supported Python version, activate it instead.
4. Install dependencies:
   ```bat
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```
5. Run the website:
   ```bat
   streamlit run app.py
   ```
6. A browser tab should open. If not, copy the local URL shown in the terminal (usually `http://localhost:8501`).

## Connect VS Code
1. Open VS Code → **File → Open Folder** → select this project folder.
2. Install the Microsoft **Python** extension and **Streamlit** extension if desired.
3. Press `Ctrl+Shift+P` → `Python: Select Interpreter` → choose the `smartclass` environment.
4. Open VS Code Terminal and run `streamlit run app.py`.

## Use a camera/video
- First use the **Simulator** source to confirm the dashboard works.
- Switch Occupancy source to **Camera / video**.
- For a local webcam, leave source blank and use camera index `0`.
- For a video file, paste its full local path into the source box.
- For CCTV, paste an authorized stream URL only if your institution permits it. Do not expose credentials in screenshots or commit them to Git.
- HOG counting runs on one frame per rerun; use a dedicated continuous video pipeline/tracker for production.

## Test the logic
From the project root:
```bat
python -m unittest discover -s tests -v
```

## Test checklist
1. Occupancy and capacity: set simulated people above room capacity and confirm alert.
2. Lighting: set occupancy > 0; confirm light policy is active. Set occupancy 0; light and HVAC go off in the current prototype.
3. Fan/AC: choose Fan, then AC; confirm only one mode is ON. At occupancy 0, HVAC is OFF.
4. Daylight: change lux from 0 to 1500 and observe brightness estimate.
5. Projection: toggle projection and compare Dim versus OFF. HVAC mode remains governed by the selected fan/AC policy.
6. Camera failure: choose Camera / video with an invalid source and confirm a warning rather than a false success.
7. Energy and weekly report: change power ratings/tariff and confirm the current estimate changes; weekly demo report remains illustrative until connected to logged data.

## Suggested hackathon demo flow
1. Show Classroom A at 18/60 occupancy.
2. Increase occupancy above capacity and show the alert.
3. Raise daylight lux and show brightness compensation.
4. Toggle projection mode and show lighting/screen status.
5. Switch HVAC between Fan and AC and show interlock.
6. Set occupancy to zero and show lights/HVAC off.
7. Show weekly baseline vs optimized energy and cost charts, clearly stating the weekly values are demo data.
