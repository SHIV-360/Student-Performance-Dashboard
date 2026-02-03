# 📚 Student Performance Dashboard

A comprehensive Python project for analyzing student performance with interactive Streamlit dashboard, statistical analysis, and data visualization.

## 🎯 Project Overview

This project provides a complete solution for analyzing student academic performance across multiple dimensions:
- **1000 Students** across 10 different classes
- **6 Subjects**: Mathematics, Physics, Chemistry, Biology, English, History
- **Multiple Metrics**: Attendance, Assignment Completion, Overall Performance
- **Advanced Analytics**: Statistical analysis, class comparisons, subject-wise insights

## 📁 Project Structure

```
student_dashboard/
├── students_data.csv              # Generated CSV with 1000 student records
├── generate_student_data.py       # Script to generate student data
├── dashboard.py                   # Streamlit dashboard application
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

## 🚀 Features

### 1. Data Generation
- Generates realistic student data for 1000 students
- Multiple classes (10A-12B)
- Correlated metrics (attendance affects performance)
- Randomized but realistic score distributions

### 2. Interactive Streamlit Dashboard

The dashboard includes 5 comprehensive views:

#### 📊 Overview
- Total students, classes, and key metrics
- Grade distribution charts
- Performance distribution
- Class-wise comparison
- Subject-wise average performance
- Gender distribution

#### 👤 Student Analysis
- Detailed individual student profile
- Subject-wise performance visualization
- Radar chart comparing to class average
- Statistical summary
- Strengths and weaknesses
- Class rank and percentile

#### 🎓 Class Analysis
- Class overview with key metrics
- Score distribution histogram
- Grade distribution pie chart
- Subject-wise performance comparison
- Top 10 and bottom 10 students
- Attendance vs Performance correlation analysis

#### 📖 Subject Analysis
- Subject-specific statistics
- Score distribution and box plots
- Class-wise comparison for each subject
- Top 15 performers in selected subject

#### 📊 Comparative Analysis
- Multi-class performance comparison
- Subject-wise comparison across classes
- Performance heatmap
- Gender-based performance analysis
- Subject-wise gender comparison

## 🛠️ Installation & Setup

### Step 1: Install Dependencies

```bash
pip install -r requirement.txt
```

Or install individually:
```bash
pip install streamlit pandas numpy plotly
```

### Step 2: Generate Student Data

The student data is already generated, but you can regenerate it:

```bash
python generate_data.py
```

This creates `students_data.csv` with 1000 student records.

### Step 3: Run the Dashboard

```bash
python -m streamlit run dashboard.py
```

The dashboard will open in your default browser at `http://localhost:8501`

## 📊 Statistical Parameters Calculated

### For Individual Students:
- Mean, Median, Standard Deviation
- Minimum and Maximum scores
- Range of scores
- Subject rankings
- Class percentile
- Rank in class
- Comparison to class average
- Attendance status
- Assignment completion status

### For Classes:
- Mean, Median, Variance, Standard Deviation
- Quartiles (Q1, Q2, Q3)
- Range
- Grade distribution
- Pass/fail rates
- Subject-wise statistics
- Gender distribution
- Attendance distribution
- Top and bottom performers

### For Subjects:
- Mean, Median, Standard Deviation
- Minimum and Maximum
- Class-wise performance comparison
- Overall distribution

## 🎨 Dashboard Features

### Interactive Visualizations:
- Bar charts for distributions
- Pie charts for categorical data
- Histograms for score distributions
- Box plots for statistical analysis
- Radar charts for multi-dimensional comparison
- Scatter plots for correlation analysis
- Heatmaps for multi-variable comparison
- Trend lines for relationship analysis

### User-Friendly Interface:
- Sidebar navigation
- Dropdown selections
- Interactive charts (zoom, pan, hover)
- Color-coded metrics
- Responsive layout
- Clean, professional design

## 📝 Data Fields

### Student Record Fields:
- **StudentID**: Unique identifier (STU0001-STU1000)
- **Name**: Student name
- **Class**: Class assignment (10A-12B)
- **Age**: Student age
- **Gender**: Male/Female
- **Attendance**: Attendance percentage (70-100%)
- **Subject Scores**: 6 subjects (0-100)
- **OverallPercentage**: Average of all subjects
- **Grade**: Letter grade (A+, A, B, C, D, F)
- **AssignmentCompletion**: Completion percentage (60-100%)
- **ExamParticipation**: Yes/No

## 🔍 Sample Insights

The dashboard can help answer questions like:
- Which students are performing best/worst in each class?
- What is the correlation between attendance and performance?
- How do different classes compare in each subject?
- Which subjects have the highest/lowest average scores?
- What is the grade distribution across the school?
- How do male and female students compare in performance?
- Which students need additional support?
- What are the strengths and weaknesses of individual students?

## 🎓 Educational Use Cases

1. **Teachers**: Identify struggling students and track class performance
2. **Administrators**: Monitor overall school performance and make data-driven decisions
3. **Students**: Understand their performance relative to peers
4. **Parents**: Track their child's academic progress
5. **Data Scientists**: Learn data analysis and visualization techniques

## 🛡️ Technical Details

- **Python Version**: 3.8+
- **Data Format**: CSV (later sql)
- **Visualization Library**: Plotly (interactive charts)
- **Web Framework**: Streamlit
- **Data Processing**: Pandas, NumPy

## 📌 Notes

- All data is randomly generated for demonstration purposes
- Scores are correlated with attendance for realism
- The dashboard is fully interactive and updates in real-time
- Statistical calculations follow standard educational metrics

## 📄 License

This project is open source and available for educational purposes.

---