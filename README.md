# gromacs-trajectory-visualizer

**Interactive Streamlit dashboard for analyzing GROMACS molecular dynamics trajectories**

This tool lets you upload `.xvg` trajectory files from GROMACS simulations and explore them with interactive charts, statistics, and data export.

## Features

- Upload `.xvg` or `.txt` trajectory files
- Interactive Plotly visualization (Line, Scatter, Area charts)
- Adjust chart options: markers, downsampling, column selection
- View frame count, time range, statistics (mean, min, max)
- Export parsed data as CSV
- Dark theme optimized for data visualization

## Quick Start

### 1. Install Python 3.8+

### 2. Clone and setup
```bash
git clone https://github.com/AyushmaanSingh941/gromacs-trajectory-visualizer.git
cd gromacs-trajectory-visualizer
```

### 3. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
# or
venv\Scripts\activate           # Windows
```

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

### 5. Run
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## Usage

1. Click **Upload a GROMACS .xvg file** in the sidebar
2. Select your `.xvg` or `.txt` file
3. Customize visualization:
   - Choose chart type (Line, Scatter, Area)
   - Toggle data point markers
   - Downsample data for faster rendering
   - Select which columns to plot
4. View statistics and download as CSV

## Supported Formats

### `.xvg` (XMGrace format)
Native GROMACS output format. Includes header lines:
- `#` - Comments (skipped)
- `@` - Plot directives with axis labels (skipped)
- Data: Whitespace-separated numeric values

### `.txt` (plain text)
Same structure as `.xvg` but with `.txt` extension

### Example file format
```
# GROMACS trajectory output
@ title "Potential Energy"
@ xaxis label "Time (ps)"
@ yaxis label "Energy (kJ/mol)"
@ s0 legend "Total"

0.00     -412345.678
0.01     -412300.123
0.02     -412280.456
```

## Dependencies

- **streamlit** (1.32.0) - Web framework
- **pandas** (2.2.1) - Data tables
- **numpy** (1.26.4) - Numerical operations
- **plotly** (5.19.0) - Interactive charts

## System Requirements

- Python 3.8 or higher
- 512 MB RAM minimum (2 GB recommended for large files)
- ~500 MB disk space for dependencies
- Modern web browser

## Troubleshooting

**"Module not found" errors**
- Activate virtual environment: `source venv/bin/activate`
- Reinstall dependencies: `pip install -r requirements.txt`

**Slow rendering with large files**
- Use "Display every Nth frame" slider
- Set to 5-10 for files with >50k frames
- Full dataset still used for statistics

**File upload fails**
- Verify file is valid `.xvg` or `.txt`
- Check file contains numeric data
- Ensure headers start with `#` or `@`

**"Address already in use" error**
- Wait 1-2 minutes for timeout, or use:
  ```bash
  streamlit run app.py --server.port 8502
  ```

## Installation Details

See [docs/INSTALLATION.md](docs/INSTALLATION.md) for:
- Platform-specific instructions (Windows, macOS, Linux)
- Docker setup
- Development installation
- Common issues and fixes

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on:
- Reporting issues
- Contributing code
- Testing changes
- Code style standards

## Publication Information

See [docs/PUBLICATION.md](docs/PUBLICATION.md) for:
- Research context and motivation
- Technical specifications
- Performance metrics
- Validation and testing
- F1000 submission details

## License

MIT License. See [LICENSE](LICENSE) file.

## Citation

```bibtex
@software{singh2026gromacs,
  title={GROMACS Trajectory Visualizer},
  author={Singh, Ayushman},
  year={2026},
  url={https://github.com/AyushmaanSingh941/gromacs-trajectory-visualizer}
}
```
