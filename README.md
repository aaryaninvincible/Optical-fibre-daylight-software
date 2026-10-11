# SolarFiber AI: Intelligent Optical-Fibre Solar Daylighting System
**Physics-Based Digital Twin, Real-Time Animated Simulation, and Machine Learning Controller**

---

## 🌟 Executive Overview
**SolarFiber AI** is a complete, production-grade cyber-physical digital twin and animated engineering simulation of an intelligent optical-fibre daylighting system for energy-efficient buildings. It realistically models astronomical solar kinematics, optical concentration, thermal balance with infrared cold-mirror rejection, dielectric waveguide propagation (Beer-Lambert attenuation), indoor photometric distribution, and an AI-driven Model Predictive Controller (MPC) with multi-horizon time-series forecasting.

---

## 🚀 Key Features

1. **Interactive Hardware Digital Twin (Canvas/SVG):**
   - Real-time celestial sun motion with dynamic day/dawn/dusk/night sky gradients.
   - Animated direct solar light rays with photon wavefronts.
   - Dual-axis motorized tracker gimbal with Fresnel lens / Parabolic concentrator optics.
   - Focal beam concentration and infrared cold-mirror rejection beam.
   - Optical fiber waveguide with internal light pulses propagating through core/cladding.
   - Architectural cross-section room with ceiling, floor, desk workplane, animated occupant, optical luminaire diffuser, and concentric LED SMD backup ring.
   - 9 Interactive Virtual Sensor HUD Pins with live telemetry.

2. **AI-Driven Model Predictive Controller (MPC):**
   - 4 Operational Modes: *Manual Override*, *Astronomical Solar Tracker*, *Closed-Loop PI Hybrid*, and *AI-Optimized MPC*.
   - Multi-horizon forecasting (T+15m, T+30m, T+60m) predicting irradiance, expected indoor lux, and pre-emptive LED power.
   - Anti-flicker exponential smoothing to prevent visual fatigue.
   - Autonomous micro-defocusing thermal protection preventing focal ferrule overheating.

3. **Multi-Channel Real-Time Telemetry & Charts:**
   - Real-time streaming charts for Daylight vs LED Power, Solar GHI/DNI, Focal Temperature, and Cumulative Energy Savings %.

4. **8 Predefined Research Experiments & 24-Hour Guided Demo:**
   - Automated scenario runner showing diurnal progression (09:00 -> 18:00) with cloud incursion, AI predictive ramp, peak solar, and summary stats.
   - 8 automated parametric sweeps (Sunny baseline, Cloud attenuation, Rapid cloud transient, Fiber length sweep, Tracker comparison, PI vs AI MPC, LED vs Hybrid, Lux target sweep).

5. **Data Generation & Real Data Hub:**
   - One-click synthetic 24-hour / annual CSV dataset generator with data provenance tagging.
   - CSV import parser for external real-world irradiance datasets (NSRDB, EnergyPlus, DOE).

6. **Research Mode:**
   - Dedicated analytical drawer displaying step-by-step mathematical formulas, LaTeX equations, parameter tables, and live variable watch windows.

7. **Python ML & Scientific Suite:**
   - Complete Python package (`python_ml/`) with synthetic dataset generator, model trainer comparing Linear Regression, Random Forest, GBDT, XGBoost, and MLP neural regressors, standalone physics validator, and microcontroller IoT serial bridge.

---

## 📁 Repository Structure

