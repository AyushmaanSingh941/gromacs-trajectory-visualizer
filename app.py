# =============================================================================
# GROMACS Trajectory Visualizer
# app.py — A Streamlit dashboard for parsing and visualizing GROMACS .xvg files
#
# Author:  Built for you by Claude (Anthropic)
# Purpose: Upload a GROMACS output file (.xvg), parse the numerical data,
#          and explore it interactively with a Plotly chart.
# =============================================================================
 
# --- 1. IMPORTS ---------------------------------------------------------------
# We bring in every library this app needs. Each one has a specific job.
 
import streamlit as st   # The framework that turns Python into a web app
import pandas as pd      # Handles our data as a structured table (DataFrame)
import numpy as np       # Fast numerical operations on arrays
import plotly.express as px  # Creates beautiful, interactive charts
import io                # Lets us treat an uploaded file like a file on disk
 
 
# --- 2. PAGE CONFIGURATION ----------------------------------------------------
# This MUST be the first Streamlit command in the script.
# It sets the browser tab title, icon, and how wide the app appears.
 
st.set_page_config(
    page_title="GROMACS Trajectory Visualizer",
    page_icon="🧬",
    layout="wide",          # Use the full browser width — better for charts
    initial_sidebar_state="expanded"  # Sidebar is open by default
)
 
 
# --- 3. CUSTOM CSS / THEME INJECTION ------------------------------------------
# Streamlit lets us inject raw CSS to override its default styles.
# We are going for a "deep space lab" aesthetic:
#   - Near-black background (#0D1117)
#   - Cyan/teal accent (#00C8C8) — inspired by molecular visualization software
#   - Mono font for data, sans-serif for UI text
# We use st.markdown() with unsafe_allow_html=True to inject a <style> block.
 
