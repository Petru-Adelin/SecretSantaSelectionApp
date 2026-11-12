import streamlit as st
import random 
import threading

st.title("Secret Santa")




@st.cache_resource
def get_store():
    return {"team": [], "assignments": {}, "lock": threading.Lock()}

store = get_store()
left, right = st.columns(2)


### Left side -> form input for the names
with left:
    st.subheader("Add a team member")
    with st.form("add_form", clear_on_submit=True):
        name = st.text_input("Name")
        submitted = st.form_submit_button("Add")

    if submitted:
        name = name.strip()
        if not name:
            st.warning("No name has been entered!!!")
        elif name in store["team"]:
            st.warning("The Name is already in there!!!")
        else:
            with store["lock"]:
                store["team"].append(name)

### Right side -> preview of the team
with right:
    st.subheader(f"Team members ({len(store["team"])})") 
    if store["team"]:
       st.multiselect("Team members", store["team"], default=store["team"], disabled=True)
    else:
        st.caption("No member yet in the team")


# random selection of the members 
st.divider()

who = st.selectbox("Who are you: ", store["team"], index=None)

if who and st.button("Drawn a random person"):
    with store["lock"]:
        team = store["team"]
        assigned = store["assignments"]

        if who not in assigned:
            taken = set(assigned.values())
            givers_left = [m for m in team if m not in assigned and m != who]
            options = [m for m in team if m not in taken and m != who]

            def dead_end(pick):
                receivers_left = [m for m in team if m not in taken and m != pick]
                return len(givers_left) == 1 and receivers_left == givers_left

            safe = [o for o in options if not dead_end(o)]
            if safe:
                assigned[who] = random.choice(safe)

if who and who in store["assignments"]:
    st.success(f"{who}, you are buying a gift for **{store['assignments'][who]}**")

done = len(store["assignments"])
st.caption(f"{done} of {len(store['team'])} people have drawn.")


