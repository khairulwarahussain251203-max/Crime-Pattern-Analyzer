import pandas as pd
import tkinter as tk
from pathlib import Path
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder
import seaborn as sns

def load_dataset():
    expected_columns = {'City', 'Date of Occurrence', 'Crime Description'}
    candidates = [
        Path(__file__).with_name("crime_dataset_india.csv"),
        Path.home() / "Downloads" / "crime_dataset_india.csv",
    ]

    dataset_path = next((path for path in candidates if path.exists()), None)
    if dataset_path is None:
        selected = filedialog.askopenfilename(
            title="Select crime dataset CSV",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
        )
        if not selected:
            raise FileNotFoundError("No dataset selected.")
        dataset_path = Path(selected)

    dataset = pd.read_csv(dataset_path)
    missing = expected_columns - set(dataset.columns)
    if missing:
        missing_cols = ", ".join(sorted(missing))
        raise ValueError(f"Dataset is missing required columns: {missing_cols}")

    return dataset[['City', 'Date of Occurrence', 'Crime Description']].dropna()


# Load dataset
df = load_dataset()
df['Date of Occurrence'] = pd.to_datetime(df['Date of Occurrence'], errors='coerce')
df = df.dropna(subset=['Date of Occurrence'])
df['Year'] = df['Date of Occurrence'].dt.year
df['Month'] = df['Date of Occurrence'].dt.month

le = LabelEncoder()
df['City_Code'] = le.fit_transform(df['City'])
X = df[['City_Code', 'Year']]

kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
df['Cluster'] = kmeans.fit_predict(X)

reg = LinearRegression()
reg.fit(X[['Year']], X['City_Code'])
future_year = 2025
predicted_city_code = float(reg.predict([[future_year]])[0])
predicted_code_index = int(round(predicted_city_code))
predicted_code_index = max(0, min(predicted_code_index, len(le.classes_) - 1))
predicted_city = le.inverse_transform([predicted_code_index])[0]

# GUI functions
def show_filtered_crimes():
    crime_type = crime_var.get()
    if crime_type:
        filtered_df = df[df['Crime Description'] == crime_type]
        if not filtered_df.empty:
            count_by_city = filtered_df['City'].value_counts().head(10)
            count_by_city.plot(kind='bar', color='teal')
            plt.title(f"Top 10 Cities for '{crime_type}' Crimes")
            plt.xlabel("City")
            plt.ylabel("Crime Count")
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()
        else:
            messagebox.showinfo("No Data", "No data available for selected crime type.")

def show_monthly_trend():
    monthly = df['Month'].value_counts().sort_index()
    monthly.plot(kind='bar', color='teal')
    plt.title("Monthly Crime Distribution")
    plt.xlabel("Month")
    plt.ylabel("Crime Count")
    plt.xticks(rotation=0)
    plt.show()            

def show_heatmap():
    pivot = df.pivot_table(index='City', columns='Year', aggfunc='size', fill_value=0)
    plt.figure(figsize=(12, 6))
    sns.heatmap(pivot, cmap='Reds', annot=True, fmt='d')
    plt.title("Crime Frequency Heatmap by City and Year")
    plt.show()

def show_clusters():
    plt.figure(figsize=(10, 6))
    plt.scatter(df['Year'], df['City_Code'], c=df['Cluster'], cmap='Set1', label='Data Points')

    # Regression line
    years = sorted(df['Year'].unique())
    predicted_codes = reg.predict([[y] for y in years])
    plt.plot(years, predicted_codes, color='black', linestyle='--', linewidth=2, label='Regression Line')

    plt.title("K-Means Clustering with Regression")
    plt.xlabel("Year")
    plt.ylabel("City (Encoded)")
    plt.legend()
    plt.show()


def predict_future():
    messagebox.showinfo("Future Hotspot Prediction", f"Predicted hotspot city for {future_year}: {predicted_city}")

def show_city_trend():
    city = city_var.get()
    if city:
        city_df = df[df['City'] == city]
        if not city_df.empty:
            trend = city_df.groupby('Year').size()
            trend.plot(kind='line', marker='o', title=f"Crime Trend in {city}")
            plt.xlabel("Year")
            plt.ylabel("Number of Crimes")
            plt.show()
        else:
            messagebox.showinfo("No Data", "No data for selected city.")

def show_top_cities():
    top = df['City'].value_counts().head(10)
    top.plot(kind='bar', color='teal')
    plt.title("Top 10 Cities by Crime Count")
    plt.xlabel("City")
    plt.ylabel("Crime Count")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def filter_by_year_range():
    y1, y2 = sorted((year_from.get(), year_to.get()))
    filtered = df[(df['Year'] >= y1) & (df['Year'] <= y2)]
    if not filtered.empty:
        pivot = filtered.pivot_table(index='City', columns='Year', aggfunc='size', fill_value=0)
        plt.figure(figsize=(12,6))
        sns.heatmap(pivot, cmap='coolwarm', annot=True, fmt='d')
        plt.title(f"Crimes from {y1} to {y2}")
        plt.show()
    else:
        messagebox.showinfo("No Data", "No data for selected year range.")

def update_label_from(val):
    from_label.config(text=f"From: {int(float(val))}")

def update_label_to(val):
    to_label.config(text=f"To: {int(float(val))}")

def predict_crime_count():
    future = future_year_entry.get()
    try:
        year = int(future)
        pred_count = max(0, int(round(year_model.predict([[year]])[0])))
        messagebox.showinfo("Crime Prediction", f"Predicted crime count for {year}: {pred_count}")
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid year.")

