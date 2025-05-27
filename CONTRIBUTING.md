# Contributing to Image Motion Effects Studio

First off, thank you for considering contributing to Image Motion Effects Studio! This tool helps YouTube content creators bring their stories to life, and your contributions can help make it even better.

## 🤝 How Can You Contribute?

### 1. Report Bugs
- Use the GitHub Issues page
- Include your OS, Python version, and OpenCV version
- Provide steps to reproduce the issue
- Include error messages if any

### 2. Suggest New Effects
We're always looking for new motion effects! When suggesting:
- Describe the effect clearly
- Explain the use case for YouTube creators
- Include reference videos if possible

### 3. Improve Documentation
- Fix typos or clarify instructions
- Add examples for different use cases
- Create video tutorials

### 4. Submit Code
- Add new effects
- Optimize performance
- Improve the GUI
- Add features

## 🔧 Development Setup

1. Fork the repository
2. Clone your fork:
```bash
git clone https://github.com/YOUR_USERNAME/image-motion-effects.git
cd image-motion-effects
```

3. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

4. Install development dependencies:
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Includes testing tools
```

5. Create a new branch:
```bash
git checkout -b feature/your-feature-name
```

## 📝 Code Style Guidelines

- Follow PEP 8
- Use meaningful variable names
- Add docstrings to all functions
- Comment complex algorithms
- Keep functions focused and small

Example:
```python
def apply_zoom_effect(image, scale_factor, duration):
    """
    Apply a zoom effect to an image.
    
    Args:
        image (np.ndarray): Input image
        scale_factor (float): Zoom scale (1.0 = no zoom, 2.0 = 2x zoom)
        duration (float): Effect duration in seconds
        
    Returns:
        np.ndarray: Processed image frame
    """
    # Implementation here
```

## 🧪 Testing

Before submitting:
1. Test your changes with various image formats
2. Ensure all existing effects still work
3. Test edge cases (very large/small images)
4. Run the test suite:
```bash
python -m pytest tests/
```

## 📤 Submitting Changes

1. Commit your changes:
```bash
git add .
git commit -m "Add amazing new feature"
```

2. Push to your fork:
```bash
git push origin feature/your-feature-name
```

3. Create a Pull Request:
- Go to the original repository
- Click "New Pull Request"
- Select your branch
- Describe your changes clearly

### Pull Request Checklist
- [ ] Code follows style guidelines
- [ ] Tests pass
- [ ] Documentation updated
- [ ] Effect works with different image sizes
- [ ] No degradation in performance

## 💡 Effect Contribution Guidelines

When adding new effects:

1. **Consider YouTube use cases**: How will creators use this?
2. **Performance matters**: Effects should process in reasonable time
3. **Predictable behavior**: Effects should work consistently
4. **User-friendly parameters**: Keep options simple

### Effect Template
```python
def new_effect_name(self, img, t, width, height):
    """
    Brief description of the effect.
    
    This effect is perfect for [use case].
    
    Args:
        img: Source image
        t: Progress (0.0 to 1.0)
        width: Output width
        height: Output height
    
    Returns:
        Processed frame
    """
    # Your implementation here
    return processed_frame
```

## 🎯 Project Goals

Keep these in mind when contributing:
- **Simplicity**: Easy for non-technical creators to use
- **Quality**: Professional-looking output
- **Performance**: Fast processing for workflow efficiency
- **Reliability**: Consistent results across platforms

## 🌟 Recognition

Contributors will be:
- Listed in the Contributors section
- Credited in release notes
- Appreciated by YouTube creators worldwide!

## ❓ Questions?

- Open a GitHub issue with the "question" label
- Check existing issues first
- Be patient - we're all volunteers!

Thank you for helping make Image Motion Effects Studio better for everyone! 🎬