```
Optical fibre daylight software/
├── index.html                      # Main Engineering Dashboard Web Application
├── css/
│   └── styles.css                  # Cyber-physical dark theme design system
├── js/
│   ├── solar_math.js               # Astronomical solar geometry (Spencer, Michalsky)
│   ├── optical_thermal_sim.js      # Concentrator, fiber propagation, and lumen photometrics
│   ├── ai_controller.js            # AI MPC controller, forecasting, and thermal guard
│   ├── digital_twin_canvas.js      # High-performance 2D Canvas animated renderer
│   ├── charts.js                   # Real-time multi-channel telemetry charts
│   ├── experiments.js              # 8 Predefined experiments & 24h demo scenario
│   ├── data_exporter.js            # CSV synthetic generator & real data importer
│   └── app.js                      # Application coordinator and UI event binder
├── python_ml/
│   ├── requirements.txt            # Python dependencies
│   ├── solar_physics_engine.py     # Standalone Python physics validator
│   ├── synthetic_data_generator.py # 1-year 35,040-sample dataset builder
│   ├── train_models.py             # ML model benchmarking suite (XGBoost, RF, MLP)
│   └── hardware_serial_bridge.py   # Microcontroller UART/Serial IoT interface
├── Data sets/                      # Real-World Measured Solar Irradiance & Sites Datasets
│   ├── 2017_2019.csv/              # 3-Year 15-Minute PSM Solar Irradiance Dataset (105,122 rows)
│   ├── 2017.csv/                   # 1-Year 15-Minute Solar Dataset (35,042 rows)
│   ├── solar_angles_dataset.csv/   # Topocentric Solar Zenith and Azimuth Angles Dataset
│   ├── Solar_Sites_Dataset_India.csv # 2,002 Regional Sites Solar & Weather Parameters
│   └── India Map Solar Irradiance.xlsx
├── RESEARCH_PAPER.md               # Complete academic research paper (IEEE format)
├── PATENT_NOVELTY_DISCLOSURE.md    # Patent-oriented novelty & claims document
└── README.md                       # Documentation and quick start guide
```

---

## ⚡ Quick Start Instructions

### Running the Web Digital Twin Simulation:
1. Double-click or open `index.html` directly in any modern web browser (Chrome, Edge, Firefox, Safari).
2. Alternatively, serve locally using Python:
   ```bash
   python -m http.server 8080
   ```
   and navigate to `http://localhost:8080`.

### Running the Python Machine Learning & Physics Suite:
1. Navigate to the `python_ml/` directory:
   ```bash
   cd python_ml
   pip install -r requirements.txt
   ```
2. Validate physics calculations:
   ```bash
   python solar_physics_engine.py
   ```
3. Generate synthetic dataset or train ML models directly on real datasets:
   ```bash
   python train_models.py
   ```

---

## 🔬 Mathematical Models Summary

- **Extraterrestrial Irradiance:** $G_{on} = G_{sc} \cdot [1 + 0.033\cos(2\pi d_n / 365)]$
- **Zenith Angle:** $\cos(\theta_z) = \sin(\phi)\sin(\delta) + \cos(\phi)\cos(\delta)\cos(\omega)$
- **Concentrator Power:** $P_{\text{focused}} = [DNI \cdot \cos(\theta_i) + c_{\text{diff}} DHI] \cdot A_{\text{col}} \cdot \eta_{\text{col}}$
- **Fiber Output Power (Beer-Lambert):** $P_{\text{out}} = P_{\text{in}} \cdot 10^{-(\alpha_{\text{dB/m}} L + \alpha_{\text{bend}})/10}$
- **Indoor Daylight Illuminance:** $E_{\text{daylight}} = \frac{\Phi_{\text{daylight}} \cdot CU \cdot LLF}{A_{\text{floor}}}$
- **Predictive LED Power:** $P_{\text{LED}} = \max\left(0, \frac{E_{\text{target}} - E_{\text{daylight}}}{E_{\text{target}}}\right) \cdot P_{\text{max}}$

---

## 📜 Scientific Provenance & Ethical Disclaimer
- **Data Provenance:** The software supports both physics-informed synthetic simulations and empirical evaluations on real-world datasets (such as the 3-Year measured Physical Solar Model dataset).
- **Academic and Research Use:** This project is engineered for university research demonstrations, IEEE conference papers, technical viva presentations, and patent prototype evaluation.