year_crime_df = df.groupby('Year').size().reset_index(name='Crime_Count')
year_model = LinearRegression()
year_model.fit(year_crime_df[['Year']], year_crime_df['Crime_Count'])    

#GUI Setup
root = tk.Tk()
root.title("Crime Pattern Analyzer")
root.configure(bg="#B0C4DE")

# Variables
city_var = tk.StringVar()
year_from = tk.IntVar(value=df['Year'].min())
year_to = tk.IntVar(value=df['Year'].max())

style = ttk.Style()
style.configure("TButton",padding=6,relief="flat",background="#B0C4DE",foreground="black",font=("Helvetica", 9, "bold"))
style.map("TButton",background=[("active", "#B0C4DE")],  # Hover effect
          foreground=[("active", "black")])
style.configure("TLabel", background="#B0C4DE")

style.configure("TLabelframe", background="#B0C4DE", borderwidth=2, relief="ridge")
style.configure("TLabelframe.Label", background="#B0C4DE", font=("Helvetica", 11, "bold"))

# Title
ttk.Label(root, text="Crime Pattern Analyzer with Predictive Mapping", font=("Helvetica", 20, "bold"), background="#B0C4DE" ).pack(pady=15)

# City Selection Frame
city_frame_title = ttk.Label(root, text="City Trend Analysis", font=("Helvetica", 11, "bold"))
city_frame = ttk.LabelFrame(root, labelwidget=city_frame_title, padding=10)
city_frame.pack(padx=10, pady=10, fill="x")

ttk.Label(city_frame, text="Select City:", font=("Helvetica", 10)).grid(row=0, column=0, padx=10, pady=10, sticky='e')
city_list = sorted(df['City'].unique())
city_dropdown = ttk.Combobox(city_frame, textvariable=city_var, values=city_list, width=30)
city_dropdown.grid(row=0, column=1, padx=5, pady=5)
ttk.Button(city_frame, text="Show City Trend", command=show_city_trend).grid(row=0, column=2, padx=10)

# Crime Type Filter Frame
crime_frame_title = ttk.Label(root, text="Crime Type Filtering", font=("Helvetica", 11, "bold"))
crime_frame = ttk.LabelFrame(root, labelwidget=crime_frame_title, padding=10)
crime_frame.pack(padx=10, pady=10, fill="x")
crime_var = tk.StringVar()
crime_list = sorted(df['Crime Description'].unique())
ttk.Label(crime_frame, text="Select Crime Type:", font=("Helvetica", 10)).grid(row=0, column=0, padx=10, pady=10)
crime_dropdown = ttk.Combobox(crime_frame, textvariable=crime_var, values=crime_list, width=40)
crime_dropdown.grid(row=0, column=1, padx=10)
ttk.Button(crime_frame, text="Show Filtered Crimes", command=show_filtered_crimes).grid(row=0, column=2, padx=10)

# Visualizations & Insights Frame
buttons_frame_title = ttk.Label(root, text="Visualizations & Insights", font=("Helvetica", 11, "bold"))
buttons_frame = ttk.LabelFrame(root, labelwidget=buttons_frame_title, padding=10)
buttons_frame.pack(padx=10, pady=10, fill="x")

ttk.Button(buttons_frame, text="Show Heatmap", command=show_heatmap).grid(row=0, column=0, padx=10, pady=5)
ttk.Button(buttons_frame, text="Show Clusters", command=show_clusters).grid(row=0, column=1, padx=10, pady=5)
ttk.Button(buttons_frame, text="Top 10 Crime Cities", command=show_top_cities).grid(row=0, column=2, padx=10, pady=5)
ttk.Button(buttons_frame, text="Predict Future Hotspot", command=predict_future).grid(row=0, column=3, padx=10, pady=5)
ttk.Button(buttons_frame, text="Monthly Trend", command=show_monthly_trend).grid(row=0, column=4, padx=10, pady=5)
ttk.Label(buttons_frame, text="Predict Crime Count for Year:", font=("Helvetica", 10)).grid(row=1, column=0, padx=10)
future_year_entry = ttk.Entry(buttons_frame, width=10)
future_year_entry.grid(row=1, column=1)
ttk.Button(buttons_frame, text="Predict Count", command=predict_crime_count).grid(row=1, column=2, padx=10)

# Year Range Filter Frame
filter_frame_title = ttk.Label(root, text="Filter by Year Range", font=("Helvetica", 11, "bold"))
filter_frame = ttk.LabelFrame(root, labelwidget=filter_frame_title, padding=10)
filter_frame.pack(padx=10, pady=10, fill="x")


from_label = ttk.Label(filter_frame, text=f"From: {year_from.get()}", font=("Helvetica", 10))
from_label.grid(row=0, column=0, padx=5)
year_from_scale = ttk.Scale(filter_frame, from_=df['Year'].min(), to=df['Year'].max(), variable=year_from, orient='horizontal', command=update_label_from)
year_from_scale.grid(row=0, column=1, padx=10, sticky='ew')

to_label = ttk.Label(filter_frame, text=f"To: {year_to.get()}", font=("Helvetica", 10))
to_label.grid(row=1, column=0, padx=5)
year_to_scale = ttk.Scale(filter_frame, from_=df['Year'].min(), to=df['Year'].max(), variable=year_to, orient='horizontal', command=update_label_to)
year_to_scale.grid(row=1, column=1, padx=10, sticky='ew')

filter_frame.columnconfigure(1, weight=1)

ttk.Button(filter_frame, text="Apply Year Filter", command=filter_by_year_range).grid(row=2, column=0, columnspan=2, pady=10)

root.mainloop()
