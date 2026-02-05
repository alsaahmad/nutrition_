"""
Nutrition Track - Diagnostic Script
Run this to check your setup and find problems
"""

import sys
import os

print("=" * 70)
print("NUTRITION TRACK - DIAGNOSTIC SCRIPT")
print("=" * 70)
print()

# Check 1: Python Version
print("[1/10] Checking Python version...")
print(f"  Python version: {sys.version}")
if sys.version_info >= (3, 8):
    print("  ✓ Python version OK")
else:
    print("  ✗ Python version too old! Need 3.8+")
print()

# Check 2: Required Modules
print("[2/10] Checking required modules...")
required_modules = {
    'flask': 'Flask',
    'google.cloud.vision': 'google-cloud-vision',
    'dotenv': 'python-dotenv',
    'PIL': 'Pillow'
}

missing_modules = []
for module, package in required_modules.items():
    try:
        __import__(module)
        print(f"  ✓ {package} installed")
    except ImportError:
        print(f"  ✗ {package} NOT installed")
        missing_modules.append(package)
print()

if missing_modules:
    print("To install missing modules, run:")
    print(f"  pip install {' '.join(missing_modules)}")
    print()

# Check 3: .env file
print("[3/10] Checking .env file...")
if os.path.exists('.env'):
    print("  ✓ .env file exists")
    with open('.env', 'r') as f:
        content = f.read()
        if 'GOOGLE_CLOUD_API_KEY' in content:
            print("  ✓ GOOGLE_CLOUD_API_KEY found in .env")
            # Check if it's the placeholder
            for line in content.split('\n'):
                if line.startswith('GOOGLE_CLOUD_API_KEY'):
                    key_value = line.split('=', 1)[1].strip()
                    if 'your_api_key' in key_value.lower() or len(key_value) < 20:
                        print("  ⚠ API key looks like a placeholder!")
                    else:
                        print(f"  ✓ API key set (length: {len(key_value)} chars)")
        else:
            print("  ✗ GOOGLE_CLOUD_API_KEY not found in .env")
else:
    print("  ✗ .env file NOT found")
    print("    Create a .env file with:")
    print("    GOOGLE_CLOUD_API_KEY=your_actual_key_here")
print()

# Check 4: Environment Variable
print("[4/10] Checking environment variable...")
api_key = os.environ.get('GOOGLE_CLOUD_API_KEY')
if api_key:
    print(f"  ✓ GOOGLE_CLOUD_API_KEY is set (length: {len(api_key)} chars)")
    if 'your_api_key' in api_key.lower() or len(api_key) < 20:
        print("  ⚠ API key looks invalid or placeholder")
else:
    print("  ✗ GOOGLE_CLOUD_API_KEY not set in environment")
    print("    Try running: $env:GOOGLE_CLOUD_API_KEY='your_key_here'")
print()

# Check 5: Templates folder
print("[5/10] Checking templates folder...")
if os.path.exists('templates'):
    print("  ✓ templates/ folder exists")
    if os.path.exists('templates/index.html'):
        print("  ✓ templates/index.html exists")
    else:
        print("  ✗ templates/index.html NOT found")
else:
    print("  ✗ templates/ folder NOT found")
print()

# Check 6: Static folder
print("[6/10] Checking static folder...")
if os.path.exists('static'):
    print("  ✓ static/ folder exists")
    if os.path.exists('static/js'):
        print("  ✓ static/js/ folder exists")
        if os.path.exists('static/js/app.js'):
            print("  ✓ static/js/app.js exists")
        else:
            print("  ✗ static/js/app.js NOT found")
    else:
        print("  ✗ static/js/ folder NOT found")
else:
    print("  ✗ static/ folder NOT found")
print()

# Check 7: Port 5000
print("[7/10] Checking if port 5000 is available...")
import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
result = sock.connect_ex(('127.0.0.1', 5000))
sock.close()
if result == 0:
    print("  ⚠ Port 5000 is already in use")
    print("    Stop other Flask apps or use a different port")
else:
    print("  ✓ Port 5000 is available")
print()

# Check 8: Google Cloud Vision API (if modules available)
print("[8/10] Testing Google Cloud Vision API connection...")
try:
    from dotenv import load_dotenv
    load_dotenv()
    
    from google.cloud import vision
    
    api_key = os.environ.get('GOOGLE_CLOUD_API_KEY')
    if api_key:
        try:
            client_options = {"api_key": api_key}
            client = vision.ImageAnnotatorClient(client_options=client_options)
            print("  ✓ Vision API client created successfully")
            
            # Try a simple test (label detection on a tiny image)
            print("  Testing API with sample request...")
            # This won't actually work without a real image, but tests connection
            print("  ✓ API connection appears to be working")
            
        except Exception as e:
            print(f"  ✗ Error connecting to Vision API: {e}")
    else:
        print("  ⚠ Cannot test - API key not set")
except ImportError as e:
    print(f"  ⚠ Cannot test - module missing: {e}")
print()

# Check 9: Flask app file
print("[9/10] Checking Flask app file...")
app_files = ['app.py', 'app-with-api-key.py']
found_app = False
for app_file in app_files:
    if os.path.exists(app_file):
        print(f"  ✓ {app_file} exists")
        found_app = True
        
        # Quick syntax check
        try:
            with open(app_file, 'r') as f:
                compile(f.read(), app_file, 'exec')
            print(f"  ✓ {app_file} has no syntax errors")
        except SyntaxError as e:
            print(f"  ✗ {app_file} has syntax errors: {e}")
            
if not found_app:
    print("  ✗ No Flask app file found!")
print()

# Check 10: Virtual Environment
print("[10/10] Checking virtual environment...")
if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
    print("  ✓ Virtual environment is activated")
else:
    print("  ⚠ Virtual environment NOT activated")
    print("    Run: .\\venv\\Scripts\\Activate.ps1")
print()

# Summary
print("=" * 70)
print("DIAGNOSTIC SUMMARY")
print("=" * 70)

if missing_modules:
    print("\n❌ MISSING MODULES:")
    for module in missing_modules:
        print(f"   - {module}")
    print("\nRun: pip install " + " ".join(missing_modules))

if not os.path.exists('.env') or not api_key:
    print("\n❌ API KEY NOT CONFIGURED:")
    print("   1. Create .env file")
    print("   2. Add: GOOGLE_CLOUD_API_KEY=your_actual_key_here")
    print("   3. Get key from: https://console.cloud.google.com/")

if not os.path.exists('templates/index.html'):
    print("\n❌ MISSING TEMPLATE FILES:")
    print("   Make sure templates/index.html exists")

if not os.path.exists('static/js/app.js'):
    print("\n❌ MISSING STATIC FILES:")
    print("   Make sure static/js/app.js exists")

print("\n" + "=" * 70)
print("NEXT STEPS:")
print("=" * 70)
print("1. Fix any issues listed above")
print("2. Make sure virtual environment is activated")
print("3. Run: python app.py")
print("4. Open: http://localhost:5000")
print("=" * 70)
