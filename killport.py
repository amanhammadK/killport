#!/usr/bin/env python3
import argparse
import subprocess
import sys
import os
import platform

# ANSI color codes for terminal output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"

def log_success(msg):
    print(f"{GREEN}✔ {msg}{RESET}")

def log_error(msg):
    print(f"{RED}✘ {msg}{RESET}")

def log_warning(msg):
    print(f"{YELLOW}⚠ {msg}{RESET}")

def kill_windows(port):
    """
    Windows implementation using netstat and taskkill.
    """
    try:
        # Find PIDs associated with the port
        cmd = f"netstat -ano | findstr :{port}"
        # Using shell=True for findstr pipe
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, _ = process.communicate()
        output = stdout.decode().strip()

        if not output:
            log_error(f"No process found on port {port}")
            return

        # Extract unique PIDs from the last column
        pids = set()
        for line in output.splitlines():
            parts = line.split()
            if parts:
                pids.add(parts[-1])

        if not pids:
            log_error(f"No process found on port {port}")
            return

        for pid in pids:
            try:
                # Force kill as specified in requirements
                subprocess.check_call(f"taskkill /F /PID {pid}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                log_success(f"PID {pid} killed on port {port}")
            except subprocess.CalledProcessError:
                log_warning(f"Failed to kill process {pid} on port {port}")
                
    except Exception as e:
        log_error(f"An error occurred: {str(e)}")

def kill_unix(port, force):
    """
    Linux/macOS implementation using lsof and kill.
    """
    try:
        # Get PIDs using lsof
        cmd = ["lsof", "-ti", f"tcp:{port}"]
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, _ = process.communicate()
        output = stdout.decode().strip()

        if not output:
            log_error(f"No process found on port {port}")
            return

        pids = output.splitlines()
        # SIGKILL (9) if force, else SIGTERM (15)
        signal = "-9" if force else "-15"

        for pid in pids:
            try:
                subprocess.check_call(["kill", signal, pid])
                log_success(f"PID {pid} killed on port {port}")
            except subprocess.CalledProcessError:
                log_warning(f"Failed to kill process {pid} on port {port}")
                
    except FileNotFoundError:
        log_error("Error: 'lsof' command not found. Please install it.")
    except Exception as e:
        log_error(f"An error occurred: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description="Kill the process hogging your port.")
    parser.add_argument("port", type=int, help="The port number you want to clear")
    parser.add_argument("--force", action="store_true", help="Use SIGKILL on Linux/macOS instead of SIGTERM")
    
    args = parser.parse_args()

    # Cross-platform check
    if sys.platform == "win32":
        kill_windows(args.port)
    else:
        kill_unix(args.port, args.force)

if __name__ == "__main__":
    main()