st.markdown("""
<style>
    /* ── Global background & font ─────────────────────────── */
    .stApp {
        background-color: #0D1117;
        color: #C9D1D9;
        font-family: 'Inter', 'Segoe UI', sans-serif;
    }
 
    /* ── Sidebar ──────────────────────────────────────────── */
    [data-testid="stSidebar"] {
        background-color: #161B22;
        border-right: 1px solid #21262D;
    }
    [data-testid="stSidebar"] .stMarkdown p,
    [data-testid="stSidebar"] label {
        color: #8B949E;
        font-size: 0.82rem;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }
 
    /* ── Main header / hero text ──────────────────────────── */
    .hero-title {
        font-size: 2.1rem;
        font-weight: 700;
        color: #E6EDF3;
        letter-spacing: -0.02em;
        line-height: 1.15;
        margin-bottom: 0.15rem;
    }
    .hero-subtitle {
        font-size: 1rem;
        color: #8B949E;
        margin-bottom: 1.8rem;
    }
    .accent {
        color: #00C8C8;   /* Our signature teal accent */
    }
 
    /* ── Metric cards (the row of stat boxes) ─────────────── */
    .metric-card {
        background: #161B22;
        border: 1px solid #21262D;
        border-radius: 8px;
        padding: 1rem 1.2rem;
        text-align: center;
    }
    .metric-value {
        font-size: 1.5rem;
        font-weight: 600;
        color: #00C8C8;
        font-family: 'Roboto Mono', 'Courier New', monospace;
    }
    .metric-label {
        font-size: 0.75rem;
        color: #8B949E;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        margin-top: 0.2rem;
    }
 
    /* ── Section divider ──────────────────────────────────── */
    .section-header {
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: #8B949E;
        border-bottom: 1px solid #21262D;
        padding-bottom: 0.4rem;
        margin: 1.2rem 0 0.8rem;
    }
 
    /* ── Streamlit widget overrides ───────────────────────── */
    /* File uploader box */
    [data-testid="stFileUploadDropzone"] {
        background-color: #0D1117 !important;
        border: 1px dashed #30363D !important;
        border-radius: 8px !important;
    }
    /* DataFrame / table */
    [data-testid="stDataFrame"] {
        border: 1px solid #21262D;
        border-radius: 8px;
        overflow: hidden;
    }
    /* Remove default Streamlit top padding */
    .block-container {
        padding-top: 2rem;
    }
    /* Selectbox, number input */
    .stSelectbox div[data-baseweb="select"] > div,
    .stNumberInput input {
        background-color: #161B22 !important;
        border-color: #30363D !important;
        color: #C9D1D9 !important;
    }
 
    /* ── Info / warning boxes ─────────────────────────────── */
    .stAlert {
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)
 
 
# --- 4. PARSING FUNCTION ------------------------------------------------------
# We define a function that takes the raw bytes of the uploaded file,
# skips all GROMACS header lines (those starting with '@' or '#'),
# and returns a clean Pandas DataFrame.
#
# Why a function? It keeps the logic reusable and easy to test.
# Why @st.cache_data? Streamlit re-runs the whole script on every interaction.
# This decorator tells Streamlit: "if the file hasn't changed, return the
# previously computed result instead of re-parsing." This makes the app fast.
 
@st.cache_data(show_spinner=False)
def parse_gromacs_xvg(file_bytes: bytes) -> tuple[pd.DataFrame, list[str], list[str]]:
    """
    Parse a GROMACS .xvg file from raw bytes.
 
    Parameters
    ----------
    file_bytes : bytes
        The raw content of the uploaded file.
 
    Returns
    -------
    df : pd.DataFrame
        A DataFrame where column 0 is typically time (ps) and subsequent
        columns are the measured quantities.
    metadata_lines : list[str]
        All header lines starting with '#' (comments).
    axis_labels : list[str]
        Any '@'-prefixed lines that describe axis labels / title.
    """
 
    # Decode the raw bytes into a plain string (UTF-8 encoding).
    # 'errors="replace"' prevents crashes if the file has unusual characters.
    raw_text = file_bytes.decode("utf-8", errors="replace")
 
    # Split the full text into individual lines
    all_lines = raw_text.splitlines()
 
    # ── Separate header from data ──────────────────────────────────────────────
    metadata_lines = []   # Lines starting with '#'
    axis_labels    = []   # Lines starting with '@'
    data_lines     = []   # Lines with actual numbers
 
    for line in all_lines:
        stripped = line.strip()
 
        if stripped.startswith("#"):
            metadata_lines.append(stripped)
 
        elif stripped.startswith("@"):
            axis_labels.append(stripped)
 
        elif stripped:   # Non-empty line that isn't a header — treat as data
            data_lines.append(stripped)
 
    # If there are no data lines, return an empty DataFrame and let the UI
    # display a helpful error message.
    if not data_lines:
        return pd.DataFrame(), metadata_lines, axis_labels
 
    # ── Vectorized parsing with NumPy ──────────────────────────────────────────
    # Instead of a slow Python loop that builds a list row by row,
    # we join all data lines into one big string and let numpy.loadtxt
    # do the heavy lifting in compiled C code. Much faster for large files.
    data_block = "\n".join(data_lines)
    data_io    = io.StringIO(data_block)   # Wrap in a file-like object for numpy
 
    try:
        # np.loadtxt reads whitespace-separated numbers into a 2-D array.
        # dtype=float64 ensures precision for scientific data.
        array = np.loadtxt(data_io, dtype=np.float64)
    except ValueError:
        # If a line has non-numeric content we missed, fall back to pandas
        # read_csv which is more forgiving. sep='\s+' handles any whitespace.
        data_io.seek(0)
        array = pd.read_csv(
            data_io,
            sep=r"\s+",
            header=None,
            comment=None,
            on_bad_lines="skip"
        ).to_numpy(dtype=np.float64)
 
    # Handle the case where the file has only a single row of data
    if array.ndim == 1:
        array = array.reshape(1, -1)
 
    # ── Build column names ─────────────────────────────────────────────────────
    # Try to extract axis labels from the '@'-prefixed header lines.
    # GROMACS typically writes:  @ xaxis  label "Time (ps)"
    #                             @ yaxis  label "Potential Energy (kJ/mol)"
    #                             @ s0 legend "Total"
    #                             @ s1 legend "LJ-14"
 
    n_cols = array.shape[1]
    col_names = []
 
    # Extract any legend names (@s0 legend "...", @s1 legend "...", etc.)
    legend_names = {}
    for lbl in axis_labels:
        if "legend" in lbl.lower():
            # Example: @ s0 legend "Potential"
            parts = lbl.split('"')
            if len(parts) >= 2:
                legend_text = parts[1]
                # Extract the series index from the token before "legend"
                tokens = lbl.split()
                for i, tok in enumerate(tokens):
                    if tok.lower() == "legend" and i > 0:
                        series_token = tokens[i - 1]   # e.g. "s0", "s1"
                        if series_token.startswith("s") and series_token[1:].isdigit():
                            legend_names[int(series_token[1:])] = legend_text
                        break
 
    # First column is almost always time in GROMACS output
    col_names.append("Time")
 
    # Fill remaining columns using legend names or generic fallbacks
    for i in range(1, n_cols):
        series_idx = i - 1
        col_names.append(legend_names.get(series_idx, f"Value_{i}"))
 
    # If somehow we have fewer names than columns (shouldn't happen), pad them
    while len(col_names) < n_cols:
        col_names.append(f"Value_{len(col_names)}")
 
    # Build the final DataFrame
    df = pd.DataFrame(array, columns=col_names[:n_cols])
 
    return df, metadata_lines, axis_labels
 
 
# --- 5. HELPER: Extract human-readable axis labels from header ----------------
 
def extract_axis_info(axis_labels: list[str]) -> dict:
    """
    Scan the '@'-prefixed header lines for the x-axis and y-axis labels,
    plus the chart title. Returns a dict with keys 'title', 'xaxis', 'yaxis'.
    """
    info = {"title": "Trajectory Data", "xaxis": "Time (ps)", "yaxis": "Value"}
 
    for line in axis_labels:
        lower = line.lower()
        parts = line.split('"')
        if len(parts) >= 2:
            label_text = parts[1]
            if "title" in lower:
                info["title"] = label_text
            elif "xaxis" in lower and "label" in lower:
                info["xaxis"] = label_text
            elif "yaxis" in lower and "label" in lower:
                info["yaxis"] = label_text
 
    return info
 
 
# =============================================================================
# --- 6. SIDEBAR ---------------------------------------------------------------
# Everything inside the `with st.sidebar:` block appears in the left panel.
# =============================================================================
 
with st.sidebar:
 
    # ── Logo / branding ────────────────────────────────────────────────────────
    st.markdown("""
    <div style="padding: 0.5rem 0 1.5rem;">
        <span style="font-size:1.5rem;">🧬</span>
        <span style="font-size:1rem; font-weight:700; color:#E6EDF3;
                     letter-spacing:-0.01em; margin-left:0.5rem;">
            GROMACS<span style="color:#00C8C8;">Viz</span>
        </span>
    </div>
    """, unsafe_allow_html=True)

# Native Session State Viewer Tracker
    if 'visitor_checked' not in st.session_state:
        st.session_state['visitor_checked'] = True
        try:
            # We initialize a localized metric card framework
            st.markdown("""
                <div style="background: #161B22; padding: 0.6rem; border: 1px solid #21262D; border-radius: 6px; text-align: center; margin: 1rem 0;">
                    <div style="font-size: 0.7rem; color: #8B949E; text-transform: uppercase; letter-spacing: 0.05em;">Visualizer Node</div>
                    <div style="font-size: 1.1rem; font-weight: 600; color: #00C8C8; font-family: monospace;">ACTIVE ● ONLINE</div>
                </div>
            """, unsafe_allow_html=True)
        except Exception:
            pass
    else:
        st.markdown("""
            <div style="background: #161B22; padding: 0.6rem; border: 1px solid #21262D; border-radius: 6px; text-align: center; margin: 1rem 0;">
                <div style="font-size: 0.7rem; color: #8B949E; text-transform: uppercase; letter-spacing: 0.05em;">Visualizer Node</div>
                <div style="font-size: 1.1rem; font-weight: 600; color: #00C8C8; font-family: monospace;">ACTIVE ● ONLINE</div>
            </div>
        """, unsafe_allow_html=True)
 
 
    # ── File uploader ──────────────────────────────────────────────────────────
    st.markdown('<div class="section-header">Input File</div>', unsafe_allow_html=True)
 
    uploaded_file = st.file_uploader(
        label="Upload a GROMACS .xvg file",
        type=["xvg", "txt"],    # Accept .xvg (native) or .txt (common rename)
        help="GROMACS output files typically end in .xvg. "
             "Text files with the same format are also supported."
    )
 
    # ── Chart options (only show after a file is loaded) ──────────────────────
    st.markdown('<div class="section-header">Chart Options</div>',
                unsafe_allow_html=True)
 
    chart_type = st.selectbox(
        "Chart type",
        options=["Line", "Scatter", "Area"],
        index=0,
        help="Line is best for continuous trajectories. "
             "Scatter helps spot individual frames."
    )
 
    show_markers = st.checkbox(
        "Show data point markers",
        value=False,
        help="Adds a dot at every data point. "
             "Useful for small datasets; can be slow for large ones."
    )
 
    # Downsampling slider — helps render large trajectories quickly
    downsample = st.slider(
        "Display every Nth frame",
        min_value=1,
        max_value=100,
        value=1,
        step=1,
        help="Set to 1 to show all frames. Increase to speed up rendering "
             "for trajectories with tens of thousands of steps."
    )
 
    # ── About section ─────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("""
    <p style="font-size:0.75rem; color:#484F58; line-height:1.6;">
        Parses GROMACS <code style="color:#8B949E;">.xvg</code> files,
        skipping <code style="color:#8B949E;">@</code> and
        <code style="color:#8B949E;">#</code> header lines.<br><br>
        Built with Streamlit · Plotly · NumPy
    </p>
    """, unsafe_allow_html=True)
 
 
# =============================================================================
# --- 7. MAIN CONTENT AREA -----------------------------------------------------
# =============================================================================
 
# ── Hero header ───────────────────────────────────────────────────────────────
st.markdown("""
<p class="hero-title">
    GROMACS Trajectory <span class="accent">Visualizer</span>
</p>
<p class="hero-subtitle">
    Upload an <code style="color:#8B949E; font-size:0.9rem;">.xvg</code> output
    file to parse, inspect, and interactively explore your simulation data.
</p>
""", unsafe_allow_html=True)
 
 
# ── No file uploaded yet — show a welcoming empty state ───────────────────────
if uploaded_file is None:
 
    # We use columns to center the empty-state card
    _, center_col, _ = st.columns([1, 2, 1])
 
    with center_col:
        st.markdown("""
        <div style="
            background:#161B22;
            border:1px dashed #30363D;
            border-radius:12px;
            padding:3rem 2rem;
            text-align:center;
            margin-top:2rem;
        ">
            <div style="font-size:3rem; margin-bottom:1rem;">📂</div>
            <p style="color:#E6EDF3; font-size:1rem; font-weight:600;
                      margin-bottom:0.4rem;">
                No file loaded yet
            </p>
            <p style="color:#8B949E; font-size:0.85rem; line-height:1.6;">
                Use the <strong style="color:#C9D1D9;">sidebar on the left</strong>
                to upload a GROMACS <code>.xvg</code> file.<br>
                Common examples: <code>energy.xvg</code>, <code>rmsd.xvg</code>,
                <code>gyrate.xvg</code>
            </p>
        </div>
        """, unsafe_allow_html=True)
 
    # Show a sample of what a valid file looks like so the user understands
    # the expected format — helpful for a first-time user.
    st.markdown("")
    with st.expander("📋  What does a valid .xvg file look like?", expanded=False):
        st.code("""
# GROMACS Energy output — lines starting with '#' are comments
# Comments describe the simulation settings or software version
# They are skipped during parsing.
 
@ title "Potential Energy"
@ xaxis  label "Time (ps)"
@ yaxis  label "Potential Energy (kJ/mol)"
@ TYPE xy
# Lines starting with '@' are Grace/xmgrace plot directives — also skipped.
 
#   Time         Potential
    0.00000      -412345.678
    0.01000      -412300.123
    0.02000      -412280.456
    0.03000      -412290.789
    0.04000      -412310.012
        """, language="text")
 
    # Stop the script here — no file means no data to show below this point.
    st.stop()
 
 
# =============================================================================
# --- 8. FILE IS UPLOADED — PARSE AND DISPLAY ----------------------------------
# =============================================================================
 
# Read the uploaded file into bytes. We do this once and pass bytes to our
# cached function so Streamlit can hash the content and cache effectively.
file_bytes = uploaded_file.read()
 
# Show a spinner while parsing (for large files, this may take a moment)
with st.spinner("Parsing file…"):
    df, metadata_lines, axis_labels = parse_gromacs_xvg(file_bytes)
 
 
# ── Handle parse failure ───────────────────────────────────────────────────────
if df.empty:
    st.error(
        "⚠️  Could not extract numerical data from this file.  \n"
        "Make sure the file contains whitespace-separated numbers after the "
        "`@` / `#` header lines.",
        icon="⚠️"
    )
    st.stop()
 
 
# ── Apply downsampling ─────────────────────────────────────────────────────────
# If the user moved the "Display every Nth frame" slider, we take every Nth row.
# This reduces the number of points plotted without changing the DataFrame itself.
if downsample > 1:
    df_display = df.iloc[::downsample].reset_index(drop=True)
    downsample_note = f"Showing every {downsample}th frame ({len(df_display):,} of {len(df):,} total)"
else:
    df_display = df
    downsample_note = f"Showing all {len(df):,} frames"
 
 
# ── Determine column roles ─────────────────────────────────────────────────────
# The first column is always our X axis (time).
# All remaining columns are Y-axis candidates.
x_col     = df.columns[0]           # "Time" (or whatever the first column is)
y_cols    = list(df.columns[1:])    # Everything else is a measurement
 
axis_info = extract_axis_info(axis_labels)
 
 
# ── Metric summary cards ───────────────────────────────────────────────────────
# We show a row of stat cards at the top so key numbers are visible at a glance.
 
# Determine which Y column to summarise (default: first Y column)
primary_y = y_cols[0] if y_cols else x_col
 
stat_cols = st.columns(5)
 
with stat_cols[0]:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{len(df):,}</div>
        <div class="metric-label">Total Frames</div>
    </div>""", unsafe_allow_html=True)
 
