import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json

# Page configuration
st.set_page_config(
    page_title="Student Performance Dashboard",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
    }
    h1 {
        color: #1f77b4;
        padding-bottom: 20px;
    }
    h2 {
        color: #2c3e50;
        padding-top: 20px;
    }
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)


class StudentDashboard:
    """Student Performance Dashboard using Streamlit"""
    
    def __init__(self, csv_file='students_data.csv'):
        self.csv_file = csv_file
        self.subjects = ['Mathematics', 'Physics', 'Chemistry', 'Biology', 'English', 'History']
        self.load_data()
    
    def load_data(self):
        """Load student data from CSV"""
        self.df = pd.read_csv(self.csv_file)
        self.classes = sorted(self.df['Class'].unique())
    
    def get_student_stats(self, student_id):
        """Get comprehensive statistics for a student"""
        student = self.df[self.df['StudentID'] == student_id].iloc[0]
        class_students = self.df[self.df['Class'] == student['Class']]
        
        scores = [student[subject] for subject in self.subjects]
        
        # Calculate rank in class
        class_students_sorted = class_students.sort_values('OverallPercentage', ascending=False)
        rank = class_students_sorted[class_students_sorted['StudentID'] == student_id].index[0] - class_students_sorted.index[0] + 1
        
        return {
            'student': student,
            'scores': scores,
            'class_average': class_students['OverallPercentage'].mean(),
            'rank': rank,
            'total_in_class': len(class_students)
        }
    
    def get_class_stats(self, class_name):
        """Get comprehensive statistics for a class"""
        class_df = self.df[self.df['Class'] == class_name]
        
        stats = {
            'total_students': len(class_df),
            'mean_score': class_df['OverallPercentage'].mean(),
            'median_score': class_df['OverallPercentage'].median(),
            'std_dev': class_df['OverallPercentage'].std(),
            'min_score': class_df['OverallPercentage'].min(),
            'max_score': class_df['OverallPercentage'].max(),
            'avg_attendance': class_df['Attendance'].mean(),
            'pass_rate': (class_df['OverallPercentage'] >= 50).sum() / len(class_df) * 100
        }
        
        return stats, class_df


