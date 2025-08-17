#!/usr/bin/env python3
"""
Comprehensive Test Automation Framework for CraftNudge AI Agent

This script provides automated testing with:
- 100% code coverage enforcement
- Quality metrics analysis
- Detailed reporting
- CI/CD integration support
"""

import os
import sys
import subprocess
import json
import time
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import xml.etree.ElementTree as ET

class TestAutomationFramework:
    """Comprehensive test automation framework with coverage and quality enforcement."""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.coverage_file = project_root / ".coverage"
        self.htmlcov_dir = project_root / "htmlcov"
        self.xmlcov_file = project_root / "coverage.xml"
        self.test_results_file = project_root / "test_results.json"
        self.quality_report_file = project_root / "quality_report.json"
        
    def run_tests_with_coverage(self, verbose: bool = True) -> Dict:
        """Run all tests with coverage analysis."""
        print("🚀 Starting comprehensive test suite...")
        
        # Clean previous coverage data
        self._clean_coverage_data()
        
        # Run tests with coverage
        cmd = [
            sys.executable, "-m", "pytest",
            "--cov=.",
            "--cov-report=term-missing",
            "--cov-report=html",
            "--cov-report=xml",
            "--cov-fail-under=100",
            "--junitxml=test-results.xml",
            "--tb=short",
            "-v" if verbose else "-q"
        ]
        
        print(f"📋 Running command: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(
                cmd,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode
            }
            
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "stdout": "",
                "stderr": "Test execution timed out after 5 minutes",
                "returncode": 1
            }
        except Exception as e:
            return {
                "success": False,
                "stdout": "",
                "stderr": str(e),
                "returncode": 1
            }
    
    def analyze_coverage(self) -> Dict:
        """Analyze coverage results and generate detailed report."""
        print("📊 Analyzing coverage results...")
        
        coverage_data = {
            "overall_coverage": 0.0,
            "missing_lines": [],
            "file_coverage": {},
            "coverage_gaps": []
        }
        
        # Parse coverage.xml if it exists
        if self.xmlcov_file.exists():
            try:
                tree = ET.parse(self.xmlcov_file)
                root = tree.getroot()
                
                # Extract overall coverage
                packages = root.findall(".//package")
                total_lines = 0
                covered_lines = 0
                
                for package in packages:
                    package_name = package.get("name", "")
                    classes = package.findall(".//class")
                    
                    for class_elem in classes:
                        class_name = class_elem.get("name", "")
                        filename = class_elem.get("filename", "")
                        
                        lines = class_elem.findall(".//line")
                        file_lines = 0
                        file_covered = 0
                        
                        for line in lines:
                            line_num = int(line.get("number", 0))
                            hits = int(line.get("hits", 0))
                            file_lines += 1
                            total_lines += 1
                            
                            if hits > 0:
                                file_covered += 1
                                covered_lines += 1
                            else:
                                coverage_data["missing_lines"].append({
                                    "file": filename,
                                    "line": line_num,
                                    "class": class_name
                                })
                        
                        if file_lines > 0:
                            file_coverage = (file_covered / file_lines) * 100
                            coverage_data["file_coverage"][filename] = {
                                "coverage": file_coverage,
                                "lines": file_lines,
                                "covered": file_covered,
                                "missing": file_lines - file_covered
                            }
                
                if total_lines > 0:
                    coverage_data["overall_coverage"] = (covered_lines / total_lines) * 100
                
            except Exception as e:
                print(f"⚠️  Warning: Could not parse coverage XML: {e}")
        
        return coverage_data
    
    def run_quality_checks(self) -> Dict:
        """Run code quality checks using various tools."""
        print("🔍 Running code quality checks...")
        
        quality_results = {
            "pylint": self._run_pylint(),
            "flake8": self._run_flake8(),
            "mypy": self._run_mypy(),
            "bandit": self._run_bandit(),
            "overall_score": 0
        }
        
        # Calculate overall quality score
        scores = []
        for tool, result in quality_results.items():
            if tool != "overall_score" and isinstance(result, dict):
                if "score" in result:
                    scores.append(result["score"])
        
        if scores:
            quality_results["overall_score"] = sum(scores) / len(scores)
        
        return quality_results
    
    def _run_pylint(self) -> Dict:
        """Run pylint for code quality analysis."""
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pylint", "--output-format=json", "."],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                return {"score": 10.0, "issues": [], "status": "passed"}
            else:
                try:
                    issues = json.loads(result.stdout)
                    score = max(0, 10 - len(issues) * 0.1)  # Deduct 0.1 per issue
                    return {
                        "score": round(score, 2),
                        "issues": issues,
                        "status": "issues_found"
                    }
                except json.JSONDecodeError:
                    return {"score": 0, "issues": [], "status": "error"}
                    
        except Exception as e:
            return {"score": 0, "issues": [], "status": f"error: {e}"}
    
    def _run_flake8(self) -> Dict:
        """Run flake8 for style checking."""
        try:
            result = subprocess.run(
                [sys.executable, "-m", "flake8", "--format=json"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                return {"score": 10.0, "issues": [], "status": "passed"}
            else:
                try:
                    issues = json.loads(result.stdout)
                    score = max(0, 10 - len(issues) * 0.1)
                    return {
                        "score": round(score, 2),
                        "issues": issues,
                        "status": "issues_found"
                    }
                except json.JSONDecodeError:
                    return {"score": 0, "issues": [], "status": "error"}
                    
        except Exception as e:
            return {"score": 0, "issues": [], "status": f"error: {e}"}
    
    def _run_mypy(self) -> Dict:
        """Run mypy for type checking."""
        try:
            result = subprocess.run(
                [sys.executable, "-m", "mypy", "--json-report", "."],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                return {"score": 10.0, "issues": [], "status": "passed"}
            else:
                # Parse mypy output for issues
                issues = []
                for line in result.stdout.split('\n'):
                    if line.strip():
                        try:
                            issue = json.loads(line)
                            issues.append(issue)
                        except json.JSONDecodeError:
                            continue
                
                score = max(0, 10 - len(issues) * 0.2)  # Deduct 0.2 per type error
                return {
                    "score": round(score, 2),
                    "issues": issues,
                    "status": "issues_found"
                }
                    
        except Exception as e:
            return {"score": 0, "issues": [], "status": f"error: {e}"}
    
    def _run_bandit(self) -> Dict:
        """Run bandit for security analysis."""
        try:
            result = subprocess.run(
                [sys.executable, "-m", "bandit", "-r", "-f", "json", "."],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            try:
                issues = json.loads(result.stdout)
                security_issues = issues.get("results", [])
                
                # Calculate score based on severity
                score = 10.0
                for issue in security_issues:
                    severity = issue.get("issue_severity", "LOW")
                    if severity == "HIGH":
                        score -= 2.0
                    elif severity == "MEDIUM":
                        score -= 1.0
                    elif severity == "LOW":
                        score -= 0.5
                
                score = max(0, score)
                return {
                    "score": round(score, 2),
                    "issues": security_issues,
                    "status": "completed"
                }
                
            except json.JSONDecodeError:
                return {"score": 0, "issues": [], "status": "error"}
                    
        except Exception as e:
            return {"score": 0, "issues": [], "status": f"error: {e}"}
    
    def _clean_coverage_data(self):
        """Clean previous coverage data."""
        if self.coverage_file.exists():
            self.coverage_file.unlink()
        
        if self.htmlcov_dir.exists():
            import shutil
            shutil.rmtree(self.htmlcov_dir)
    
    def generate_report(self, test_results: Dict, coverage_data: Dict, quality_results: Dict) -> str:
        """Generate comprehensive test report."""
        print("📝 Generating comprehensive test report...")
        
        report = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "test_results": test_results,
            "coverage": coverage_data,
            "quality": quality_results,
            "summary": self._generate_summary(test_results, coverage_data, quality_results)
        }
        
        # Save report to file
        with open(self.test_results_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        # Generate human-readable report
        return self._format_report(report)
    
    def _generate_summary(self, test_results: Dict, coverage_data: Dict, quality_results: Dict) -> Dict:
        """Generate test summary."""
        overall_success = test_results.get("success", False)
        coverage_percentage = coverage_data.get("overall_coverage", 0.0)
        quality_score = quality_results.get("overall_score", 0.0)
        
        # Determine overall status
        if overall_success and coverage_percentage >= 100.0 and quality_score >= 9.0:
            status = "PASSED"
            grade = "A+"
        elif overall_success and coverage_percentage >= 95.0 and quality_score >= 8.0:
            status = "PASSED"
            grade = "A"
        elif overall_success and coverage_percentage >= 90.0 and quality_score >= 7.0:
            status = "PASSED"
            grade = "B"
        else:
            status = "FAILED"
            grade = "F"
        
        return {
            "status": status,
            "grade": grade,
            "test_success": overall_success,
            "coverage_percentage": coverage_percentage,
            "quality_score": quality_score,
            "recommendations": self._generate_recommendations(test_results, coverage_data, quality_results)
        }
    
    def _generate_recommendations(self, test_results: Dict, coverage_data: Dict, quality_results: Dict) -> List[str]:
        """Generate improvement recommendations."""
        recommendations = []
        
        if not test_results.get("success", False):
            recommendations.append("Fix failing tests before proceeding")
        
        coverage = coverage_data.get("overall_coverage", 0.0)
        if coverage < 100.0:
            missing_lines = coverage_data.get("missing_lines", [])
            recommendations.append(f"Add tests to cover {len(missing_lines)} missing lines (current coverage: {coverage:.1f}%)")
        
        quality_score = quality_results.get("overall_score", 0.0)
        if quality_score < 9.0:
            recommendations.append(f"Improve code quality (current score: {quality_score:.1f}/10)")
        
        return recommendations
    
    def _format_report(self, report: Dict) -> str:
        """Format report for console output."""
        summary = report["summary"]
        
        output = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                        CRAFTNUDGE AI AGENT - TEST REPORT                    ║
╚══════════════════════════════════════════════════════════════════════════════╝

📊 SUMMARY
   Status: {summary['status']}
   Grade: {summary['grade']}
   Test Success: {'✅ PASSED' if summary['test_success'] else '❌ FAILED'}
   Code Coverage: {summary['coverage_percentage']:.1f}% {'✅' if summary['coverage_percentage'] >= 100 else '❌'}
   Quality Score: {summary['quality_score']:.1f}/10 {'✅' if summary['quality_score'] >= 9.0 else '❌'}

📈 DETAILED METRICS
   Coverage Analysis:
   - Overall Coverage: {summary['coverage_percentage']:.1f}%
   - Missing Lines: {len(report['coverage'].get('missing_lines', []))}
   - Files with Coverage: {len(report['coverage'].get('file_coverage', {}))}

   Quality Analysis:
   - Pylint Score: {report['quality']['pylint']['score']:.1f}/10
   - Flake8 Score: {report['quality']['flake8']['score']:.1f}/10
   - MyPy Score: {report['quality']['mypy']['score']:.1f}/10
   - Bandit Score: {report['quality']['bandit']['score']:.1f}/10

🎯 RECOMMENDATIONS
"""
        
        for i, rec in enumerate(summary['recommendations'], 1):
            output += f"   {i}. {rec}\n"
        
        if not summary['recommendations']:
            output += "   ✅ All quality targets met! Excellent work!\n"
        
        output += f"""
📁 REPORTS GENERATED
   - Test Results: {self.test_results_file}
   - Coverage HTML: {self.htmlcov_dir}/index.html
   - Coverage XML: {self.xmlcov_file}
   - Quality Report: {self.quality_report_file}

⏰ Generated at: {report['timestamp']}
"""
        
        return output

def main():
    """Main entry point for test automation."""
    parser = argparse.ArgumentParser(description="CraftNudge AI Agent Test Automation")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--quick", "-q", action="store_true", help="Quick test run (skip quality checks)")
    parser.add_argument("--coverage-only", action="store_true", help="Run only coverage tests")
    parser.add_argument("--quality-only", action="store_true", help="Run only quality checks")
    
    args = parser.parse_args()
    
    project_root = Path(__file__).parent
    framework = TestAutomationFramework(project_root)
    
    print("🔧 CraftNudge AI Agent - Automated Testing Framework")
    print("=" * 60)
    
    test_results = {"success": False, "stdout": "", "stderr": "", "returncode": 1}
    coverage_data = {"overall_coverage": 0.0, "missing_lines": [], "file_coverage": {}}
    quality_results = {"overall_score": 0}
    
    try:
        # Run tests and coverage
        if not args.quality_only:
            print("\n🧪 PHASE 1: Running Tests with Coverage")
            test_results = framework.run_tests_with_coverage(verbose=args.verbose)
            
            if test_results["success"]:
                print("✅ Tests completed successfully")
                coverage_data = framework.analyze_coverage()
            else:
                print("❌ Tests failed")
                print(f"Error: {test_results['stderr']}")
        
        # Run quality checks
        if not args.coverage_only:
            print("\n🔍 PHASE 2: Running Quality Checks")
            quality_results = framework.run_quality_checks()
        
        # Generate report
        print("\n📊 PHASE 3: Generating Report")
        report = framework.generate_report(test_results, coverage_data, quality_results)
        print(report)
        
        # Exit with appropriate code
        summary = framework._generate_summary(test_results, coverage_data, quality_results)
        if summary["status"] == "PASSED":
            sys.exit(0)
        else:
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n⚠️  Test execution interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()



