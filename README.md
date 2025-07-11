# 🧠 Job Scheduling Problem Solver (AI Project)

This project is part of our Artificial Intelligence & Machine Learning course at [Your University Name]. It aims to solve the **Job Scheduling Problem (JSP)** using two intelligent approaches: **Backtracking Search Algorithm** and **Genetic Algorithm**, both implemented in **Python**.

---

## 📌 Table of Contents
- [Overview](#overview)
- [Project Objectives](#project-objectives)
- [Technologies Used](#technologies-used)
- [Features](#features)
- [Algorithms Used](#algorithms-used)
- [Datasets](#datasets)
- [Installation & Usage](#installation--usage)
- [Results](#results)
- [Team Roles](#team-roles)
- [License](#license)

---

## 🧩 Overview

The **Job Scheduling Problem (JSP)** involves assigning a set of jobs to a limited number of machines or resources while satisfying constraints such as:
- Job precedence (some jobs must be completed before others)
- Time constraints
- Resource availability

The goal is to produce a valid schedule that **minimizes the makespan** (total completion time) or **maximizes resource utilization**.

---

## 🎯 Project Objectives

- Apply fundamental AI concepts in a real-world scenario.
- Implement and compare two AI approaches for solving JSP:
  - Backtracking Search Algorithm
  - Genetic Algorithm
- Explore trade-offs between optimality and efficiency.
- Handle different types of scheduling constraints.
- Document the process, challenges, results, and literature reviewed.

---

## 🛠 Technologies Used

- **Language:** Python 3.x  
- **Libraries:** 
  - `numpy`
  - `random`
  - `matplotlib` (for optional visualization)
  - `tkinter` (for optional GUI)
- **Development Environment:** Jupyter Notebook / VS Code / PyCharm

---

## ✨ Features

- ✔️ Custom input of jobs, durations, and resource constraints
- ✔️ Two algorithm implementations: Backtracking and Genetic
- ✔️ Performance evaluation with real datasets
- ✔️ Experimental results and visualizations
- ✔️ Constraint-handling for:
  - Resource capacity
  - Temporal dependencies
- ✔️ Optional GUI with Gantt Chart visualization

---

## 🧮 Algorithms Used

### 1. 🔁 Backtracking Search
- Recursively builds job sequences
- Backtracks when constraint violations occur
- Guarantees optimal solutions (if feasible)
- Suitable for small to medium instances

### 2. 🧬 Genetic Algorithm
- Evolves solutions through crossover & mutation
- Uses fitness function based on makespan and resource utilization
- Fast and effective for large problem sizes
- Results are near-optimal

---

## 📂 Datasets

- Publicly available datasets from scheduling benchmarks (e.g., [OR-Library](http://people.brunel.ac.uk/~mastjjb/jeb/orlib/jobshopinfo.html))
- Small and medium-sized synthetic test cases

---

## 🚀 Installation & Usage

### Prerequisites
Ensure you have Python 3 installed. Then install required libraries:

```bash
pip install numpy matplotlib
