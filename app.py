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

    /* Main page */
    .main {
        padding-top: 1rem;
    }

    /* Header */
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

    /* Section cards */
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

    /* Step badges */
    .step-badge {
        display: inline-block;
        padding: 0.25rem 0.65rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }

    /* Metrics */
    [data-testid="stMetric"] {
        background-color: #fafafa;
        border: 1px solid #e5e5e5;
        padding: 0.8rem;
        border-radius: 10px;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        border-right: 1px solid #e5e5e5;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
    }

    /* Download buttons */
    .stDownloadButton > button {
        border-radius: 8px;
    }

    /* Tables */
    [data-testid="stDataFrame"] {
        border-radius: 8px;
    }

    /* Divider */
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

    st.write("**Window length**")
    st.write("6 seconds")

    st.write("**Window overlap**")
    st.write("3 seconds")

    st.write("**Sampling interval**")
    st.write("1 second")

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
        "The analysis adapts the short-timescale windowing approach "
        "described by Garcia-Retortillo et al."
    )


# =========================================================
# INTRODUCTION
# =========================================================

with st.expander("About this analysis", expanded=False):

    st.write(
        "This program analyzes synchronized 1-second physiological "
        "data using short-timescale coupling analysis. It uses "
        "6-second windows with 3-second overlap, adapting the "
        "time-window approach described by Garcia-Retortillo et al."
    )

    st.info(
        "The original study examined heart rate and EMG. "
        "This program adapts the approach to examine HR–RR, "
        "HR–SmO₂, and HR–THb coupling."
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
            1-second physiological data.
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


# File information

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


for column in analysis_data.columns:

    analysis_data[column] = pd.to_numeric(
        analysis_data[column],
        errors="coerce"
    )


total_rows = len(
    analysis_data
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
            The program checks for missing values and confirms
            that the data are approximately 1 second apart.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


missing_counts = (
    analysis_data.isna().sum()
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
        "Expected sampling",
        "1 s"
    )


# ---------------------------------------------------------
# Missing values
# ---------------------------------------------------------

if total_missing > 0:

    st.error(
        "⚠ Missing or non-numeric values were detected."
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

    st.info(
        "Rows are not automatically deleted because removing "
        "rows could disrupt the time alignment between signals."
    )

    st.stop()

else:

    st.success(
        "✓ No missing or non-numeric values detected."
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

    irregular_intervals = np.sum(
        ~np.isclose(
            time_differences,
            1.0,
            atol=0.01
        )
    )

else:

    median_difference = np.nan
    irregular_intervals = 0


col1, col2 = st.columns(2)


with col1:

    if not np.isnan(
        median_difference
    ):

        st.metric(
            "Median time interval",
            f"{median_difference:.3f} s"
        )


with col2:

    st.metric(
        "Irregular intervals",
        int(irregular_intervals)
    )


if (
    not np.isnan(median_difference)
    and
    irregular_intervals == 0
):

    st.success(
        "✓ Time alignment check passed — all intervals are "
        "approximately 1 second."
    )

elif irregular_intervals > 0:

    st.warning(
        f"⚠ {irregular_intervals} time intervals are not "
        "approximately 1 second. Check the synchronization "
        "before continuing."
    )

else:

    st.warning(
        "Time spacing could not be checked."
    )


# ---------------------------------------------------------
# Minimum data
# ---------------------------------------------------------

if total_rows < 6:

    st.error(
        "At least 6 seconds of data are required."
    )

    st.stop()


# =========================================================
# HELPER FUNCTION
# =========================================================

def z_score(values):

    values = np.asarray(
        values,
        dtype=float
    )

    std = np.std(
        values,
        ddof=1
    )

    if std == 0 or np.isnan(std):

        return np.full(
            len(values),
            np.nan
        )

    return (
        values - np.mean(values)
    ) / std


# =========================================================
# COUPLING FUNCTION
# =========================================================

def calculate_coupling(
    df,
    variable
):

    results = []

    window_length = 6
    step = 3

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
        ]


        hr_values = z_score(
            window["HR"].values
        )

        variable_values = z_score(
            window[variable].values
        )


        if (
            np.any(
                np.isnan(hr_values)
            )
            or
            np.any(
                np.isnan(variable_values)
            )
        ):

            correlation = np.nan

        else:

            correlation = np.corrcoef(
                hr_values,
                variable_values
            )[0, 1]


        results.append({

            "Variable":
                variable,

            "Window start (s)":
                window["Time"].iloc[0],

            "Window end (s)":
                window["Time"].iloc[-1],

            "Coupling":
                correlation
        })


    return pd.DataFrame(
        results
    )


# =========================================================
# STEP 4 — RUN ANALYSIS
# =========================================================

st.divider()

st.markdown(
    """
    <div class="section-card">
        <div class="step-badge">STEP 4</div>
        <div class="section-title">Run coupling analysis</div>
        <div class="section-description">
            Calculate short-timescale Pearson correlations
            between HR and RR, SmO₂, and THb.
        </div>
    </div>
    """,
    unsafe_allow_html=True
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
                analysis_data,
                variable
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


    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(
            "Window length",
            "6 s"
        )


    with col2:

        st.metric(
            "Overlap",
            "3 s"
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
            "calculated within a 6-second window."
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
            "the 6-second windows."
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


    # =====================================================
    # INTERPRETATION NOTE
    # =====================================================

    st.divider()

    st.info(
        "Each coupling coefficient is calculated from six "
        "1-second observations within a 6-second window. "
        "Because windows overlap by 3 seconds, neighboring "
        "coupling coefficients are not independent observations."
    )
