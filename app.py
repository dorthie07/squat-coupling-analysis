import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# =========================================================
# PAGE SETUP
# =========================================================

st.set_page_config(
    page_title="Squat Physiological Coupling Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    .main {
        padding-top: 1rem;
    }

    .main-header {
        padding: 1.2rem 0 0.5rem 0;
    }

    .main-header h1 {
        font-size: 2.2rem;
        margin-bottom: 0.2rem;
    }

    .main-header p {
        font-size: 1rem;
        color: #666;
    }

    .section-card {
        padding: 1.2rem 1.4rem;
        border-radius: 12px;
        border: 1px solid #e5e5e5;
        background-color: #fafafa;
        margin-bottom: 1rem;
    }

    .section-title {
        font-size: 1.25rem;
        font-weight: 600;
        margin-bottom: 0.4rem;
    }

    .section-description {
        color: #666;
        font-size: 0.92rem;
    }

    .step-badge {
        display: inline-block;
        padding: 0.25rem 0.65rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }

    [data-testid="stMetric"] {
        background-color: #fafafa;
        border: 1px solid #e5e5e5;
        padding: 0.8rem;
        border-radius: 10px;
    }

    section[data-testid="stSidebar"] {
        border-right: 1px solid #e5e5e5;
    }

    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
    }

    .stDownloadButton > button {
        border-radius: 8px;
    }

    [data-testid="stDataFrame"] {
        border-radius: 8px;
    }

    hr {
        margin: 1.5rem 0;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# HEADER
# =========================================================

st.markdown(
    """
    <div class="main-header">
        <h1>📊 Squat Physiological Coupling Analysis</h1>
        <p>
        Short-timescale analysis of synchronized physiological signals
        during the squat protocol.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("## Analysis overview")

    st.write(
        "This tool calculates short-timescale coupling between "
        "heart rate and three physiological signals."
    )

    st.divider()

    st.markdown("### Analysis settings")

    st.write("**Analysis sampling rate**")
    st.write("1 Hz")

    st.write("**Window length**")
    st.write("6 seconds")

    st.write("**Window step**")
    st.write("3 seconds")

    st.write("**Window overlap**")
    st.write("50%")

    st.write("**Coupling method**")
    st.write("Pearson correlation")

    st.divider()

    st.markdown("### Signals")

    st.write("❤️ HR — Heart rate")
    st.write("🫁 RR — Respiratory rate")
    st.write("🩸 SmO₂ — Muscle oxygen saturation")
    st.write("〰️ THb — Total hemoglobin")

    st.divider()

    st.caption(
        "Signals are converted to a common 1 Hz analysis grid before "
        "short-timescale coupling is calculated."
    )


# =========================================================
# INTRODUCTION
# =========================================================

with st.expander("About this analysis", expanded=False):

    st.write(
        "This program analyzes synchronized physiological data using "
        "short-timescale coupling analysis. Signals can have different "
        "native sampling rates and are converted to a common 1 Hz "
        "analysis grid before coupling is calculated."
    )

    st.write(
        "For example, a 2000 Hz signal is summarized within each "
        "1-second interval so that it can be compared with signals "
        "sampled at approximately 1 Hz."
    )

    st.info(
        "The original study examined heart rate and EMG. "
        "This program adapts the short-timescale approach to examine "
        "HR–RR, HR–SmO₂, and HR–THb coupling."
    )


st.divider()


# =========================================================
# STEP 1 — UPLOAD
# =========================================================

st.markdown(
    """
    <div class="section-card">
        <div class="step-badge">STEP 1</div>
        <div class="section-title">Upload your data</div>
        <div class="section-description">
            Upload the Excel file containing your synchronized
            physiological data.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


uploaded_file = st.file_uploader(
    "Choose an Excel file",
    type=["xlsx", "xls"],
    label_visibility="collapsed"
)


if uploaded_file is None:

    st.info(
        "👆 Upload an Excel file to begin."
    )

    st.stop()


try:

    data = pd.read_excel(
        uploaded_file
    )

except Exception as e:

    st.error(
        f"Could not read the Excel file: {e}"
    )

    st.stop()


st.success(
    "✓ File uploaded successfully"
)


# =========================================================
# FILE INFORMATION
# =========================================================

col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Rows",
        len(data)
    )


with col2:

    st.metric(
        "Columns",
        len(data.columns)
    )


with col3:

    st.metric(
        "File",
        uploaded_file.name
    )


with st.expander(
    "Preview uploaded data"
):

    st.dataframe(
        data.head(10),
        use_container_width=True
    )


# =========================================================
# STEP 2 — SELECT COLUMNS
# =========================================================

st.divider()

st.markdown(
    """
    <div class="section-card">
        <div class="step-badge">STEP 2</div>
        <div class="section-title">Select your signals</div>
        <div class="section-description">
            Match each measurement to the correct column in your
            Excel file.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


columns = list(
    data.columns
)


col1, col2 = st.columns(2)


with col1:

    time_col = st.selectbox(
        "⏱ Time",
        columns
    )

    hr_col = st.selectbox(
        "❤️ Heart rate (HR)",
        columns
    )

    rr_col = st.selectbox(
        "🫁 Respiratory rate (RR)",
        columns
    )


with col2:

    smo2_col = st.selectbox(
        "🩸 Muscle oxygen saturation (SmO₂)",
        columns
    )

    thb_col = st.selectbox(
        "〰️ Total hemoglobin (THb)",
        columns
    )


# =========================================================
# SIGNAL SAMPLING RATES
# =========================================================

st.markdown("### Native sampling rates")

st.write(
    "Enter the native sampling rate of each signal. "
    "These rates are used to convert all signals to the "
    "common 1 Hz analysis grid."
)


rate_options = [
    1,
    2,
    5,
    10,
    20,
    50,
    100,
    200,
    500,
    1000,
    2000
]


col1, col2, col3, col4 = st.columns(4)


with col1:

    hr_rate = st.selectbox(
        "HR sampling rate (Hz)",
        rate_options,
        index=0
    )


with col2:

    rr_rate = st.selectbox(
        "RR sampling rate (Hz)",
        rate_options,
        index=0
    )


with col3:

    smo2_rate = st.selectbox(
        "SmO₂ sampling rate (Hz)",
        rate_options,
        index=0
    )


with col4:

    thb_rate = st.selectbox(
        "THb sampling rate (Hz)",
        rate_options,
        index=0
    )


st.info(
    "For your data, enter 2000 Hz for the signal sampled at 2000 Hz "
    "and 1 Hz for the signal sampled at 1 Hz. The other signals should "
    "be set according to their actual native sampling rates."
)


# =========================================================
# DATA PREPARATION
# =========================================================

analysis_data = data[
    [
        time_col,
        hr_col,
        rr_col,
        smo2_col,
        thb_col
    ]
].copy()


analysis_data.columns = [
    "Time",
    "HR",
    "RR",
    "SmO2",
    "THb"
]


# Convert everything to numeric

for column in analysis_data.columns:

    analysis_data[column] = pd.to_numeric(
        analysis_data[column],
        errors="coerce"
    )


# Remove rows where time itself is missing

analysis_data = analysis_data[
    analysis_data["Time"].notna()
].copy()


# Sort chronologically

analysis_data = analysis_data.sort_values(
    "Time"
).reset_index(
    drop=True
)


# =========================================================
# STEP 3 — DATA CHECK
# =========================================================

st.divider()

st.markdown(
    """
    <div class="section-card">
        <div class="step-badge">STEP 3</div>
        <div class="section-title">Check your data</div>
        <div class="section-description">
            The program checks the time column, missing values,
            and the native sampling structure of your data.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


total_rows = len(
    analysis_data
)


missing_counts = (
    analysis_data[
        [
            "HR",
            "RR",
            "SmO2",
            "THb"
        ]
    ]
    .isna()
    .sum()
)


total_missing = int(
    missing_counts.sum()
)


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Total rows",
        total_rows
    )


with col2:

    st.metric(
        "Missing values",
        total_missing
    )


with col3:

    st.metric(
        "Analysis sampling",
        "1 Hz"
    )


# ---------------------------------------------------------
# Missing values
# ---------------------------------------------------------

if total_missing > 0:

    st.warning(
        "⚠ Missing or non-numeric values were detected. "
        "The analysis will continue. Missing observations will "
        "not be automatically deleted or interpolated."
    )

    st.write(
        "Missing values by column:"
    )

    st.dataframe(
        missing_counts[
            missing_counts > 0
        ].to_frame(
            "Missing values"
        ),
        use_container_width=True
    )

else:

    st.success(
        "✓ No missing or non-numeric signal values detected."
    )


# ---------------------------------------------------------
# Time check
# ---------------------------------------------------------

time_values = (
    analysis_data["Time"].values
)


if len(time_values) > 1:

    time_differences = np.diff(
        time_values
    )

    median_difference = np.median(
        time_differences
    )

    min_difference = np.min(
        time_differences
    )

    max_difference = np.max(
        time_differences
    )

else:

    median_difference = np.nan
    min_difference = np.nan
    max_difference = np.nan


col1, col2, col3 = st.columns(3)


with col1:

    if not np.isnan(
        median_difference
    ):

        st.metric(
            "Median time interval",
            f"{median_difference:.6f} s"
        )


with col2:

    if not np.isnan(
        min_difference
    ):

        st.metric(
            "Minimum interval",
            f"{min_difference:.6f} s"
        )


with col3:

    if not np.isnan(
        max_difference
    ):

        st.metric(
            "Maximum interval",
            f"{max_difference:.6f} s"
        )


if len(time_values) > 1:

    if (
        np.all(
            np.diff(time_values) > 0
        )
    ):

        st.success(
            "✓ Time values are strictly increasing."
        )

    else:

        st.error(
            "Time values are not strictly increasing. "
            "Please check your time column."
        )

        st.stop()


# =========================================================
# STEP 4 — CONVERT TO 1 Hz
# =========================================================

st.divider()

st.markdown(
    """
    <div class="section-card">
        <div class="step-badge">STEP 4</div>
        <div class="section-title">Convert signals to a common time base</div>
        <div class="section-description">
            Signals with different native sampling rates are converted
            to a common 1 Hz analysis grid before coupling is calculated.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


st.write(
    "The 2000 Hz signal is summarized within each 1-second interval. "
    "Signals already sampled at 1 Hz are retained on the 1-second grid."
)


# ---------------------------------------------------------
# Function to convert a signal to 1 Hz
# ---------------------------------------------------------

def convert_to_1hz(
    df,
    signal,
    native_rate
):

    temp = df[
        [
            "Time",
            signal
        ]
    ].copy()

    temp = temp.dropna(
        subset=["Time"]
    )

    temp = temp.sort_values(
        "Time"
    )

    # Create 1-second bins.
    #
    # The floor operation means:
    #
    # 0.000 - 0.999 -> second 0
    # 1.000 - 1.999 -> second 1
    # 2.000 - 2.999 -> second 2
    #
    # This is appropriate for converting high-frequency data
    # into one value per second.

    temp["AnalysisTime"] = np.floor(
        temp["Time"]
    ).astype(int)


    # Aggregate within each 1-second interval.
    #
    # mean() automatically ignores NA values.
    #
    # If every value in the second is NA,
    # the resulting value remains NA.

    result = (
        temp
        .groupby(
            "AnalysisTime"
        )[signal]
        .mean()
        .reset_index()
    )


    result = result.rename(
        columns={
            "AnalysisTime": "Time"
        }
    )


    return result


# ---------------------------------------------------------
# Convert each signal
# ---------------------------------------------------------

hr_1hz = convert_to_1hz(
    analysis_data,
    "HR",
    hr_rate
)


rr_1hz = convert_to_1hz(
    analysis_data,
    "RR",
    rr_rate
)


smo2_1hz = convert_to_1hz(
    analysis_data,
    "SmO2",
    smo2_rate
)


thb_1hz = convert_to_1hz(
    analysis_data,
    "THb",
    thb_rate
)


# ---------------------------------------------------------
# Merge signals onto common 1 Hz grid
# ---------------------------------------------------------

signals_1hz = pd.merge(
    hr_1hz,
    rr_1hz,
    on="Time",
    how="outer"
)


signals_1hz = pd.merge(
    signals_1hz,
    smo2_1hz,
    on="Time",
    how="outer"
)


signals_1hz = pd.merge(
    signals_1hz,
    thb_1hz,
    on="Time",
    how="outer"
)


signals_1hz = signals_1hz.sort_values(
    "Time"
).reset_index(
    drop=True
)


# ---------------------------------------------------------
# Display converted data
# ---------------------------------------------------------

st.success(
    "✓ Signals converted to the common 1 Hz analysis grid."
)


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "HR rate",
        f"{hr_rate} Hz"
    )


with col2:

    st.metric(
        "RR rate",
        f"{rr_rate} Hz"
    )


with col3:

    st.metric(
        "SmO₂ rate",
        f"{smo2_rate} Hz"
    )


with col4:

    st.metric(
        "THb rate",
        f"{thb_rate} Hz"
    )


with st.expander(
    "Preview 1 Hz analysis data"
):

    st.dataframe(
        signals_1hz.head(20),
        use_container_width=True
    )


# =========================================================
# ANALYSIS PARAMETERS
# =========================================================

window_seconds = 6
step_seconds = 3

minimum_valid_observations = 4


# =========================================================
# CHECK MINIMUM DATA
# =========================================================

if len(signals_1hz) < window_seconds:

    st.error(
        f"At least {window_seconds} seconds of 1 Hz data "
        "are required for the analysis."
    )

    st.stop()


# =========================================================
# COUPLING FUNCTION
# =========================================================

def calculate_coupling(
    df,
    variable,
    window_seconds=6,
    step_seconds=3,
    minimum_valid_observations=4
):

    results = []


    # -----------------------------------------------------
    # Because the data are now on a 1 Hz grid:
    #
    # 6 rows = 6 seconds
    # 3 rows = 3 seconds
    # -----------------------------------------------------

    window_length = int(
        window_seconds
    )

    step = int(
        step_seconds
    )


    max_start = (
        len(df)
        - window_length
    )


    for start in range(
        0,
        max_start + 1,
        step
    ):


        window = df.iloc[
            start:start + window_length
        ].copy()


        # -------------------------------------------------
        # Pairwise deletion
        #
        # Only retain observations where BOTH HR and the
        # target physiological variable are available.
        # -------------------------------------------------

        valid = window[
            [
                "HR",
                variable
            ]
        ].dropna()


        n_valid = len(
            valid
        )


        # -------------------------------------------------
        # Calculate Pearson correlation
        # -------------------------------------------------

        if n_valid >= minimum_valid_observations:

            hr_values = valid[
                "HR"
            ].to_numpy(
                dtype=float
            )


            variable_values = valid[
                variable
            ].to_numpy(
                dtype=float
            )


            # Check for zero variance

            if (
                np.std(
                    hr_values,
                    ddof=1
                ) == 0
                or
                np.std(
                    variable_values,
                    ddof=1
                ) == 0
            ):

                correlation = np.nan

            else:

                correlation = np.corrcoef(
                    hr_values,
                    variable_values
                )[0, 1]

        else:

            correlation = np.nan


        results.append({

            "Variable":
                variable,

            "Window start (s)":
                window["Time"].iloc[0],

            "Window end (s)":
                window["Time"].iloc[-1],

            "N valid":
                n_valid,

            "N missing":
                window_seconds - n_valid,

            "Coupling":
                correlation

        })


    return pd.DataFrame(
        results
    )


# =========================================================
# STEP 5 — RUN ANALYSIS
# =========================================================

st.divider()

st.markdown(
    """
    <div class="section-card">
        <div class="step-badge">STEP 5</div>
        <div class="section-title">Run coupling analysis</div>
        <div class="section-description">
            Calculate short-timescale Pearson correlations
            between HR and RR, SmO₂, and THb.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


st.write(
    f"Each correlation uses a {window_seconds}-second window "
    f"with a {step_seconds}-second step. A minimum of "
    f"{minimum_valid_observations} paired observations is required "
    "to calculate a correlation."
)


run_analysis = st.button(
    "▶  Run coupling analysis",
    type="primary",
    use_container_width=True
)


if run_analysis:


    with st.spinner(
        "Analyzing physiological coupling..."
    ):


        variables = [
            "RR",
            "SmO2",
            "THb"
        ]


        all_results = []


        for variable in variables:

            result = calculate_coupling(
                signals_1hz,
                variable,
                window_seconds,
                step_seconds,
                minimum_valid_observations
            )


            all_results.append(
                result
            )


        results = pd.concat(
            all_results,
            ignore_index=True
        )


        # -------------------------------------------------
        # First / middle / last third
        # -------------------------------------------------

        results["Third"] = ""


        for variable in variables:

            mask = (
                results["Variable"]
                == variable
            )


            indices = results.index[
                mask
            ]


            n = len(
                indices
            )


            first_end = int(
                np.ceil(
                    n / 3
                )
            )


            last_start = int(
                np.floor(
                    2 * n / 3
                )
            )


            results.loc[
                indices[:first_end],
                "Third"
            ] = "First third"


            results.loc[
                indices[first_end:last_start],
                "Third"
            ] = "Middle third"


            results.loc[
                indices[last_start:],
                "Third"
            ] = "Last third"


    # =====================================================
    # RESULTS
    # =====================================================

    st.divider()

    st.header("Analysis results")


    st.success(
        "✓ Coupling analysis completed successfully."
    )


    # =====================================================
    # TOP METRICS
    # =====================================================

    number_of_windows = (
        results[
            "Window start (s)"
        ]
        .nunique()
    )


    valid_correlations = (
        results[
            "Coupling"
        ]
        .notna()
        .sum()
    )


    total_correlations = len(
        results
    )


    col1, col2, col3, col4, col5 = st.columns(5)


    with col1:

        st.metric(
            "Window length",
            f"{window_seconds} s"
        )


    with col2:

        st.metric(
            "Step",
            f"{step_seconds} s"
        )


    with col3:

        st.metric(
            "Coupling pairs",
            "3"
        )


    with col4:

        st.metric(
            "Windows",
            number_of_windows
        )


    with col5:

        st.metric(
            "Valid correlations",
            f"{valid_correlations}/{total_correlations}"
        )


    # =====================================================
    # MISSING DATA IN COUPLING
    # =====================================================

    missing_coupling = (
        results["Coupling"]
        .isna()
        .sum()
    )


    if missing_coupling > 0:

        st.warning(
            f"{missing_coupling} window-level correlations "
            "could not be calculated because there were fewer "
            f"than {minimum_valid_observations} valid paired "
            "observations or one signal had zero variance."
        )


    # =====================================================
    # RESULTS TABS
    # =====================================================

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "📈 Coupling over time",
            "📊 First vs. last third",
            "📉 Distributions",
            "⬇️ Download results"
        ]
    )


    # =====================================================
    # TAB 1 — COUPLING OVER TIME
    # =====================================================

    with tab1:

        st.subheader(
            "Coupling over time"
        )


        st.caption(
            "Each point represents the Pearson correlation "
            f"calculated within a {window_seconds}-second window. "
            "Correlations are based only on valid paired observations."
        )


        for variable in variables:

            variable_results = results[
                results["Variable"]
                == variable
            ]


            fig, ax = plt.subplots(
                figsize=(10, 4)
            )


            ax.plot(
                variable_results[
                    "Window start (s)"
                ],
                variable_results[
                    "Coupling"
                ],
                marker="o"
            )


            ax.axhline(
                0,
                linestyle="--",
                color="black",
                alpha=0.5
            )


            ax.set_xlabel(
                "Time (s)"
            )


            ax.set_ylabel(
                "Pearson correlation"
            )


            ax.set_title(
                f"HR–{variable} coupling"
            )


            ax.set_ylim(
                -1,
                1
            )


            ax.grid(
                alpha=0.2
            )


            st.pyplot(
                fig
            )


            plt.close(
                fig
            )


    # =====================================================
    # TAB 2 — FIRST VS LAST
    # =====================================================

    with tab2:

        st.subheader(
            "First third vs. last third"
        )


        summary = (

            results[
                results["Third"].isin(
                    [
                        "First third",
                        "Last third"
                    ]
                )
            ]

            .groupby(
                [
                    "Variable",
                    "Third"
                ]
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


        st.subheader(
            "Change from first to last third"
        )


        comparison_rows = []


        for variable in variables:

            first_values = results.loc[
                (
                    (results["Variable"] == variable)
                    &
                    (results["Third"] == "First third")
                ),
                "Coupling"
            ].dropna()


            last_values = results.loc[
                (
                    (results["Variable"] == variable)
                    &
                    (results["Third"] == "Last third")
                ),
                "Coupling"
            ].dropna()


            if (
                len(first_values) > 0
                and
                len(last_values) > 0
            ):


                first_mean = (
                    first_values.mean()
                )


                last_mean = (
                    last_values.mean()
                )


                difference = (
                    last_mean
                    - first_mean
                )


                comparison_rows.append({

                    "Variable":
                        variable,

                    "First-third mean":
                        first_mean,

                    "Last-third mean":
                        last_mean,

                    "Change (last - first)":
                        difference

                })


        comparison_table = pd.DataFrame(
            comparison_rows
        )


        st.dataframe(
            comparison_table.round(3),
            use_container_width=True
        )


        # -------------------------------------------------
        # Positive and negative coupling
        # -------------------------------------------------

        st.subheader(
            "Positive and negative coupling"
        )


        distribution_summary = []


        for variable in variables:

            for third in [
                "First third",
                "Last third"
            ]:


                values = results.loc[
                    (
                        (results["Variable"] == variable)
                        &
                        (results["Third"] == third)
                    ),
                    "Coupling"
                ].dropna()


                if len(values) > 0:


                    positive = (
                        np.sum(
                            values > 0
                        )
                        /
                        len(values)
                        *
                        100
                    )


                    negative = (
                        np.sum(
                            values < 0
                        )
                        /
                        len(values)
                        *
                        100
                    )


                    distribution_summary.append({

                        "Variable":
                            variable,

                        "Third":
                            third,

                        "Positive coupling (%)":
                            positive,

                        "Negative coupling (%)":
                            negative,

                        "Number of windows":
                            len(values)

                    })


        distribution_table = pd.DataFrame(
            distribution_summary
        )


        st.dataframe(
            distribution_table.round(1),
            use_container_width=True
        )


    # =====================================================
    # TAB 3 — DISTRIBUTIONS
    # =====================================================

    with tab3:

        st.subheader(
            "Coupling distributions"
        )


        st.caption(
            "Distribution of correlation coefficients across "
            f"the {window_seconds}-second windows."
        )


        for variable in variables:

            variable_results = results[
                results["Variable"]
                == variable
            ]


            values = variable_results[
                "Coupling"
            ].dropna()


            fig, ax = plt.subplots(
                figsize=(8, 4)
            )


            bins = np.arange(
                -1,
                1.05,
                0.05
            )


            ax.hist(
                values,
                bins=bins,
                edgecolor="black",
                alpha=0.7
            )


            ax.axvline(
                0,
                linestyle="--",
                color="black",
                alpha=0.5
            )


            ax.set_xlabel(
                "Pearson correlation"
            )


            ax.set_ylabel(
                "Number of windows"
            )


            ax.set_title(
                f"HR–{variable} coupling distribution"
            )


            ax.set_xlim(
                -1,
                1
            )


            ax.grid(
                alpha=0.2
            )


            st.pyplot(
                fig
            )


            plt.close(
                fig
            )


    # =====================================================
    # TAB 4 — DOWNLOAD
    # =====================================================

    with tab4:

        st.subheader(
            "Download your results"
        )


        st.write(
            "Download the analysis results as CSV files."
        )


        # -------------------------------------------------
        # Window results
        # -------------------------------------------------

        csv_data = (
            results
            .to_csv(
                index=False
            )
            .encode(
                "utf-8"
            )
        )


        st.download_button(

            label=
            "⬇ Download window-by-window results",

            data=
            csv_data,

            file_name=
            "squat_coupling_window_results.csv",

            mime=
            "text/csv",

            use_container_width=True

        )


        # -------------------------------------------------
        # Summary
        # -------------------------------------------------

        summary_csv = (
            summary
            .to_csv(
                index=False
            )
            .encode(
                "utf-8"
            )
        )


        st.download_button(

            label=
            "⬇ Download first-vs-last summary",

            data=
            summary_csv,

            file_name=
            "squat_coupling_summary.csv",

            mime=
            "text/csv",

            use_container_width=True

        )


        # -------------------------------------------------
        # Positive / negative
        # -------------------------------------------------

        distribution_csv = (
            distribution_table
            .to_csv(
                index=False
            )
            .encode(
                "utf-8"
            )
        )


        st.download_button(

            label=
            "⬇ Download positive/negative results",

            data=
            distribution_csv,

            file_name=
            "squat_positive_negative_coupling.csv",

            mime=
            "text/csv",

            use_container_width=True

        )


        # -------------------------------------------------
        # 1 Hz processed data
        # -------------------------------------------------

        processed_csv = (
            signals_1hz
            .to_csv(
                index=False
            )
            .encode(
                "utf-8"
            )
        )


        st.download_button(

            label=
            "⬇ Download 1 Hz processed data",

            data=
            processed_csv,

            file_name=
            "squat_coupling_1hz_processed_data.csv",

            mime=
            "text/csv",

            use_container_width=True

        )


    # =====================================================
    # INTERPRETATION NOTE
    # =====================================================

    st.divider()


    st.info(
        f"Each coupling coefficient is calculated from up to "
        f"{window_seconds} one-second observations within a "
        f"{window_seconds}-second window. Missing observations "
        "are excluded only from the specific HR–signal pair being "
        "correlated. Windows overlap by "
        f"{window_seconds - step_seconds} seconds, so neighboring "
        "coupling coefficients are not independent observations."
    )
