# gromacs-trajectory-visualizer

## Overview

**GROMACS Trajectory Visualizer** is an interactive Streamlit dashboard for parsing and analyzing GROMACS molecular dynamics simulation output files. Upload a `.xvg` trajectory file, and the application automatically parses the data, displays it with interactive Plotly charts, and provides statistical summaries for quick analysis.

The tool bridges the gap between raw GROMACS output and visual analysis, reducing the learning curve for scientists new to trajectory visualization while providing experienced researchers with rapid data exploration capabilities.

## System Requirements

- **Python**: 3.8 or higher
- **Operating System**: Windows, macOS, or Linux
- **RAM**: Minimum 512 MB (recommended 2+ GB for large trajectories with >100k frames)
- **Disk Space**: ~500 MB for dependencies
- **Browser**: Modern web browser (Chrome, Firefox, Safari, Edge)

## Quick Start Guide

Follow these steps to get the visualizer running on your machine:

### 1. Clone the Repository
```bash
git clone https://github.com/AyushmaanSingh941/gromacs-trajectory-visualizer.git
cd gromacs-trajectory-visualizer
```

### 2. Create a Virtual Environment (Recommended)
```bash
python -m venv venv
source venv/bin/activate        # On macOS/Linux
# or
venv\Scripts\activate           # On Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
streamlit run app.py
```

Your browser will automatically open to `http://localhost:8501` displaying the dashboard.

### 5. Upload and Analyze
- Click **"Upload a GROMACS .xvg file"** in the sidebar
- Select your `.xvg` or `.txt` trajectory file
- Use the **Chart Options** to customize visualization (chart type, markers, downsampling)
- View statistics, raw data table, and export your parsed results as CSV

## Features

- ✨ **Instant Visualization**: Interactive Plotly charts with optimized dark theme for scientific data
- 📊 **Multi-Series Support**: Plot multiple trajectories or energy components side-by-side
- 🎛️ **Real-Time Controls**: Toggle markers, switch chart types, downsample data for fast rendering
- 📋 **Data Export**: Download parsed data as CSV for external analysis
- 🧬 **GROMACS Native**: Automatically parses `@` and `#` header lines; supports standard `.xvg` format
- ⚡ **High Performance**: Vectorized parsing with NumPy for handling trajectories with tens of thousands of frames

## Demo

Below is an example of the dashboard analyzing a GROMACS trajectory:

![GROMACS Trajectory Visualizer Dashboard](docs/dashboard-demo.png)

### Dashboard Features:
- **Metric Cards** (top): Frame count, time range, mean/min/max values
- **Interactive Plotly Chart** (center): Multi-series trajectory visualization with hover tooltips
- **Raw Data Table** (bottom left): Full dataset with scientific notation
- **Descriptive Statistics** (bottom right): Statistical summary for quick insights
- **Sidebar Controls**: File upload, chart type, markers, and downsampling options

See [docs/dashboard-demo.md](docs/dashboard-demo.md) for detailed feature descriptions.

## Example Workflow

```bash
# With GROMACS installed, generate a sample energy file
gmx energy -f ener.edr -o energy.xvg

# Then visualize it
streamlit run app.py
# Upload energy.xvg → explore trajectories → export results
```

## Supported File Formats

- **`.xvg`** – Native GROMACS output (XMGrace format)
- **`.txt`** – Plain text with equivalent structure

### Expected File Structure
```
# GROMACS comment (starts with #)
@ xaxis label "Time (ps)"
@ yaxis label "Potential Energy (kJ/mol)"
@ s0 legend "Total"

0.00    -412345.678
0.01    -412300.123
0.02    -412280.456
```

## Dependencies

| Package  | Version | Purpose                          |
|----------|---------|----------------------------------|
| streamlit | 1.32.0  | Web app framework                |
| pandas   | 2.2.1   | Data manipulation & analysis     |
| numpy    | 1.26.4  | Numerical computing              |
| plotly   | 5.19.0  | Interactive visualization        |

## Technical Details

### Parsing Strategy
The application uses a robust two-stage parsing approach:
1. **Header filtering**: Skips lines beginning with `#` (comments) and `@` (plot directives)
2. **Vectorized parsing**: Leverages NumPy for efficient numerical data extraction, which is significantly faster than Python loops for large files

### Performance Optimization
For trajectories exceeding 50,000 frames, the downsampling feature (accessible via the "Display every Nth frame" slider) reduces rendering latency without losing statistical accuracy on the full dataset.

### Color Scheme
The interface uses a carefully selected color palette designed for clarity on dark backgrounds and accessibility for colorblind users:
- Teal (#00C8C8) for primary accent and first data series
- Warm orange, purple, green, amber, and blue for additional series

## Troubleshooting

### "Module not found" errors
Ensure you've activated the virtual environment and installed dependencies:
```bash
source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

### Slow rendering with large files
Use the **"Display every Nth frame"** slider in the sidebar to downsample data. Set to 5 or higher for files with >50k frames. The full dataset is still used for statistics calculations.

### File upload fails
Verify your file is a valid `.xvg` or `.txt` with numeric data. Header lines must start with `#` or `@`. Ensure there are no special characters or corrupted lines in the data section.

### Application crashes on startup
Clear the Streamlit cache:
```bash
rm -rf ~/.streamlit/cache
streamlit run app.py --logger.level=debug
```

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Make your changes with clear, descriptive commit messages
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request with a description of your changes

## Citation

If you use this tool in your research, please cite it as:

```
Singh, A. (2026). GROMACS Trajectory Visualizer: An Interactive Dashboard for Molecular Dynamics Analysis. 
Available at: https://github.com/AyushmaanSingh941/gromacs-trajectory-visualizer
```

## Contact & Support

For questions, bug reports, or feature requests, please open a [GitHub Issue](https://github.com/AyushmaanSingh941/gromacs-trajectory-visualizer/issues).

For collaboration inquiries, reach out directly through GitHub.

---

**Built for molecular dynamics researchers and students seeking efficient trajectory analysis and visualization.**
