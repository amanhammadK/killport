# killport

Kill the process hogging your port. One command. Zero memory strain.

![Python](https://img.shields.io/badge/python-3.6+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-windows%20%7C%20macos%20%7C%20linux-lightgrey.svg)

![Demo](demo.gif)

## Why?
"Because `kill -9 $(lsof -t -i:3000)` is too long to remember when your server refuses to start."

## Installation
Download `killport.py` and either:
1. Make it executable and move to your PATH:
   ```bash
   chmod +x killport.py
   # Then move to /usr/local/bin or similar
   ```
2. Or just run it directly with Python:
   ```bash
   python killport.py <port>
   ```

## Usage
```bash
# Kill process on port 3000
killport 3000

# Force kill with SIGKILL (Linux/macOS)
killport 3000 --force
```

## License
MIT
