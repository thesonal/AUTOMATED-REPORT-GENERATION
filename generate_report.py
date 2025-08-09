import csv
import json
import os
from statistics import mean
from datetime import datetime
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

# --- Setup paths ---
folder_path = r"C:\Users\SONAL\project\DataReportApp_Task2"
data_path = r"C:\Users\SONAL\project\DataReportApp_Task2\data.csv.csv"
json_path = os.path.join(folder_path, "summary.json")
logo_path = os.path.join(folder_path, "assets", "logo.png")  # Optional logo
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
report_path = os.path.join(folder_path, f"Report_{timestamp}.pdf")
chart_path = os.path.join(folder_path, "chart.png")

# --- Read data ---
headers, rows = [], []
with open(data_path, newline='') as csvfile:
    reader = csv.reader(csvfile)
    headers = next(reader)
    for row in reader:
        rows.append([float(val) if val.replace('.', '', 1).isdigit() else 0.0 for val in row])

# --- Calculate Summary Stats ---
columns = list(zip(*rows))
summary = {
    headers[i]: {
        "Mean": round(mean(col), 2),
        "Max": max(col),
        "Min": min(col)
    } for i, col in enumerate(columns)
}

# --- Export to JSON ---
with open(json_path, "w") as jsonfile:
    json.dump(summary, jsonfile, indent=4)

# --- Generate Chart ---
means = [stat["Mean"] for stat in summary.values()]
plt.bar(headers, means, color='skyblue')
plt.title("Column-Wise Mean Values")
plt.ylabel("Value")
plt.savefig(chart_path)
plt.close()

# --- Generate PDF Report ---
c = canvas.Canvas(report_path, pagesize=A4)
width, height = A4

# Title & Metadata
c.setFont("Helvetica-Bold", 18)
c.drawString(60, height - 60, "📊 DataReportApp Pro")
c.setFont("Helvetica", 12)
c.drawString(60, height - 90, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# --- Optional Logo with Fallback ---
try:
    if os.path.exists(logo_path):
        c.drawImage(ImageReader(logo_path), width - 140, height - 100, width=60, preserveAspectRatio=True)
    else:
        print("ℹ️ No logo found, continuing without branding.")
except Exception as e:
    print(f"⚠️ Error loading logo: {e}")

# Summary
y = height - 140
for key, stats in summary.items():
    c.setFont("Helvetica-Bold", 13)
    c.drawString(60, y, f"Column: {key}")
    y -= 20
    c.setFont("Helvetica", 11)
    for stat, val in stats.items():
        c.drawString(80, y, f"{stat}: {val}")
        y -= 15
    y -= 10

# Chart
c.drawImage(chart_path, 60, y - 200, width=400, preserveAspectRatio=True)

# Finish
c.save()
print(f"✅ PDF generated: {report_path}")