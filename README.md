# Crime Pattern Analyzer with Predictive Mapping

A Python desktop application that analyzes crime records, visualizes trends, and provides simple predictive insights using machine learning.

This project combines:
- **Data processing** with `pandas`
- **Interactive GUI** with `tkinter`
- **Visual analytics** with `matplotlib` and `seaborn`
- **ML models** with `scikit-learn` (`KMeans`, `LinearRegression`, `LabelEncoder`)

## Project Highlights

- Analyze crime trends by **city**, **year**, and **crime type**
- Generate visualizations:
  - Top cities for selected crime type
  - Monthly crime distribution
  - City-vs-year heatmap
  - K-Means clustering scatter
  - Per-city yearly trend line
- Predict:
  - A **future hotspot city** (for year 2025 in current UI)
  - **Estimated crime count** for a user-entered year
- Filter data by year range using interactive sliders

## Folder Structure

- `main.py` - Main application script (GUI + analysis + prediction logic)
- `Project_Report.docx` - Project report/documentation
- `requirements.txt` - Python dependency list
- `README.md` - This file

## Requirements

- Python **3.9+** (recommended)
- Required Python packages:
  - `pandas`
  - `matplotlib`
  - `seaborn`
  - `scikit-learn`

Install dependencies:

```bash
pip install -r requirements.txt
```

Alternative one-line install:

```bash
pip install pandas matplotlib seaborn scikit-learn
```

## Dataset Requirements

The application expects a CSV file with at least these columns:

- `City`
- `Date of Occurrence`
- `Crime Description`

### Dataset Loading Behavior

On startup, `main.py` tries to load data in this order:
1. `crime_dataset_india.csv` in the **same folder** as `main.py`
2. `crime_dataset_india.csv` in your **Downloads** folder
3. If not found, it opens a **file picker** to let you select a CSV manually

If required columns are missing, the app shows an error and stops.

## How to Run

From the project directory:

```bash
python main.py
```

The GUI window will open with all controls and visual actions.

## Application Features (Detailed)

### 1) City Trend Analysis
- Select a city from dropdown
- Click **Show City Trend**
- Displays line chart of crimes per year for that city

### 2) Crime Type Filtering
- Select crime type
- Click **Show Filtered Crimes**
- Displays top 10 cities affected by that crime type

### 3) Heatmap
- Click **Show Heatmap**
- Displays city vs year matrix of crime counts

### 4) K-Means Clustering
- Click **Show Clusters**
- Uses features:
  - Encoded city (`City_Code`)
  - `Year`
- Clusters into 5 groups and overlays a regression line

### 5) Top Cities
- Click **Top 10 Crime Cities**
- Shows cities with highest total crime records

### 6) Monthly Trend
- Click **Monthly Trend**
- Shows month-wise crime distribution

### 7) Future Hotspot Prediction
- Click **Predict Future Hotspot**
- Uses linear regression on `Year -> City_Code` and maps prediction back to city label

### 8) Crime Count Prediction
- Enter a year in text box
- Click **Predict Count**
- Predicts total crime count for that year using linear regression on yearly totals

### 9) Year Range Filter
- Adjust **From** and **To** sliders
- Click **Apply Year Filter**
- Shows heatmap for selected year interval

## Data Preprocessing Pipeline

1. Read CSV
2. Keep required columns only
3. Drop null rows in required fields
4. Parse `Date of Occurrence` as datetime
5. Drop invalid dates
6. Extract:
   - `Year`
   - `Month`
7. Label-encode city names into numeric `City_Code`

## Machine Learning Models Used

### K-Means Clustering
- Model: `KMeans(n_clusters=5, random_state=42, n_init=10)`
- Input: `City_Code`, `Year`
- Output: cluster label per row

### Linear Regression (Hotspot)
- Model: `LinearRegression()`
- Input: `Year`
- Target: `City_Code`
- Predicted code is rounded and clamped to valid city index range before decoding

### Linear Regression (Crime Count)
- Model: `LinearRegression()`
- Input: `Year`
- Target: total yearly crime count
- Predicted values are rounded and lower-bounded at 0

## Troubleshooting

### App does not start due to dataset error
- Ensure your CSV has exact required columns:
  - `City`
  - `Date of Occurrence`
  - `Crime Description`
- Place file as `crime_dataset_india.csv` in project folder, or select it from file picker

### Plots not visible
- Ensure GUI is not blocked behind other windows
- Verify `matplotlib` is installed correctly

### Prediction results seem unrealistic
- Linear regression is used as a simple baseline and may not capture complex real-world behavior
- See limitations section below

## Known Limitations

- Predicting city label via regression on encoded IDs is a simplified academic approach
- No geospatial mapping (latitude/longitude) is currently included
- No advanced time-series model (e.g., ARIMA/Prophet/LSTM)
- Data quality strongly affects insights and predictions

## Suggested Improvements

- Add map-based visualization (e.g., Folium/GeoPandas)
- Replace hotspot logic with classification/ranking approaches
- Support user-defined cluster count (`k`)
- Add export options (CSV/PDF reports)
- Add model evaluation metrics and validation split

## License

This project currently has no explicit license file.
Add a `LICENSE` file (for example MIT) if you want open-source reuse terms.

## Authors

According to the report:
- Khair ul wara Hussain (FA23-BAI-022)
- Arhum Fareed (FA23-BAI-006)

