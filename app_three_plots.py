import streamlit as st
from example_1_simplest_case.ex_1_model_classes import g, Trial
from vidigi.prep import reshape_for_animations, generate_animation_df
from vidigi.animation import animate_activity_log, generate_animation
import plotly.express as px
from utils import dict_diff
import pandas as pd
from streamlit_utils import play_both, pause_both

st.set_page_config(layout="wide")

st.title("Side-by-side DES Animation - Animations Plus Additional Plots")

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

num_runs_input = st.slider("How many runs of the simulation should be done?",
                                  min_value=1, max_value=20, value=3)

sim_duration_input = st.number_input("How long should the simulation run for (minutes)?",
                                      min_value=60, max_value=480, value=480)

g.sim_duration = sim_duration_input
g.number_of_runs = num_runs_input

st.write("---")

scenario1, gap, scenario2 = st.columns([0.45, 0.1, 0.45])

with scenario1:
    s1_n_cubicles = st.slider("What is the number of nurses in the system?",
                            min_value=1, max_value=10, value=1)

    s1_trauma_treat_mean = st.slider("What is the mean length of time (in minutes) for a consultation?",
                                min_value = 3, max_value=60, value=10)

    s1_trauma_treat_var = st.slider("How much does the time for a consultation vary by (in minutes)?",
                                min_value = 0, max_value=30, value=15)

    s1_arrival_rate = st.slider("What is the average length of time between patients arriving?",
                            min_value=1, max_value=30, value=5)

with scenario2:
    s2_n_cubicles = st.slider("What is the number of nurses in the system?",
                            min_value=1, max_value=10, value=1, key="s2_n_cubicles")

    s2_trauma_treat_mean = st.slider("What is the mean length of time (in minutes) for a consultation?",
                                min_value = 3, max_value=60, value=15, key="s2_trauma_treat_m")

    s2_trauma_treat_var = st.slider("How much does the time for a consultation vary by (in minutes)?",
                                min_value = 0, max_value=30, value=20, key="s2_trauma_treat_v")

    s2_arrival_rate = st.slider("What is the average length of time between patients arriving?",
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
            "Number of Cubicles": g.n_cubicles,
            "Trauma Treatment Mean (Minutes)": g.trauma_treat_mean,
            "Trauma Treatment Variance (Minutes)": g.trauma_treat_var,
            "Inter-Arrival Time (Minutes)": g.arrival_rate
        }

        results_df_1 = Trial()
        results_df_1.run_trial()

        interval_audits_1 = results_df_1.get_interval_audits()

        patient_count_df_1 = reshape_for_animations(
            event_log=results_df_1.all_event_logs[results_df_1.all_event_logs['run']==1],
            every_x_time_units=g.audit_interval,
            limit_duration=g.sim_duration,
            step_snapshot_max=9999
        )

        full_patient_df_1 = reshape_for_animations(
            event_log=results_df_1.all_event_logs[results_df_1.all_event_logs['run']==1],
            every_x_time_units=g.audit_interval,
            limit_duration=g.sim_duration,
            step_snapshot_max=15*3,
            debug_mode=False
        )

        animation_df_1 = generate_animation_df(
            full_patient_df=full_patient_df_1,
            event_position_df=event_position_df,
            wrap_queues_at=15,
            step_snapshot_max=15*3,
            gap_between_entities=10,
            gap_between_rows=25,
        )

        activity_animation_1 = generate_animation(
                    animation_df_1,
                    event_position_df=event_position_df ,
                    scenario=g(),
                    debug_mode=True,
                    include_play_button=True,
                    icon_and_text_size=18,
                    plotly_height=800/1.3,
                    frame_duration=200,
                    plotly_width=1200/1.3,
                    override_x_max=300,
                    override_y_max=500,
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
            "Number of Cubicles": g.n_cubicles,
            "Trauma Treatment Mean (Minutes)": g.trauma_treat_mean,
            "Trauma Treatment Variance (Minutes)": g.trauma_treat_var,
            "Inter-Arrival Time (Minutes)": g.arrival_rate
        }

        results_df_2 = Trial()
        results_df_2.run_trial()

        interval_audits_2 = results_df_2.get_interval_audits()

        patient_count_df_2 = reshape_for_animations(
            event_log=results_df_2.all_event_logs[results_df_2.all_event_logs['run']==1],
            every_x_time_units=g.audit_interval,
            limit_duration=g.sim_duration,
            step_snapshot_max=9999
        )

        full_patient_df_2 = reshape_for_animations(
            event_log=results_df_2.all_event_logs[results_df_2.all_event_logs['run']==1],
            every_x_time_units=g.audit_interval,
            limit_duration=g.sim_duration,
            step_snapshot_max=15*3,
            debug_mode=False
        )

        animation_df_2 = generate_animation_df(
            full_patient_df=full_patient_df_2,
            event_position_df=event_position_df,
            wrap_queues_at=15,
            step_snapshot_max=15*3,
            gap_between_entities=10,
            gap_between_rows=25,
        )

        activity_animation_2 = generate_animation(
                    animation_df_2,
                    event_position_df=event_position_df,
                    scenario=g(),
                    debug_mode=True,
                    include_play_button=True,
                    icon_and_text_size=18,
                    plotly_height=800/1.3,
                    frame_duration=200,
                    plotly_width=1200/1.3,
                    override_x_max=300,
                    override_y_max=500,
                    time_display_units="dhm",
                    display_stage_labels=False,
                    add_background_image="https://raw.githubusercontent.com/Bergam0t/side_by_side_des_animations/refs/heads/main/Simplest%20Model%20Background%20Image%20-%20Horizontal%20Layout.png",
                )

        queue_audit_1 = pd.DataFrame(patient_count_df_1[patient_count_df_1["event"]=="treatment_wait_begins"].value_counts(["minute", "run"]).sort_index())
        queue_audit_1['Scenario'] = "Scenario 1"
        queue_audit_2 = pd.DataFrame(patient_count_df_2[patient_count_df_2["event"]=="treatment_wait_begins"].value_counts(["minute", "run"]).sort_index())
        queue_audit_2['Scenario'] = "Scenario 2"
        queue_audit_full = pd.concat([queue_audit_1, queue_audit_2])

        minutes_new = pd.DataFrame({'minute': range(0, 476, 5)})
        # Create a DataFrame with two scenarios: 'Scenario 1' and 'Scenario 2'
        scenarios = pd.DataFrame({'Scenario': ['Scenario 1', 'Scenario 2']})
        expanded_minutes = minutes_new.merge(scenarios, how='cross')

        # Merge the original DataFrame with the new DataFrame
        queue_audit_full = pd.merge(expanded_minutes, queue_audit_full.reset_index(), on=['minute', 'Scenario'], how='left')

        # Fill missing 'count' values with 0
        queue_audit_full['count'] = queue_audit_full['count'].fillna(0).astype(int)

        queue_audit_full.sort_values(['Scenario','minute'], inplace=True)


        queue_bar = px.bar(
                queue_audit_full,
                y='Scenario', x='count',
                title="Queue Lengths Over Time",
                # color="Scenario",
                animation_frame="minute",
                animation_group="Scenario",
                range_x=[0, queue_audit_full['count'].max()*1.1],
                orientation="h"
                )

        queue_bar.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 200
        queue_bar.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 600

        # st.dataframe(queue_audit_full)

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

            st.button("Play Animations Simultaneously", on_click=play_both)

            st.button("Pause All Animations", on_click=pause_both)

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



        st.plotly_chart(queue_bar)



        pathway_animations()
