import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# ---------------------------------------------------------
# PAGE SETUP
# ---------------------------------------------------------

st.set_page_config(
    page_title="Squat Physiological Coupling Analysis",
    page_icon="📊",
    layout="wide"
)

st.title("Squat Physiological Coupling Analysis")

st.write(
    "This program analyzes synchronized 1-second physiological data "
    "collected during a squat protocol. It uses 6-second windows with "
    "3-second overlap, following the time-window approach described by "
    "Garcia-Retortillo et al."
)

st.divider()


# ---------------------------------------------------------
# STEP 1 — UPLOAD DATA
# ---------------------------------------------------------

st.header("Step 1 — Upload data")

uploaded_file = st.file_uploader(
    "Upload your Excel file",
    type=["xlsx", "xls"]
)

if uploaded_file is None:
    st.info("Upload an Excel file to begin the analysis.")
    st.stop()

try:
    data = pd.read_excel(uploaded_file)
except Exception as e:
    st.error(f"Could not read the Excel file: {e}")
    st.stop()

st.success("Excel file uploaded successfully.")

col1, col2 = st.columns(2)

with col1:
    st.metric("Rows", len(data))

with col2:
    st.metric("Columns", len(data.columns))

with st.expander("Preview uploaded data"):
    st.dataframe(data.head(10), use_container_width=True)


# ---------------------------------------------------------
# STEP 2 — SELECT COLUMNS
# ---------------------------------------------------------

st.divider()
st.header("Step 2 — Select columns")

st.write(
    "Select the columns containing your synchronized 1-second "
    "physiological measurements."
)

columns = list(data.columns)

col1, col2 = st.columns(2)

with col1:
    time_col = st.selectbox("Time column", columns)

    hr_col = st.selectbox(
        "Heart rate (HR) column",
        columns
    )

    rr_col = st.selectbox(
        "Respiratory rate (RR) column",
        columns
    )

with col2:
    smo2_col = st.selectbox(
        "Muscle oxygen saturation (SmO₂) column",
        columns
    )

    thb_col = st.selectbox(
        "Total hemoglobin (THb) column",
        columns
    )


# ---------------------------------------------------------
# DATA PREPARATION
# ---------------------------------------------------------

analysis_data = data[
    [time_col, hr_col, rr_col, smo2_col, thb_col]
].copy()

analysis_data.columns = [
    "Time",
    "HR",
    "RR",
    "SmO2",
    "THb"
]

for column in analysis_data.columns:
    analysis_data[column] = pd.to_numeric(
        analysis_data[column],
        errors="coerce"
    )

total_rows = len(analysis_data)

analysis_data = analysis_data.dropna()

usable_rows = len(analysis_data)
missing_rows = total_rows - usable_rows


# ---------------------------------------------------------
# STEP 3 — DATA CHECK
# ---------------------------------------------------------

st.divider()
st.header("Step 3 — Data check")

check1, check2, check3 = st.columns(3)

with check1:
    st.metric("Total rows", total_rows)

with check2:
    st.metric("Usable rows", usable_rows)

with check3:
    st.metric("Rows removed", missing_rows)

if usable_rows < 6:
    st.error(
        "There are fewer than 6 usable rows. "
        "At least one 6-second window is required."
    )
    st.stop()

if missing_rows == 0:
    st.success("Data check passed — no missing values were detected.")
else:
    st.warning(
        f"{missing_rows} row(s) were removed because of missing or "
        "non-numeric values."
    )

st.write(
    "**Analysis settings:** 6-second windows with 3-second overlap."
)


# ---------------------------------------------------------
# HELPER FUNCTION
# ---------------------------------------------------------

def z_score(values):
    values = np.asarray(values, dtype=float)

    std = np.std(values, ddof=1)

    if std == 0 or np.isnan(std):
        return np.full(len(values), np.nan)

    return (values - np.mean(values)) / std


# ---------------------------------------------------------
# COUPLING ANALYSIS FUNCTION
# ---------------------------------------------------------

def calculate_coupling(df, variable):

    results = []

    window_length = 6
    step = 3

    max_start = len(df) - window_length

    for start in range(0, max_start + 1, step):

        window = df.iloc[
            start:start + window_length
        ]

        hr_values = z_score(window["HR"].values)
        variable_values = z_score(window[variable].values)

        if (
            np.any(np.isnan(hr_values))
            or np.any(np.isnan(variable_values))
        ):
            correlation = np.nan
        else:
            correlation = np.corrcoef(
                hr_values,
                variable_values
            )[0, 1]

        results.append({
            "Variable": variable,
            "Window start (s)": window["Time"].iloc[0],
            "Window end (s)": window["Time"].iloc[-1],
            "Coupling": correlation
        })

    return pd.DataFrame(results)


# ---------------------------------------------------------
# STEP 4 — RUN ANALYSIS
# ---------------------------------------------------------

st.divider()
st.header("Step 4 — Run coupling analysis")

st.write(
    "The program will calculate short-timescale Pearson correlations "
    "between HR and each physiological variable."
)

