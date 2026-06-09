# Installation Guide

## Prerequisites

- **Python 3.8+** (check with `python --version`)
- **pip** package manager (included with Python)
- **Git** for cloning the repository (optional; can download ZIP instead)

## Step-by-Step Installation

### Windows

1. **Download and Install Python**
   - Visit https://www.python.org/downloads/
   - Download Python 3.9 or higher
   - During installation, **check "Add Python to PATH"**
   - Click "Install Now"

2. **Clone or Download the Repository**
   ```cmd
   git clone https://github.com/AyushmaanSingh941/gromacs-trajectory-visualizer.git
   cd gromacs-trajectory-visualizer
   ```
   Or download the ZIP file from GitHub and extract it.

3. **Create a Virtual Environment**
   ```cmd
   python -m venv venv
   venv\Scripts\activate
   ```

4. **Install Dependencies**
   ```cmd
   pip install -r requirements.txt
   ```

5. **Run the Application**
   ```cmd
   streamlit run app.py
   ```
   The app will open automatically at `http://localhost:8501`

### macOS

1. **Install Python (if not already installed)**
   
   Using Homebrew (recommended):
   ```bash
   brew install python@3.11
   ```
   
   Or download from https://www.python.org/downloads/

2. **Clone the Repository**
   ```bash
   git clone https://github.com/AyushmaanSingh941/gromacs-trajectory-visualizer.git
   cd gromacs-trajectory-visualizer
   ```

3. **Create and Activate Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

4. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the Application**
   ```bash
   streamlit run app.py
   ```

### Linux (Ubuntu/Debian)

1. **Install Python and pip**
   ```bash
   sudo apt-get update
   sudo apt-get install python3.9 python3-pip python3-venv
   ```

2. **Clone the Repository**
   ```bash
   git clone https://github.com/AyushmaanSingh941/gromacs-trajectory-visualizer.git
   cd gromacs-trajectory-visualizer
   ```

3. **Create and Activate Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

4. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the Application**
   ```bash
   streamlit run app.py
   ```

## Verifying Installation

After installation, verify everything works by running:

```bash
python -c "import streamlit, pandas, numpy, plotly; print('✓ All packages installed successfully')"
```

If all imports succeed without errors, you're ready to use the visualizer.

## Common Issues & Solutions

### Issue: "Python not found" or "python: command not found"
**Solution**: 
- **Windows**: Python is not in your system PATH. Reinstall Python and ensure "Add Python to PATH" is checked during installation
- **macOS/Linux**: Use `python3` instead of `python` (e.g., `python3 --version`)

### Issue: "pip not found" or "pip: command not found"
**Solution**: Install pip using:
```bash
python -m ensurepip --upgrade
# or
python3 -m ensurepip --upgrade
```

### Issue: "Permission denied" when installing (Linux/macOS)
**Solution**: Use a virtual environment (recommended) rather than system-wide installation:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Never use `sudo pip install` as it can break your system Python.

### Issue: Streamlit won't launch or "module not found" errors
**Solution**: 
1. Verify virtual environment is activated (should see `(venv)` in terminal)
2. Reinstall dependencies:
   ```bash
   pip install --upgrade -r requirements.txt
   ```
3. Clear Streamlit cache:
   ```bash
   rm -rf ~/.streamlit/cache
   streamlit run app.py
   ```

### Issue: "Address already in use" error on port 8501
**Solution**: Either wait for the previous session to timeout (typically 1 minute), or specify a different port:
```bash
streamlit run app.py --server.port 8502
```

## Next Steps

Once installed and running:

1. **Visit the Application**: Open `http://localhost:8501` in your browser
2. **Upload a Sample File**: Create a test `.xvg` file or find one from a GROMACS simulation
3. **Explore Features**: Try different chart types, markers, and downsampling options
4. **Export Results**: Download parsed data as CSV for external analysis

## Getting Help

If you encounter issues:

1. Check this troubleshooting section
2. Review the main [README.md](../README.md)
3. Open an issue on GitHub: https://github.com/AyushmaanSingh941/gromacs-trajectory-visualizer/issues