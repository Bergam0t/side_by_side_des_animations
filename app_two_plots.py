import streamlit as st
from example_1_simplest_case.ex_1_model_classes import g, Trial
from vidigi.animation import animate_activity_log
import pandas as pd
from streamlit_utils import play_both, pause_both
from utils import dict_diff
from streamlit_javascript import st_javascript

st.set_page_config(layout="wide")

st.title("Side-by-side DES Animation - Animations Only")

st.write(
    """
This page demonstrates a method for allowing animated versions of simulated pathways to be displayed side by side and triggered (nearly) simultaneously.

This could be used to effectively demonstrate the benefits or downsides of 'what-if' scenarios that are tried out in the simulation - either comparing this with the current reality, or the difference between two proposed scenarios.

By being able to view the size of queues and resource utilisation at the same point in time, it is hoped that users will be able to build up a sense of the impact of changes on their system.

There are several limitations of this approach at the moment:

- it is not possible to simultaneously pause the animations
- grabbing the timeline bar in one animation does not propagate the change to the other bar (though some progress has been made on this)
- there is a very small delay before the second plot is animated, leading to the animations being up to a couple of time steps out

However, it is hoped that the benefits of being able to offer this sort of visual will - for now - outweigh the downsides.
    """
)

event_position_df = pd.DataFrame([
                    {'event': 'arrival',
                     'x':  50, 'y': 280,
                     'label': "Arrival" },

                    # Triage - minor and trauma
                    {'event': 'treatment_wait_begins',
                     'x':  205, 'y': 170,
                     'label': "Waiting for Treatment"},

                    {'event': 'treatment_begins',
                     'x':  205, 'y': 110,
                     'resource':'n_cubicles',
                     'label': "Being Treated"},

                    {'event': 'exit',
                     'x':  270, 'y': 70,
                     'label': "Exit"}

                ])

num_runs_input = 2 #st.slider("How many runs of the simulation should be done?",
                                #   min_value=1, max_value=20, value=3)

sim_duration_input = st.number_input("How long should the simulation run for (minutes)?",
                                      min_value=60, max_value=480, value=480)

g.sim_duration = sim_duration_input
g.number_of_runs = num_runs_input

st.write("---")

scenario1, gap, scenario2 = st.columns([0.45, 0.1, 0.45])

with scenario1:
    st.subheader("Scenario 1")
    s1_n_cubicles = st.slider("What is the number of nurses in the system?",
                            min_value=1, max_value=10, value=1)

    s1_trauma_treat_mean = st.slider("What is the mean length of time (in minutes) for a consultation?",
                                min_value = 3, max_value=60, value=10)

    s1_trauma_treat_var = st.slider("How much does the time for a consultation vary by (in minutes)?",
                                min_value = 0, max_value=30, value=15)

    s1_arrival_rate = st.slider("What is the average length of time between patients arriving (in minutes)?",
                            min_value=1, max_value=30, value=5)

with scenario2:
    st.subheader("Scenario 2")
    s2_n_cubicles = st.slider("What is the number of nurses in the system?",
                            min_value=1, max_value=10, value=1, key="s2_n_cubicles")

    s2_trauma_treat_mean = st.slider("What is the mean length of time (in minutes) for a consultation?",
                                min_value = 3, max_value=60, value=25, key="s2_trauma_treat_m")

    s2_trauma_treat_var = st.slider("How much does the time for a consultation vary by (in minutes)?",
                                min_value = 0, max_value=30, value=20, key="s2_trauma_treat_v")

    s2_arrival_rate = st.slider("What is the average length of time between patients arriving (in minutes)?",
                            min_value=1, max_value=30, value=5, key="s2_trauma_treat_iat")

st.write("---")

button_run_pressed = st.button("Run simulations")

