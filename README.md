# 🪵 Wood-Block Sorting Robot (YOLOv5 + TensorRT on Jetson Nano)

## 🚀 Project Overview
A real-time visual inspection and sorting system for a conveyor-belt robotic arm. Developed for the **Zhejiang Provincial AI Competition**, this system detects defects in wood blocks and triggers a 6-DOF arm to separate them.

### 🛠️ Tech Stack
*   **Software:** Python, C++, YOLOv5, OpenCV
*   **Edge Deployment:** TensorRT, NVIDIA Jetson Nano
*   **Hardware:** STM32 Microcontroller, UART

---

## 💡 My Core Contributions
*   **Dataset & Model:** Built and annotated a custom dataset of **1,820 images**. Trained YOLOv5 and tuned confidence/IoU thresholds to balance precision and recall.
*   **Edge Deployment:** Deployed the model to Jetson Nano using TensorRT. Successfully achieved real-time frame processing without memory leaks.
*   **System Integration:** Engineered UART communication routines between Jetson Nano and STM32 to transmit detection coordinates for accurate pick-and-place operations.

---

## 🐛 Engineering Troubleshooting (The Hard Part)
*Real engineering is about solving unexpected problems.*
*   **OpenCV & TensorRT Conflicts:** Encountered severe compatibility issues and crashes on the Jetson Nano. I recompiled the C++ libraries and debugged the environment dependencies to stabilize the pipeline.
*   **Vision-Motion Synchronization:** Addressed spatial offsets between the camera's perspective and the robotic arm's reach, ensuring accurate target localization.

---

## 🏆 Results & Achievements
*   **Awarded Third Prize** (Provincial Level) at the Zhejiang Provincial Undergraduate AI Competition (Dec 2025).
*   Coordinated the team and delivered the functional prototype **one week ahead** of the deadline.

---

## 🙏 Acknowledgements
*   **Academic Advisors:** [Vice-Prof.Zu] at [ZJSU], for his guidance on system architecture.
*   **Team Members:** [Miss XiaoQing&Mr Zhan], for their collaboration in mechanical design and hardware testing.

---
*Maintained by FishInCode. For more details, please feel free to contact me.*
