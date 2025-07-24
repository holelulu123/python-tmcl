# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a comprehensive Python project for controlling Trinamic TMCM stepper motor modules via TMCL (Trinamic Motion Control Language) over serial communication. The project includes:

- **TMCL Library**: Low-level Python library for programmatic motor control
- **Modern GUI Application**: User-friendly tkinter-based interface with real-time monitoring
- **Cross-platform Support**: Windows, macOS, and Linux compatibility
- **Virtual Environment Setup**: Isolated dependency management

## Development Commands

### Quick Setup
```bash
# Run the automated setup script
./setup.sh
```

### Manual Setup
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Make main.py executable
chmod +x main.py
```

### Running the Application
```bash
# Run the GUI application (with virtual environment activated)
./main.py

# Or with python directly
python main.py

# Check application imports without running GUI
python -c "import main; print('Application imports successful')"
```

### Testing and Validation
```bash
# Test application startup (3-second timeout)
timeout 3s ./main.py

# Validate all imports
python -c "import TMCL, serial; print('All dependencies available')"
```

No automated test suite is present. Testing typically involves connecting to actual hardware modules.

## Code Architecture

### Core Components

**TMCL/__init__.py**: Main entry point providing the `connect()` function that returns a Bus instance.

**Bus (bus.py)**: Central communication hub that handles:
- Serial protocol communication with TMCM modules
- Message serialization/deserialization using struct packing
- Checksum calculation for message integrity
- Support for both standard serial and CAN bus protocols
- Factory methods for creating Module and Motor instances

**Motor/Module (motor.py)**: Two-level hierarchy:
- `Module`: Represents a physical TMCM module with an address
- `Motor`: Represents an individual axis/motor on a module
- `AxisParameterInterface`: Provides property-based access to motor parameters

**Command (commands.py)**: Static class defining TMCL command constants (ROL, ROR, MVP, etc.)

**Reply (reply.py)**: Handles response parsing and error handling with TrinamicException for failed operations.

**GUI Application (main.py)**: Modern tkinter-based interface featuring:
- Connection management with auto-port detection
- Real-time motor control (rotation, positioning, emergency stop)
- Live monitoring of position and speed
- Tabbed interface for organized controls
- Status logging with timestamps
- Thread-safe GUI updates for real-time feedback

### Communication Flow
1. User creates Bus via `TMCL.connect(serial_port)`
2. Bus.get_motor() or Bus.get_module().get_motor() returns Motor instance
3. Motor methods send commands via Bus.send()
4. Bus handles protocol details, checksum, and returns Reply objects
5. Errors are raised as TrinamicException

### Key Design Patterns
- Factory pattern: Bus creates Motor/Module instances
- Command pattern: Commands defined as constants, executed via send()
- Property pattern: Motor parameters accessible as properties through AxisParameterInterface
- Error handling: Custom exceptions with status codes

### Serial Protocol Details
- Message structure: `>BBBBiB` (address, command, type, motorbank, value, checksum)
- Reply structure: `>BBBBiB` (reply_address, module_address, status, command, value, checksum)
- CAN support with different message formats
- Binary checksum calculation for message integrity

## Hardware Context

This library is designed for Trinamic stepper motor controllers. Motors must be properly configured with:
- Unique serial addresses when multiple modules share a bus
- Correct baud rate (typically 9600)
- Proper RS485 wiring through serial adapter

Common module types: TMCM-310, TMCM-610, and other TMCM series controllers.