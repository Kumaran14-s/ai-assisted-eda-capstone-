# ai-assisted-eda-capstone-
AI-Assisted Exploratory Data Analysis on an Open Dataset

CSE Capstone Project

Project Overview

This project uses Python and AI-assisted workflows to explore open datasets, identify data-quality issues, visualize patterns, and generate evidence-based insights.

Objectives

- Analyze open datasets using Python.
- Detect missing values and duplicate records.
- Perform data cleaning and validation.
- Create interactive data visualizations.
- Generate a data-quality checklist and insights report.
- Verify AI-generated explanations using actual calculations.

Technologies Used

- Python
- Pandas and NumPy
- Matplotlib and Seaborn
- Plotly
- Streamlit
- Jupyter Notebook
- Git and GitHub

Key Features

1. CSV dataset upload
2. Data preview and summary statistics
3. Missing-value and duplicate detection
4. Data-type and outlier analysis
5. Interactive visualizations
6. Before-and-after data cleaning
7. Download cleaned CSV files
8. Automated tests and documentation

Project Structure

- "app.py" — Interactive dashboard
- "src/" — Data analysis functions
- "data/" — Sample dataset
- "notebooks/" — Jupyter notebook
- "tests/" — Automated tests
- "reports/" — Analysis and verification reports
- "docs/" — Dataset notes and project documentation
- "presentation/" — Project presentation
- "requirements.txt" — Python dependencies

How to Run

Install dependencies:

pip install -r requirements.txt

Start the application:

streamlit run app.py

Run tests:

python -m unittest discover -s tests -v

Responsible AI and Ethics

Use public, non-personal datasets. Verify all numerical results using Python. Document dataset sources and licences. Outliers require investigation, and correlation does not prove causation.

Conclusion

This project demonstrates a reproducible workflow for data exploration, data-quality assessment, visualization, and responsible AI-assisted analysis.

Project Type: CSE Capstone Project
Status: Development and testing
