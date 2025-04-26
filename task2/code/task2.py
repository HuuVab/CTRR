import csv
import random
from datetime import datetime, timedelta
from typing import List, Dict, Any

def generate_student_dataset(num_records=20, filename="students.csv"):
    """Generate a student dataset with random data and save to CSV"""
    # Headers for the CSV file
    headers = ["StudentID", "StudentName", "DayOfBirth", "Math", "CS", "Eng"]
    
    # Lists for generating random names
    first_names = ["John", "Emma", "Michael", "Sophia", "William", "Olivia", "James", "Ava", 
                  "Alexander", "Isabella", "Benjamin", "Mia", "Elijah", "Charlotte", "Daniel", 
                  "Amelia", "Matthew", "Harper", "David", "Evelyn"]
    
    last_names = ["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson", 
                 "Moore", "Taylor", "Anderson", "Thomas", "Jackson", "White", "Harris", "Martin", 
                 "Thompson", "Garcia", "Martinez", "Robinson"]
    
    # Generate random student data
    students = []
    for i in range(1, num_records + 1):
        # Generate a random student ID
        student_id = f"S{i:03d}"
        
        # Generate a random name
        student_name = f"{random.choice(first_names)} {random.choice(last_names)}"
        
        # Generate a random birth date (between 18-25 years ago)
        days_ago = random.randint(18*365, 25*365)
        birth_date = (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d")
        
        # Generate random scores (0-10)
        math_score = round(random.uniform(3, 10), 1)
        cs_score = round(random.uniform(2, 10), 1)
        eng_score = round(random.uniform(3, 10), 1)
        
        # Ensure we have some cases where students are struggling and some with high math
        if i % 5 == 0:  # Every 5th student has high math
            math_score = round(random.uniform(9, 10), 1)
        if i % 7 == 0:  # Every 7th student is struggling
            math_score = round(random.uniform(2, 5.9), 1)
            cs_score = round(random.uniform(2, 5.9), 1)
        if i % 3 == 0:  # Every 3rd student improved in CS
            cs_score = math_score + round(random.uniform(0.5, 2), 1)
            if cs_score > 10:
                cs_score = 10.0
        
        students.append([student_id, student_name, birth_date, math_score, cs_score, eng_score])
    
    # Write to CSV file
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        writer.writerows(students)
    
    print(f"Generated {num_records} student records in {filename}")
    return filename


def load_student_data(filename: str) -> List[Dict[str, Any]]:
    """Load student data from a CSV file into a list of dictionaries."""
    students = []
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Convert scores to float
            row['Math'] = float(row['Math'])
            row['CS'] = float(row['CS'])
            row['Eng'] = float(row['Eng'])
            students.append(row)
    return students


# Predicate functions
def is_passing(student: Dict[str, Any]) -> bool:
    """All scores are greater than or equal to 5."""
    return student['Math'] >= 5 and student['CS'] >= 5 and student['Eng'] >= 5


def is_high_math(student: Dict[str, Any]) -> bool:
    """Math score is greater than or equal to 9."""
    return student['Math'] >= 9


def is_struggling(student: Dict[str, Any]) -> bool:
    """Math and CS score is less than 6."""
    return student['Math'] < 6 and student['CS'] < 6


def improved_in_cs(student: Dict[str, Any]) -> bool:
    """CS score is greater than math score."""
    return student['CS'] > student['Math']


# Universal quantification functions
def all_students_passed(students: List[Dict[str, Any]]) -> bool:
    """All students passed all subjects."""
    return all(is_passing(student) for student in students)


def all_students_math_above_3(students: List[Dict[str, Any]]) -> bool:
    """All students have a math score higher than 3."""
    return all(student['Math'] > 3 for student in students)


# Existential quantification functions
def exists_student_high_math(students: List[Dict[str, Any]]) -> bool:
    """There exists a student who scored above 9 in math."""
    return any(is_high_math(student) for student in students)


def exists_student_improved_cs(students: List[Dict[str, Any]]) -> bool:
    """There exists a student who improved in CS over Math."""
    return any(improved_in_cs(student) for student in students)


# Combined/nested statements
def for_every_student_exists_subject_above_6(students: List[Dict[str, Any]]) -> bool:
    """For every student, there exists a subject in which they scored above 6."""
    return all(
        student['Math'] > 6 or student['CS'] > 6 or student['Eng'] > 6
        for student in students
    )


def for_struggling_math_exists_subject_above_6(students: List[Dict[str, Any]]) -> bool:
    """For every student scoring below 6 in Math, there exists a subject where they scored above 6."""
    return all(
        student['CS'] > 6 or student['Eng'] > 6
        for student in students if student['Math'] < 6
    )


# Negation functions
def not_all_students_passed(students: List[Dict[str, Any]]) -> bool:
    """Not all students passed all subjects. This is equivalent to saying:
    'There exists at least one student who did not pass all subjects.'"""
    return not all_students_passed(students)


def not_all_students_math_above_3(students: List[Dict[str, Any]]) -> bool:
    """Not all students have a math score higher than 3. This is equivalent to saying:
    'There exists at least one student whose math score is 3 or below.'"""
    return not all_students_math_above_3(students)


def not_exists_student_high_math(students: List[Dict[str, Any]]) -> bool:
    """There does not exist a student who scored above 9 in math. This is equivalent to saying:
    'All students scored 9 or below in math.'"""
    return not exists_student_high_math(students)


def not_exists_student_improved_cs(students: List[Dict[str, Any]]) -> bool:
    """There does not exist a student who improved in CS over Math. This is equivalent to saying:
    'All students' CS scores are equal to or lower than their math scores.'"""
    return not exists_student_improved_cs(students)


def not_for_every_student_exists_subject_above_6(students: List[Dict[str, Any]]) -> bool:
    """It is not the case that for every student, there exists a subject in which they scored above 6.
    This is equivalent to saying: 'There exists at least one student who scored 6 or below in all subjects.'"""
    return not for_every_student_exists_subject_above_6(students)


def not_for_struggling_math_exists_subject_above_6(students: List[Dict[str, Any]]) -> bool:
    """It is not the case that for every student scoring below 6 in Math, there exists a subject where 
    they scored above 6. This is equivalent to saying: 'There exists at least one student scoring below 6 
    in Math who scored 6 or below in all other subjects.'"""
    return not for_struggling_math_exists_subject_above_6(students)


def evaluate_all_statements(students: List[Dict[str, Any]]):
    """Evaluate all predicate logic statements on the student dataset."""
    # Define all statements with their names and functions
    statements = [
        ("Universal 1: All students passed all subjects", all_students_passed),
        ("Universal 2: All students have a math score higher than 3", all_students_math_above_3),
        ("Existential 1: There exists a student who scored above 9 in math", exists_student_high_math),
        ("Existential 2: There exists a student who improved in CS over Math", exists_student_improved_cs),
        ("Combined 1: For every student, there exists a subject in which they scored above 6", 
         for_every_student_exists_subject_above_6),
        ("Combined 2: For every student scoring below 6 in Math, there exists a subject where they scored above 6", 
         for_struggling_math_exists_subject_above_6),
        ("Negation 1: Not all students passed all subjects", not_all_students_passed),
        ("Negation 2: Not all students have a math score higher than 3", not_all_students_math_above_3),
        ("Negation 3: There does not exist a student who scored above 9 in math", not_exists_student_high_math),
        ("Negation 4: There does not exist a student who improved in CS over Math", not_exists_student_improved_cs),
        ("Negation 5: It is not the case that for every student, there exists a subject in which they scored above 6", 
         not_for_every_student_exists_subject_above_6),
        ("Negation 6: It is not the case that for every student scoring below 6 in Math, there exists a subject where they scored above 6", 
         not_for_struggling_math_exists_subject_above_6)
    ]
    
    # Evaluate and print results
    print("\nEvaluating predicate logic statements on student data:")
    print("-" * 80)
    
    for name, func in statements:
        result = func(students)
        print(f"{name}: {result}")


def main():
    # Generate student dataset
    filename = generate_student_dataset(25)  # Generate 25 records
    
    # Load student data
    students = load_student_data(filename)
    
    # Display a few student records
    print("\nSample of student records:")
    for i, student in enumerate(students[:5]):
        print(f"{student['StudentID']}: {student['StudentName']}, Math={student['Math']}, CS={student['CS']}, Eng={student['Eng']}")
    
    # Evaluate all statements
    evaluate_all_statements(students)


if __name__ == "__main__":
    main()
