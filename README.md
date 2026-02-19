 Pest Risk Prediction & IPM Recommendation System
EYIC Innovation Challenge Project

 Overview
This project was developed for the EYIC Innovation Challenge to address a real agricultural problem: delayed pest detection and inefficient pest management decisions.
The system predicts pest risk using machine learning and provides rule-based Integrated Pest Management (IPM) recommendations, focusing not only on accuracy but also on interpretability and practical decision support.

Problem Statement
Farmers often rely on manual inspection or delayed signals to detect pest outbreaks. This leads to:
Late intervention
Excessive pesticide usage
Increased crop damage
Higher costs
The goal of this project was to build a data-driven early risk prediction system that supports better pest management decisions.

 Solution Approach
The system combines:
Machine Learning Classification Model
Predicts pest risk level based on agricultural and environmental inputs.
Explainability Layer
Uses feature importance / SHAP-based analysis to interpret predictions.
Helps understand which features influence pest risk.
Rule-Based IPM Recommendation Engine
Maps predicted risk levels to Integrated Pest Management actions.
Includes chemical and non-chemical control suggestions.
Encourages responsible pesticide usage.
Cost-Aware Decision Logic
Suggests practical recommendations considering feasibility and real-world constraints.

System Architecture
Input Data → Preprocessing → Feature Engineering →
ML Model → Risk Prediction →
Explainability Layer →
Rule-Based IPM Mapping →
Final Recommendation Output

 Dataset
ICAR cotton pest dataset
Agricultural and environmental features
Historical pest occurrence data
Data preprocessing steps:
Missing value handling
Feature encoding
Normalization
Train-test split
Cross-validation

 Technologies Used
Python
Pandas
NumPy
Scikit-learn
SHAP (for explainability)
Matplotlib / Seaborn (for visualization)
Google Colab

Model Development
Tested multiple classification models
Evaluated using:
Accuracy
Precision
Recall
F1-score
Cross-validation
Focus was placed on robust evaluation, especially in case of class imbalance.

Key Features
✔ Risk-level prediction instead of only binary detection
✔ Explainable model outputs
✔ Integrated Pest Management recommendations
✔ Real-world deployment thinking
✔ Competition-level development (EYIC)

Impact
This project goes beyond model accuracy by:
Supporting early intervention
Encouraging sustainable pest management
Providing interpretable ML outputs
Bridging ML research and real-world agricultural deployment

Future Improvements
Integration with live weather APIs
SMS-based farmer alerts
Multi-language recommendation output
Mobile-based interface
MoA rotation optimization
