#!/usr/bin/env python3
"""
macOS Silicon Cache & Temp File Cleaner - Desktop GUI Application
Modern desktop interface for the cache cleaning utility

Created by: Tommy Xaypanya
GitHub: https://github.com/knightdev
Version: 1.0.0
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import queue
import sys
import os
from pathlib import Path
import subprocess
import time
from cache_cleaner import MacOSCacheCleaner

class CacheCleanerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("macOS Cache Cleaner")
        self.root.geometry("800x700")
        self.root.minsize(600, 500)
        
        # Configure style
        self.setup_styles()
        
        # Variables
        self.cleaner = None
        self.cleaning_thread = None
        self.is_cleaning = False
        self.message_queue = queue.Queue()
        
        # Create GUI
        self.create_widgets()
        
        # Start message processor
        self.process_queue()
        
        # Center window
        self.center_window()

    def setup_styles(self):
        """Configure ttk styles for a modern look"""
        style = ttk.Style()
        
        # Configure colors
        bg_color = "#f8f9fa"
        accent_color = "#007bff"
        success_color = "#28a745"
        warning_color = "#ffc107"
        danger_color = "#dc3545"
        
        self.root.configure(bg=bg_color)
        
        # Button styles
        style.configure("Accent.TButton", 
                       background=accent_color,
                       foreground="white",
                       borderwidth=0,
                       focuscolor='none')
        
        style.configure("Success.TButton",
                       background=success_color,
                       foreground="white", 
                       borderwidth=0,
                       focuscolor='none')
        
        style.configure("Warning.TButton",
                       background=warning_color,
                       foreground="black",
                       borderwidth=0,
                       focuscolor='none')

    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def create_widgets(self):
        """Create the main GUI widgets"""
        # Header frame
        header_frame = ttk.Frame(self.root)
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        # Title and icon
        title_label = ttk.Label(header_frame, text="🧹 macOS Cache Cleaner", 
                               font=("SF Pro Display", 24, "bold"))
        title_label.pack()
        
        subtitle_label = ttk.Label(header_frame, 
                                  text="Free up disk space by cleaning cache and temporary files",
                                  font=("SF Pro Text", 12))
        subtitle_label.pack(pady=(5, 0))
        
        # Creator credit
        credit_label = ttk.Label(header_frame, 
                               text="Created by Tommy Xaypanya (@knightdev)",
                               font=("SF Pro Text", 10), 
                               foreground="#666666")
        credit_label.pack(pady=(2, 0))
        
        # Disk usage frame
        self.create_disk_usage_frame()
        
        # Options frame
        self.create_options_frame()
        
        # Action buttons frame
        self.create_action_buttons_frame()
        
        # Progress frame
        self.create_progress_frame()
        
        # Output frame
        self.create_output_frame()
        
        # Status bar
        self.create_status_bar()

    def create_disk_usage_frame(self):
        """Create disk usage display"""
        disk_frame = ttk.LabelFrame(self.root, text="Disk Usage", padding=15)
        disk_frame.pack(fill="x", padx=20, pady=10)
        
        self.disk_info = ttk.Label(disk_frame, text="Loading disk information...", 
                                  font=("SF Mono", 11))
        self.disk_info.pack()
        
        # Update disk info
        self.update_disk_info()

    def create_options_frame(self):
        """Create cleaning options"""
        options_frame = ttk.LabelFrame(self.root, text="Cleaning Options", padding=15)
        options_frame.pack(fill="x", padx=20, pady=10)
        
        # Create option variables
        self.dry_run_var = tk.BooleanVar(value=True)
        self.verbose_var = tk.BooleanVar(value=True)
        self.skip_trash_var = tk.BooleanVar(value=False)
        self.skip_maintenance_var = tk.BooleanVar(value=False)
        self.find_large_files_var = tk.BooleanVar(value=False)
        
        # Create checkboxes in a grid
        options_grid = ttk.Frame(options_frame)
        options_grid.pack(fill="x")
        
        ttk.Checkbutton(options_grid, text="🔍 Dry Run (safe preview)", 
                       variable=self.dry_run_var).grid(row=0, column=0, sticky="w", padx=(0, 20))
        
        ttk.Checkbutton(options_grid, text="📝 Verbose output", 
                       variable=self.verbose_var).grid(row=0, column=1, sticky="w")
        
        ttk.Checkbutton(options_grid, text="🗑️ Skip emptying trash", 
                       variable=self.skip_trash_var).grid(row=1, column=0, sticky="w", padx=(0, 20), pady=(5, 0))
        
        ttk.Checkbutton(options_grid, text="⚙️ Skip system maintenance", 
                       variable=self.skip_maintenance_var).grid(row=1, column=1, sticky="w", pady=(5, 0))
        
        ttk.Checkbutton(options_grid, text="🔍 Find large files", 
                       variable=self.find_large_files_var).grid(row=2, column=0, sticky="w", pady=(5, 0))

    def create_action_buttons_frame(self):
        """Create action buttons"""
        buttons_frame = ttk.Frame(self.root)
        buttons_frame.pack(fill="x", padx=20, pady=10)
        
        # Quick actions frame
        quick_frame = ttk.LabelFrame(buttons_frame, text="Quick Actions", padding=10)
        quick_frame.pack(fill="x", pady=(0, 10))
        
        quick_buttons = ttk.Frame(quick_frame)
        quick_buttons.pack()
        
        self.scan_btn = ttk.Button(quick_buttons, text="🔍 Scan Only", 
                                  command=self.scan_only,
                                  style="Warning.TButton")
        self.scan_btn.pack(side="left", padx=(0, 10))
        
        self.clean_safe_btn = ttk.Button(quick_buttons, text="🧹 Safe Clean", 
                                        command=self.clean_safe,
                                        style="Success.TButton")
        self.clean_safe_btn.pack(side="left", padx=(0, 10))
        
        self.clean_deep_btn = ttk.Button(quick_buttons, text="🔥 Deep Clean", 
                                        command=self.clean_deep,
                                        style="Accent.TButton")
        self.clean_deep_btn.pack(side="left")
        
        # Main action frame
        action_frame = ttk.Frame(buttons_frame)
        action_frame.pack(fill="x")
        
        self.start_btn = ttk.Button(action_frame, text="▶️ Start Cleaning", 
                                   command=self.start_cleaning,
                                   style="Accent.TButton")
        self.start_btn.pack(side="left")
        
        self.stop_btn = ttk.Button(action_frame, text="⏹️ Stop", 
                                  command=self.stop_cleaning,
                                  state="disabled")
        self.stop_btn.pack(side="left", padx=(10, 0))
        
        # Utility buttons
        utility_frame = ttk.Frame(action_frame)
        utility_frame.pack(side="right")
        
        ttk.Button(utility_frame, text="📁 Open Logs", 
                  command=self.open_logs).pack(side="right", padx=(10, 0))
        
        ttk.Button(utility_frame, text="💾 Export Report", 
                  command=self.export_report).pack(side="right", padx=(10, 0))

    def create_progress_frame(self):
        """Create progress indicators"""
        progress_frame = ttk.LabelFrame(self.root, text="Progress", padding=10)
        progress_frame.pack(fill="x", padx=20, pady=10)
        
        # Progress bar
        self.progress = ttk.Progressbar(progress_frame, mode='indeterminate')
        self.progress.pack(fill="x", pady=(0, 10))
        
        # Status labels
        status_frame = ttk.Frame(progress_frame)
        status_frame.pack(fill="x")
        
        self.current_action = ttk.Label(status_frame, text="Ready to clean")
        self.current_action.pack(side="left")
        
        self.space_freed = ttk.Label(status_frame, text="Space freed: 0 B")
        self.space_freed.pack(side="right")

    def create_output_frame(self):
        """Create output text area"""
        output_frame = ttk.LabelFrame(self.root, text="Output", padding=10)
        output_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Text widget with scrollbar
        self.output_text = scrolledtext.ScrolledText(output_frame, 
                                                    height=15,
                                                    font=("SF Mono", 10),
                                                    wrap=tk.WORD)
        self.output_text.pack(fill="both", expand=True)
        
        # Configure text tags for colored output
        self.output_text.tag_configure("info", foreground="#007bff")
        self.output_text.tag_configure("success", foreground="#28a745")
        self.output_text.tag_configure("warning", foreground="#ffc107")
        self.output_text.tag_configure("error", foreground="#dc3545")

    def create_status_bar(self):
        """Create status bar"""
        self.status_bar = ttk.Label(self.root, text="Ready", 
                                   relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side="bottom", fill="x")

    def update_disk_info(self):
        """Update disk usage information"""
        try:
            result = subprocess.run(['df', '-h', '/'], capture_output=True, text=True)
            lines = result.stdout.strip().split('\n')
            if len(lines) >= 2:
                parts = lines[1].split()
                if len(parts) >= 6:
                    filesystem = parts[0]
                    size = parts[1]
                    used = parts[2]
                    available = parts[3]
                    percent = parts[4]
                    mount = parts[5]
                    
                    disk_text = f"💾 {filesystem}: {used} used of {size} ({percent} full) - {available} available"
                    self.disk_info.config(text=disk_text)
        except Exception as e:
            self.disk_info.config(text=f"Error getting disk info: {e}")

    def scan_only(self):
        """Run scan only mode"""
        self.dry_run_var.set(True)
        self.verbose_var.set(True)
        self.find_large_files_var.set(True)
        self.start_cleaning()

    def clean_safe(self):
        """Run safe cleaning mode"""
        self.dry_run_var.set(False)
        self.skip_trash_var.set(True)
        self.skip_maintenance_var.set(True)
        self.start_cleaning()

    def clean_deep(self):
        """Run deep cleaning mode"""
        result = messagebox.askyesno("Deep Clean", 
                                   "Deep clean will remove all cache files, empty trash, and run system maintenance.\n\n" +
                                   "This is safe but may require administrator privileges.\n\n" +
                                   "Continue?")
        if result:
            self.dry_run_var.set(False)
            self.skip_trash_var.set(False)
            self.skip_maintenance_var.set(False)
            self.start_cleaning()

    def start_cleaning(self):
        """Start the cleaning process in a separate thread"""
        if self.is_cleaning:
            return
            
        # Clear output
        self.output_text.delete(1.0, tk.END)
        
        # Update UI state
        self.is_cleaning = True
        self.start_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        self.progress.start(10)
        
        # Create cleaner instance
        self.cleaner = GUICleanerWrapper(
            dry_run=self.dry_run_var.get(),
            verbose=self.verbose_var.get(),
            message_queue=self.message_queue
        )
        
        # Start cleaning thread
        self.cleaning_thread = threading.Thread(
            target=self.run_cleaning,
            args=(
                self.skip_trash_var.get(),
                self.skip_maintenance_var.get(),
                self.find_large_files_var.get()
            ),
            daemon=True
        )
        self.cleaning_thread.start()

    def run_cleaning(self, skip_trash, skip_maintenance, find_large_files):
        """Run the cleaning process"""
        try:
            self.message_queue.put(("status", "Starting cleanup..."))
            self.cleaner.run(skip_trash, skip_maintenance, find_large_files)
            self.message_queue.put(("complete", f"Cleanup complete! Total freed: {self.cleaner.format_size(self.cleaner.total_freed)}"))
        except Exception as e:
            self.message_queue.put(("error", f"Error during cleanup: {e}"))
        finally:
            self.message_queue.put(("finished", ""))

    def stop_cleaning(self):
        """Stop the cleaning process"""
        if self.cleaning_thread and self.cleaning_thread.is_alive():
            # Note: Python threads can't be forcefully stopped safely
            # This is a limitation, but the cleaning operations are generally quick
            messagebox.showinfo("Stop Cleaning", 
                               "Cleaning operations cannot be stopped mid-process for safety.\n" +
                               "Please wait for the current operation to complete.")

    def process_queue(self):
        """Process messages from the cleaning thread"""
        try:
            while True:
                message_type, message = self.message_queue.get_nowait()
                
                if message_type == "output":
                    self.append_output(message)
                elif message_type == "status":
                    self.current_action.config(text=message)
                    self.status_bar.config(text=message)
                elif message_type == "space_freed":
                    self.space_freed.config(text=f"Space freed: {message}")
                elif message_type == "complete":
                    self.append_output(message, "success")
                    self.current_action.config(text="Cleanup complete!")
                    self.update_disk_info()
                elif message_type == "error":
                    self.append_output(message, "error")
                    self.current_action.config(text="Error occurred")
                elif message_type == "finished":
                    self.cleanup_finished()
                    
        except queue.Empty:
            pass
        
        # Schedule next check
        self.root.after(100, self.process_queue)

    def append_output(self, text, tag="info"):
        """Append text to the output area"""
        self.output_text.insert(tk.END, text + "\n", tag)
        self.output_text.see(tk.END)

    def cleanup_finished(self):
        """Reset UI after cleaning is finished"""
        self.is_cleaning = False
        self.start_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
        self.progress.stop()
        self.status_bar.config(text="Ready")

    def open_logs(self):
        """Open the logs directory"""
        logs_dir = Path.home() / "Library/Logs"
        if logs_dir.exists():
            subprocess.run(['open', str(logs_dir)])
        else:
            messagebox.showwarning("Logs", "Logs directory not found")

    def export_report(self):
        """Export cleaning report to file"""
        if not hasattr(self, 'output_text'):
            return
            
        content = self.output_text.get(1.0, tk.END)
        if not content.strip():
            messagebox.showwarning("Export", "No output to export")
            return
            
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Export Cleaning Report"
        )
        
        if filename:
            try:
                with open(filename, 'w') as f:
                    f.write(f"macOS Cache Cleaner Report\n")
                    f.write(f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write("=" * 50 + "\n\n")
                    f.write(content)
                messagebox.showinfo("Export", f"Report exported to {filename}")
            except Exception as e:
                messagebox.showerror("Export Error", f"Failed to export report: {e}")


class GUICleanerWrapper(MacOSCacheCleaner):
    """Wrapper for MacOSCacheCleaner that sends output to GUI"""
    
    def __init__(self, dry_run=False, verbose=False, message_queue=None):
        super().__init__(dry_run, verbose)
        self.message_queue = message_queue
        
    def print_message(self, message, msg_type="output"):
        """Send message to GUI queue"""
        if self.message_queue:
            self.message_queue.put((msg_type, message))
        
    def clean_directory(self, cache_dir):
        """Override to send progress updates"""
        self.print_message(f"Cleaning: {cache_dir}", "status")
        freed = super().clean_directory(cache_dir)
        if freed > 0:
            self.print_message(f"Freed {self.format_size(freed)} from {cache_dir}")
            self.print_message(self.format_size(self.total_freed), "space_freed")
        return freed
        
    def run(self, skip_trash=False, skip_maintenance=False, find_large_files=False):
        """Override run method with GUI updates"""
        self.print_message("🧹 macOS Silicon Cache & Temp File Cleaner")
        self.print_message("=" * 50)
        
        if self.dry_run:
            self.print_message("🔍 DRY RUN MODE - No files will be deleted")
        
        # Show disk usage
        try:
            result = subprocess.run(['df', '-h', '/'], capture_output=True, text=True)
            lines = result.stdout.strip().split('\n')
            if len(lines) >= 2:
                self.print_message("💾 Current Disk Usage:")
                self.print_message(f"  {lines[1]}")
        except:
            pass
        
        self.print_message("")
        
        # Run cleaning operations
        self.print_message("🖥️  Cleaning System Caches...", "status")
        self.clean_system_caches()
        
        self.print_message("🌐 Cleaning Browser Data...", "status") 
        self.clean_browser_data()
        
        self.print_message("🗑️  Cleaning Temporary Files...", "status")
        self.clean_temp_files()
        
        self.print_message("💻 Cleaning Development Caches...", "status")
        self.clean_development_caches()
        
        self.print_message("📋 Cleaning Log Files...", "status")
        self.clean_logs()
        
        if not skip_trash:
            self.print_message("🗂️  Emptying Trash...", "status")
            self.empty_trash()
            
        if not skip_maintenance:
            self.print_message("🔧 Running macOS Maintenance...", "status")
            self.run_maintenance_scripts()
            
        if find_large_files:
            self.print_message("🔍 Scanning for Large Files...", "status")
            self.scan_large_files()
        
        self.print_message("")
        self.print_message("=" * 50)
        self.print_message(f"🎉 Cleaning Complete!")
        self.print_message(f"Total space freed: {self.format_size(self.total_freed)}")
        
        if self.dry_run:
            self.print_message("(This was a dry run - no files were actually deleted)")


def main():
    # Check if running on macOS
    if sys.platform != "darwin":
        messagebox.showerror("Platform Error", 
                           "This application is designed for macOS only.")
        return
    
    # Create and run the GUI
    root = tk.Tk()
    app = CacheCleanerGUI(root)
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()