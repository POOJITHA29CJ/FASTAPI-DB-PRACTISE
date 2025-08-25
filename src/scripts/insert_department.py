from models.department import Department

departments = [
    Department(dep_name="Java",dep_description="Handles java related projects"),
    Department(dep_name="Data Science",dep_description="Handles data science related projects"),
    Department(dep_name="Web Development", dep_description="Builds web apps"),
    Department(dep_name="HR", dep_description="Manages hiring and employee welfare"),
    Department(dep_name="UI",dep_description="Handles UI/UX related projects"),
]
for dept in departments:
    dept.save(force_insert=True)
    
