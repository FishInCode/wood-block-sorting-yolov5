# Wood-Block Sorting Robot (YOLOv5 + TensorRT on Jetson Nano)

## Overview
A real-time visual inspection system for a conveyor-belt robotic arm. We built this for the Zhejiang Provincial Undergraduate AI Competition to identify defects in wood blocks and control the arm to separate them.

## Tech Stack
*   **Language:** Python, C++
*   **Computer Vision:** YOLOv5, OpenCV
*   **Deployment:** TensorRT, NVIDIA Jetson Nano
*   **Hardware:** STM32 Microcontroller, UART

## My Key Contributions
1. **Dataset & Model:** Built and annotated a custom dataset of 1,820 images under different lighting conditions. Trained the YOLOv5 model and tuned the confidence/IoU thresholds.
2. **Edge Deployment:** Deployed the model to a Jetson Nano using TensorRT for faster inference.
   * *Troubleshooting:* I encountered severe compatibility issues between OpenCV and TensorRT, which caused memory leaks. I had to debug the environment, recompile the libraries, and finally achieved stable real-time processing.
3. **Hardware Integration:** Wrote UART communication code to send the detection results from the Jetson Nano to the STM32 controller, allowing the 6-DOF arm to pick the correct blocks.

## Results & Achievements
*   Completed the end-to-end pipeline from image capture to robotic sorting.
*   **Awarded Third Prize (Provincial Level)** at the Zhejiang Provincial Undergraduate AI Competition (Dec 2025).
*   Coordinated the team and submitted the project one week before the deadline.

## Future Improvements
In this project, I mainly focused on making the model detect defects and sending the data to the controller. However, I realized I didn't build a systematic evaluation framework to compare different model configurations (like speed vs. accuracy). In my future graduate studies, I hope to learn more about data analysis and statistical methods to evaluate model performance in real-world environments.# wood-block-sorting-yolov5
YOLOv5-based visual inspection for conveyor sorting
