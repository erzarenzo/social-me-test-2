#!/usr/bin/env python3

import os
import json
import hashlib
import subprocess
import re
import sys

class ProjectAnalyzer:
    def __init__(self, root_dir):
        self.root_dir = root_dir
        self.report = {
            "project_structure": {},
            "file_analysis": {},
            "dependencies": {},
            "code_insights": {}
        }

    def analyze_directory_structure(self):
        """Recursively map out the project directory structure"""
        structure = {}
        for root, dirs, files in os.walk(self.root_dir):
            # Create relative path
            rel_path = os.path.relpath(root, self.root_dir)
            
            # Skip version control and virtual environment directories
            if any(x in rel_path for x in ['.git', 'venv', 'myenv', '__pycache__']):
                continue
            
            # Build directory structure
            if rel_path == '.':
                structure['root'] = files
            else:
                structure[rel_path] = files
        
        self.report['project_structure'] = structure

    def generate_report(self, output_path=None):
        """Generate a basic project report"""
        # Run directory structure analysis
        self.analyze_directory_structure()
        
        # Convert to JSON for readability
        report_json = json.dumps(self.report, indent=2)
        
        # Output to file if path provided
        if output_path:
            with open(output_path, 'w') as f:
                f.write(report_json)
        
        return report_json

def main():
    # Get the directory path from command line or use current directory
    directory = sys.argv[1] if len(sys.argv) > 1 else '.'
    
    # Create analyzer and generate report
    analyzer = ProjectAnalyzer(directory)
    report = analyzer.generate_report('project_analysis_report.json')
    
    print("Project analysis complete. Report saved to project_analysis_report.json")

if __name__ == '__main__':
    main()
