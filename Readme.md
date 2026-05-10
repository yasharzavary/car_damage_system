![CDD](https://en.smartautoscan.com/comdata/69843/202401/20240102152404bbfee4.png)

<!-- Repo badges -->
![GitHub stars](https://img.shields.io/github/stars/yasharzavary/car_damage_system?style=flat-square&color=yellow)
![GitHub forks](https://img.shields.io/github/forks/yasharzavary/car_damage_system?style=flat-square&color=blue)
![GitHub issues](https://img.shields.io/github/issues/yasharzavary/car_damage_system?style=flat-square&color=red)
![GitHub last commit](https://img.shields.io/github/last-commit/yasharzavary/car_damage_system?style=flat-square&color=green)
![GitHub repo size](https://img.shields.io/github/repo-size/yasharzavary/car_damage_system?style=flat-square)

<!-- Project / tech stack badges -->
![Python](https://img.shields.io/badge/Python-3.10-blue?style=flat-square&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-Inference%20Server-black?style=flat-square&logo=flask&logoColor=white)
![Raspberry Pi](https://img.shields.io/badge/Raspberry%20Pi-4-C51A4A?style=flat-square&logo=raspberry-pi&logoColor=white)
![Proteus](https://img.shields.io/badge/Proteus-VSM%209-0078D7?style=flat-square)
![Platform](https://img.shields.io/badge/Platform-Embedded%20System-orange?style=flat-square)

<!-- Project status / type badges -->
![Status](https://img.shields.io/badge/Status-In%20Development-yellow?style=flat-square)
![License](https://img.shields.io/github/license/yasharzavary/car_damage_system?style=flat-square)
![Language](https://img.shields.io/github/languages/top/yasharzavary/car_damage_system?style=flat-square)

⭐ Star on GitHub — your support motivates us a lot! 🙏😊

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Follow-blue?logo=linkedin)](https://www.linkedin.com/in/yashar-zavary-rezaie/)
[![Telegram](https://img.shields.io/badge/Telegram-Join-blue?logo=telegram)](https://t.me/YZR_Computer)

---

## Table of Contents
1. [Introduction](#-introduction)
2. [Requirements](#-requirements)
3. [Architecture](#architecture)
4. [How to Use](#how-to-use)
5. [Notes](#notes)
6. [Contributions & Feedback](#contributions--feedback)

---

## 🚀 Introduction

Have you ever returned to a parking lot and found your car damaged — with no idea when or how it happened?

This system is designed to solve exactly that problem. When a **car enters a parking lot**, the system captures photos of the **front and rear** of the vehicle and stores them. When the **car exits**, it takes new photos and compares them against the entry images. If any **new damage is detected**:

- 🔔 A **buzzer sounds** to immediately alert nearby staff
- 📟 The **LCD display** shows the damage status (front and rear result)
- 🔒 The incident is logged so security can take action before the car leaves

---

## 📋 Requirements

### Software
| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.10 | Main language for all scripts |
| Proteus VSM | 9.x | Board simulation |
| PyTorch | latest | Damage detection model |
| Flask | latest | Inference API server |

### Hardware (for real deployment)
| Component | Details |
|-----------|---------|
| Board | Raspberry Pi 4 |
| Display | 16×2 LCD (4-bit mode) |
| Sensors | 2× PIR sensors (car in / car out) |
| Output | Active buzzer |
| Camera | Compatible with Raspberry Pi (front + rear) |

### Inference Server
The image processing server can run on:
- A **PC or laptop** on the same network
- The **Raspberry Pi 4** itself (when deploying to real hardware)
- An **ESP32** or other Wi-Fi-capable device

---

## Architecture

This project is built around a **Raspberry Pi 4** board, simulated in **Proteus VSM**, and can be deployed on real hardware for use in actual parking facilities.

All code is written in **Python**.

The image processing system is built with **PyTorch** and runs on a separate server via a **Flask API**. The Raspberry Pi communicates with this server over the network — meaning the same inference server can also be used with other devices such as an **ESP32** or any other network-capable embedded system.

---

## How to Use

**1. Clone the project**

```bash
git clone https://github.com/yasharzavary/car_damage_system.git
cd car_damage_system
```

**2. Install dependencies**

```bash
pip install -r requirements.txt
```

**3. Open the project in Proteus**

Open `car_damage_system.pdsprj` in Proteus VSM 9.

**4. Update file paths**

> [!IMPORTANT]
> Proteus cannot resolve relative paths, so you must update the hardcoded paths in **4 files**:
> - 3 files inside the `rasberry PI codes/` folder
> - `worker_damage_detection.py`
>
> Change all path strings to match your local directory structure.

**5. Run the project in Proteus**

Start the simulation in Proteus.

**6. Test car entry (CAR IN)**

Add photos to the `incoming/` folder, then set the **CAR_IN** pin `HIGH`. The system will move the images into the `data/images/` folder (indexed storage). The `incoming/` folder will be cleared automatically.

> [!NOTE]
> Licence plate detection is not yet implemented. Currently, the system works with **one car at a time**. Multi-car support is planned for a future update.

**7. Test car exit (CAR OUT)**

Add new photos to the `incoming/` folder and set the **CAR_OUT** pin `HIGH`. The system will compare the new images against the stored entry images. If new damage is detected, the **buzzer will sound** and the **LCD will display the result**.

**8. Stopping the simulation**

> [!WARNING]
> Do **not** stop the simulation abruptly. Follow these steps to shut down safely:
> 1. Set the **STOP** LogicState pin to `HIGH`.
> 2. Wait until the LCD displays **"System Stopped"**.
> 3. Then stop the Proteus simulation.
>
> Skipping this step will leave the `worker_damage_detection.py` process running in the background on your PC.

---

## Notes

- 🚗 **Single car mode only** — the current version handles one car at a time. Licence plate detection for multi-car support is planned for the next update.

- 🖥️ **Why a separate inference server?** — Proteus VSM cannot simulate the PyTorch library directly on the Raspberry Pi. The image processing runs on an external server and communicates with the board via Flask API. When deploying to real hardware, you can run the inference code directly on the Raspberry Pi or on any server on the same network.

- 📡 **Wireless deployment** — the inference server can also be hosted on an **ESP32** or any Wi-Fi-capable device, making it easy to integrate into a wireless setup.

---

## Contributions & Feedback

Suggestions, improvements, and code reviews are always welcome.  
Feel free to open an issue, submit a pull request, or reach out directly.

[![Telegram](https://img.shields.io/badge/Telegram-Contact-blue?logo=telegram)](https://t.me/YZR_Computer)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?logo=linkedin)](https://www.linkedin.com/in/yashar-zavary-rezaie/)