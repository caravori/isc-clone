# Contributing to ISC Clone

Thank you for considering contributing to ISC Clone! This document provides guidelines for contributing to the project.

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/caravori/isc-clone/issues)
2. If not, create a new issue with:
   - Clear, descriptive title
   - Detailed description of the bug
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details (OS, Python version, Django version)

### Suggesting Features

1. Check existing feature requests
2. Create a new issue with:
   - Clear description of the feature
   - Use case and benefits
   - Potential implementation approach

### Code Contributions

1. **Fork the repository**
   ```bash
   git clone https://github.com/caravori/isc-clone.git
   cd isc-clone
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow Django coding standards
   - Write clear, commented code
   - Add tests for new features
   - Update documentation as needed

4. **Test your changes**
   ```bash
   python manage.py test
   python manage.py check
   ```

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add feature: brief description"
   ```

6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request**
   - Provide clear description of changes
   - Reference related issues
   - Include screenshots if UI changes

## Coding Standards

### Python/Django

- Follow PEP 8 style guide
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and concise
- Use Django's built-in features when possible

### Git Commit Messages

- Use present tense ("Add feature" not "Added feature")
- First line: brief summary (50 chars or less)
- Add detailed description if needed
- Reference issues: "Fixes #123"

### Code Review Process

1. All submissions require review
2. Maintainers will review within 1-2 weeks
3. Address review comments
4. Once approved, changes will be merged

## Development Setup

```bash
# Clone repository
git clone https://github.com/caravori/isc-clone.git
cd isc-clone

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup database
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

## Testing

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test blog
python manage.py test threats

# Check code quality
python manage.py check
```

## Documentation

- Update README.md for user-facing changes
- Add inline code comments for complex logic
- Update DEPLOYMENT.md for infrastructure changes
- Document new models, views, and APIs

## Areas for Contribution

### High Priority
- Test coverage improvements
- API documentation
- Docker deployment setup
- Performance optimization

### Medium Priority
- Additional threat intelligence sources
- Enhanced visualization/charts
- Email notifications
- Advanced search functionality

### Good First Issues
- UI/UX improvements
- Documentation enhancements
- Additional template customization
- Bug fixes

## Questions?

Feel free to open an issue with the `question` label or reach out to the maintainers.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
