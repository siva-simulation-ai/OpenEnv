# 🚆 Intelligent Train Control RL Environment

## 📌 Overview
This project implements a Reinforcement Learning (RL) environment that simulates a train approaching a station. The agent must intelligently control acceleration and braking to achieve a safe, smooth, and energy-efficient stop.

The environment is exposed via a FastAPI server and deployed on Hugging Face Spaces for real-time interaction.

---

## 🌐 Live Demo
👉 https://sivaepuri-train-control-env.hf.space  

Test endpoints:
- `/reset` → Initialize environment  
- `/step` → Take action  

---

## 🎯 Objectives
- Ensure safe stopping at the station
- Avoid overshooting (crash scenario)
- Minimize energy consumption
- Encourage smooth braking behavior

---

## 🧠 Environment Design

### 🔹 State
- `speed` → Current train speed  
- `distance` → Distance remaining to station  

### 🔹 Actions
- `accelerate` → Increase speed  
- `brake` → Decrease speed  

---

## 🏆 Reward Strategy
The reward function is carefully designed to balance safety and efficiency:

- ⛔ Step penalty: `-1` (encourages faster completion)
- ⚡ Energy penalty: proportional to speed
- 🚧 Overspeed penalty near station (distance < 50m)
- 🎯 Smooth stop bonus for low-speed stopping
- 💥 Overshoot penalty (`-100`) for unsafe stopping

---

## 🚀 Key Features
- Realistic train dynamics simulation
- Adaptive speed control near station
- Energy-efficient driving behavior
- Smooth braking optimization
- Fully API-driven (FastAPI)
- Deployable and testable via Hugging Face Spaces

---

## 🧪 Inference Script
A compliant `inference.py` script is included to:
- Interact with the environment API
- Simulate an agent policy
- Follow required hackathon logging format:
  - `[START]`
  - `[STEP]`
  - `[END]`

---

## 🛠️ How to Run Locally

### 1. Install dependencies
```bash
pip install -r requirements.txt