with stat_cols[1]:
    t_start = df[x_col].iloc[0]
    t_end   = df[x_col].iloc[-1]
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{t_start:.3g} – {t_end:.3g}</div>
        <div class="metric-label">Time Range</div>
    </div>""", unsafe_allow_html=True)
 
with stat_cols[2]:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{df[primary_y].mean():.4g}</div>
        <div class="metric-label">Mean {primary_y}</div>
    </div>""", unsafe_allow_html=True)
 
with stat_cols[3]:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{df[primary_y].min():.4g}</div>
        <div class="metric-label">Min {primary_y}</div>
    </div>""", unsafe_allow_html=True)
 
with stat_cols[4]:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{df[primary_y].max():.4g}</div>
        <div class="metric-label">Max {primary_y}</div>
    </div>""", unsafe_allow_html=True)
 
 
# ── Column selector (only shown when there are multiple Y columns) ────────────
st.markdown('<div class="section-header">Visualization</div>',
            unsafe_allow_html=True)
 
if len(y_cols) > 1:
    selected_y_cols = st.multiselect(
        "Select columns to plot",
        options=y_cols,
        default=y_cols,        # Pre-select all columns
        help="Choose which data series to display on the chart."
    )
    if not selected_y_cols:
        st.warning("Please select at least one column to plot.")
        st.stop()
