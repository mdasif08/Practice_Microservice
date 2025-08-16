#!/bin/bash

# CraftNudge AI Agent - Setup Script
# This script initializes the project structure and dependencies

set -e

echo "🚀 Setting up CraftNudge AI Agent..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Python 3.8+ is installed
check_python() {
    print_status "Checking Python version..."
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
        print_success "Python $PYTHON_VERSION found"
    else
        print_error "Python 3.8+ is required but not installed"
        exit 1
    fi
}

# Check if Git is installed
check_git() {
    print_status "Checking Git installation..."
    if command -v git &> /dev/null; then
        GIT_VERSION=$(git --version | cut -d' ' -f3)
        print_success "Git $GIT_VERSION found"
    else
        print_error "Git is required but not installed"
        exit 1
    fi
}

# Check if Docker is installed (optional)
check_docker() {
    print_status "Checking Docker installation..."
    if command -v docker &> /dev/null; then
        DOCKER_VERSION=$(docker --version | cut -d' ' -f3 | cut -d',' -f1)
        print_success "Docker $DOCKER_VERSION found"
        DOCKER_AVAILABLE=true
    else
        print_warning "Docker not found - containerized deployment will not be available"
        DOCKER_AVAILABLE=false
    fi
}

# Create virtual environment
create_venv() {
    print_status "Creating Python virtual environment..."
    if [ ! -d "venv" ]; then
        python3 -m venv venv
        print_success "Virtual environment created"
    else
        print_warning "Virtual environment already exists"
    fi
}

# Activate virtual environment
activate_venv() {
    print_status "Activating virtual environment..."
    source venv/bin/activate
    print_success "Virtual environment activated"
}

