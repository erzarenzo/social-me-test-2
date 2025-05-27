#!/usr/bin/env python3
import os
import sys
import json
import subprocess
import re
import ast
import importlib.util

class ProjectAnalyzer:
    def __init__(self, project_path):
        self.project_path = project_path
        self.report = {
            "project_overview": {},
            "dependencies": {
                "direct_imports": [],
                "package_requirements": [],
                "installed_packages": []
            },
            "code_structure": {
                "files": {},
                "modules": {},
                "classes": {},
                "functions": {}
            },
            "potential_frameworks": [],
            "api_insights": [],
            "database_connections": []
        }

    def analyze_project(self):
        # Project overview
        self._get_project_overview()
        
        # Scan files
        self._scan_project_files()
        
        # Analyze dependencies
        self._analyze_dependencies()
        
        # Detect frameworks and technologies
        self._detect_frameworks()
        
        return self.report

    def _get_project_overview(self):
        """Gather basic project information"""
        self.report["project_overview"] = {
            "root_path": self.project_path,
            "total_files": len(self._find_files()),
            "python_files": len(self._find_files(ext='.py')),
            "directories": len([d for d in os.listdir(self.project_path) 
                                if os.path.isdir(os.path.join(self.project_path, d))])
        }

    def _find_files(self, ext=None):
        """Find files in the project"""
        matches = []
        for root, _, filenames in os.walk(self.project_path):
            for filename in filenames:
                if ext is None or filename.endswith(ext):
                    matches.append(os.path.join(root, filename))
        return matches

    def _scan_project_files(self):
        """Deep scan of Python files"""
        for pyfile in self._find_files(ext='.py'):
            try:
                with open(pyfile, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    self._parse_python_file(pyfile, content)
            except Exception as e:
                print(f"Error parsing {pyfile}: {e}")

    def _parse_python_file(self, filepath, content):
        """Parse individual Python file"""
        # Relative path for reporting
        rel_path = os.path.relpath(filepath, self.project_path)
        
        # Parse file using AST
        try:
            tree = ast.parse(content)
        except SyntaxError:
            return

        # Extract imports
        imports = []
        from_imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.extend([name.name for name in node.names if name.name])
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    from_imports.append(node.module)

        # Extract classes and functions
        classes = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
        functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]

        # Store file analysis
        self.report["code_structure"]["files"][rel_path] = {
            "imports": imports + from_imports,
            "classes": classes,
            "functions": functions
        }

        # Collect unique imports
        self.report["dependencies"]["direct_imports"].extend(imports + from_imports)

    def _analyze_dependencies(self):
        """Analyze project dependencies"""
        # Check for requirements.txt
        req_file = os.path.join(self.project_path, 'requirements.txt')
        if os.path.exists(req_file):
            with open(req_file, 'r') as f:
                self.report["dependencies"]["package_requirements"] = [
                    line.strip() for line in f if line.strip() and not line.startswith('#')
                ]
        
        # Try to get installed packages
        try:
            pip_freeze = subprocess.check_output(['pip', 'freeze'], universal_newlines=True)
            self.report["dependencies"]["installed_packages"] = [
                line.strip() for line in pip_freeze.split('\n') if line.strip()
            ]
        except Exception:
            pass

    def _detect_frameworks(self):
        """Detect web frameworks and technologies"""
        framework_markers = {
            "FastAPI": ["fastapi", "uvicorn"],
            "Flask": ["flask"],
            "Django": ["django"],
            "SQLAlchemy": ["sqlalchemy"],
            "Requests": ["requests"],
            "Selenium": ["selenium"],
            "BeautifulSoup": ["beautifulsoup4"],
            "Anthropic": ["anthropic"],
            "OpenAI": ["openai"]
        }

        # Safely filter imports and requirements
        safe_imports = [imp for imp in self.report["dependencies"]["direct_imports"] if imp]
        safe_requirements = [req for req in self.report["dependencies"]["package_requirements"] if req]

        # Check imports and requirements
        for framework, markers in framework_markers.items():
            if any(any(marker in str(imp).lower() for marker in markers) 
                   for imp in safe_imports) or \
               any(any(marker in str(req).lower() for marker in markers) 
                   for req in safe_requirements):
                self.report["potential_frameworks"].append(framework)

def main():
    # Use current directory if no path provided
    project_path = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    
    # Create and run analyzer
    analyzer = ProjectAnalyzer(project_path)
    report = analyzer.analyze_project()
    
    # Output to file and stdout
    with open('socialme_project_analysis.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    # Print key insights
    print("\n=== SocialMe Project Analysis ===")
    print(f"Total Python Files: {len(report['code_structure']['files'])}")
    print("Detected Frameworks:", report['potential_frameworks'])
    print("Direct Imports:", report['dependencies']['direct_imports'][:10], 
          "..." if len(report['dependencies']['direct_imports']) > 10 else "")
    print("\nFull analysis saved to socialme_project_analysis.json")

if __name__ == '__main__':
    main()