else:
    selected_y_cols = y_cols   # Only one column — just use it automatically
 
 
# ── Build the Plotly chart ─────────────────────────────────────────────────────
# We choose the Plotly function based on the sidebar chart_type selector.
 
# A clean color sequence that stands out on our dark background
COLORS = [
    "#00C8C8",  # Teal (primary — our accent color)
    "#FF7B54",  # Warm orange
    "#9B72CF",  # Soft purple
    "#5CE65C",  # Lime green
    "#F0C040",  # Amber
    "#54AAFF",  # Sky blue
]
 
mode = "lines+markers" if show_markers else "lines"
 
if chart_type == "Line":
    fig = px.line(
        df_display,
        x=x_col,
        y=selected_y_cols,
        title=axis_info["title"],
        labels={x_col: axis_info["xaxis"]},
        color_discrete_sequence=COLORS
    )
    # Override mode to include markers if checkbox is ticked
    if show_markers:
        fig.update_traces(mode="lines+markers", marker=dict(size=3))
 
elif chart_type == "Scatter":
    fig = px.scatter(
        df_display,
        x=x_col,
        y=selected_y_cols,
        title=axis_info["title"],
        labels={x_col: axis_info["xaxis"]},
        color_discrete_sequence=COLORS
    )
 
else:  # Area
    fig = px.area(
        df_display,
        x=x_col,
        y=selected_y_cols,
        title=axis_info["title"],
        labels={x_col: axis_info["xaxis"]},
        color_discrete_sequence=COLORS
    )
 
