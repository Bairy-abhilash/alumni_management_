import streamlit as st
import pandas as pd
import streamlit_authenticator as stauth
from alumni import create_table, add_alumni, view_alumni, delete_alumni, search_alumni

# --- LOGIN SETUP ---
names = ['Admin']
usernames = ['admin']
hashed_passwords = [
    '$pbkdf2-sha256$29000$N/fd0wq1tO5w2mbXxUoIYQ$q6H+o6XWzZxBhcFPkb39XYCWiRwVZDrG2A7aZsYhnnY'
]  # password = 'admin123'

authenticator = stauth.Authenticate(
    names, usernames, hashed_passwords,
    "alumni_app", "abcdef", cookie_expiry_days=1
)

name, auth_status, username = authenticator.login("Login", "main")

if auth_status is False:
    st.error("Incorrect username or password")
elif auth_status is None:
    st.warning("Please enter your credentials")
elif auth_status:

    authenticator.logout("Logout", "sidebar")
    st.sidebar.success(f"Welcome {name}")

    create_table()
    st.title("🎓 Alumni Management System")

    menu = ["Add Alumni", "View Alumni", "Search", "Delete Alumni"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Add Alumni":
        st.subheader("Add Alumni Details")
        full_name = st.text_input("Full Name")
        email = st.text_input("Email")
        year = st.number_input("Graduation Year", min_value=1950, max_value=2100)
        course = st.text_input("Course")
        profession = st.text_input("Profession")

        if st.button("Submit"):
            if full_name and email:
                try:
                    add_alumni(full_name, email, year, course, profession)
                    st.success(f"Alumni '{full_name}' added successfully!")
                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.warning("Name and Email are required.")

    elif choice == "View Alumni":
        st.subheader("All Alumni Records")
        data = view_alumni()
        df = pd.DataFrame(data, columns=["ID", "Name", "Email", "Year", "Course", "Profession"])

        with st.expander("🔍 Filters"):
            years = ["All"] + sorted(df["Year"].dropna().unique().tolist())
            courses = ["All"] + sorted(df["Course"].dropna().unique())
            professions = ["All"] + sorted(df["Profession"].dropna().unique())

            selected_year = st.selectbox("Graduation Year", years)
            selected_course = st.selectbox("Course", courses)
            selected_profession = st.selectbox("Profession", professions)

            if selected_year != "All":
                df = df[df["Year"] == selected_year]
            if selected_course != "All":
                df = df[df["Course"] == selected_course]
            if selected_profession != "All":
                df = df[df["Profession"] == selected_profession]

        st.dataframe(df, use_container_width=True)
        st.download_button("📁 Download CSV", df.to_csv(index=False), file_name="alumni.csv")

    elif choice == "Search":
        st.subheader("🔎 Search Alumni by Name or Email")
        keyword = st.text_input("Enter search keyword")
        if st.button("Search"):
            results = search_alumni(keyword)
            if results:
                st.dataframe(pd.DataFrame(results, columns=["ID", "Name", "Email", "Year", "Course", "Profession"]))
            else:
                st.warning("No results found.")

    elif choice == "Delete Alumni":
        st.subheader("❌ Delete Alumni Record")
        data = view_alumni()
        df =
