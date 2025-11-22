import streamlit as st
from profiles import create_profile, get_profile, get_notes
from form_submit import update_profile, add_note, delete_note
from ai import get_macros


st.title("Fitness Coach AI")

def data_form():
    with st.form("user_data_form"):
        st.header("Enter Your Fitness Data")

        profile=st.session_state.profile

        name=st.text_input("Name", value=profile["general"]["name"])
        age=st.number_input("Age", min_value=0, max_value=120, step=1, value=profile["general"]["age"])
        weight=st.number_input("Weight (Kgs)", min_value=0.0, max_value=300.0, step=0.1, value=float(profile["general"]["weight"]))
        height=st.number_input("Height (cm)", min_value=0.0, max_value=250.0, step=0.1, value=float(profile["general"]["height"]))
        genders=["Male", "Female", "Other"]
        gender=st.radio("Gender", genders, genders.index(profile["general"].get("gender", "Male")), horizontal=True)
        activity_options = {
            "Sedentary": "Little or no exercise; desk job",
            "Lightly Active": "Light exercise 1-3 days/week",
            "Moderately Active": "Moderate exercise 3-5 days/week",
            "Very Active": "Hard exercise 6-7 days/week",
            "Extra Active": "Very hard exercise + physical job or 2x training"
        }
        activity_display = [f"{level} - {desc}" for level, desc in activity_options.items()]
        selected = st.selectbox(
            "Activity Level",
            activity_display,
            index=list(activity_options.keys()).index(profile["general"]["activity_level"]),
            help="Select the option that best matches your typical weekly activity."
        )
        activity_level = selected.split(" - ")[0]

        submitted = st.form_submit_button("Submit")
        if submitted:
            if all([name, age, weight, height, gender, activity_level]):
                with st.spinner("Submitting your data..."):
                    updated_profile = update_profile(
                        profile,
                        "general",
                        name=name,
                        age=age,
                        weight=weight,
                        height=height,
                        gender=gender,
                        activity_level=activity_level
                    )
                    st.success("Data submitted successfully!")
            else:
                st.error("Please fill in all the fields before submitting.")

@st.fragment
def goals_form():
    profile=st.session_state.profile
    with st.form("goals_form"):
        st.header("Update Your Fitness Goals")
        goals = st.multiselect(
            "Fitness Goals",
            options=["Lose weight", "Muscle Gain", "Improve endurance"],
            help="Select your fitness goals",
            default=profile.get("goals", ["Muscle Gain"])
        )
        submitted = st.form_submit_button("Submit Goals")
        if submitted:
            if goals:
                with st.spinner("Updating your goals..."):
                    updated_profile = update_profile(
                        profile,
                        "goals",
                        goals=goals
                    )
                    st.session_state.profile = updated_profile
                    st.success("Goals updated successfully!")
            else:
                st.error("Please enter at least one goal before submitting.")


@st.fragment
def macros():
    profile=st.session_state.profile
    nutrition=st.container(border=True)
    nutrition.header("Nutrition Information")
    if nutrition.button("Generate Recommended Macros"):
        print(profile.get("general", {}))
        print('------------')
        print(profile.get("goals", []))
        res=get_macros(profile.get("general", {}), profile.get("goals", []))
        profile["nutrition"]=res
        nutrition.success("Recommended Macros Updated!")

    with nutrition.form("nutrition_form", border=False):
        col1,col2,col3,col4=st.columns(4)
        with col1:
            calories=st.number_input("Daily Calories", min_value=0, max_value=10000, step=50, value=int(profile["nutrition"].get("calories", 0)))
        with col2:
            protein=st.number_input("Daily Protein (grams)", min_value=0, max_value=1000, step=5, value=int(profile["nutrition"].get("protein", 0)))
        with col3:
            fat=st.number_input("Daily Fat (grams)", min_value=0, max_value=500, step=5, value=int(profile["nutrition"].get("fat", 0)))
        with col4:
            carbs=st.number_input("Daily Carbs (grams)", min_value=0, max_value=1000, step=5, value=int(profile["nutrition"].get("carbs", 0)))

        submitted = st.form_submit_button("Submit Nutrition Info")
        if submitted:
            with st.spinner("Submitting your nutrition info..."):
                if all([calories, protein, fat, carbs]):
                    updated_profile = update_profile(
                        profile,
                        "nutrition",
                        calories=calories,
                        protein=protein,
                        fat=fat,
                        carbs=carbs
                    )
                    st.session_state.profile = updated_profile
                    st.success("Nutrition info submitted successfully!")
                else:
                    st.error("Please fill in all the fields before submitting.")

@st.fragment
def notes():
    st.subheader("Your Notes")
    print("Notes:", st.session_state.notes)
    for i,note in enumerate(st.session_state.notes):
        cols=st.columns([5,1])
        with cols[0]:
            st.text(note["text"])
        with cols[1]:
            if st.button("Delete", key=f"delete_note_{i}"):
                delete_note(note["_id"])
                st.session_state.notes.pop(i)
                st.experimental_rerun()
        
    new_note=st.text_area("Add a new note")
    if st.button("Add Note"):
        if new_note.strip():
            added_note=add_note(st.session_state.profileid, new_note.strip())
            st.session_state.notes["entries"].append(added_note)
            st.experimental_rerun()
        else:
            st.error("Note cannot be empty.")


def forms():
    if 'profile_created' not in st.session_state:
        print("Creating profile...")
        profile_id = "1" 
        profile = get_profile(profile_id)
        if not profile:
            profile_id, profile = create_profile(profile_id)
        st.session_state.profile=profile
        st.session_state.profileid=profile_id
        st.session_state.profile_created = True
    if "notes" not in st.session_state:
        print("Fetching notes...")
        notes = get_notes(st.session_state.profileid)
        print(notes)
        st.session_state.notes = notes
    
    data_form()
    goals_form()
    macros()
    notes()

if __name__ == "__main__":
    st.session_state.clear()

    forms()