def main():
    """Main dashboard function"""
    
    # Initialize dashboard
    dashboard = StudentDashboard()
    
    # Title and header
    st.title("📚 Student Performance Analytics Dashboard")
    st.markdown("---")
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Select View",
        ["Overview", "Student Analysis", "Class Analysis", "Subject Analysis", "Comparative Analysis"]
    )
    
    # ==================== OVERVIEW PAGE ====================
    if page == "Overview":
        st.header("📊 Overview Dashboard")
        
        # Key metrics
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("Total Students", len(dashboard.df))
        
        with col2:
            st.metric("Total Classes", len(dashboard.classes))
        
        with col3:
            avg_performance = dashboard.df['OverallPercentage'].mean()
            st.metric("Avg Performance", f"{avg_performance:.2f}%")
        
        with col4:
            avg_attendance = dashboard.df['Attendance'].mean()
            st.metric("Avg Attendance", f"{avg_attendance:.2f}%")
        
        with col5:
            pass_rate = (dashboard.df['OverallPercentage'] >= 50).sum() / len(dashboard.df) * 100
            st.metric("Pass Rate", f"{pass_rate:.1f}%")
        
        st.markdown("---")
        
        # Charts row 1
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Grade Distribution")
            grade_counts = dashboard.df['Grade'].value_counts().sort_index()
            fig = px.bar(
                x=grade_counts.index,
                y=grade_counts.values,
                labels={'x': 'Grade', 'y': 'Number of Students'},
                color=grade_counts.values,
                color_continuous_scale='Blues'
            )
            fig.update_layout(showlegend=False, height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Performance Distribution")
            fig = px.histogram(
                dashboard.df,
                x='OverallPercentage',
                nbins=20,
                labels={'OverallPercentage': 'Overall Percentage'},
                color_discrete_sequence=['#1f77b4']
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        # Charts row 2
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Class-wise Performance")
            class_performance = dashboard.df.groupby('Class')['OverallPercentage'].mean().sort_values(ascending=False)
            fig = px.bar(
                x=class_performance.index,
                y=class_performance.values,
                labels={'x': 'Class', 'y': 'Average Performance (%)'},
                color=class_performance.values,
                color_continuous_scale='Viridis'
            )
            fig.update_layout(showlegend=False, height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Gender Distribution")
            gender_counts = dashboard.df['Gender'].value_counts()
            fig = px.pie(
                values=gender_counts.values,
                names=gender_counts.index,
                hole=0.4,
                color_discrete_sequence=['#1f77b4', '#ff7f0e']
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        # Subject-wise performance
        st.subheader("Subject-wise Average Performance")
        subject_avg = dashboard.df[dashboard.subjects].mean().sort_values(ascending=False)
        fig = px.bar(
            x=subject_avg.index,
            y=subject_avg.values,
            labels={'x': 'Subject', 'y': 'Average Score'},
            color=subject_avg.values,
            color_continuous_scale='RdYlGn'
        )
        fig.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # ==================== STUDENT ANALYSIS PAGE ====================
    elif page == "Student Analysis":
        st.header("👤 Individual Student Analysis")
        
        # Student selection
        col1, col2 = st.columns([1, 2])
        
        with col1:
            selected_student_id = st.selectbox(
                "Select Student ID",
                options=dashboard.df['StudentID'].tolist()
            )
        
        if selected_student_id:
            stats = dashboard.get_student_stats(selected_student_id)
            student = stats['student']
            
            # Student info card
            st.markdown("### Student Information")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.info(f"**Name:** {student['Name']}")
            with col2:
                st.info(f"**Class:** {student['Class']}")
            with col3:
                st.info(f"**Age:** {student['Age']}")
            with col4:
                st.info(f"**Gender:** {student['Gender']}")
            
            st.markdown("---")
            
            # Performance metrics
            st.markdown("### Academic Performance")
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                st.metric("Overall %", f"{student['OverallPercentage']:.2f}%")
            with col2:
                st.metric("Grade", student['Grade'])
            with col3:
                st.metric("Class Rank", f"{stats['rank']}/{stats['total_in_class']}")
            with col4:
                diff = student['OverallPercentage'] - stats['class_average']
                st.metric("vs Class Avg", f"{diff:+.2f}%", delta=f"{diff:.2f}%")
            with col5:
                st.metric("Attendance", f"{student['Attendance']:.1f}%")
            
            st.markdown("---")
            
            # Charts
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Subject-wise Performance")
                subject_scores = pd.DataFrame({
                    'Subject': dashboard.subjects,
                    'Score': [student[subject] for subject in dashboard.subjects]
                }).sort_values('Score', ascending=False)
                
                fig = px.bar(
                    subject_scores,
                    x='Subject',
                    y='Score',
                    color='Score',
                    color_continuous_scale='RdYlGn',
                    labels={'Score': 'Score (%)'}
                )
                fig.add_hline(y=student['OverallPercentage'], line_dash="dash", 
                             line_color="red", annotation_text="Overall Average")
                fig.update_layout(height=400, showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.subheader("Performance Radar Chart")
                fig = go.Figure()
                
                fig.add_trace(go.Scatterpolar(
                    r=[student[subject] for subject in dashboard.subjects],
                    theta=dashboard.subjects,
                    fill='toself',
                    name='Student',
                    line_color='#1f77b4'
                ))
                
                # Add class average
                class_df = dashboard.df[dashboard.df['Class'] == student['Class']]
                class_avg_scores = [class_df[subject].mean() for subject in dashboard.subjects]
                
                fig.add_trace(go.Scatterpolar(
                    r=class_avg_scores,
                    theta=dashboard.subjects,
                    fill='toself',
                    name='Class Average',
                    line_color='orange',
                    opacity=0.5
                ))
                
                fig.update_layout(
                    polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                    showlegend=True,
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Additional stats
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Statistical Summary")
                stats_df = pd.DataFrame({
                    'Metric': ['Mean', 'Median', 'Std Dev', 'Min Score', 'Max Score', 'Range'],
                    'Value': [
                        f"{np.mean(stats['scores']):.2f}",
                        f"{np.median(stats['scores']):.2f}",
                        f"{np.std(stats['scores']):.2f}",
                        f"{min(stats['scores']):.2f}",
                        f"{max(stats['scores']):.2f}",
                        f"{max(stats['scores']) - min(stats['scores']):.2f}"
                    ]
                })
                st.dataframe(stats_df, hide_index=True, use_container_width=True)
            
            with col2:
                st.subheader("Strengths & Weaknesses")
                subject_scores_sorted = sorted(
                    [(subject, student[subject]) for subject in dashboard.subjects],
                    key=lambda x: x[1],
                    reverse=True
                )
                
                st.success(f"**Top Subject:** {subject_scores_sorted[0][0]} ({subject_scores_sorted[0][1]:.2f}%)")
                st.success(f"**2nd Best:** {subject_scores_sorted[1][0]} ({subject_scores_sorted[1][1]:.2f}%)")
                st.error(f"**Needs Focus:** {subject_scores_sorted[-1][0]} ({subject_scores_sorted[-1][1]:.2f}%)")
                st.error(f"**2nd Weakest:** {subject_scores_sorted[-2][0]} ({subject_scores_sorted[-2][1]:.2f}%)")
    
    # ==================== CLASS ANALYSIS PAGE ====================
    elif page == "Class Analysis":
        st.header("🎓 Class-wise Analysis")
        
        # Class selection
        selected_class = st.selectbox("Select Class", options=dashboard.classes)
        
        if selected_class:
            stats, class_df = dashboard.get_class_stats(selected_class)
            
            # Class metrics
            st.markdown("### Class Overview")
            col1, col2, col3, col4, col5, col6 = st.columns(6)
            
            with col1:
                st.metric("Total Students", stats['total_students'])
            with col2:
                st.metric("Mean Score", f"{stats['mean_score']:.2f}%")
            with col3:
                st.metric("Median Score", f"{stats['median_score']:.2f}%")
            with col4:
                st.metric("Std Dev", f"{stats['std_dev']:.2f}")
            with col5:
                st.metric("Attendance", f"{stats['avg_attendance']:.1f}%")
            with col6:
                st.metric("Pass Rate", f"{stats['pass_rate']:.1f}%")
            
            st.markdown("---")
            
            # Charts row 1
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Score Distribution")
                fig = px.histogram(
                    class_df,
                    x='OverallPercentage',
                    nbins=15,
                    labels={'OverallPercentage': 'Overall Percentage'},
                    color_discrete_sequence=['#1f77b4']
                )
                fig.add_vline(x=stats['mean_score'], line_dash="dash", 
                             line_color="red", annotation_text="Mean")
                fig.add_vline(x=stats['median_score'], line_dash="dash", 
                             line_color="green", annotation_text="Median")
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.subheader("Grade Distribution")
                grade_counts = class_df['Grade'].value_counts()
                fig = px.pie(
                    values=grade_counts.values,
                    names=grade_counts.index,
                    hole=0.4,
                    color_discrete_sequence=px.colors.sequential.Blues_r
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
            
            # Subject performance
            st.subheader("Subject-wise Class Performance")
            subject_stats = []
            for subject in dashboard.subjects:
                subject_stats.append({
                    'Subject': subject,
                    'Mean': class_df[subject].mean(),
                    'Median': class_df[subject].median(),
                    'Std Dev': class_df[subject].std(),
                    'Min': class_df[subject].min(),
                    'Max': class_df[subject].max()
                })
            
            subject_df = pd.DataFrame(subject_stats)
            
            fig = go.Figure()
            fig.add_trace(go.Bar(name='Mean', x=subject_df['Subject'], y=subject_df['Mean']))
            fig.add_trace(go.Bar(name='Median', x=subject_df['Subject'], y=subject_df['Median']))
            fig.update_layout(barmode='group', height=400)
            st.plotly_chart(fig, use_container_width=True)
            
            # Top and bottom performers
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("🏆 Top 10 Performers")
                top_students = class_df.nlargest(10, 'OverallPercentage')[
                    ['StudentID', 'Name', 'OverallPercentage', 'Grade']
                ].reset_index(drop=True)
                top_students.index += 1
                st.dataframe(top_students, use_container_width=True)
            
            with col2:
                st.subheader("⚠️ Students Needing Support")
                bottom_students = class_df.nsmallest(10, 'OverallPercentage')[
                    ['StudentID', 'Name', 'OverallPercentage', 'Grade', 'Attendance']
                ].reset_index(drop=True)
                bottom_students.index += 1
                st.dataframe(bottom_students, use_container_width=True)
            
            # Correlation analysis
            st.subheader("Attendance vs Performance Analysis")
            fig = px.scatter(
                class_df,
                x='Attendance',
                y='OverallPercentage',
                color='Grade',
                hover_data=['Name', 'StudentID'],
                labels={'Attendance': 'Attendance (%)', 'OverallPercentage': 'Overall Percentage (%)'},
                trendline="ols"
            )
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
            
            # Correlation coefficient
            correlation = class_df['Attendance'].corr(class_df['OverallPercentage'])
            st.info(f"**Correlation between Attendance and Performance:** {correlation:.3f}")
    
    # ==================== SUBJECT ANALYSIS PAGE ====================
    elif page == "Subject Analysis":
        st.header("📖 Subject-wise Analysis")
        
        # Subject selection
        selected_subject = st.selectbox("Select Subject", options=dashboard.subjects)
        
        if selected_subject:
            subject_data = dashboard.df[selected_subject]
            
            # Subject metrics
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                st.metric("Mean Score", f"{subject_data.mean():.2f}%")
            with col2:
                st.metric("Median Score", f"{subject_data.median():.2f}%")
            with col3:
                st.metric("Std Dev", f"{subject_data.std():.2f}")
            with col4:
                st.metric("Min Score", f"{subject_data.min():.2f}%")
            with col5:
                st.metric("Max Score", f"{subject_data.max():.2f}%")
            
            st.markdown("---")
            
            # Charts
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Score Distribution")
                fig = px.histogram(
                    x=subject_data,
                    nbins=20,
                    labels={'x': f'{selected_subject} Score'},
                    color_discrete_sequence=['#1f77b4']
                )
                fig.add_vline(x=subject_data.mean(), line_dash="dash", 
                             line_color="red", annotation_text="Mean")
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.subheader("Box Plot")
                fig = px.box(
                    y=subject_data,
                    labels={'y': f'{selected_subject} Score'},
                    color_discrete_sequence=['#1f77b4']
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
            
            # Class-wise comparison
            st.subheader(f"{selected_subject} Performance by Class")
            class_subject_means = dashboard.df.groupby('Class')[selected_subject].agg(['mean', 'median', 'std']).reset_index()
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                name='Mean',
                x=class_subject_means['Class'],
                y=class_subject_means['mean'],
                error_y=dict(type='data', array=class_subject_means['std'])
            ))
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
            
            # Top performers in subject
            st.subheader(f"🏆 Top 15 Performers in {selected_subject}")
            top_in_subject = dashboard.df.nlargest(15, selected_subject)[
                ['StudentID', 'Name', 'Class', selected_subject, 'OverallPercentage']
            ].reset_index(drop=True)
            top_in_subject.index += 1
            st.dataframe(top_in_subject, use_container_width=True)
    
    # ==================== COMPARATIVE ANALYSIS PAGE ====================
    elif page == "Comparative Analysis":
        st.header("📊 Comparative Analysis")
        
        # Multi-class comparison
        st.subheader("Multi-Class Performance Comparison")
        selected_classes = st.multiselect(
            "Select Classes to Compare",
            options=dashboard.classes,
            default=dashboard.classes[:3]
        )
        
        if selected_classes:
            comparison_data = dashboard.df[dashboard.df['Class'].isin(selected_classes)]
            
            # Box plot comparison
            fig = px.box(
                comparison_data,
                x='Class',
                y='OverallPercentage',
                color='Class',
                labels={'OverallPercentage': 'Overall Percentage (%)'},
                title="Performance Distribution by Class"
            )
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
            
            # Subject comparison
            st.subheader("Subject-wise Comparison Across Classes")
            
            subject_comparison = []
            for class_name in selected_classes:
                class_data = dashboard.df[dashboard.df['Class'] == class_name]
                for subject in dashboard.subjects:
                    subject_comparison.append({
                        'Class': class_name,
                        'Subject': subject,
                        'Average Score': class_data[subject].mean()
                    })
            
            comparison_df = pd.DataFrame(subject_comparison)
            
            fig = px.bar(
                comparison_df,
                x='Subject',
                y='Average Score',
                color='Class',
                barmode='group',
                labels={'Average Score': 'Average Score (%)'}
            )
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
            
            # Heatmap
            st.subheader("Performance Heatmap")
            heatmap_data = []
            for class_name in selected_classes:
                class_data = dashboard.df[dashboard.df['Class'] == class_name]
                row = [class_name] + [class_data[subject].mean() for subject in dashboard.subjects]
                heatmap_data.append(row)
            
            heatmap_df = pd.DataFrame(heatmap_data, columns=['Class'] + dashboard.subjects)
            heatmap_df = heatmap_df.set_index('Class')
            
            fig = px.imshow(
                heatmap_df,
                labels=dict(x="Subject", y="Class", color="Average Score"),
                color_continuous_scale='RdYlGn',
                aspect="auto"
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # Gender comparison
        st.subheader("Gender-based Performance Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            gender_performance = dashboard.df.groupby('Gender')['OverallPercentage'].agg(['mean', 'median', 'std'])
            st.dataframe(gender_performance, use_container_width=True)
        
        with col2:
            fig = px.box(
                dashboard.df,
                x='Gender',
                y='OverallPercentage',
                color='Gender',
                labels={'OverallPercentage': 'Overall Percentage (%)'}
            )
            fig.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        
        # Subject-wise gender comparison
        gender_subject_data = []
        for gender in dashboard.df['Gender'].unique():
            gender_data = dashboard.df[dashboard.df['Gender'] == gender]
            for subject in dashboard.subjects:
                gender_subject_data.append({
                    'Gender': gender,
                    'Subject': subject,
                    'Average Score': gender_data[subject].mean()
                })
        
        gender_subject_df = pd.DataFrame(gender_subject_data)
        
        fig = px.bar(
            gender_subject_df,
            x='Subject',
            y='Average Score',
            color='Gender',
            barmode='group',
            labels={'Average Score': 'Average Score (%)'},
            title="Subject-wise Performance by Gender"
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    main()