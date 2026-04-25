students = {
    "Juan": {"python": 85, "data_science": 78, "attendance": 90},
    "Marie": {"python": 90, "data_science": 88, "attendance": 95},
    "Ali": {"python": 85, "data_science": 92, "attendance": 85},
    "Jose": {"python": 78, "data_science": 80, "attendance": 98}
}

def evaluate_students(students):
    for name, subjects in students.items():
        average_score = (subjects["python"] + subjects["data_science"]) / 2
        attendance = subjects["attendance"]
        
        if average_score >= 85:
            print(f"{name} is an excellent student.")
        else:
            print(f"{name} needs improvement.")

def highest_python_score(students):
    highest_score = 0
    top_student = ""
    
    for name, subjects in students.items():
        if subjects["python"] > highest_score:
            highest_score = subjects["python"]
            top_student = name
            
    print(f"The student with the highest Python score is {top_student} with a score of {highest_score}.")


print(evaluate_students(students))
highest_python_score(students) 


juan = students["Juan"]
ali = students["Ali"]

if juan["attendance"] > 80 or ali["attendance"] > 80:
    if juan["python"] > ali["python"]:
        print("Juan has the higher Python score.")
    elif ali["python"] > juan["python"]:
        print("Ali has the higher Python score.")
    else:
        print("Juan and Ali have the same Python score.")
else:
    print("Neither Juan nor Ali has attendance above 80.")