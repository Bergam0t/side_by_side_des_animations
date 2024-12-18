import streamlit as st

pg = st.navigation(
    [st.Page("app_two_plots.py", title="Animations Only"),
     st.Page("app_three_plots.py", title="Animations Plus Additional Plot"),
     ]
     )

pg.run()
