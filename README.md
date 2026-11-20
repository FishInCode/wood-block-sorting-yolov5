<div align="center">

# 🪵 Wood-Block Sorting Robot
### A Real-time YOLOv5 Visual Inspection System on Edge Device

[![Competition](https://img.shields.io/badge/Award-Zhejiang_Provincial_Third_Prize-blue)]()
[![Python](https://img.shields.io/badge/Python-3.8+-yellow)]()
[![Hardware](https://img.shields.io/badge/Deploy-Jetson_Nano-green)]()

</div>

---

## 📖 1. Project Overview
This project was developed for the **Zhejiang Provincial Undergraduate Artificial Intelligence Competition**. It is an end-to-end robotic sorting system designed to identify defects in wood blocks on a conveyor belt and control a 6-DOF robotic arm to separate them.

*( 👇 在这里插入现场运行的照片 👇 )*
*[Insert setup.jpg here]*

### 🛠️ System Architecture
The system operates in a **closed-loop pipeline**:
`Camera Capture` ➡️ `YOLOv5 Inference (Jetson Nano)` ➡️ `UART Communication` ➡️ `Motion Execution (STM32)`.

---

## 🚀 2. My Core Contributions
As the Team Leader and Vision Developer, I focused on the intersection of software algorithms and hardware deployment.

| Module | Technical Implementation |
| :--- | :--- |
| **Dataset & Model** | Built and annotated a custom dataset of **1,820 images** under various lighting conditions. Trained YOLOv5 and tuned confidence/IoU thresholds for precise defect detection. |
| **Edge Deployment** | Deployed the PyTorch model to **Jetson Nano** using **TensorRT** to achieve real-time inference speed. |
| **Hardware Integration** | Engineered **UART communication protocols** between Jetson Nano and STM32. Converted vision coordinates into serial command frames for accurate arm control. |

---

## 🐛 3. Engineering Challenges & Troubleshooting
Real-world engineering is never without bugs. Here are the key challenges we faced and solved:

- **Vision Library Compatibility:** While deploying to the Jetson Nano, we encountered severe memory leaks and crashes due to conflicts between OpenCV libraries and the TensorRT engine. 
  - *Solution:* I debugged the environment dependencies, recompiled the necessary C++ libraries, and successfully stabilized the real-time video stream.
- **Coordinate Transformation:** The camera perspective introduced a spatial offset. 
  - *Solution:* I calculated the pixel-to-millimeter mapping ratio and applied a geometric transformation matrix, ensuring the arm grasps the correct position.
  
*( 👇 在这里插入一张代码截图或识别结果图 👇 )*
*[Insert result.png here]*

---

## 📊 4. Results & Achievements
- **🏆 Awarded Third Prize** at the Zhejiang Provincial AI Competition (Dec 2025).
- **⏱️ Delivered** the fully functional prototype **one week ahead** of the deadline.
- Achieved stable real-time frame processing on the Jetson Nano without memory drops.

---

## 🧠 5. Future Improvements
While the system successfully sorted wooden blocks, the parameter tuning process was largely empirical. Fixing localization errors for one shape sometimes broke another. 

In my future graduate studies (focusing on Computer Vision and Data Science), I aim to build a more systematic evaluation framework. I want to use statistical learning methods to analyze *why* a model fails under spatial distribution shifts, rather than just adjusting parameters until it works by chance.

---

## 🙏 6. Acknowledgements (特别感谢)
This project wouldn't have been possible without the brilliant team behind it.

- **Academic Advisor:** [填写指导老师的名字/拼音，比如 Prof. Zhang] (Zhejiang University) - *For his invaluable guidance on hardware integration and system architecture.*
- **Team Members:** [填写队友名字，比如 Li Ming, Wang Hua] - *For their dedication in mechanical design, data annotation, and hardware testing.*
- **Lab Support:** [填写实验室/学院名称，比如 Smart Vision Lab at ZJSU] - *For providing the equipment and testing environment.*

---
<div align="center">
  <i>Developed with ❤️ by FishInCode</i>
</div>
