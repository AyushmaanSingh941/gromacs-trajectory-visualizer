# Contributing to GROMACS Trajectory Visualizer

Thank you for your interest in contributing to this research software! This document provides guidelines for maintaining research integrity and code quality.

## Philosophy: Transparency for Research

This tool is intended for scientific research and publication. All contributions should maintain transparency and reproducibility:

- **Code must be understandable** to domain experts, not just programmers
- **Changes should be traceable** and reversible via git history
- **Avoid unnecessary complexity** that obscures the original logic
- **Include clear explanations** of why changes are necessary
- **Preserve research integrity**: No hidden dependencies, external APIs, or magic numbers

## Reporting Issues

If you encounter a bug or have a question:

1. **Check existing issues** first: https://github.com/AyushmaanSingh941/gromacs-trajectory-visualizer/issues

2. **Create a new issue** with:
   - Clear, descriptive title
   - Steps to reproduce (if applicable)
   - Expected vs. actual behavior
   - Your system info: Python version, OS, file size/type being tested
   - Error message or full stack trace (if applicable)
   - Sample file (sanitized if containing sensitive data)

## Code Contributions

### Before You Start

- Ensure you have permission to contribute (you own the code or have explicit approval)
- This project uses MIT License; your contributions will be licensed the same way
- Read through the existing code to understand the style and approach

### Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/gromacs-trajectory-visualizer.git
   cd gromacs-trajectory-visualizer
   ```
3. **Create a feature branch**:
   ```bash
   git checkout -b feature/descriptive-feature-name
   ```
4. **Create and activate virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```

### Code Style

- Follow **PEP 8** conventions
- **Maximum line length**: 100 characters
- Use **descriptive variable names**
- Use **comments liberally** for non-obvious logic
- Keep functions **focused and single-purpose**

### Testing Your Changes

Before submitting, test thoroughly:

1. **Test with various file sizes**: Small (100 frames), Medium (10,000 frames), Large (100,000+ frames)
2. **Test with different data types**: Single column, Multiple columns, Non-standard headers
3. **Test all features**: Chart interactions, markers, downsampling, column selection
4. **Test error handling**: Invalid formats, Corrupted data, Empty files
5. **Test on different platforms**: Windows, macOS, Linux (if possible)

### Submitting Your Changes

1. **Push your branch** to your fork:
   ```bash
   git push origin feature/descriptive-feature-name
   ```

2. **Create a Pull Request** on GitHub with:
   - Clear title summarizing the change
   - Description of what changed and why
   - Reference to related issues (e.g., "Fixes #42")
   - Any testing notes or known limitations

3. **Respond to feedback** promptly

## License Reminder

By contributing, you agree your contributions are licensed under the **MIT License**, same as the project.

---

Thank you for contributing to making molecular dynamics research more accessible and reproducible! 🧬