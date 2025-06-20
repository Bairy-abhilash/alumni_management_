import streamlit as st
import pandas as pd
import datetime

# Initialize session state for alumni data (resets on refresh)
if 'alumni_data' not in st.session_state:
    st.session_state.alumni_data = pd.DataFrame(columns=[
        "Name", "Email", "Year", "Branch", "Registration Date"
    ])

def main():
    st.title("🎓 Alumni Management System")

    menu = ["Register Alumni", "View Alumni", "Search Alumni", "Filter Alumni"]
    choice = st.sidebar.radio("Menu", menu)

    df = st.session_state.alumni_data

    # 1️⃣ Register Alumni
    if choice == "Register Alumni":
        st.subheader("📝 Register New Alumni")
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        year = st.selectbox("Year of Graduation", list(range(1980, datetime.datetime.now().year + 1)))
        branch = st.selectbox("Branch", ["CSE", "ECE", "EEE", "ME", "CE", "Other"])

        if st.button("Register"):
            new_entry = {
                "Name": name,
                "Email": email,
                "Year": year,
                "Branch": branch,
                "Registration Date": datetime.date.today()
            }
            st.session_state.alumni_data = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
            st.success("✅ Alumni Registered!")

    # 2️⃣ View Alumni
    elif choice == "View Alumni":
        st.subheader("📋 All Registered Alumni")
        if df.empty:
            st.info("No alumni registered yet.")
        else:
            st.dataframe(df)

    # 3️⃣ Search Alumni
    elif choice == "Search Alumni":
        st.subheader("🔍 Search Alumni by Name or Email")
        search_term = st.text_input("Enter name or email to search")
        if search_term:
            results = df[
                df["Name"].str.contains(search_term, case=False) |
                df["Email"].str.contains(search_term, case=False)
            ]
            st.dataframe(results if not results.empty else "No results found.")

    # 4️⃣ Filter Alumni
    elif choice == "Filter Alumni":
        st.subheader("🎯 Filter Alumni by Year and Branch")

        year_options = ["All"] + sorted(df["Year"].dropna().unique().astype(str).tolist())
        branch_options = ["All"] + sorted(df["Branch"].dropna().unique().tolist())

        selected_year = st.selectbox("Select Year", year_options)
        selected_branch = st.selectbox("Select Branch", branch_options)

        filtered_df = df.copy()

        if selected_year != "All":
            filtered_df = filtered_df[filtered_df["Year"] == int(selected_year)]

        if selected_branch != "All":
            filtered_df = filtered_df[filtered_df["Branch"] == selected_branch]

        if filtered_df.empty:
            st.warning("No alumni found for the selected filters.")
        else:
            st.dataframe(filtered_df)

if __name__ == "__main__":
    main()
