Python TMCL Motor Controller
============================

A modern Python library and GUI application for controlling Trinamic TMCM stepper motor modules via TMCL (Trinamic Motion Control Language) over serial communication.

## ✨ Features

- **Modern GUI Application**: Intuitive interface for motor control with real-time monitoring
- **Python Library**: Low-level TMCL library for programmatic control
- **Real-time Feedback**: Live position and speed monitoring
- **Multiple Control Modes**: Manual rotation, absolute/relative positioning, reference search
- **Connection Management**: Auto-detection of serial ports with visual status indicators
- **Cross-platform**: Works on Windows, macOS, and Linux

## 🚀 Quick Start

### Installation
```bash
# Run the automated setup
./setup.sh

# Launch the GUI application
./main.py
```

### Manual Setup
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Make executable and run
chmod +x main.py
./main.py
```

## GUI Application

The modern GUI provides an intuitive interface for motor control:

### Connection Panel
- **Serial Port**: Auto-detects available serial ports
- **Refresh Button**: Updates the port list (🔄 icon)
- **Module Address**: Configure the TMCM module address (1-255)
- **Status Indicator**: Visual connection status with colored dot

### Motor Controls
- **Quick Controls**: Left/Right rotation with adjustable velocity
- **Emergency Stop**: Immediate motor stop
- **Positioning**: Absolute and relative movement controls
- **Reference Search**: Automatic limit switch detection
- **Real-time Monitoring**: Live position and speed display

### Status Log
- Real-time command feedback
- Error reporting and diagnostics
- Timestamped activity log

## System Requirements

### Python Dependencies
- Python 3.7+
- pyserial 3.5+

### System Dependencies (Tkinter GUI Support)

The GUI application requires tkinter, which depends on system-level Tk libraries:

#### **Linux** 🐧
Tkinter requires the Tk GUI toolkit to be installed at the system level:

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3-tk
```

**Arch Linux:**
```bash
sudo pacman -S tk
```

**RHEL/CentOS/Fedora:**
```bash
# RHEL/CentOS
sudo yum install tkinter
# or for newer versions
sudo dnf install python3-tkinter

#### **Troubleshooting Tkinter Issues**

If you encounter `ImportError: libtk8.6.so: cannot open shared object file`:
1. Install the system Tk package for your distribution (see above)
2. Verify installation: `python3 -c "import tkinter; print('Tkinter working!')"`
3. If issues persist, try reinstalling Python development packages

## 🎛️ Interface Elements Explained

### Module Address
The **Module Address** field (right side of connection panel) specifies which TMCM module to communicate with on the RS485 bus. Each physical module must have a unique address (1-255). This is crucial when multiple motors are connected to the same serial bus.

### Refresh Button
The **🔄** button refreshes the list of available serial ports. If the icon appears as a question mark, it may be a font rendering issue - the functionality remains the same.

## 📖 API Reference

### Motor Class Methods

#### Movement Commands
- `move_absolute(position)` - Move to absolute position
- `move_relative(offset)` - Move by relative offset
- `rotate_left(velocity)` - Rotate left at specified velocity
- `rotate_right(velocity)` - Rotate right at specified velocity
- `stop()` - Stop motor immediately

#### Configuration
- `reference_search(rfs_type)` - Start reference search routine
- `run_command(cmd)` - Execute predefined user subroutine
- `send(cmd, type, motorbank, value)` - Send raw TMCL command

#### Parameter Access
- `motor.axis.actual_position` - Current position
- `motor.axis.actual_speed` - Current speed
- `motor.axis.target_position` - Target position
- `motor.axis.max_current` - Maximum current setting

## 🛠️ Development

### Project Structure
```
python-tmcl/
├── TMCL/              # Core library package
│   ├── __init__.py    # Main entry point
│   ├── bus.py         # Serial communication handler
│   ├── motor.py       # Motor and module classes
│   ├── commands.py    # TMCL command constants
│   └── reply.py       # Response parsing and errors
├── main.py            # Modern GUI application
├── requirements.txt   # Python dependencies
└── setup.sh          # Automated setup script
```

- [TMCL IDE](https://www.trinamic.com/support/software/tmcl-ide/) - Official Trinamic development environment
- [TMCL Protocol Reference](https://www.trinamic.com/support/software/tmcl/) - Complete command documentation
- [Hardware Documentation](https://www.trinamic.com/products/modules/) - TMCM module specifications