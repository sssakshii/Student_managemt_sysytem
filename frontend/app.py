
import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Student Management System",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 Student Management System")


# Fetch students from FastAPI
def get_students():
    try:
        response = requests.get(
            f"{API_URL}/students",
            timeout=5
        )
        response.raise_for_status()

        data = response.json()

        if isinstance(data, dict):
            return data.get("students", [])

        return data

    except requests.RequestException as e:
        st.error(f"Backend connection failed: {e}")
        return []


# Four frontend sections
tab1, tab2, tab3, tab4 = st.tabs([
    "➕ Add Student",
    "📋 View Students",
    "✏️ Update Student",
    "🗑️ Delete Student"
])


# ---------------- ADD STUDENT ----------------

with tab1:

    st.subheader("Add New Student")

    with st.form("add_student_form"):

        name = st.text_input("Student Name")
        class_name = st.selectbox(
            "Class",
            ["10", "11", "12"]
        )

        age = st.number_input(
            "Age", min_value=1, max_value=100, value=18
        )

        father_name = st.text_input("Father Name")
        mother_name = st.text_input("Mother Name")

        monthly_fee = st.number_input(
            "Monthly Fee", min_value=0.0
        )

        height = st.number_input(
            "Height (meters)", min_value=0.01, value=1.65
        )

        weight = st.number_input(
            "Weight (kg)", min_value=0.1, value=60.0
        )

        submit = st.form_submit_button(
            "Add Student",
            use_container_width=True
        )

        if submit:

            student = {
                "name": name,
                "class_name": class_name,
                "age": age,
                "father_name": father_name,
                "mother_name": mother_name,
                "monthly_fee": monthly_fee,
                "height": height,
                "weight": weight
            }

            try:
                response = requests.post(
                    f"{API_URL}/students",
                    json=student,
                    timeout=10
                )

                if response.status_code in [200, 201]:
                    st.success("Student added successfully!")
                    st.json(response.json())
                else:
                    st.error(response.text)

            except requests.RequestException as e:
                st.error(f"Error: {e}")


# ---------------- VIEW STUDENTS ----------------

with tab2:

    st.subheader("All Student Records")

    if st.button("Refresh Records"):
        st.rerun()

    students = get_students()

    if students:
        df = pd.DataFrame(students)
        st.dataframe(df, use_container_width=True)

        st.metric("Total Students", len(students))
    else:
        st.info("No student records found.")


# ---------------- UPDATE STUDENT ----------------

with tab3:

    st.subheader("Update Student Details")

    student_id = st.text_input(
        "Enter Student ID"
    )

    with st.form("update_student_form"):

        update_name = st.text_input("New Name")
        update_class = st.selectbox(
            "New Class", ["10", "11", "12"]
        )

        update_age = st.number_input(
            "New Age", min_value=1, max_value=100, value=18
        )

        update_father = st.text_input("New Father Name")
        update_mother = st.text_input("New Mother Name")

        update_fee = st.number_input(
            "New Monthly Fee", min_value=0.0
        )

        update_height = st.number_input(
            "New Height (meters)", min_value=0.01, value=1.65
        )

        update_weight = st.number_input(
            "New Weight (kg)", min_value=0.1, value=60.0
        )

        update_btn = st.form_submit_button("Update Student")

        if update_btn:

            student = {
                "name": update_name,
                "class_name": update_class,
                "age": update_age,
                "father_name": update_father,
                "mother_name": update_mother,
                "monthly_fee": update_fee,
                "height": update_height,
                "weight": update_weight
            }

            if not student_id:
                st.warning("Enter Student ID first.")
            else:
                try:
                    response = requests.put(
                        f"{API_URL}/students/{student_id}",
                        json=student,
                        timeout=10
                    )

                    if response.ok:
                        st.success("Student updated successfully!")
                        st.json(response.json())
                    else:
                        st.error(response.text)

                except requests.RequestException as e:
                    st.error(str(e))


# ---------------- DELETE STUDENT ----------------

with tab4:

    st.subheader("Delete Student Record")

    delete_id = st.text_input(
        "Enter Student ID to Delete"
    )

    confirm = st.checkbox(
        "I confirm that I want to delete this student."
    )

    if st.button("Delete Student", type="primary"):

        if not delete_id:
            st.warning("Enter Student ID.")
        elif not confirm:
            st.warning("Please confirm deletion.")
        else:
            try:
                response = requests.delete(
                    f"{API_URL}/students/{delete_id}",
                    timeout=10
                )

                if response.ok:
                    st.success("Student deleted successfully!")
                else:
                    st.error(response.text)

            except requests.RequestException as e:
                st.error(str(e))
