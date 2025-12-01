
# **Cybersecurity EDA Project — CISSM Cyber Attacks Dataset**

This repository contains an Exploratory Data Analysis (EDA) project conducted for an AI Bootcamp data analysis course. The project uses the **CISSM Cyber Attacks Dataset** compiled by the University of Maryland’s Center for International and Security Studies (CISSM).
The analysis explores cyber incidents, threat actors, targeted sectors, and trends in cyber activity across time.

---

## **📌 Project Overview**

Cybersecurity incidents are rising globally, and understanding the patterns behind these attacks is crucial for both researchers and practitioners.
This project provides an analytical look into:

* Which industries are most frequently targeted
* The behavior of different actor types (criminal groups, nation states, hacktivists, etc.)
* How attack patterns change over time
* Whether specific actors target specific sectors
* Trends and turning points in cyber activity

The final notebook answers several key analytical questions using visualizations and statistical summaries.

---

## **📊 Dataset**

**Source:** CISSM Cyber Attacks Dataset
**Provider:** University of Maryland, Center for International and Security Studies

The dataset includes information such as:

* Attack date
* Target country and sector
* Actor type (criminal, nation-state, hacktivist, etc.)
* Incident description
* Impact type

The dataset enables analysis of both *who* is conducting cyber attacks and *who* is being targeted.

---

## **🧠 Guiding Questions**

The EDA addresses the following key questions:

1. **Which industry is most often targeted by cyber attacks?**
2. **Is there a relationship between actor type and attack frequency?**
3. **Which target sectors do nation-state actors focus on compared to criminal groups?**
4. **How do attack patterns vary across years?**
5. **When did specific actor types (e.g., criminal groups) become more prominent?**

Each question is answered using visual analytics (Seaborn/Matplotlib) and narrative explanations.

---

## **🔍 Methods Used**

The analysis includes:

* Data cleaning and preprocessing
* Handling missing values
* Grouping and aggregations using Pandas
* Count plots, bar charts, line plots, and time-series visualizations
* Interpretation of trends through data-driven narrative analysis

Libraries used:

* **Pandas**
* **NumPy**
* **Seaborn**
* **Matplotlib**
* **Jupyter Notebook**

---

## **📁 Repository Structure**

```
├── Data_Analysis_Project.ipynb     # Main Jupyter Notebook containing the full EDA  
├── README.md                       # Project documentation  
└── data/                           # (Optional folder if you include dataset files)
```

---

## **🚀 Key Findings (Summary)**

Based on the analyses:

* **Healthcare** emerged as the most targeted sector, largely due to its sensitive data and relatively weak cybersecurity posture.
* **Criminal groups** were responsible for the vast majority of attacks, especially after 2017.
* **Nation-state actors** tended to target government and strategic sectors rather than purely financial targets.
* **2017 was a major turning point**, coinciding with the global spread of exploits like EternalBlue and the rise of ransomware-as-a-service platforms.

These findings highlight the changing landscape of cyber threats and the increasing accessibility of offensive capabilities.

---

## **▶️ How to Run the Notebook**

1. Clone the repository:

```bash
git clone https://github.com/your-username/your-repo-name.git
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Open the notebook:

```bash
jupyter notebook Data_Analysis_Project.ipynb
```

---

## **📌 Course Context**

This project was completed as part of a university-level **Data Analysis** course, demonstrating skills in:

* Exploratory Data Analysis
* Data visualization
* Cybersecurity incident interpretation
* Analytical storytelling

---

## **📜 License**

This project is for educational purposes only. Please refer to the CISSM dataset’s license for usage restrictions.

