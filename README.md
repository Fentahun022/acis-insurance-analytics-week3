AlphaCare Insurance Solutions (ACIS): Risk & Marketing Analytics
This repository contains the full data analysis project for AlphaCare Insurance Solutions (ACIS). The primary objective is to analyze historical car insurance data from South Africa to optimize marketing strategies, refine pricing models by identifying key risk drivers, and discover low-risk customer segments.
# Repository Structure
The project is organized into a modular structure to separate concerns and improve maintainability:

acis-analytics/
├── .github/workflows/      # CI/CD workflows for GitHub Actions
├── data/                   # Data files (raw and processed), tracked by DVC
│   ├── raw/                # Original, immutable data
│   └── processed/          # Cleaned, analysis-ready data
├── notebooks/              # Jupyter notebooks for experimentation and analysis
│   ├── 01_EDA.ipynb
│   ├── 02_Hypothesis_Testing.ipynb
│   └── 03_Modeling.ipynb
├── src/                    
│   ├── prepare_data.py     # Script to process raw data into clean data
│   └── modeling_pipeline.py# Helper for scikit-learn preprocessing pipeline
├── .dvc/                   # DVC metadata directory
├── reports/                # Final reports and presentations
├── .gitignore              # Files and directories to be ignored by Git
├── requirements.txt        # Project dependencies
└── README.md    

# Setup & Usage
To set up and run this project locally, follow these steps.
1. Clone the Repository:
git clone https://github.com/Fentahun022/acis-insurance-analytics-week3.git
cd acis-insurance-analytics-week3

# 2. Set Up a Virtual Environment:
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# install dependencies

pip install --upgrade pip
pip install -r requirements.txt

# run the data pipeline 
python src/prepare_data.py