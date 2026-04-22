# Traffic Accident Analytics System 🚗

A modern, interactive mini-project built with Python, Pandas, Plotly, and Streamlit to analyze and visualize traffic accident data.

## Features Included:
- **Data Generation & Cleaning:** A script to generate a synthetic traffic accidents dataset (with missing values for realistic cleaning practice).
- **Interactive Dashboard:** Built with Streamlit for a clean, responsive UI.
- **KPI Cards:** Quick insights like total accidents, most dangerous time, and most affected locations.
- **Visualizations (Plotly):**
  - Pie chart for severity distributions
  - Bar charts for accidents by weather and time of day
  - Line charts for accident trends over time
  - Heatmap showing severity vs time-of-day
- **Interactive Geospatial Map:** View accident hotspots on an OpenStreetMap base.
- **Sidebar Filters:** Filter the entire dashboard by City, Weather Condition, and Severity.

---

## 🚀 How to Run the Project Step-by-Step

### Step 1: Install Dependencies
Open your terminal in VS Code (`Ctrl` + `` ` ``) and make sure you are in the project folder (`c:\Users\Chanakyan\OneDrive\Desktop\da`). Run:
```bash
pip install -r requirements.txt
```
*(This installs Streamlit, Pandas, NumPy, and Plotly).*

### Step 2: Generate the Dataset
Since this project uses a dataset, we included a script to generate a dummy `traffic_accidents.csv`. Run:
```bash
python generate_data.py
```
You should see a message saying `✅ Generated 1000 dummy accident records...`

### Step 3: Run the Streamlit Dashboard
Now start the interactive web application by running:
```bash
streamlit run app.py
```

### Step 4: View the Dashboard
After running the command above, Streamlit will automatically open a new tab in your default web browser (usually at `http://localhost:8501`).
- **Sidebar:** Use the left panel to filter the data.
- **Tabs:** Switch between Analysis Visualizations, Hotspots Map, and Data Insights.

Enjoy your traffic analytics dashboard!