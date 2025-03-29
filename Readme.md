
# CityX Crime Watch: Operation Safe Streets

**Rihal ML Codestacker Challenge 2025 Submission**

**Submitted by:**
- **Mohd Saif Ali**
- **Email:** growthwithsaif@gmail.com
- **Contact:** +968 77123132

---

## Overview

CityX, once a peaceful metropolis, now faces a surge in criminal activity. This project leverages Machine Learning and data-driven methods to assist the CityX Police Department by:

- **Cleaning and Preprocessing:** Transforming raw crime data into a structured format.
- **Exploratory Data Analysis (EDA):** Uncovering trends and patterns with interactive visualizations.
- **Crime Classification:** Using NLP techniques (TF-IDF and OneHotEncoder) along with ML models (with Random Forest selected as the best) to predict crime categories.
- **Severity Assignment:** Applying rule-based logic to assign severity levels to each crime.
- **Geo-Spatial Mapping:** Visualizing crime hotspots using interactive maps.
- **PDF Report Extraction & Inference:** Extracting key fields from police crime reports in PDF format and performing real-time ML inference.
- **Web Dashboard:** Deploying an interactive Streamlit application for data exploration and inference.

---

## Project Structure

```plaintext
CityX_Crime/
├── Competition_Dataset.csv       # Original raw crime dataset
├── processed_crime_data.csv       # Cleaned and feature-engineered dataset with severity assignment
├── eda_and_modeling.ipynb        # Python script for EDA, model training, and artifact persistence
├── level3_app.py                  # Streamlit app implementing Levels 1-3 (data exploration, visualization, and geo-spatial mapping)
├── app.py                         # Unified Streamlit app containing the complete solution (Levels 3 & 4)
├── best_model.pkl                 # Pickled best-performing ML model (e.g., Random Forest)
├── tfidf_vectorizer.pkl           # Pickled, fitted TF-IDF vectorizer
├── onehot_encoder.pkl             # Pickled, fitted OneHotEncoder for categorical features
├── requirements.txt               # Python dependencies
├── Dockerfile                     # Docker configuration file for containerization
└── README.md                      # This file
```

---

## Installation

### Local Setup

1. **Clone the Repository**

   ```bash
   git clone https://github.com/mohammedsaifali/rihal-citx-crime-ml-2025.git
   cd rihal-citx-crime-ml-2025
   ```

2. **Create a Virtual Environment**

   - **On Linux/Mac:**
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
   - **On Windows:**
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```

3. **Install Dependencies**

   Upgrade pip and install the required packages from `requirements.txt`:

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

   This command installs all necessary libraries such as pandas, numpy, scikit-learn, streamlit, pdfplumber, and others specified in the file.

---

## How to Run

### Running Locally (Without Docker)

- **Level 3 Application:**

  The file `level3_app.py` implements data exploration, EDA, and geo-spatial mapping (Levels 1-3).

  To run:
  ```bash
  streamlit run level3_app.py
  ```
  Open [http://localhost:8501](http://localhost:8501) in your browser to explore the dashboard.

- **Unified Application (Levels 3 & 4):**

  The file `app.py` contains the complete solution, including:
  - All functionalities of Level 3 (data exploration and geo-spatial visualization).
  - PDF report extraction and real-time ML inference (crime classification and severity assignment) for Level 4.

  To run:
  ```bash
  streamlit run app.py
  ```
  Open [http://localhost:8501](http://localhost:8501) to use the full application.

---

### Running via Docker (Containerized Deployment)

1. **Build the Docker Image**

   Ensure Docker is installed and running. In the project directory, run:
   ```bash
   docker build --no-cache -t cityx_crime_app:latest .
   ```

2. **Run the Docker Container**

   ```bash
   docker run -p 8501:8501 cityx_crime_app:latest
   ```

3. **Access the Application**

   Open [http://localhost:8501](http://localhost:8501) in your browser to interact with the dashboard.

---

## Application Features

### Level 1 & 2: Data Preprocessing, EDA, and Modeling
- **Data Cleaning & Preprocessing:**  
  Conversion of dates, handling missing values, and feature engineering (temporal, geographical, and categorical).
- **Exploratory Data Analysis (EDA):**  
  Bar charts, time-series plots, and interactive geo-spatial maps highlighting crime frequencies and hotspots.
- **Crime Classification & Severity Assignment:**  
  An NLP pipeline using TF-IDF for text features and OneHotEncoder for additional features.
  Multiple models were evaluated with Random Forest selected as the best performer.
  A rule-based approach assigns severity levels to predicted crime categories.

### Level 3: Interactive Web Dashboard (level3_app.py)
- **Data Overview & Filtering:**  
  Interactive sidebar filters for severity and year.
- **Geo-Spatial Visualization:**  
  Dynamic maps displaying crime density and hotspots.
- **Charting:**  
  Bar charts showing crime category and severity distributions.

### Level 4: PDF Report Extraction & Real-Time Inference (app.py)
- **PDF Parsing:**  
  Uses `pdfplumber` and regular expressions to extract key fields (e.g., Report Number, Date & Time, Incident Location, Detailed Description, Police District, Resolution) from police crime reports.
- **Real-Time Inference:**  
  Applies the same feature engineering steps (for both text and numeric/categorical data) as used during training.
  The trained model predicts the crime category, and a rule-based function assigns severity.
- **Unified Dashboard:**  
  Combines Level 3 and Level 4 functionalities in one Streamlit app for a complete end-to-end solution.

---

## Model Training and Artifacts

- **Artifact Persistence:**  
  The ML pipeline involves:
  - **TF-IDF Vectorization:** Fitting a TF-IDF vectorizer on crime descriptions.
  - **OneHotEncoder:** Transforming numerical and categorical features.
  - **Model Training:** Evaluating multiple classifiers (Random Forest, Logistic Regression, Multinomial Naive Bayes) with Random Forest selected as the best model.
- **Saved Artifacts:**  
  - `best_model.pkl` – the trained ML model.
  - `tfidf_vectorizer.pkl` – the fitted TF-IDF vectorizer.
  - `onehot_encoder.pkl` – the fitted OneHotEncoder.
- **Processed Data:**  
  - `processed_crime_data.csv` contains the cleaned, feature-engineered dataset with assigned severity levels.

---

## Docker Deployment

The project is containerized using Docker. The Dockerfile provided in this repository:
- Uses a full Python 3.9 image for a complete environment.
- Installs system build tools.
- Installs all required Python packages.
- Copies project files and sets up the Streamlit app to run on port 8501.

This makes the application portable and easy to deploy to cloud platforms such as Heroku, DigitalOcean, AWS, Azure, or Google Cloud.

---

## Additional Notes

- **Version Consistency:**  
  Ensure that the library versions (especially scikit-learn and pyparsing) used during training match those used in production to avoid issues with pickled models.
- **Error Handling:**  
  The application includes basic error handling for PDF parsing and missing fields.
- **Future Enhancements:**  
  Consider hyperparameter tuning, additional model validation, enhanced UI/UX, and scaling the deployment.

---

## Contact

For further questions or additional information, please contact:  
**Mohd Saif Ali**  
- Email: [growthwithsaif@gmail.com](mailto:growthwithsaif@gmail.com)  
- Phone: +968 77123132

