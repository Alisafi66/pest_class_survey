🌾 Part 3: Human-in-the-Loop Validation & Farmer Survey

Validating AI Pest Detection Against Real-World Farmer Expertise

📖 Project Context

This repository represents Phase 3 (The Final Phase) of the Pest Detection for Smart Farming project.

After developing the Grounding DINO (Phase 1) and AIMv2 (Phase 2) models, it was critical to validate their performance not just against mathematical metrics, but against human expertise. We developed a custom web-based survey tool to collect ground-truth labels from real farmers and agricultural experts.

Key Finding:
The AI model (Grounding DINO) outperformed human evaluation in specific pest identification tasks, achieving a 13% higher accuracy on average compared to the human baseline.

🛠️ The Validation Tool

To facilitate this study, I built a custom, lightweight web application designed to be easily accessible to farmers.

Features:

Simple Interface: A "Yes/No" binary classification interface (Is this a pest?).

Real Data: Served images directly from our curated dataset of >100,000 agricultural images.

Data Capture: Automatically logged user responses into a CSV backend for statistical analysis.

(The interface designed for rapid farmer feedback)

⚙️ Methodology

Target Audience: Real farmers and agricultural workers.

Task: Participants were shown a series of randomized images (crops, insects, foliage) and asked to identify if a "Pest" was present.

Data Collection:

User Decisions: Recorded as "Human Labels".

Model Decisions: Recorded as "AI Predictions" (from Phase 1 & 2 models).

Ground Truth: Validated by expert entomologists.

Analysis: We compared the Human Error Rate against the AI Error Rate.

📊 Results: AI vs. Human Expert

We analyzed the CSV logs to calculate the comparative performance.

Evaluator

Accuracy

Error Rate

Notes

Grounding DINO (AI)

High

Low

Consistent detection of small/camouflaged pests.

Human Farmers

Moderate

Moderate

Struggles with fatigue and minute details.

Performance Gap

+13%

-13%

The AI outperformed humans by 13%.

📉 Impact Analysis

This validation phase proves that the AI system is not only a viable support tool but a superior diagnostic instrument for early pest detection. It eliminates the "fatigue factor" that affects human workers and can detect micro-pests often missed by the naked eye.

🚀 Usage (Survey Tool)

The web tool source code is included in this repository for reproducibility.

1. Prerequisites

Node.js or Python (depending on your backend choice).

A local web server.

2. Launching the App

# Clone the repository
git clone [https://github.com/Alisafi66/Pest-Detection-Smart-Farming.git](https://github.com/Alisafi66/Pest-Detection-Smart-Farming.git)

# Navigate to the web tool directory
cd web-survey-tool

# Start the local server (Example using Python)
python -m http.server 8000


3. Access

Open your browser to http://localhost:8000 to view the survey interface.

📂 Repository Structure

.
├── assets/
│   └── survey_tool_screenshot.png  # Interface image
├── data/
│   └── survey_results.csv          # Anonymized results from the farmer survey
├── src/
│   ├── index.html                  # The survey frontend
│   ├── style.css                   # Styling for the simple UI
│   └── app.js                      # Logic to serve images and save CSV data
└── README.md                       # This documentation


🤝 Acknowledgements

We extend our gratitude to the farmers and agricultural experts who participated in this study. Their time and expertise provided the crucial ground-truth data needed to validate this technology.
