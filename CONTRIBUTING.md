# Contributing to AI Sustainable Cities Planner

Thank you for your interest in contributing to the AI Sustainable Cities Planner! This document provides guidelines for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Contributing Guidelines](#contributing-guidelines)
- [Pull Request Process](#pull-request-process)
- [Issue Reporting](#issue-reporting)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Documentation](#documentation)

## Code of Conduct

This project follows a code of conduct to ensure a welcoming environment for all contributors. Please be respectful and constructive in all interactions.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/your-username/sustainable-cities-planner.git`
3. Create a feature branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Test your changes
6. Submit a pull request

## Development Setup

### Prerequisites

- Python 3.9+
- Node.js 16+
- PostgreSQL 13+
- Redis 6+
- Docker (optional)

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Frontend Setup

```bash
cd frontend
npm install
```

### Database Setup

```bash
# Start PostgreSQL and Redis
docker-compose up -d postgres redis

# Run migrations
cd backend
python -m alembic upgrade head

# Seed initial data
python scripts/seed_data.py
```

### Running the Application

```bash
# Backend
cd backend
python main.py

# Frontend (in another terminal)
cd frontend
npm start
```

## Contributing Guidelines

### Types of Contributions

We welcome contributions in the following areas:

1. **Bug Fixes**: Fix issues in existing code
2. **Features**: Add new functionality
3. **Documentation**: Improve or add documentation
4. **Tests**: Add or improve test coverage
5. **Performance**: Optimize existing code
6. **UI/UX**: Improve the user interface

### Before Contributing

1. Check existing issues and pull requests
2. Discuss major changes in an issue first
3. Ensure your changes align with the project goals
4. Follow the coding standards

## Pull Request Process

### 1. Create a Pull Request

- Use a descriptive title
- Reference related issues
- Provide a clear description of changes
- Include screenshots for UI changes

### 2. Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] New tests added for new functionality
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
```

### 3. Review Process

- All PRs require review from maintainers
- Address feedback promptly
- Keep PRs focused and reasonably sized
- Ensure CI/CD checks pass

## Issue Reporting

### Bug Reports

When reporting bugs, include:

1. **Environment**: OS, Python/Node versions, browser
2. **Steps to Reproduce**: Clear, numbered steps
3. **Expected Behavior**: What should happen
4. **Actual Behavior**: What actually happens
5. **Screenshots**: If applicable
6. **Logs**: Relevant error messages

### Feature Requests

For feature requests, include:

1. **Use Case**: Why is this feature needed?
2. **Proposed Solution**: How should it work?
3. **Alternatives**: Other solutions considered
4. **Additional Context**: Any other relevant information

## Coding Standards

### Python (Backend)

- Follow PEP 8 style guide
- Use type hints
- Maximum line length: 88 characters (Black formatter)
- Use meaningful variable and function names
- Add docstrings for functions and classes

```python
def calculate_co2_emissions(distance_km: float, transport_mode: str) -> float:
    """
    Calculate CO2 emissions for a given distance and transport mode.
    
    Args:
        distance_km: Distance in kilometers
        transport_mode: Transportation mode (car, transit, bike, walk)
        
    Returns:
        CO2 emissions in kg
    """
    emissions_factors = {
        'car': 0.12,
        'transit': 0.05,
        'bike': 0.0,
        'walk': 0.0
    }
    return distance_km * emissions_factors.get(transport_mode, 0.12)
```

### TypeScript/React (Frontend)

- Use TypeScript for type safety
- Follow React best practices
- Use functional components with hooks
- Use meaningful component and variable names
- Add JSDoc comments for complex functions

```typescript
interface CityData {
  id: number;
  name: string;
  population: number;
  area_km2: number;
}

/**
 * Renders a city card with basic information
 */
const CityCard: React.FC<{ city: CityData }> = ({ city }) => {
  return (
    <Card title={city.name}>
      <p>Population: {city.population.toLocaleString()}</p>
      <p>Area: {city.area_km2} km²</p>
    </Card>
  );
};
```

### Database

- Use descriptive table and column names
- Add appropriate indexes
- Use foreign key constraints
- Include timestamps for audit trails

### Git Commit Messages

Use conventional commit format:

```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Test changes
- `chore`: Build/tooling changes

Examples:
```
feat(simulation): add multi-agent simulation engine
fix(api): resolve city data validation error
docs(readme): update installation instructions
```

## Testing

### Backend Testing

```bash
cd backend
pytest tests/ -v --cov=app
```

### Frontend Testing

```bash
cd frontend
npm test
```

### Test Coverage

- Maintain test coverage above 80%
- Write unit tests for new functions
- Write integration tests for API endpoints
- Write component tests for React components

### Test Types

1. **Unit Tests**: Test individual functions/components
2. **Integration Tests**: Test API endpoints
3. **End-to-End Tests**: Test complete user workflows
4. **Performance Tests**: Test system performance

## Documentation

### Code Documentation

- Add docstrings to Python functions and classes
- Add JSDoc comments to TypeScript functions
- Use meaningful variable and function names
- Add inline comments for complex logic

### API Documentation

- Update API documentation for new endpoints
- Include request/response examples
- Document error codes and messages

### User Documentation

- Update README for new features
- Add usage examples
- Update deployment instructions

## Development Workflow

### Branch Naming

- `feature/description`: New features
- `fix/description`: Bug fixes
- `docs/description`: Documentation updates
- `refactor/description`: Code refactoring

### Release Process

1. Create release branch from main
2. Update version numbers
3. Update CHANGELOG.md
4. Create pull request
5. Merge after review
6. Create GitHub release
7. Deploy to production

## Performance Guidelines

### Backend

- Use database indexes appropriately
- Implement caching where beneficial
- Use async/await for I/O operations
- Monitor memory usage

### Frontend

- Use React.memo for expensive components
- Implement lazy loading for routes
- Optimize bundle size
- Use efficient data structures

## Security Guidelines

- Never commit secrets or API keys
- Use environment variables for configuration
- Validate all user inputs
- Use HTTPS in production
- Implement proper authentication/authorization

## Getting Help

- Check existing documentation
- Search existing issues
- Join our community discussions
- Contact maintainers directly

## Recognition

Contributors will be recognized in:
- CONTRIBUTORS.md file
- Release notes
- Project documentation

Thank you for contributing to the AI Sustainable Cities Planner! 🌱
