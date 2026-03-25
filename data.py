import pandas as pd
import numpy as np

np.random.seed(42)

n = 500

data = {
    "EmployeeID": range(1, n+1),
    "Age": np.random.randint(22, 60, n),
    "Department": np.random.choice(["HR", "IT", "Sales", "Finance"], n),
    "Salary": np.random.randint(20000, 100000, n),
    "YearsAtCompany": np.random.randint(1, 20, n),
    "PerformanceScore": np.random.randint(1, 5, n),
    "WorkHours": np.random.randint(35, 60, n),
    "Attrition": np.random.choice([0, 1], n)  # 0 = Stay, 1 = Leave
}

df = pd.DataFrame(data)
df.to_csv("employees.csv", index=False)

print("✅ 500 Employee dataset created!")