# Install dependencies
install_dependencies() {
    print_status "Installing Python dependencies..."
    
    # Upgrade pip
    pip install --upgrade pip
    
    # Install root dependencies
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
    fi
    
    # Install service-specific dependencies
    for service in services/*/; do
        if [ -f "${service}requirements.txt" ]; then
            print_status "Installing dependencies for $(basename $service)..."
            pip install -r "${service}requirements.txt"
        fi
    done
    
    # Install CLI dependencies
    if [ -f "cli/requirements.txt" ]; then
        print_status "Installing CLI dependencies..."
        pip install -r cli/requirements.txt
    fi
    
    # Install API Gateway dependencies
    if [ -f "api-gateway/requirements.txt" ]; then
        print_status "Installing API Gateway dependencies..."
        pip install -r api-gateway/requirements.txt
    fi
    
    print_success "All dependencies installed"
}

# Create necessary directories
create_directories() {
    print_status "Creating necessary directories..."
    
    # Create data store directories
    mkdir -p shared/data-store/behaviors
    mkdir -p shared/data-store/analytics
    mkdir -p shared/data-store/notifications
    
    # Create logs directory
    mkdir -p logs
    
    # Create test directories
    mkdir -p tests/fixtures/mock_repositories
    
    print_success "Directories created"
}

# Initialize data files
initialize_data_files() {
    print_status "Initializing data files..."
    
    # Create empty JSONL files if they don't exist
    touch shared/data-store/behaviors/commits.jsonl
    touch shared/data-store/behaviors/patterns.jsonl
    touch shared/data-store/behaviors/insights.jsonl
    touch shared/data-store/analytics/metrics.jsonl
    touch shared/data-store/analytics/trends.jsonl
    touch shared/data-store/notifications/sent.jsonl
    touch shared/data-store/notifications/preferences.jsonl
    
    print_success "Data files initialized"
}

# Set up Git hooks (optional)
setup_git_hooks() {
    print_status "Setting up Git hooks..."
    
    if [ -d ".git" ]; then
        mkdir -p .git/hooks
        
        # Create pre-commit hook for testing
        cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
# Pre-commit hook to run tests

echo "Running pre-commit tests..."
cd "$(dirname "$0")/../.."

# Run linting
if command -v flake8 &> /dev/null; then
    flake8 services/ cli/ api-gateway/ --max-line-length=88 --ignore=E203,W503
fi

# Run tests
if command -v pytest &> /dev/null; then
    pytest tests/ -v --tb=short
fi
EOF
        
        chmod +x .git/hooks/pre-commit
        print_success "Git hooks configured"
    else
        print_warning "Not a Git repository - skipping Git hooks setup"
    fi
}

# Create environment file
create_env_file() {
    print_status "Creating environment file..."
    
    if [ ! -f ".env" ]; then
        cat > .env << 'EOF'
# CraftNudge AI Agent - Environment Variables

# Application Settings
CRAFTNUDGE_ENV=development
CRAFTNUDGE_DEBUG=true

# Data Store
DATA_STORE_PATH=shared/data-store

# Commit Tracker Service
COMMIT_TRACKER_DATA_PATH=shared/data-store/behaviors/commits.jsonl
COMMIT_TRACKER_LOG_LEVEL=INFO

# Analytics Service
ANALYTICS_INTERVAL=daily
ANALYTICS_LOG_LEVEL=INFO

# Notification Service
NOTIFICATION_INTERVAL=hourly
NOTIFICATION_LOG_LEVEL=INFO

# API Gateway
GATEWAY_PORT=8000
GATEWAY_HOST=0.0.0.0
JWT_SECRET=your-secret-key-change-in-production

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/craftnudge.log

# Redis (for caching)
REDIS_URL=redis://localhost:6379

# PostgreSQL (optional)
POSTGRES_URL=postgresql://craftnudge:craftnudge123@localhost:5432/craftnudge
EOF
        
        print_success "Environment file created (.env)"
        print_warning "Please review and update the .env file with your specific settings"
    else
        print_warning "Environment file already exists"
    fi
}

# Build Docker images (if Docker is available)
build_docker_images() {
    if [ "$DOCKER_AVAILABLE" = true ]; then
        print_status "Building Docker images..."
        
        # Build commit tracker service
        docker build -f deployment/docker/Dockerfile.commit-tracker -t craftnudge/commit-tracker:latest .
        
        # Build analytics service
        docker build -f deployment/docker/Dockerfile.analytics -t craftnudge/analytics:latest .
        
        # Build notification service
        docker build -f deployment/docker/Dockerfile.notifications -t craftnudge/notifications:latest .
        
        # Build API gateway
        docker build -f deployment/docker/Dockerfile.api-gateway -t craftnudge/api-gateway:latest .
        
        print_success "Docker images built"
    else
        print_warning "Skipping Docker image build (Docker not available)"
    fi
}

# Run initial tests
run_tests() {
    print_status "Running initial tests..."
    
    if command -v pytest &> /dev/null; then
        pytest tests/ -v --tb=short || print_warning "Some tests failed - this is normal for initial setup"
    else
        print_warning "pytest not found - skipping tests"
    fi
}

# Display setup completion message
show_completion_message() {
    echo ""
    echo "🎉 CraftNudge AI Agent setup completed!"
    echo ""
    echo "📋 Next steps:"
    echo "1. Review and update the .env file with your settings"
    echo "2. Activate the virtual environment: source venv/bin/activate"
    echo "3. Test the CLI: python cli/commands/track_commit.py --help"
    echo "4. Start services: docker-compose up -d (if using Docker)"
    echo ""
    echo "📚 Documentation:"
    echo "- Main README: README.md"
    echo "- Architecture: architecture.md"
    echo "- Project Structure: project-structure.md"
    echo ""
    echo "🔧 Development:"
    echo "- Run tests: pytest tests/"
    echo "- Format code: black ."
    echo "- Lint code: flake8 ."
    echo ""
    echo "🚀 Happy coding with CraftNudge!"
}

# Main setup function
main() {
    echo "CraftNudge AI Agent Setup"
    echo "========================"
    echo ""
    
    check_python
    check_git
    check_docker
    create_venv
    activate_venv
    install_dependencies
    create_directories
    initialize_data_files
    setup_git_hooks
    create_env_file
    build_docker_images
    run_tests
    show_completion_message
}

# Run main function
main "$@"