# ── Style the Plotly chart to match our dark theme ────────────────────────────
fig.update_layout(
    # Dark paper and plot background
    paper_bgcolor="#0D1117",
    plot_bgcolor="#0D1117",
 
    # Title styling
    title=dict(
        font=dict(family="Inter, Segoe UI, sans-serif", size=16, color="#E6EDF3"),
        x=0,        # Left-align the title
        xanchor="left"
    ),
 
    # Axis styling
    xaxis=dict(
        title=dict(text=axis_info["xaxis"],
                   font=dict(color="#8B949E", size=12)),
        tickfont=dict(color="#8B949E", size=10,
                      family="Roboto Mono, Courier New, monospace"),
        gridcolor="#21262D",
        linecolor="#30363D",
        zerolinecolor="#30363D"
    ),
    yaxis=dict(
        title=dict(text=axis_info["yaxis"],
                   font=dict(color="#8B949E", size=12)),
        tickfont=dict(color="#8B949E", size=10,
                      family="Roboto Mono, Courier New, monospace"),
        gridcolor="#21262D",
        linecolor="#30363D",
        zerolinecolor="#30363D"
    ),
 
    # Legend
    legend=dict(
        font=dict(color="#C9D1D9", size=11),
        bgcolor="#161B22",
        bordercolor="#21262D",
        borderwidth=1
    ),
 
    # Hover tooltip
    hoverlabel=dict(
        bgcolor="#161B22",
        bordercolor="#30363D",
        font=dict(color="#E6EDF3", size=12,
                  family="Roboto Mono, Courier New, monospace")
    ),
 
    # Allow the chart to stretch with the browser window
    autosize=True,
    margin=dict(l=60, r=20, t=60, b=60),
 
    # Range selector buttons for the X axis (zoom presets)
    xaxis_rangeslider_visible=False
)
 
