# 🚆 Intelligent Train Control RL Environment

## 📌 Overview
This project simulates a real-world train approaching a station. The objective is to control acceleration and braking to stop efficiently without overshooting, while minimizing energy consumption.

## 🎯 Objectives
- Ensure safe stopping at station
- Avoid overshoot
- Optimize energy usage
- Encourage smooth braking

## 🧠 Environment Design

### State
- Train speed
- Distance to station

### Actions
- Acceleration
- Braking

### Reward Strategy
- Step penalty: -1 (encourages faster completion)
- Energy penalty proportional to speed
- Overspeed penalty near station
- Smooth stopping bonus
- Overshoot penalty

## 🚀 Features
- Realistic train dynamics
- Speed control near station
- Energy-efficient driving behavior
- Smooth braking optimization

## 🛠️ How to Run

```bash
python -m uvicorn my_env.server:app --reload