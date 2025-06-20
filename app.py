import streamlit as st
from alumni import create_table, add_alumni, view_alumni

st.set_page_config(page_title="Alumni Management System")

create_table()

st.title("🎓 Alumni Management System")

menu = ["Add Alumni", "View Alumni"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Add Alumni":
    st.subheader("Add Alumni Details")
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    year = st.number_input("Graduation Year", min_value=1950, max_value=2100)
    course = st.text_input("Course")
    profession = st.text_input("Profession")

    if st.button("Submit"):
        if name and email:
            try:
                add_alumni(name, email, year, course, profession)
                st.success(f"Alumni '{name}' added successfully!")
            except Exception as e:
                st.error(f"Failed to add alumni: {e}")
        else:
            st.warning("Name and Email are required.")

elif choice == "View Alumni":
    st.subheader("Alumni Records")
    data = view_alumni()
    if data:
        st.dataframe(data, use_container_width=True)
    else:
        st.info("No alumni records found.")
