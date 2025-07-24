#!/bin/bash
set -e

echo "🔧 Setting up Python TMCL Motor Controller..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is required but not installed.${NC}"
    exit 1
fi

echo -e "${BLUE}🐍 Python 3 found: $(python3 --version)${NC}"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}📦 Creating virtual environment...${NC}"
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
else
    echo -e "${YELLOW}📦 Virtual environment already exists${NC}"
fi

# Activate virtual environment
echo -e "${YELLOW}🔌 Activating virtual environment...${NC}"
source venv/bin/activate

# Upgrade pip
echo -e "${YELLOW}⬆️  Upgrading pip...${NC}"
pip install --upgrade pip

# Install requirements
if [ -f "requirements.txt" ]; then
    echo -e "${YELLOW}📋 Installing dependencies from requirements.txt...${NC}"
    pip install -r requirements.txt
    echo -e "${GREEN}✓ Dependencies installed successfully${NC}"
else
    echo -e "${RED}❌ requirements.txt not found${NC}"
    exit 1
fi

# Make main.py executable
if [ -f "main.py" ]; then
    echo -e "${YELLOW}🔧 Making main.py executable...${NC}"
    chmod +x main.py
    echo -e "${GREEN}✓ main.py is now executable${NC}"
else
    echo -e "${RED}❌ main.py not found${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}🎉 Setup completed successfully!${NC}"
echo ""
echo -e "${BLUE}To run the application:${NC}"
echo -e "${YELLOW}  ./main.py${NC}"
echo ""
echo -e "${BLUE}To activate the virtual environment manually:${NC}"
echo -e "${YELLOW}  source venv/bin/activate${NC}"
echo ""
echo -e "${BLUE}To deactivate the virtual environment:${NC}"
echo -e "${YELLOW}  deactivate${NC}"
echo ""