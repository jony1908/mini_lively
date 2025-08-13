
# Mini Lively Backend Setup Guide

## Project Overview
Mini Lively is a FastAPI-based family activity monitoring system that allows parents and guardians to track their children's daily activities, manage schedules for recurring activities (like hockey, art, soccer classes), and organize events (like birthday parties).

## Prerequisites
- Python 3.9 or higher
- PostgreSQL 12 or higher
- Git

## Installation Steps

### 1. Clone and Setup Environment
```bash
git clone <repository-url>
cd mini-lively/backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Database Configuration
- **Database**: PostgreSQL
- **Connection**: Configured via `DATABASE_URL` environment variable in `.env`
- **Default**: `postgresql://username:password@localhost:5432/mini_lively`

#### PostgreSQL Setup
```bash
# Create database
createdb mini_lively

# Or using psql
psql -U postgres
CREATE DATABASE mini_lively;
```

### 3. Environment Variables
Create a `.env` file in the backend directory:
```env
# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/mini_lively

# Optional: Override default settings
CORS_ORIGINS=["http://localhost:3000", "http://localhost:5173"]
DEBUG=true
```

### 4. Database Setup
The application automatically creates tables on startup via the `init_db()` function in the lifespan context manager.

**Manual table creation (if needed):**
```bash
# Using Alembic for migrations
alembic upgrade head
```

### 5. Running the Application
```bash
# Development server
python -m app.main

# Or using uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Dependencies
```txt
fastapi==0.116.1          # Web framework
uvicorn==0.35.0           # ASGI server
sqlalchemy==2.0.43        # ORM and database toolkit
psycopg2-binary==2.9.10   # PostgreSQL adapter
alembic==1.16.4           # Database migrations
python-dotenv==1.1.1      # Environment variable loading
python-multipart==0.0.20  # Form data parsing
pytest==8.3.4             # Testing framework
httpx==0.25.0             # HTTP client for testing
requests==2.31.0          # HTTP library
```

## Testing

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_children.py
```

### Test Database
Tests use a separate test database. Configure in `conftest.py` or use in-memory SQLite for testing.

## API Documentation

### Interactive Documentation
Once the application is running, access:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

### Health Endpoints
- **Root**: http://localhost:8000/ - Service status
- **Health Check**: http://localhost:8000/health - Health status
- **Database Test**: http://localhost:8000/db-test - Database connectivity

## Production Deployment

### Environment Setup
```env
DATABASE_URL=postgresql://user:password@production-db:5432/mini_lively
DEBUG=false
CORS_ORIGINS=["https://your-frontend-domain.com"]
```

### Security Considerations
1. **Authentication**: Implement JWT or session-based authentication
2. **CORS**: Restrict to specific origins
3. **Database**: Use connection pooling and SSL
4. **Secrets**: Use environment variables for sensitive data
5. **Rate Limiting**: Implement request rate limiting

## Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Check PostgreSQL is running
   - Verify DATABASE_URL format
   - Ensure database exists

2. **Import Errors**
   - Activate virtual environment
   - Install requirements: `pip install -r requirements.txt`

3. **Port Already in Use**
   - Check for existing processes: `lsof -i :8000`
   - Kill process or use different port

4. **Migration Issues**
   - Reset database: `alembic downgrade base && alembic upgrade head`
   - Check Alembic configuration

### Logs and Debugging
```bash
# Enable debug logging
export DEBUG=true

# View application logs
tail -f app.log

# Database query logging
export SQLALCHEMY_LOG_LEVEL=debug
```

## Development Workflow

### Adding New Features
1. Create new models in `app/models/`
2. Add CRUD operations in `app/crud/`
3. Define Pydantic schemas in `app/schemas/`
4. Create API routes in `app/routers/`
5. Add route to `app/main.py`
6. Write tests in `tests/`
7. Update documentation

### Code Quality
```bash
# Format code
black app/

# Lint code
flake8 app/

# Type checking
mypy app/
```

### Database Migrations
```bash
# Generate migration
alembic revision --autogenerate -m "Add new table"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```
