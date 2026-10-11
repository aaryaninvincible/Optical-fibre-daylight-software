# Patent-Oriented Novelty & Technical Invention Disclosure

## Title of Invention
**"AI-Controlled Adaptive Optical-Fibre Daylighting System with Predictive Hybrid LED Supplementation and Autonomous Thermal Protection"**

---

## 1. Field of the Invention
The present disclosure relates to renewable daylighting systems and energy-efficient building automation, and more specifically to an intelligent solar concentrator system coupled with optical fibre waveguides, automated multi-axis sun tracking, machine-learning-driven lookahead daylight prediction, and predictive hybrid LED dimming.

---

## 2. Background and Prior Art Differentiation

### 2.1 Known in the Art (Prior Art Baseline):
1. **Solar Concentrators:** Fresnel lenses and parabolic mirrors for solar thermal or PV systems.
2. **Light Pipes and Optical Fibres:** Bundles of PMMA or silica fibres routing unmanaged natural light into buildings.
3. **Reactive Photo-Dimming:** Ambient light sensors that decrease or increase LED current in immediate response to instantaneous indoor lux.

### 2.2 Prior Art Shortcomings:
- **Thermal Ferrule Failure:** In conventional fiber coupling systems, intense infrared (IR) concentration at the focal point can heat the fiber ferrule above 120°C, causing polymer cladding melting or optical epoxy carbonization.
- **Visual Flicker / Dimmer Hunting:** Under intermittent cloud cover, classical PI dimmers rapidly oscillate LED brightness, causing severe occupant eye strain and visual fatigue.
- **Blind Tracking:** Standard trackers follow astronomical tables blindly without assessing whether cloud cover renders tracking ineffective, wasting motor electrical energy.

---

## 3. Core Inventive Novelty & Proposed Claims

### Novel Combination & Method Claims:
1. **Predictive Lookahead Multi-Horizon Control Architecture:**
   - Incorporating an ensemble machine-learning model (AR-GBDT/MPC) that processes time-lagged global horizontal irradiance ($GHI$), direct normal irradiance ($DNI$), cloud factor vectors, and celestial coordinates to forecast illuminance 15, 30, and 60 minutes into the future.
2. **Pre-emptive Anti-Flicker Dimming Trajectory:**
   - Rather than reacting *after* daylight has already plummeted, the controller initiates a smooth, exponential pre-ramp of the backup LED luminaire ahead of an incoming cloud shadow, maintaining continuous illuminance uniformity ($U_0 \ge 0.8$) without abrupt switching.
3. **Autonomous Micro-Defocusing Thermal Safety Guard:**
   - A closed-loop thermal protection method where, upon focal spot thermocouple telemetry reaching a safety threshold ($T_{\text{safe}} \approx 80^\circ\text{C}$), the dual-axis gimbal introduces a controlled $0.8^\circ\text{–}1.5^\circ$ angular offset (intentional micro-defocusing) or activates an IR shutter, reducing peak focal flux density while sustaining non-destructive visible light delivery into the core.
4. **Co-axial Hybrid Luminaire Design:**
   - An integrated luminaire comprising a central wide-angle micro-prism daylight diffuser surrounded by a concentric dimmable LED SMD array, governed by a unified digital controller that modulates the complementary luminous flux ratio $\Phi_{\text{daylight}} : \Phi_{\text{LED}}$.

---

## 4. System Block Diagram & Flow

```
[ Astronomical Ephemeris & Pyranometer ]
                   │
                   ▼
       [ AI Lookahead Forecaster ]
                   │ (15-60 min Horizon)
                   ▼
     [ Model Predictive Controller (MPC) ]
          │                    │
   (Angle / Defocus)     (Predictive PWM)
          │                    │
          ▼                    ▼
[ Motorized Concentrator ]   [ Hybrid LED Luminaire ]
          │ (Visible Flux)     │ (Electrical Flux)
          └───────────┬────────┘
                      ▼
            [ Combined Room Lux ]
                      │
            [ Occupancy Feedback ]
```

---

## 5. Industrial Applicability
The disclosed system is readily applicable to commercial corporate headquarters, zero-energy research laboratories, hospitals, educational campuses, underground metro transit stations, and green building standard certifications (LEED Platinum, WELL Building Standard).

*Disclaimer: This document outlines conceptual and architectural novelty for technical disclosure and academic demonstration. Formal patentability requires prior art novelty search and patent attorney review.*