if button_run_pressed:
    with st.spinner('Simulating...'):

        g.n_cubicles = s1_n_cubicles
        g.trauma_treat_mean = s1_trauma_treat_mean
        g.trauma_treat_var = s1_trauma_treat_var
        g.arrival_rate = s1_arrival_rate

        scenario_1_attrs = {
            "Number of Nurses": g.n_cubicles,
            "Trauma Treatment Mean (Minutes)": g.trauma_treat_mean,
            "Trauma Treatment Variance (Minutes)": g.trauma_treat_var,
            "Inter-Arrival Time (Minutes)": g.arrival_rate
        }

        results_df_1 = Trial()
        results_df_1.run_trial()

        activity_animation_1 = animate_activity_log(
                    event_log=results_df_1.all_event_logs[results_df_1.all_event_logs['run']==1],
                    event_position_df= event_position_df,
                    scenario=g(),
                    debug_mode=True,
                    every_x_time_units=2,
                    include_play_button=True,
                    icon_and_text_size=18,
                    gap_between_entities=10,
                    gap_between_rows=25,
                    plotly_height=800/1.3,
                    frame_duration=200,
                    plotly_width=1200/1.3,
                    override_x_max=300,
                    override_y_max=500,
                    limit_duration=g.sim_duration,
                    wrap_queues_at=15,
                    step_snapshot_max=15*3,
                    time_display_units="dhm",
                    display_stage_labels=False,
                    add_background_image="https://raw.githubusercontent.com/Bergam0t/side_by_side_des_animations/refs/heads/main/Simplest%20Model%20Background%20Image%20-%20Horizontal%20Layout.png",
                )

        # activity_animation_1["layout"].pop("updatemenus")

    #     activity_animation_1.update_layout(
    #         updatemenus=[dict(
    #         type="buttons",
    #         name="PlayButton",
    #         buttons=[dict(label="Play/Pause",
    #                       method="animate",
    #                       args=[None])])]
    # )


        g.n_cubicles = s2_n_cubicles
        g.trauma_treat_mean = s2_trauma_treat_mean
        g.trauma_treat_var = s2_trauma_treat_var
        g.arrival_rate = s2_arrival_rate

        scenario_2_attrs = {
            "Number of Nurses": g.n_cubicles,
            "Trauma Treatment Mean (Minutes)": g.trauma_treat_mean,
            "Trauma Treatment Variance (Minutes)": g.trauma_treat_var,
            "Inter-Arrival Time (Minutes)": g.arrival_rate
        }

        results_df_2 = Trial()
        results_df_2.run_trial()

        activity_animation_2 = animate_activity_log(
                    event_log=results_df_2.all_event_logs[results_df_2.all_event_logs['run']==1],
                    event_position_df= event_position_df,
                    scenario=g(),
                    debug_mode=True,
                    every_x_time_units=2,
                    include_play_button=True,
                    icon_and_text_size=18,
                    gap_between_entities=10,
                    gap_between_rows=25,
                    plotly_height=800/1.3,
                    frame_duration=200,
                    plotly_width=1200/1.3,
                    override_x_max=300,
                    override_y_max=500,
                    limit_duration=g.sim_duration,
                    wrap_queues_at=15,
                    step_snapshot_max=15*3,
                    time_display_units="dhm",
                    display_stage_labels=False,
                    add_background_image="https://raw.githubusercontent.com/Bergam0t/side_by_side_des_animations/refs/heads/main/Simplest%20Model%20Background%20Image%20-%20Horizontal%20Layout.png",
                )

    #     activity_animation_2.update_layout(
    #         updatemenus=[dict(
    #         type="buttons",
    #         buttons=[dict(label="Play",
    #                       method="animate",
    #                       args=[None],
    #                       name="PlayButton"),
    #                 dict(label="Pause",
    #                       method="animate",
    #                       args=[None],
    #                       name="PauseButton")])]
    # )

        scenario1_out, scenario2_out = st.columns(2)

        with scenario1_out:
            st.write("**Parameters that Differ**")

            st.write(dict_diff(scenario_1_attrs, scenario_2_attrs))

        with scenario2_out:
                st.write("**Parameters that Differ**")

                st.write(dict_diff(scenario_2_attrs, scenario_1_attrs))

        @st.fragment
        def pathway_animations():

            with scenario1_out:

                st.plotly_chart(
                activity_animation_1,
                key="animation_scenario_1"
                )

            with scenario2_out:


                st.plotly_chart(
                activity_animation_2,
                    key="animation_scenario_2"
                )

            col_blank_button_a, col_button_1, col_blank_button_b = st.columns(3)

            col_button_1.button("Play Both Animations Simultaneously", on_click=play_both, use_container_width=True)

        pathway_animations()
