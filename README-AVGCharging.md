# Info for the Group from Roman
I Recommand including 3 kinds of your program to the solution you reach in
1. Workling Simulation (wih description which steps are to take to make it run)
2. A state where the Robotinos can be sent and docked manually to a closest charger
3. The most current state of your work towards adapting the logic of the simulation to the real world


# Project Title: Optimization of Charging Management for Robotino AGVs in the IoT Factory

## Project Overview:
In this project, your team will improve the charging management system for **Robotino AGVs** (Autonomous Guided Vehicles) used in the IoT Factory at HSBI. Currently, Robotinos are used to transport materials between various modules, navigating autonomously, avoiding obstacles, and interacting with factory modules. However, their charging management system is basic, relying on fixed stations and simple rules, such as sending robots to charge whenever they are idle. This project aims to develop a more advanced charging system that optimizes charging times, maximizes the use of available stations, and integrates smoothly with the factory’s software architecture, **HSBI-OptiFlow**.

## Context:
The **IoT Factory** at HSBI is a cutting-edge facility where autonomous systems, including Robotino AGVs, interact with various production modules. These AGVs are essential for material transport, ensuring smooth logistics in real-time. The existing charging system for the Robotinos has significant limitations: it assigns fixed charging stations to each Robotino and triggers charging whenever a robot is idle. This is inefficient, as it doesn’t consider factors such as the robot's battery health, current location, or the overall distribution of charging loads across multiple stations.

Your task is to design a **smarter charging management system** to address these inefficiencies and improve overall system performance. This will involve analyzing the current infrastructure, designing optimized charging algorithms, and ensuring seamless integration into the factory’s existing software framework.

## Key Project Goals:

### 1. Analyze Components and Environment:
- **Investigate Robotinos**: Explore the technical specifications of Robotinos, including battery types, available sensors, interfaces, and the limitations of the current system.
- **Charging Stations**: Examine the available charging stations, their placement in the factory, and their compatibility with different Robotino models. Consider if relocating or adding new stations could improve efficiency.
- **Data Collection**: Set up methods to track battery levels in real-time and gather data about station usage, Robotino tasks, and charging durations.

### 2. Evaluate Current and Previous Solutions:
- Study the **existing basic charging system** to understand its strengths and limitations.
- Review any **previous implementations** or systems that might have attempted to improve charging strategies (both within the IoT factory and in similar industrial settings) and compare their effectiveness.

### 3. Design a New Charging Concept:
- Develop a more advanced, **dynamic charging system** that optimizes station assignments based on real-time data about robot locations, battery levels, and station availability.
- Ensure **battery preservation** and **balanced station usage** to prevent bottlenecks.
- Use **flowcharts and diagrams** to visualize the new process.

### 4. Implement the New Charging System:
- Use Python or another suitable programming language to develop the new system.
- Implement **real-time tracking** of battery levels and station statuses and automate decisions about when and where each Robotino should charge.
- Incorporate a **fail-safe mechanism** for handling station malfunctions or Robotino failures.

### 5. Integrate into HSBI-OptiFlow:
- Ensure seamless integration into **HSBI-OptiFlow**, the factory’s logistics software.
- Enable clear data flows between the charging system and existing OptiFlow modules.

## Deliverables:
1. **Research Report**:
   - Detailed analysis of the current system and your proposed solution.
   - The report should include:
     - **Introduction**: Motivation and importance of efficient charging.
     - **Analysis**: Breakdown of Robotinos, charging stations, and system limitations.
     - **Design**: Flowcharts, process diagrams, and technical specifications.
     - **Implementation Plan**: Outline how the system will be developed and tested.
     - **Integration Strategy**: Explanation of how it will work within OptiFlow.

2. **Software Prototype**:
   - A working prototype of the charging management system implemented in Python.
   - Real-time decision-making for Robotino charging.

3. **Integration with OptiFlow**:
   - Integrated system within **HSBI-OptiFlow**.
   - User interface elements for monitoring and controlling the charging processes.

4. **Presentation and Demonstration**:
   - Present your research, design, and working prototype to the class.
   - Include a live demonstration of the system in real-time.

