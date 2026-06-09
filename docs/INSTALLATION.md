# Installation

## Requirements

- Python 3.8 or higher
- pip (included with Python)
- Git (optional - can download ZIP)

## Windows

1. Download Python from https://www.python.org/downloads/
2. Install and **check "Add Python to PATH"**
3. Clone repo:
   ```cmd
   git clone https://github.com/AyushmaanSingh941/gromacs-trajectory-visualizer.git
   cd gromacs-trajectory-visualizer
   ```
4. Create virtual environment:
   ```cmd
   python -m venv venv
   venv\Scripts\activate
   ```
5. Install dependencies:
   ```cmd
   pip install -r requirements.txt
   ```
6. Run:
   ```cmd
   streamlit run app.py
   ```

## macOS

1. Install Python (via homebrew recommended):
   ```bash
   brew install python@3.11
   ```
   Or download from https://www.python.org/downloads/

2. Clone repo:
   ```bash
   git clone https://github.com/AyushmaanSingh941/gromacs-trajectory-visualizer.git
   cd gromacs-trajectory-visualizer
   ```

3. Create virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Run:
   ```bash
   streamlit run app.py
   ```

## Linux (Ubuntu/Debian)

1. Install Python and pip:
   ```bash
   sudo apt-get update
   sudo apt-get install python3.9 python3-pip python3-venv
   ```

2. Clone repo:
   ```bash
   git clone https://github.com/AyushmaanSingh941/gromacs-trajectory-visualizer.git
   cd gromacs-trajectory-visualizer
   ```

3. Create virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Run:
   ```bash
   streamlit run app.py
   ```

## Verify Installation

```bash
python -c "import streamlit, pandas, numpy, plotly; print('OK')"
```

## Troubleshooting

**"Python not found"**
- Windows: Reinstall and check "Add Python to PATH"
- macOS/Linux: Use `python3` instead of `python`

**"pip not found"**
```bash
python -m ensurepip --upgrade
```

**"Permission denied" (Linux/macOS)**
- Use virtual environment instead of system-wide install
- Never use `sudo pip install`

**Streamlit won't run**
- Verify venv is activated (should see `(venv)` in terminal)
- Reinstall: `pip install --upgrade -r requirements.txt`
- Clear cache: `rm -rf ~/.streamlit/cache`

**"Address already in use" port 8501**
```bash
streamlit run app.py --server.port 8502
```
