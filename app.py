import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from sklearn.linear_model import LogisticRegression

import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from sklearn.linear_model import LogisticRegression

# 👇 PASTE UI CODE HERE
st.set_page_config(page_title="HR Analytics", layout="wide")

st.markdown("""
<style>

/* Main background */
.stApp {
    background-color: #0E1117;
    color: white;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #161B22;
}

/* Cards */
.card {
    background-color: #1E1E1E;
    padding: 20px;
    border-radius: 15px;
    margin: 10px 0;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.5);
    transition: 0.3s;
}
.card:hover {
    transform: scale(1.03);
}

/* Buttons */
.stButton>button {
    background-color: #4CAF50;
    color: white;
    border-radius: 10px;
}

/* Animation */
.fade-in {
    animation: fadeIn 1s ease-in;
}
@keyframes fadeIn {
    from {opacity: 0;}
    to {opacity: 1;}
}

</style>
""", unsafe_allow_html=True)
# ---------------- DATABASE ----------------
conn = sqlite3.connect("employees.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS employees (
    EmployeeID INTEGER,
    Age INTEGER,
    Department TEXT,
    Salary INTEGER,
    YearsAtCompany INTEGER,
    PerformanceScore INTEGER,
    WorkHours INTEGER,
    Attrition INTEGER
)
""")

# Load CSV into DB (only once)
try:
    df_csv = pd.read_csv("employees.csv")
    df_csv.to_sql("employees", conn, if_exists="replace", index=False)
except:
    pass

# Load data
df = pd.read_sql("SELECT * FROM employees", conn)

# ---------------- LOGIN ----------------
if "login" not in st.session_state:
    st.session_state.login = False

def login():
    st.title("🔐 HR Login")
    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):
        if user == "admin" and pwd == "1234":
            st.session_state.login = True
        else:
            st.error("Invalid login")

if not st.session_state.login:
    login()
    st.stop()

# ---------------- DARK MODE ----------------
st.set_page_config(page_title="HR Analytics", layout="wide")

st.markdown("""
<style>
body {background-color: #0E1117; color: white;}
</style>
""", unsafe_allow_html=True)

st.title("🏢 HR Analytics System")

menu = st.sidebar.selectbox("Menu", [
    "Dashboard",
    "Search",
    "Add Employee",
    "Upload CSV",
    "Prediction"
])

# ---------------- DASHBOARD ----------------
if menu == "Dashboard":
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)

    st.title("📊 Smart HR Dashboard")

    col1, col2, col3 = st.columns(3)

    col1.markdown(f'<div class="card">👥 Total Employees <h2>{len(df)}</h2></div>', unsafe_allow_html=True)
    col2.markdown(f'<div class="card">💰 Avg Salary <h2>{int(df["Salary"].mean())}</h2></div>', unsafe_allow_html=True)
    col3.markdown(f'<div class="card">⭐ Avg Performance <h2>{round(df["PerformanceScore"].mean(),2)}</h2></div>', unsafe_allow_html=True)

    import plotly.express as px

    fig = px.pie(df, names="Department", title="Department Distribution")
    st.plotly_chart(fig, use_container_width=True)

    fig2 = px.scatter(df, x="Age", y="Salary", color="Department",
                      size="PerformanceScore",
                      title="Employee Insights")
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- SEARCH ----------------
elif menu == "Search":
    emp_id = st.number_input("Enter ID", 1, 1000)
    result = df[df["EmployeeID"] == emp_id]
    st.write(result)

# ---------------- ADD EMPLOYEE ----------------
elif menu == "Add Employee":
    st.subheader("➕ Add Employee")

    age = st.number_input("Age")
    dept = st.selectbox("Department", ["HR", "IT", "Sales", "Finance"])
    salary = st.number_input("Salary")
    years = st.number_input("Years")
    perf = st.slider("Performance", 1, 5)
    hours = st.number_input("Work Hours")

    if st.button("Add"):
        cursor.execute("INSERT INTO employees VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                       (len(df)+1, age, dept, salary, years, perf, hours, 0))
        conn.commit()
        st.success("Employee Added")

# ---------------- UPLOAD CSV ----------------
elif menu == "Upload CSV":
    file = st.file_uploader("Upload CSV")

    if file:
        new_df = pd.read_csv(file)
        new_df.to_sql("employees", conn, if_exists="replace", index=False)
        st.success("Data Uploaded")

# ---------------- PREDICTION ----------------
elif menu == "Prediction":
    model = LogisticRegression()

    X = df[["Age", "Salary", "YearsAtCompany", "WorkHours"]]
    y = df["Attrition"]

    model.fit(X, y)

    age = st.slider("Age", 20, 60)
    salary = st.slider("Salary", 20000, 100000)
    years = st.slider("Years", 1, 20)
    hours = st.slider("Hours", 30, 60)

    pred = model.predict([[age, salary, years, hours]])

    if pred[0] == 1:
        st.error("⚠️ Employee likely to leave")
    else:
        st.success("✅ Employee likely to stay")