run_analysis = st.button(
    "▶ Run coupling analysis",
    type="primary",
    use_container_width=True
)


if run_analysis:

    with st.spinner("Running coupling analysis..."):

        variables = ["RR", "SmO2", "THb"]

        all_results = []

        for variable in variables:

            result = calculate_coupling(
                analysis_data,
                variable
            )

            all_results.append(result)

        results = pd.concat(
            all_results,
            ignore_index=True
        )

        # -------------------------------------------------
        # FIRST THIRD / LAST THIRD
        # -------------------------------------------------

        results["Third"] = ""

        for variable in variables:

            variable_mask = (
                results["Variable"] == variable
            )

            variable_indices = results.index[
                variable_mask
            ]

            n = len(variable_indices)

            third_size = n // 3

            if third_size > 0:

                first_indices = variable_indices[
                    :third_size
                ]

                last_indices = variable_indices[
                    -third_size:
                ]

                results.loc[
                    first_indices,
                    "Third"
                ] = "First third"

                results.loc[
                    last_indices,
                    "Third"
                ] = "Last third"


    # -----------------------------------------------------
    # RESULTS
    # -----------------------------------------------------

    st.divider()
    st.header("Results")

    # -----------------------------------------------------
    # ANALYSIS SETTINGS
    # -----------------------------------------------------

    st.subheader("Analysis settings")

    settings_col1, settings_col2, settings_col3 = st.columns(3)

    with settings_col1:
        st.metric("Window length", "6 s")

    with settings_col2:
        st.metric("Window overlap", "3 s")

    with settings_col3:
        st.metric(
            "Coupling pairs",
            "3"
        )

    st.write(
        "Coupling pairs: HR–RR, HR–SmO₂, and HR–THb."
    )


    # -----------------------------------------------------
    # SUMMARY TABLE
    # -----------------------------------------------------

    st.subheader("First third vs. last third")

    summary = (
        results[
            results["Third"].isin(
                ["First third", "Last third"]
            )
        ]
        .groupby(
            ["Variable", "Third"]
        )["Coupling"]
        .agg(
            Mean="mean",
            Median="median",
            SD="std",
            N="count"
        )
        .reset_index()
    )

    st.dataframe(
        summary.round(3),
        use_container_width=True
    )


    # -----------------------------------------------------
    # POSITIVE / NEGATIVE COUPLING
    # -----------------------------------------------------

    st.subheader("Positive and negative coupling")

    distribution_summary = []

    for variable in variables:

        values = results.loc[
            results["Variable"] == variable,
            "Coupling"
        ].dropna()

        if len(values) > 0:

            positive = (
                np.sum(values > 0) /
                len(values) *
                100
            )

            negative = (
                np.sum(values < 0) /
                len(values) *
                100
            )

            distribution_summary.append({
                "Variable": variable,
                "Positive coupling (%)": positive,
                "Negative coupling (%)": negative
            })

    distribution_table = pd.DataFrame(
        distribution_summary
    )

    st.dataframe(
        distribution_table.round(1),
        use_container_width=True
    )


    # -----------------------------------------------------
    # COUPLING OVER TIME
    # -----------------------------------------------------

    st.subheader("Coupling over time")

    for variable in variables:

        variable_results = results[
            results["Variable"] == variable
        ]

        fig, ax = plt.subplots()

        ax.plot(
            variable_results["Window start (s)"],
            variable_results["Coupling"],
            marker="o"
        )

        ax.axhline(
            0,
            linestyle="--"
        )

        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Pearson correlation")
        ax.set_title(
            f"HR–{variable} coupling over time"
        )

        ax.set_ylim(-1, 1)

        st.pyplot(fig)

        plt.close(fig)


    # -----------------------------------------------------
    # COUPLING DISTRIBUTIONS
    # -----------------------------------------------------

    st.subheader("Coupling distributions")

    for variable in variables:

        values = results.loc[
            results["Variable"] == variable,
            "Coupling"
        ].dropna()

        fig, ax = plt.subplots()

        bins = np.arange(
            -1,
            1.05,
            0.05
        )

        ax.hist(
            values,
            bins=bins
        )

        ax.set_xlabel(
            "Pearson correlation"
        )

        ax.set_ylabel(
            "Number of windows"
        )

        ax.set_title(
            f"Distribution of HR–{variable} coupling"
        )

        ax.set_xlim(-1, 1)

        st.pyplot(fig)

        plt.close(fig)


    # -----------------------------------------------------
    # DOWNLOAD RESULTS
    # -----------------------------------------------------

    st.subheader("Download results")

    csv_data = results.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="Download window-by-window results",
        data=csv_data,
        file_name="squat_coupling_window_results.csv",
        mime="text/csv",
        use_container_width=True
    )

    summary_csv = summary.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="Download summary results",
        data=summary_csv,
        file_name="squat_coupling_summary.csv",
        mime="text/csv",
        use_container_width=True
    )

    st.success(
        "Coupling analysis completed successfully."
    )
