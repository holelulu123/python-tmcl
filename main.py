#! venv/bin/python3
"""
Modern TMCL Motor Control GUI
A sleek, user-friendly interface for controlling Trinamic stepper motors
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import time
from serial import Serial, SerialException
from serial.tools import list_ports
import TMCL


class ModernTMCLController:
    def __init__(self, root):
        self.root = root
        self.root.title("TMCL Motor Controller")
        self.root.geometry("1000x750")
        self.root.minsize(900, 650)
        self.root.configure(bg='#f0f0f0')
        
        # Connection state
        self.bus = None
        self.motor = None
        self.connected = False
        self.current_position = 0
        
        # Colors
        self.colors = {
            'primary': '#2563eb',
            'success': '#16a34a', 
            'warning': '#f59e0b',
            'danger': '#dc2626',
            'secondary': '#6b7280',
            'light': '#f8fafc',
            'dark': '#1e293b'
        }
        
        self.setup_styles()
        self.create_widgets()
        self.update_connection_status()
        
    def setup_styles(self):
        """Configure modern styling for tkinter widgets"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure button styles
        style.configure('Primary.TButton',
                       background=self.colors['primary'],
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none')
        
        style.configure('Success.TButton',
                       background=self.colors['success'],
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none')
        
        style.configure('Warning.TButton',
                       background=self.colors['warning'],
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none')
        
        style.configure('Danger.TButton',
                       background=self.colors['danger'],
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none')

    def create_widgets(self):
        """Create the main GUI layout"""
        # Main container
        main_frame = tk.Frame(self.root, bg='#f0f0f0', padx=20, pady=20)
        main_frame.pack(fill='both', expand=True)
        
        # Title
        title_label = tk.Label(main_frame, 
                              text="TMCL Motor Controller",
                              font=('Segoe UI', 24, 'bold'),
                              fg=self.colors['dark'],
                              bg='#f0f0f0')
        title_label.pack(pady=(0, 30))
        
        # Connection Section
        self.create_connection_section(main_frame)
        
        # Motor Control Section
        self.create_motor_control_section(main_frame)
        
        # Status Section
        self.create_status_section(main_frame)
        
    def create_connection_section(self, parent):
        """Create connection management section"""
        # Connection Frame
        conn_frame = tk.LabelFrame(parent, 
                                  text="Connection",
                                  font=('Segoe UI', 12, 'bold'),
                                  bg='#f0f0f0',
                                  fg=self.colors['dark'],
                                  padx=15, pady=15)
        conn_frame.pack(fill='x', pady=(0, 20))
        
        # Connection controls row
        conn_controls = tk.Frame(conn_frame, bg='#f0f0f0')
        conn_controls.pack(fill='x')
        
        # Serial port selection
        tk.Label(conn_controls, text="Serial Port:", 
                font=('Segoe UI', 10), bg='#f0f0f0').pack(side='left', padx=(0, 10))
        
        self.port_var = tk.StringVar()
        self.port_combo = ttk.Combobox(conn_controls, textvariable=self.port_var, 
                                      width=15, state='readonly')
        self.port_combo.pack(side='left', padx=(0, 10))
        
        # Refresh ports button (using text fallback for better compatibility)
        refresh_btn = ttk.Button(conn_controls, text="↻", width=3,
                               command=self.refresh_ports)
        refresh_btn.pack(side='left', padx=(0, 10))
        
        # Module address
        tk.Label(conn_controls, text="Module Address:", 
                font=('Segoe UI', 10), bg='#f0f0f0').pack(side='left', padx=(10, 5))
        
        self.address_var = tk.StringVar(value="1")
        address_spin = tk.Spinbox(conn_controls, from_=1, to=255, width=5,
                                 textvariable=self.address_var)
        address_spin.pack(side='left', padx=(0, 20))
        
        # Connect button
        self.connect_btn = ttk.Button(conn_controls, text="Connect",
                                    style='Success.TButton',
                                    command=self.toggle_connection)
        self.connect_btn.pack(side='right')
        
        # Connection status indicator
        status_frame = tk.Frame(conn_frame, bg='#f0f0f0')
        status_frame.pack(fill='x', pady=(10, 0))
        
        self.status_indicator = tk.Label(status_frame, text="●", 
                                       font=('Segoe UI', 16),
                                       fg=self.colors['danger'],
                                       bg='#f0f0f0')
        self.status_indicator.pack(side='left')
        
        self.status_label = tk.Label(status_frame, text="Disconnected",
                                   font=('Segoe UI', 10),
                                   fg=self.colors['secondary'],
                                   bg='#f0f0f0')
        self.status_label.pack(side='left', padx=(5, 0))
        
        # Initialize port list
        self.refresh_ports()
        
    def create_motor_control_section(self, parent):
        """Create motor control interface"""
        # Motor Control Frame
        motor_frame = tk.LabelFrame(parent,
                                   text="Motor Control",
                                   font=('Segoe UI', 12, 'bold'),
                                   bg='#f0f0f0',
                                   fg=self.colors['dark'],
                                   padx=15, pady=15)
        motor_frame.pack(fill='both', expand=True, pady=(0, 20))
        
        # Create notebook for organized controls
        notebook = ttk.Notebook(motor_frame)
        notebook.pack(fill='both', expand=True)
        
        # Movement tab
        movement_frame = tk.Frame(notebook, bg='#f0f0f0')
        notebook.add(movement_frame, text="Movement")
        self.create_movement_controls(movement_frame)
        
        # Parameters tab
        params_frame = tk.Frame(notebook, bg='#f0f0f0')
        notebook.add(params_frame, text="Parameters")
        self.create_parameter_controls(params_frame)
        
    def create_movement_controls(self, parent):
        """Create movement control widgets"""
        # Quick movement buttons
        quick_frame = tk.LabelFrame(parent, text="Quick Controls",
                                   font=('Segoe UI', 10, 'bold'),
                                   bg='#f0f0f0', padx=10, pady=10)
        quick_frame.pack(fill='x', pady=(10, 20))
        
        btn_frame = tk.Frame(quick_frame, bg='#f0f0f0')
        btn_frame.pack()
        
        # Direction buttons with modern styling
        self.left_btn = ttk.Button(btn_frame, text="◀ Rotate Left",
                                  style='Primary.TButton',
                                  command=self.rotate_left,
                                  state='disabled')
        self.left_btn.pack(side='left', padx=5)
        
        self.stop_btn = ttk.Button(btn_frame, text="⏹ STOP",
                                  style='Danger.TButton',
                                  command=self.stop_motor,
                                  state='disabled')
        self.stop_btn.pack(side='left', padx=5)
        
        self.right_btn = ttk.Button(btn_frame, text="Rotate Right ▶",
                                   style='Primary.TButton',
                                   command=self.rotate_right,
                                   state='disabled')
        self.right_btn.pack(side='left', padx=5)
        
        # Velocity control
        vel_frame = tk.Frame(quick_frame, bg='#f0f0f0')
        vel_frame.pack(pady=(10, 0))
        
        tk.Label(vel_frame, text="Velocity:", font=('Segoe UI', 10),
                bg='#f0f0f0').pack(side='left', padx=(0, 5))
        
        self.velocity_var = tk.StringVar(value="1000")
        velocity_entry = tk.Entry(vel_frame, textvariable=self.velocity_var, width=10)
        velocity_entry.pack(side='left', padx=(0, 5))
        
        tk.Label(vel_frame, text="steps/sec", font=('Segoe UI', 9),
                fg=self.colors['secondary'], bg='#f0f0f0').pack(side='left')
        
        # Positioning controls
        pos_frame = tk.LabelFrame(parent, text="Positioning",
                                 font=('Segoe UI', 10, 'bold'),
                                 bg='#f0f0f0', padx=10, pady=10)
        pos_frame.pack(fill='x', pady=(0, 10))
        
        # Absolute positioning
        abs_frame = tk.Frame(pos_frame, bg='#f0f0f0')
        abs_frame.pack(fill='x', pady=5)
        
        tk.Label(abs_frame, text="Move to position:", font=('Segoe UI', 10),
                bg='#f0f0f0').pack(side='left', padx=(0, 8))
        
        self.abs_pos_var = tk.StringVar(value="0")
        abs_entry = tk.Entry(abs_frame, textvariable=self.abs_pos_var, width=12)
        abs_entry.pack(side='left', padx=(0, 8))
        
        self.abs_move_btn = ttk.Button(abs_frame, text="Move Absolute",
                                      style='Primary.TButton',
                                      command=self.move_absolute,
                                      state='disabled')
        self.abs_move_btn.pack(side='left', padx=(15, 0))
        
        # Relative positioning
        rel_frame = tk.Frame(pos_frame, bg='#f0f0f0')
        rel_frame.pack(fill='x', pady=5)
        
        tk.Label(rel_frame, text="Move by offset:", font=('Segoe UI', 10),
                bg='#f0f0f0').pack(side='left', padx=(0, 8))
        
        self.rel_pos_var = tk.StringVar(value="100")
        rel_entry = tk.Entry(rel_frame, textvariable=self.rel_pos_var, width=12)
        rel_entry.pack(side='left', padx=(0, 8))
        
        self.rel_move_btn = ttk.Button(rel_frame, text="Move Relative",
                                      style='Primary.TButton',
                                      command=self.move_relative,
                                      state='disabled')
        self.rel_move_btn.pack(side='left', padx=(15, 0))
        
    def create_parameter_controls(self, parent):
        """Create parameter monitoring and control widgets"""
        # Parameter display
        param_frame = tk.Frame(parent, bg='#f0f0f0', padx=10, pady=10)
        param_frame.pack(fill='both', expand=True)
        
        # Current position display
        pos_display_frame = tk.LabelFrame(param_frame, text="Current Status",
                                         font=('Segoe UI', 10, 'bold'),
                                         bg='#f0f0f0', padx=10, pady=10)
        pos_display_frame.pack(fill='x', pady=(0, 10))
        
        self.position_label = tk.Label(pos_display_frame,
                                      text="Position: 0 steps",
                                      font=('Segoe UI', 12),
                                      bg='#f0f0f0')
        self.position_label.pack(pady=5)
        
        self.speed_label = tk.Label(pos_display_frame,
                                   text="Speed: 0 steps/sec",
                                   font=('Segoe UI', 12),
                                   bg='#f0f0f0')
        self.speed_label.pack(pady=5)
        
        # Reference search
        ref_frame = tk.LabelFrame(param_frame, text="Reference Search",
                                 font=('Segoe UI', 10, 'bold'),
                                 bg='#f0f0f0', padx=10, pady=10)
        ref_frame.pack(fill='x')
        
        self.ref_btn = ttk.Button(ref_frame, text="Start Reference Search",
                                 style='Warning.TButton',
                                 command=self.reference_search,
                                 state='disabled')
        self.ref_btn.pack(pady=5)
        
    def create_status_section(self, parent):
        """Create status and logging section"""
        status_frame = tk.LabelFrame(parent,
                                    text="Status Log",
                                    font=('Segoe UI', 10, 'bold'),
                                    bg='#f0f0f0',
                                    fg=self.colors['dark'],
                                    padx=10, pady=10)
        status_frame.pack(fill='x')
        
        # Create text widget with scrollbar
        text_frame = tk.Frame(status_frame, bg='#f0f0f0')
        text_frame.pack(fill='x')
        
        self.status_text = tk.Text(text_frame, height=4, width=70,
                                  font=('Consolas', 9),
                                  bg='#1e293b', fg='#f1f5f9',
                                  insertbackground='white')
        scrollbar = ttk.Scrollbar(text_frame, orient='vertical', command=self.status_text.yview)
        self.status_text.configure(yscrollcommand=scrollbar.set)
        
        self.status_text.pack(side='left', fill='x', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        self.log_message("Application started. Connect to begin controlling motors.")
        
    def refresh_ports(self):
        """Refresh available serial ports"""
        ports = [port.device for port in list_ports.comports()]
        self.port_combo['values'] = ports
        if ports:
            self.port_combo.set(ports[0])
        self.log_message(f"Found {len(ports)} serial ports")
        
    def toggle_connection(self):
        """Connect or disconnect from the motor"""
        if not self.connected:
            self.connect_motor()
        else:
            self.disconnect_motor()
            
    def connect_motor(self):
        """Connect to the motor"""
        try:
            port = self.port_var.get()
            if not port:
                messagebox.showerror("Error", "Please select a serial port")
                return
                
            address = int(self.address_var.get())
            
            self.log_message(f"Connecting to {port} (Module {address})...")
            
            # Open serial connection
            serial_port = Serial(port, baudrate=9600, timeout=1)
            self.bus = TMCL.connect(serial_port)
            self.motor = self.bus.get_motor(address)
            
            # Test connection by getting current position
            try:
                position = self.motor.axis.actual_position
                self.current_position = position
                self.connected = True
                self.update_connection_status()
                self.enable_motor_controls()
                self.log_message(f"✓ Connected successfully! Current position: {position}")
                
                # Start position monitoring
                self.start_position_monitoring()
                
            except Exception as e:
                serial_port.close()
                raise e
                
        except Exception as e:
            self.log_message(f"✗ Connection failed: {str(e)}")
            messagebox.showerror("Connection Error", f"Failed to connect: {str(e)}")
            
    def disconnect_motor(self):
        """Disconnect from the motor"""
        try:
            if self.bus and hasattr(self.bus, 'serial'):
                self.bus.serial.close()
            self.connected = False
            self.bus = None
            self.motor = None
            self.update_connection_status()
            self.disable_motor_controls()
            self.log_message("Disconnected from motor")
        except Exception as e:
            self.log_message(f"Error during disconnection: {str(e)}")
            
    def update_connection_status(self):
        """Update connection status indicators"""
        if self.connected:
            self.status_indicator.config(fg=self.colors['success'])
            self.status_label.config(text="Connected", fg=self.colors['success'])
            self.connect_btn.config(text="Disconnect", style='Danger.TButton')
        else:
            self.status_indicator.config(fg=self.colors['danger'])
            self.status_label.config(text="Disconnected", fg=self.colors['secondary'])
            self.connect_btn.config(text="Connect", style='Success.TButton')
            
    def enable_motor_controls(self):
        """Enable motor control buttons"""
        controls = [self.left_btn, self.right_btn, self.stop_btn, 
                   self.abs_move_btn, self.rel_move_btn, self.ref_btn]
        for control in controls:
            control.config(state='normal')
            
    def disable_motor_controls(self):
        """Disable motor control buttons"""
        controls = [self.left_btn, self.right_btn, self.stop_btn,
                   self.abs_move_btn, self.rel_move_btn, self.ref_btn]
        for control in controls:
            control.config(state='disabled')
            
    def rotate_left(self):
        """Rotate motor left"""
        if not self.motor:
            return
        try:
            velocity = int(self.velocity_var.get())
            self.motor.rotate_left(velocity)
            self.log_message(f"Rotating left at {velocity} steps/sec")
        except Exception as e:
            self.log_message(f"Error rotating left: {str(e)}")
            
    def rotate_right(self):
        """Rotate motor right"""
        if not self.motor:
            return
        try:
            velocity = int(self.velocity_var.get())
            self.motor.rotate_right(velocity)
            self.log_message(f"Rotating right at {velocity} steps/sec")
        except Exception as e:
            self.log_message(f"Error rotating right: {str(e)}")
            
    def stop_motor(self):
        """Stop motor movement"""
        if not self.motor:
            return
        try:
            self.motor.stop()
            self.log_message("Motor stopped")
        except Exception as e:
            self.log_message(f"Error stopping motor: {str(e)}")
            
    def move_absolute(self):
        """Move to absolute position"""
        if not self.motor:
            return
        try:
            position = int(self.abs_pos_var.get())
            self.motor.move_absolute(position)
            self.log_message(f"Moving to absolute position: {position}")
        except Exception as e:
            self.log_message(f"Error moving to absolute position: {str(e)}")
            
    def move_relative(self):
        """Move by relative offset"""
        if not self.motor:
            return
        try:
            offset = int(self.rel_pos_var.get())
            self.motor.move_relative(offset)
            self.log_message(f"Moving by relative offset: {offset}")
        except Exception as e:
            self.log_message(f"Error moving by relative offset: {str(e)}")
            
    def reference_search(self):
        """Start reference search"""
        if not self.motor:
            return
        try:
            self.motor.reference_search(0)  # RFS_START
            self.log_message("Reference search started")
        except Exception as e:
            self.log_message(f"Error starting reference search: {str(e)}")
            
    def start_position_monitoring(self):
        """Start monitoring motor position in background"""
        def monitor():
            while self.connected and self.motor:
                try:
                    position = self.motor.axis.actual_position
                    speed = self.motor.axis.actual_speed
                    
                    self.root.after(0, lambda: self.update_position_display(position, speed))
                    time.sleep(0.5)  # Update every 500ms
                except:
                    break
                    
        thread = threading.Thread(target=monitor, daemon=True)
        thread.start()
        
    def update_position_display(self, position, speed):
        """Update position and speed display"""
        self.position_label.config(text=f"Position: {position} steps")
        self.speed_label.config(text=f"Speed: {speed} steps/sec")
        
    def log_message(self, message):
        """Add message to status log"""
        timestamp = time.strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        # Only log if status_text widget exists
        if hasattr(self, 'status_text'):
            self.status_text.insert(tk.END, log_entry)
            self.status_text.see(tk.END)
        

def main():
    """Main application entry point"""
    root = tk.Tk()
    app = ModernTMCLController(root)
    
    # Center window on screen
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()


if __name__ == "__main__":
    main()
