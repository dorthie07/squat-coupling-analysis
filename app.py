import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# ---------------------------------------------------------
# PAGE SETUP
# ---------------------------------------------------------

st.set_page_config(
    page_title="Squat Coupling Analysis",
    layout="wide"
)

st.title("Squat Physiological Coupling Analysis")

st.write(
    """
    This program analyzes synchronized 1-second physiological data
    collected during a squat protocol. It uses 6-second windows with
    3-second overlap, following the time-window approach described
    by Garcia-Retortillo et al.
    """
)


# ---------------------------------------------------------
# UPLOAD DATA
# ---------------------------------------------------------

uploaded_file = st.file_uploader(
    "Upload your Excel file",
    type=["xlsx", "xls"]
)

if uploaded_file is not None:

    # Read Excel file
    df = pd.read_excel(uploaded_file)

    st.subheader("Uploaded data")

    st.write(
        f"Your file contains **{len(df)} rows** and "
        f"**{len(df.columns)} columns**."
    )

    st.dataframe(df.head(10))


    # -----------------------------------------------------
    # COLUMN SELECTION
    # -----------------------------------------------------

    st.subheader("Select your columns")

    st.write(
        "Select the columns containing your synchronized "
        "1-second physiological measurements."
    )

    columns = list(df.columns)

    time_column = st.selectbox(
        "Time column",
        columns
    )

    hr_column = st.selectbox(
        "Heart rate (HR) column",
        columns
    )

    rr_column = st.selectbox(
        "Respiratory rate (RR) column",
        columns
    )

    smo2_column = st.selectbox(
        "Muscle oxygen saturation (SmO₂) column",
        columns
    )

    thb_column = st.selectbox(
        "Total hemoglobin (THb) column",
        columns
    )


    # -----------------------------------------------------
    # PREPARE DATA
    # -----------------------------------------------------

    analysis_df = df[
        [
            time_column,
            hr_column,
            rr_column,
            smo2_column,
            thb_column
        ]
    ].copy()

    analysis_df.columns = [
        "Time",
        "HR",
        "RR",
        "SmO2",
        "THb"
    ]

    # Convert measurements to numbers
    for column in ["Time", "HR", "RR", "SmO2", "THb"]:
        analysis_df[column] = pd.to_numeric(
            analysis_df[column],
            errors="coerce"
        )

    # Remove rows with missing values
    analysis_df = analysis_df.dropna().reset_index(drop=True)


    # -----------------------------------------------------
    # DATA CHECK
    # -----------------------------------------------------

    st.subheader("Data check")

    st.write(
        f"**Usable rows after removing missing values:** "
        f"{len(analysis_df)}"
    )

    if len(analysis_df) < 6:
        st.error(
            "There are not enough data points to perform the "
            "6-second window analysis."
        )
        st.stop()


    # -----------------------------------------------------
    # NORMALIZATION FUNCTION
    # -----------------------------------------------------

    def z_score(values):

        mean_value = np.mean(values)
        sd_value = np.std(values, ddof=1)

        if sd_value == 0 or np.isnan(sd_value):
            return np.zeros(len(values))

        return (values - mean_value) / sd_value


    # -----------------------------------------------------
    # 6-SECOND WINDOW CORRELATION
    # 3-SECOND OVERLAP
    # -----------------------------------------------------

    def calculate_window_correlations(data, variable):

        window_length = 6
        step = 3

        results = []

        start = 0

        while start + window_length <= len(data):

            window = data.iloc[
                start:start + window_length
            ].copy()

            hr_values = window["HR"].values
            variable_values = window[variable].values

            # Normalize separately within each 6-second window
            hr_z = z_score(hr_values)
            variable_z = z_score(variable_values)

            # Pearson correlation
            correlation = np.corrcoef(
                hr_z,
                variable_z
            )[0, 1]

            results.append(
                {
                    "Start_Time": window["Time"].iloc[0],
                    "End_Time": window["Time"].iloc[-1],
                    "Mid_Time": np.mean(window["Time"]),
                    "Variable": variable,
                    "Correlation": correlation
                }
            )

            start += step

        return pd.DataFrame(results)


    # -----------------------------------------------------
    # RUN ANALYSIS
    # -----------------------------------------------------

    if st.button("Run coupling analysis"):

        variables = ["RR", "SmO2", "THb"]

        all_results = []

        for variable in variables:

            result = calculate_window_correlations(
                analysis_df,
                variable
            )

            all_results.append(result)

        results_df = pd.concat(
            all_results,
            ignore_index=True
        )


        # -------------------------------------------------
        # FIRST THIRD VS LAST THIRD
        # -------------------------------------------------

        total_windows = len(
            results_df[
                results_df["Variable"] == "RR"
            ]
        )

        first_third_end = total_windows // 3

        last_third_start = (
            total_windows - total_windows // 3
        )

        results_df["Segment"] = "Middle"

        for variable in variables:

            variable_indices = results_df.index[
                results_df["Variable"] == variable
            ]

            results_df.loc[
                variable_indices[:first_third_end],
                "Segment"
            ] = "Beginning"

            results_df.loc[
                variable_indices[last_third_start:],
                "Segment"
            ] = "End"


        # -------------------------------------------------
        # DISPLAY WINDOW RESULTS
        # -------------------------------------------------

        st.subheader(
            "6-second window coupling results"
        )

        st.write(
            """
            Each correlation represents the relationship between
            HR and the selected physiological variable within one
            6-second window. Windows overlap by 3 seconds.
            """
        )

        st.dataframe(results_df)


        # -------------------------------------------------
        # SUMMARY OF BEGINNING VS END
        # -------------------------------------------------

        st.subheader(
            "Beginning vs. End coupling"
        )

        summary = (
            results_df[
                results_df["Segment"].isin(
                    ["Beginning", "End"]
                )
            ]
            .groupby(
                ["Variable", "Segment"]
            )["Correlation"]
            .agg(
                [
                    "mean",
                    "median",
                    "std",
                    "count"
                ]
            )
            .reset_index()
        )

        st.dataframe(summary)


        # -------------------------------------------------
        # POSITIVE / NEGATIVE COUPLING
        # -------------------------------------------------

        st.subheader(
            "Positive and negative coupling"
        )

        coupling_summary = []

        for variable in variables:

            variable_data = results_df[
                results_df["Variable"] == variable
            ]

            for segment in ["Beginning", "End"]:

                segment_data = variable_data[
                    variable_data["Segment"] == segment
                ]["Correlation"].dropna()

                if len(segment_data) > 0:

                    positive = np.sum(
                        segment_data > 0
                    ) / len(segment_data)

                    negative = np.sum(
                        segment_data < 0
                    ) / len(segment_data)

                else:
                    positive = np.nan
                    negative = np.nan

                coupling_summary.append(
                    {
                        "Variable": variable,
                        "Segment": segment,
                        "Positive_Coupling": positive,
                        "Negative_Coupling": negative
                    }
                )

        coupling_df = pd.DataFrame(
            coupling_summary
        )

        st.dataframe(coupling_df)


        # -------------------------------------------------
        # CORRELATION DISTRIBUTION
        # -------------------------------------------------

        st.subheader(
            "Distribution of coupling values"
        )

        for variable in variables:

            fig, ax = plt.subplots()

            variable_data = results_df[
                results_df["Variable"] == variable
            ]["Correlation"].dropna()

            ax.hist(
                variable_data,
                bins=np.arange(
                    -1,
                    1.05,
                    0.05
                )
            )

            ax.axvline(
                0,
                linestyle="--"
            )

            ax.set_xlabel(
                "Pearson correlation coefficient"
            )

            ax.set_ylabel(
                "Number of 6-second windows"
            )

            ax.set_title(
                f"HR–{variable} Coupling Distribution"
            )

            st.pyplot(fig)

            plt.close(fig)


        # -------------------------------------------------
        # TIME-RESOLVED COUPLING
        # -------------------------------------------------

        st.subheader(
            "Coupling over time"
        )

        for variable in variables:

            variable_data = results_df[
                results_df["Variable"] == variable
            ]

            fig, ax = plt.subplots()

            ax.plot(
                variable_data["Mid_Time"],
                variable_data["Correlation"]
            )

            ax.axhline(
                0,
                linestyle="--"
            )

            ax.set_xlabel(
                "Time"
            )

            ax.set_ylabel(
                "Pearson correlation"
            )

            ax.set_title(
                f"HR–{variable} Coupling Over Time"
            )

            st.pyplot(fig)

            plt.close(fig)


        # -------------------------------------------------
        # DOWNLOAD RESULTS
        # -------------------------------------------------

        st.subheader(
            "Download results"
        )

        csv = results_df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="Download window correlation results",
            data=csv,
            file_name="squat_coupling_results.csv",
            mime="text/csv"
        )

        summary_csv = summary.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="Download beginning vs end summary",
            data=summary_csv,
            file_name="beginning_vs_end_summary.csv",
            mime="text/csv"
        )

        coupling_csv = coupling_df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="Download positive negative coupling results",
            data=coupling_csv,
            file_name="positive_negative_coupling.csv",
            mime="text/csv"
        )
