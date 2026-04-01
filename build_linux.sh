#!/bin/bash
# Build script for Linux executable

echo "Building Regenerative Addresses Tool Pro v3.0 for Linux..."

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf build/ dist/

# Build the executable
echo "Building executable..."
python setup.py build

# Check if build was successful
if [ $? -eq 0 ]; then
    echo "Build successful!"
    echo "Executable location: build/exe.linux-x86_64-3.13/RegenerativeAddressesPro.exe"
    
    # Make executable
    chmod +x build/exe.linux-x86_64-3.13/RegenerativeAddressesPro.exe
    
    # Create distribution directory
    echo "Creating Linux distribution..."
    mkdir -p dist/RegenerativeAddressesPro_Linux
    
    # Copy executable and files
    cp build/exe.linux-x86_64-3.13/RegenerativeAddressesPro.exe dist/RegenerativeAddressesPro_Linux/
    cp -r build/exe.linux-x86_64-3.13/lib dist/RegenerativeAddressesPro_Linux/
    cp build/exe.linux-x86_64-3.13/*.txt dist/RegenerativeAddressesPro_Linux/ 2>/dev/null
    cp build/exe.linux-x86_64-3.13/*.py dist/RegenerativeAddressesPro_Linux/ 2>/dev/null
    cp build/exe.linux-x86_64-3.13/*.php dist/RegenerativeAddressesPro_Linux/ 2>/dev/null
    cp build/exe.linux-x86_64-3.13/*.json dist/RegenerativeAddressesPro_Linux/ 2>/dev/null
    cp build/exe.linux-x86_64-3.13/*.bat dist/RegenerativeAddressesPro_Linux/ 2>/dev/null
    cp -r build/exe.linux-x86_64-3.13/src dist/RegenerativeAddressesPro_Linux/ 2>/dev/null
    
    # Copy launcher script
    cp run_linux.sh dist/RegenerativeAddressesPro_Linux/
    chmod +x dist/RegenerativeAddressesPro_Linux/run_linux.sh
    
    # Create README
    cat > dist/RegenerativeAddressesPro_Linux/README_LINUX.md << 'EOF'
# Regenerative Addresses Tool Pro v3.0 - Linux

## Installation and Usage

### Requirements
- Linux x86_64 system
- Python 3.9+ (if running from source)
- X11 display server (for GUI)

### Running the Tool

#### Method 1: Using the Launcher Script
```bash
./run_linux.sh
```

#### Method 2: Direct Execution
```bash
./RegenerativeAddressesPro.exe
```

### Features
- Professional link regeneration with 10 techniques
- Real-time security scanning and protection
- System hardening tools
- Network vulnerability assessment
- Password security analysis
- Comprehensive security reporting
- Educational networking security tools

### Security Features
- System vulnerability scanner
- Password strength analyzer
- Network security auditor
- System hardening utilities
- Real-time protection monitoring
- Professional security reporting

### Troubleshooting

#### Permission Denied
```bash
chmod +x RegenerativeAddressesPro.exe
chmod +x run_linux.sh
```

#### Missing Libraries
The tool includes most required libraries. If you encounter issues:
```bash
sudo apt-get install python3-tk python3-pil python3-pil.imagetk
```

#### Display Issues
If GUI doesn't display:
```bash
export DISPLAY=:0
./run_linux.sh
```

### Support
For issues and updates, check the GitHub repository.

### Legal Notice
This tool is for legitimate security testing and educational purposes only.
EOF
    
    # Create archive
    echo "Creating distribution archive..."
    cd dist
    tar -czf RegenerativeAddressesPro_v3.0_Linux.tar.gz RegenerativeAddressesPro_Linux/
    cd ..
    
    echo "Linux distribution created successfully!"
    echo "Archive: dist/RegenerativeAddressesPro_v3.0_Linux.tar.gz"
    echo "Directory: dist/RegenerativeAddressesPro_Linux/"
    
else
    echo "Build failed!"
    exit 1
fi
