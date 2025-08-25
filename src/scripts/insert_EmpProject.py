from models.employee_project import Employee_project
assignments = [
    {"employee": 101, "project": 201, "assigned_date": "2025-07-10"},
    {"employee": 102, "project": 202, "assigned_date": "2025-08-05"},
    {"employee": 103, "project": 203, "assigned_date": "2025-06-20"},
    {"employee": 101, "project": 203, "assigned_date": "2025-09-01"},
]
for entry in assignments:
    try:
        emp_proj = Employee_project.create(
            employee_id=entry["employee"],
            project_id=entry["project"],
            assigned_date=entry["assigned_date"]
        )
        print(f"Assignment added: Employee {entry['employee']} -> Project {entry['project']}")
    except Exception as e:
        print(f"Error saving assignment (Employee {entry['employee']}, Project {entry['project']}): {e}")