# Render the chart. use_container_width=True makes it fill the column.
st.plotly_chart(fig, use_container_width=True)
 
# Small note about downsampling below the chart
st.caption(f"ℹ️  {downsample_note}")
 
 
# ── Raw data table ─────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">Raw Data Table</div>',
            unsafe_allow_html=True)
 
# Two columns: the table on the left, stats on the right
table_col, stats_col = st.columns([3, 1])
 
with table_col:
    st.dataframe(
        df_display.style.format("{:.6g}"),   # Compact scientific notation
        use_container_width=True,
        height=320
    )
 
with stats_col:
    st.markdown("**Descriptive Stats**")
    # .describe() gives count, mean, std, min, quartiles, max for each column
    st.dataframe(
        df[selected_y_cols].describe().style.format("{:.4g}"),
        use_container_width=True,
        height=320
    )
 
 
# ── File metadata expander ────────────────────────────────────────────────────
# Show the raw header lines from the file so power users can verify what was
# parsed. Collapsed by default so it doesn't clutter the page.
 
with st.expander("📄  File Metadata (header lines from uploaded file)", expanded=False):
 
    if metadata_lines or axis_labels:
        all_header = metadata_lines + axis_labels
        st.code("\n".join(all_header), language="text")
    else:
        st.info("No header lines found in this file.")
 
    st.markdown(f"""
    <p style="font-size:0.8rem; color:#8B949E; margin-top:0.8rem;">
        📁 <strong style="color:#C9D1D9;">{uploaded_file.name}</strong>
        &nbsp;·&nbsp; {len(file_bytes)/1024:.1f} KB
        &nbsp;·&nbsp; {len(df):,} data rows
        &nbsp;·&nbsp; {len(df.columns)} columns
    </p>
    """, unsafe_allow_html=True)
 
 
# ── Download parsed CSV ────────────────────────────────────────────────────────
# Let the user export the cleaned DataFrame as a CSV file.
 
st.markdown('<div class="section-header">Export</div>', unsafe_allow_html=True)
 
csv_buffer = df.to_csv(index=False).encode("utf-8")
 
st.download_button(
    label="⬇  Download parsed data as CSV",
    data=csv_buffer,
    file_name=uploaded_file.name.replace(".xvg", "_parsed.csv").replace(".txt", "_parsed.csv"),
    mime="text/csv",
    help="Downloads the full (un-downsampled) parsed DataFrame as a CSV file."
)
 
