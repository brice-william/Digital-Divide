# 🌐 Rural vs Urban Access Inequality – Solo Data Analysis Project

This repository contains a data analysis project that explores the **digital divide between rural and urban areas in the U.S.**, focusing on broadband access disparities. The project aims to highlight the challenges rural communities face in accessing high-speed internet and the broader implications for education, healthcare, work, and economic opportunity.

## 🧠 Problem Statement

Rural communities in the U.S. face significant disparities in broadband access compared to urban areas. This lack of access hinders their ability to participate in:
- Remote education
- Telehealth services
- Remote work
- E-commerce

This **digital divide** contributes to ongoing social and economic inequalities.

## 🎯 Objectives

- Analyze disparities in broadband access across rural and urban settings.
- Identify trends in internet speed and coverage by state.
- Merge datasets from different sources to build a unified, feature-rich dataset.

## ❓ Data Questions

- How does broadband access differ between rural and urban communities?
- Which states have the slowest and fastest average advertised internet speeds?
- Can datasets be merged to uncover deeper correlations between connectivity and housing data?

## 📁 Repository Structure

- `/data/`
  - `raw/`: Raw datasets from FCC, ACS, and MCDC
  - `clean/`: Cleaned and preprocessed datasets
- `/notebooks/`: Python notebooks for data cleaning, wrangling, feature engineering, and visualization
- `/visualizations/`: Saved plots and charts (e.g., histogram of download speeds)
- `compressed_data.zip`: Zipped archive of all data files due to large dataset size
- `Final_Project_Presentation.pptx`: Slide deck summarizing the project process and findings

## 🧹 Data Sources

- **FCC Broadband Data**: Information about advertised internet speeds by location
- **American Community Survey (ACS)**: Housing and demographic data
- **Missouri Census Data Center (MCDC)**: Additional geographic identifiers for data merging

## 🔧 Data Wrangling & Feature Engineering

- Creation of unique IDs in each dataset to enable merging
- Merged multiple large-scale datasets for unified analysis
- Engineered features for comparing download speeds by state and community type
- Cleaned and processed over **690,000+** instances from the ACS dataset

## 📊 Visualizations

- Average Maximum Advertised Download Speed by State (Histogram and Bar Chart)
- Data summaries highlighting disparities between rural and urban areas

## ⚠️ Challenges & Limitations

- Difficulty handling full-scale FCC dataset due to size constraints
- Challenges in creating a comprehensive, unified unique ID for all data sources
- Limited capacity to explore more granular local-level insights

## ✅ What Could Be Improved

- Improve merging logic for better alignment across datasets
- Incorporate more features to deepen the analysis
- Utilize machine learning to predict areas most impacted by poor connectivity

---

**Author:** Brice Fokou  
**Tools Used:** Python (Pandas, Matplotlib, Seaborn), Cursor
**Note:** All data files are zipped in `compressed_data.zip` due to file size limitations.
