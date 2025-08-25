from models.project import Project
projects = [
    Project( project_name="Multi agent", description="Agent-powered chatbot", start_date="2025-07-01", end_date="2025-12-15"),
    Project(project_name="E-Commerce Website", description="Online store", start_date="2025-08-01", end_date="2026-01-01"),
    Project( project_name="Employee Portal", description="Internal portal for staff", start_date="2025-06-15", end_date="2025-11-30"),
]
for proj in projects:
    proj.save(force_insert=True)
