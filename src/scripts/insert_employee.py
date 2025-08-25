from models.employee import Employee

employees = [
    Employee( emp_name="Poojitha", email="pooji@example.com", phone="1234567890", department_id=1,hire_date="2023-01-15", salary=3000.00),
    Employee(emp_name="Sudhan", email="sudhan@example.com", phone="9876543210", department_id=2, hire_date="2022-05-10", salary=72000.00),
    Employee( emp_name="Susha", email="susha@example.com", phone="4567891230", department_id=3, hire_date="2024-03-25", salary=60000.00),
]

for emp in employees:
    emp.save(force_insert=True)
