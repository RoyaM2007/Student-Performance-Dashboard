
import streamlit as st
import pandas as pd

from database import add_student, get_students, get_student
from services import calculate_grade, calculate_statistics


st.set_page_config(
    page_title="Student Performance Dashboard",
    page_icon="🎓",
    layout="wide"
)


def display_students(students):
    """Tələbələrin siyahısını və qiymət dərəcələrini göstərir."""

    if not students:
        st.info("Hələ heç bir tələbə əlavə edilməyib.")
        return

    for student in students:
        student["Grade"] = calculate_grade(student["Score"])

    dataframe = pd.DataFrame(students)
    dataframe = dataframe.rename(
        columns={
            "StudentID": "ID",
            "Name": "Name",
            "Score": "Score",
            "Grade": "Grade"
        }
    )

    st.dataframe(
        dataframe[["ID", "Name", "Score", "Grade"]],
        use_container_width=True,
        hide_index=True
    )


def display_statistics(students):
    """Tələbələrin ümumi statistikasını göstərir."""

    statistics = calculate_statistics(students)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Students", statistics["total_students"])
    col2.metric("Average Score", statistics["average_score"])
    col3.metric("Highest Score", statistics["highest_score"])
    col4.metric("Lowest Score", statistics["lowest_score"])


def main():
    st.title("🎓 Student Performance Dashboard")
    st.write("Tələbə nəticələrinin idarə edilməsi sistemi")

    # Tələbə əlavə etmək
    st.header("Add Student")

    with st.form("add_student_form"):
        student_name = st.text_input("Student Name")

        score = st.number_input(
            "Score",
            min_value=0,
            max_value=100,
            value=0,
            step=1
        )

        submitted = st.form_submit_button("Add Student")

        if submitted:
            if not student_name.strip():
                st.error("Tələbənin adını daxil edin!")
            else:
                try:
                    add_student(student_name.strip(), int(score))
                    st.success("Tələbə uğurla əlavə edildi!")
                    st.rerun()
                except Exception as error:
                    st.error(f"Tələbə əlavə edilə bilmədi: {error}")

    try:
        students = get_students()

        # Tələbələrin siyahısı
        st.header("Student List")
        display_students(students)

        # Tələbə axtarışı
        st.header("Search Student")

        search_name = st.text_input(
            "Tələbənin adını daxil edin",
            key="search_student"
        )

        if search_name.strip():
            matching_students = get_student(search_name.strip())

            if matching_students:
                display_students(matching_students)
            else:
                st.warning("Tələbə tapılmadı.")

        # Statistikalar
        st.header("Statistics")
        display_statistics(students)

    except Exception as error:
        st.error(f"Database ilə işləyərkən xəta baş verdi: {error}")


if __name__ == "__main__":
    main()
