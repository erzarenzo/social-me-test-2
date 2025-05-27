import os
import sys
import json
import importlib.util
import subprocess

# Define base directory
BASE_DIR = "/root/socialme/social-me-test-2/"
APP_DIR = os.path.join(BASE_DIR, "app")
CRAWLER_DIR = os.path.join(APP_DIR, "crawlers")
VENV_DIR = os.path.join(BASE_DIR, "myenv")
EXPECTED_FILES = ["app.py", "universal_crawler.py", "requirements.txt"]

# Function to check if a virtual environment exists and is active
def check_virtual_env():
    venv_exists = os.path.exists(VENV_DIR)
    venv_active = sys.prefix != sys.base_prefix

    return {
        "virtual_env_exists": venv_exists,
        "virtual_env_active": venv_active,
        "venv_path": VENV_DIR if venv_exists else "Not found"
    }

# Function to check Python dependencies
def check_installed_packages():
    required_packages = ["flask", "requests", "beautifulsoup4", "lxml"]
    missing_packages = []

    for package in required_packages:
        spec = importlib.util.find_spec(package)
        if spec is None:
            missing_packages.append(package)

    return {
        "installed_packages": [pkg for pkg in required_packages if pkg not in missing_packages],
        "missing_packages": missing_packages
    }

# Function to scan directory structure
def scan_directory(root_dir):
    structure = {}
    for dirpath, dirnames, filenames in os.walk(root_dir):
        relative_path = os.path.relpath(dirpath, root_dir)
        if relative_path == ".":
            relative_path = "/"
        structure[relative_path] = {"dirs": dirnames, "files": filenames}
    return structure

# Function to check file imports and dependencies
def check_file_imports():
    import_check = {}

    # List of files to check
    files_to_check = {
        "Flask API": os.path.join(APP_DIR, "app.py"),
        "Universal Crawler": os.path.join(BASE_DIR, "universal_crawler.py")
    }

    for name, file_path in files_to_check.items():
        if os.path.exists(file_path):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    imports = [line for line in content.split("\n") if line.startswith("import") or line.startswith("from")]
                    import_check[name] = imports
            except Exception as e:
                import_check[name] = f"Error reading file: {str(e)}"
        else:
            import_check[name] = "File not found"

    return import_check

# Function to check if Flask is running
def check_flask_running():
    result = subprocess.run(["lsof", "-i", ":5001"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return "LISTEN" in result.stdout

# Run all checks and output JSON results
def run_full_diagnostics():
    print("\n🚀 Running Full SocialMe Diagnostic Tool...\n")

    diagnostics = {
        "python_version": sys.version,
        "virtual_env": check_virtual_env(),
        "installed_packages": check_installed_packages(),
        "project_structure": scan_directory(BASE_DIR),
        "file_imports": check_file_imports(),
        "flask_running": check_flask_running()
    }

    # Save to JSON file
    with open(os.path.join(BASE_DIR, "diagnostic_output.json"), "w") as f:
        json.dump(diagnostics, f, indent=4)

    print("✅ Diagnostic completed! Output saved to `diagnostic_output.json`")

if __name__ == "__main__":
    run_full_diagnostics()
