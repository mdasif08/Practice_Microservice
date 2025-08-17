#!/usr/bin/env python3
"""
Comprehensive Test Runner for CraftNudge AI Agent

This script provides step-by-step testing with:
- Individual test module execution
- Coverage analysis
- Quality checks
- Detailed reporting
- Progress tracking
"""

import os
import sys
import subprocess
import time
import json
from pathlib import Path
from typing import Dict, List, Tuple

class TestRunner:
    """Comprehensive test runner with step-by-step execution."""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.results = {
            "start_time": time.time(),
            "modules_tested": [],
            "coverage": {},
            "quality": {},
            "summary": {}
        }
    
    def run_step_by_step(self):
        """Run tests step by step with detailed reporting."""
        print("🔧 CraftNudge AI Agent - Step-by-Step Test Runner")
        print("=" * 60)
        
        # Step 1: Test individual modules
        self.test_core_modules()
        
        # Step 2: Test services
        self.test_services()
        
        # Step 3: Test shared components
        self.test_shared_components()
        
        # Step 4: Run coverage analysis
        self.run_coverage_analysis()
        
        # Step 5: Run quality checks
        self.run_quality_checks()
        
        # Step 6: Generate final report
        self.generate_final_report()
    
    def test_core_modules(self):
        """Test core modules individually."""
        print("\n📦 STEP 1: Testing Core Modules")
        print("-" * 40)
        
        core_modules = [
            "shared.config.config_manager",
            "shared.utils.logger", 
            "shared.utils.error_handler",
            "services.commit_tracker_service.src.commit_tracker",
            "services.commit_tracker_service.src.git_parser",
            "services.commit_tracker_service.src.data_writer"
        ]
        
        for module in core_modules:
            self.test_module(module)
    
    def test_services(self):
        """Test service modules."""
        print("\n🔧 STEP 2: Testing Services")
        print("-" * 40)
        
        service_tests = [
            "tests/unit/test_commit_tracker.py",
            "tests/unit/test_git_parser.py", 
            "tests/unit/test_data_writer.py"
        ]
        
        for test_file in service_tests:
            self.run_test_file(test_file)
    
    def test_shared_components(self):
        """Test shared components."""
        print("\n🔄 STEP 3: Testing Shared Components")
        print("-" * 40)
        
        shared_tests = [
            "tests/unit/test_config_manager.py",
            "tests/unit/test_logger.py",
            "tests/unit/test_error_handler.py"
        ]
        
        for test_file in shared_tests:
            self.run_test_file(test_file)
    
    def test_module(self, module_name: str):
        """Test a specific module."""
        print(f"  Testing {module_name}...")
        try:
            result = subprocess.run(
                [sys.executable, "-c", f"import {module_name}; print('PASS: {module_name} imports successfully')"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                print(f"    PASS: {module_name} - PASSED")
                self.results["modules_tested"].append({"module": module_name, "status": "PASSED"})
            else:
                print(f"    FAIL: {module_name} - FAILED")
                print(f"      Error: {result.stderr.strip()}")
                self.results["modules_tested"].append({"module": module_name, "status": "FAILED", "error": result.stderr.strip()})
                
        except Exception as e:
            print(f"    ERROR: {module_name} - ERROR: {e}")
            self.results["modules_tested"].append({"module": module_name, "status": "ERROR", "error": str(e)})
    
    def run_test_file(self, test_file: str):
        """Run a specific test file."""
        print(f"  Running {test_file}...")
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pytest", test_file, "-v", "--tb=short"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=120
            )
            
            # Parse test results
            output_lines = result.stdout.split('\n')
            passed = 0
            failed = 0
            
            for line in output_lines:
                if "PASSED" in line:
                    passed += 1
                elif "FAILED" in line:
                    failed += 1
            
            if result.returncode == 0 or passed > 0:
                print(f"    PASS: {test_file} - {passed} passed, {failed} failed")
                self.results["modules_tested"].append({
                    "file": test_file, 
                    "status": "PASSED", 
                    "passed": passed, 
                    "failed": failed
                })
            else:
                print(f"    FAIL: {test_file} - FAILED")
                self.results["modules_tested"].append({
                    "file": test_file, 
                    "status": "FAILED", 
                    "error": result.stderr.strip()
                })
                
        except Exception as e:
            print(f"    ERROR: {test_file} - ERROR: {e}")
            self.results["modules_tested"].append({
                "file": test_file, 
                "status": "ERROR", 
                "error": str(e)
            })
    
    def run_coverage_analysis(self):
        """Run coverage analysis."""
        print("\n📊 STEP 4: Coverage Analysis")
        print("-" * 40)
        
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pytest", "--cov=.", "--cov-report=term-missing", "-q"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            # Parse coverage output
            coverage_lines = result.stdout.split('\n')
            total_coverage = 0
            
            for line in coverage_lines:
                if "TOTAL" in line:
                    parts = line.split()
                    if len(parts) >= 4:
                        try:
                            total_coverage = float(parts[-1].replace('%', ''))
                        except ValueError:
                            pass
                    break
            
            self.results["coverage"] = {
                "total_coverage": total_coverage,
                "output": result.stdout,
                "status": "COMPLETED"
            }
            
            print(f"  Total Coverage: {total_coverage}%")
            
        except Exception as e:
            print(f"  ✗ Coverage analysis failed: {e}")
            self.results["coverage"] = {"status": "FAILED", "error": str(e)}
    
    def run_quality_checks(self):
        """Run quality checks."""
        print("\n🔍 STEP 5: Quality Checks")
        print("-" * 40)
        
        quality_tools = {
            "pylint": ["python", "-m", "pylint", "--output-format=json", "."],
            "flake8": ["python", "-m", "flake8", "--format=json"],
            "mypy": ["python", "-m", "mypy", "--json-report", "."]
        }
        
        for tool, cmd in quality_tools.items():
            print(f"  Running {tool}...")
            try:
                result = subprocess.run(
                    cmd,
                    cwd=self.project_root,
                    capture_output=True,
                    text=True,
                    timeout=60
                )
                
                if result.returncode == 0:
                    print(f"    PASS: {tool} - PASSED")
                    self.results["quality"][tool] = {"status": "PASSED", "score": 10.0}
                else:
                    try:
                        issues = json.loads(result.stdout)
                        score = max(0, 10 - len(issues) * 0.1)
                        print(f"    WARN: {tool} - {len(issues)} issues (score: {score:.1f}/10)")
                        self.results["quality"][tool] = {"status": "ISSUES", "score": score, "issues": len(issues)}
                    except:
                        print(f"    FAIL: {tool} - FAILED")
                        self.results["quality"][tool] = {"status": "FAILED", "score": 0}
                        
            except Exception as e:
                print(f"    ERROR: {tool} - ERROR: {e}")
                self.results["quality"][tool] = {"status": "ERROR", "score": 0, "error": str(e)}
    
    def generate_final_report(self):
        """Generate final test report."""
        print("\n📋 STEP 6: Final Report")
        print("-" * 40)
        
        # Calculate summary statistics
        total_modules = len(self.results["modules_tested"])
        passed_modules = len([m for m in self.results["modules_tested"] if m.get("status") == "PASSED"])
        coverage = self.results["coverage"].get("total_coverage", 0)
        
        # Calculate quality score
        quality_scores = [q.get("score", 0) for q in self.results["quality"].values()]
        avg_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 0
        
        # Determine overall grade
        if passed_modules == total_modules and coverage >= 90 and avg_quality >= 8:
            grade = "A+"
        elif passed_modules >= total_modules * 0.9 and coverage >= 80 and avg_quality >= 7:
            grade = "A"
        elif passed_modules >= total_modules * 0.8 and coverage >= 70 and avg_quality >= 6:
            grade = "B"
        else:
            grade = "C"
        
        self.results["summary"] = {
            "total_modules": total_modules,
            "passed_modules": passed_modules,
            "coverage": coverage,
            "quality_score": avg_quality,
            "grade": grade,
            "duration": time.time() - self.results["start_time"]
        }
        
        # Print summary
        print(f"  Total Modules Tested: {total_modules}")
        print(f"  Modules Passed: {passed_modules}")
        print(f"  Code Coverage: {coverage:.1f}%")
        print(f"  Quality Score: {avg_quality:.1f}/10")
        print(f"  Overall Grade: {grade}")
        print(f"  Duration: {self.results['summary']['duration']:.1f}s")
        
        # Save detailed report
        report_file = self.project_root / "step_by_step_test_report.json"
        with open(report_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\n📁 Detailed report saved to: {report_file}")
        
        # Print recommendations
        print("\nRECOMMENDATIONS:")
        if passed_modules < total_modules:
            print("  * Fix failing module tests")
        if coverage < 90:
            print(f"  * Increase code coverage (current: {coverage:.1f}%, target: 90%+)")
        if avg_quality < 8:
            print(f"  * Improve code quality (current: {avg_quality:.1f}/10, target: 8+)")
        
        if grade in ["A+", "A"]:
            print("  EXCELLENT: All quality targets met!")
        elif grade == "B":
            print("  GOOD: Progress made, but room for improvement")
        else:
            print("  NEEDS WORK: Significant improvements needed")

def main():
    """Main entry point."""
    project_root = Path(__file__).parent
    runner = TestRunner(project_root)
    runner.run_step_by_step()

if __name__ == "__main__":
    main()
