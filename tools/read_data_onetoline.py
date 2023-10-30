import pandas as pd

path = "data_onetonline/"
jobs_metadata = pd.read_csv(path + "jobs_metadata.csv")
abilities = pd.read_csv(path + "abilities.csv")
detailed_work_activities = pd.read_csv(path + "detailed_work_activities.csv")
interests = pd.read_csv(path + "interests.csv")
knowledge = pd.read_csv(path + "knowledge.csv")
related_occupations = pd.read_csv(path + "related_occupations.csv")
skills = pd.read_csv(path + "skills.csv")
tasks = pd.read_csv(path + "tasks.csv")
technology_skills = pd.read_csv(path + "technology_skills.csv")
tools_used = pd.read_csv(path + "tools_used.csv")
work_activities = pd.read_csv(path + "work_activities.csv")
work_context = pd.read_csv(path + "work_activities.csv")
work_styles = pd.read_csv(path + "work_styles.csv")
work_values = pd.read_csv(path + "work_values.csv")
