#!/bin/bash
# Run OpenVAS vulnerability scan
openvas-start
openvas-scan --target 192.168.1.0/24 --scan-type full
