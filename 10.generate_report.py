from datetime import datetime

def generate_report(vulnerabilities):
    report = f"Penetration Testing Report - {datetime.now()}\n"
    report += "=" * 50 + "\n"
    for vuln in vulnerabilities:
        report += f"Vulnerability: {vuln['name']}\n"
        report += f"Severity: {vuln['severity']}\n"
        report += f"Impact: {vuln['impact']}\n"
        report += "-" * 50 + "\n"
    return report

# Example vulnerabilities
vulnerabilities = [
    {"name": "SQL Injection", "severity": "High", "impact": "Data breach"},
    {"name": "XSS", "severity": "Medium", "impact": "Session hijacking"}
]

print(generate_report(vulnerabilities))
