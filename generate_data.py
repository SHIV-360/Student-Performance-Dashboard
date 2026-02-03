import csv
import random
import numpy as np

# Set random seed for reproducibility
random.seed(42)
np.random.seed(42)

# Student data configuration
num_students = 1000
classes = ['10A', '10B', '10C', '10D', '11A', '11B', '11C', '11D', '12A', '12B']
subjects = ['Mathematics', 'Physics', 'Chemistry', 'Biology', 'English', 'History']

# Generate student data
students = []

for i in range(1, num_students + 1):
    student_id = f"STU{i:04d}"
    first_names = ['Raj', 'Priya', 'Amit', 'Sneha', 'Vikram', 'Anjali', 'Rohan', 'Kavya', 
                   'Arjun', 'Divya', 'Karan', 'Pooja', 'Rahul', 'Neha', 'Aditya', 'Riya',
                   'Sanjay', 'Meera', 'Nikhil', 'Shruti', 'Varun', 'Ishita', 'Akash', 'Tanvi']
    last_names = ['Sharma', 'Patel', 'Kumar', 'Singh', 'Reddy', 'Nair', 'Gupta', 'Mehta',
                  'Joshi', 'Rao', 'Verma', 'Agarwal', 'Shah', 'Iyer', 'Desai', 'Kulkarni']
    
    name = f"{random.choice(first_names)} {random.choice(last_names)}"
    student_class = random.choice(classes)
    age = int(student_class[:2]) + random.randint(0, 1)
    gender = random.choice(['Male', 'Female'])
    
    # Generate attendance (70-100%)
    attendance = round(random.uniform(70, 100), 2)
    
    # Generate subject scores with some correlation to attendance
    base_performance = (attendance - 70) / 30  # Normalize to 0-1
    
    scores = {}
    for subject in subjects:
        # Add some randomness but correlate with attendance
        mean_score = 50 + (base_performance * 40) + random.uniform(-10, 10)
        score = max(0, min(100, np.random.normal(mean_score, 12)))
        scores[subject] = round(score, 2)
    
    # Calculate overall percentage
    overall_percentage = round(sum(scores.values()) / len(scores), 2)
    
    # Determine grade
    if overall_percentage >= 90:
        grade = 'A+'
    elif overall_percentage >= 80:
        grade = 'A'
    elif overall_percentage >= 70:
        grade = 'B'
    elif overall_percentage >= 60:
        grade = 'C'
    elif overall_percentage >= 50:
        grade = 'D'
    else:
        grade = 'F'
    
    # Generate assignment completion (60-100%)
    assignment_completion = round(random.uniform(60, 100), 2)
    
    # Generate exam participation
    exam_participation = random.choice(['Yes', 'Yes', 'Yes', 'Yes', 'No'])
    
    student = {
        'StudentID': student_id,
        'Name': name,
        'Class': student_class,
        'Age': age,
        'Gender': gender,
        'Attendance': attendance,
        'Mathematics': scores['Mathematics'],
        'Physics': scores['Physics'],
        'Chemistry': scores['Chemistry'],
        'Biology': scores['Biology'],
        'English': scores['English'],
        'History': scores['History'],
        'OverallPercentage': overall_percentage,
        'Grade': grade,
        'AssignmentCompletion': assignment_completion,
        'ExamParticipation': exam_participation
    }
    
    students.append(student)

# Write to CSV
csv_file = 'students_data.csv'
fieldnames = ['StudentID', 'Name', 'Class', 'Age', 'Gender', 'Attendance',
              'Mathematics', 'Physics', 'Chemistry', 'Biology', 'English', 'History',
              'OverallPercentage', 'Grade', 'AssignmentCompletion', 'ExamParticipation']

with open(csv_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(students)

print(f"✓ Successfully generated {num_students} student records in {csv_file}")
print(f"\nSample data:")
print(f"First student: {students[0]}")
print(f"\nClass distribution:")
class_counts = {}
for student in students:
    class_name = student['Class']
    class_counts[class_name] = class_counts.get(class_name, 0) + 1
for cls, count in sorted(class_counts.items()):
    print(f"  {cls}: {count} students")