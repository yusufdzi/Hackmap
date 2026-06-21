Hmap All-in-One Tool

A powerful GUI-based network scanner built with Python and Nmap. Designed for authorized network discovery, host enumeration, service detection, OS fingerprinting, and security assessments through an intuitive hacker-style interface.

Features:
Modern hacker-themed graphical user interface (Tkinter)
Multiple scan profiles:
Quick Scan
Ping Sweep
OS Detection
Aggressive Scan
Full Port Scan
Service Version Detection
Vulnerability Scan
UDP Scan
Stealth SYN Scan
Comprehensive Scan
Real-time scan output
Host discovery and network enumeration
Open port and service detection
Operating system fingerprinting
Scan history tracking
Export results to TXT and JSON
Supports both:
python-nmap
Native Nmap subprocess execution
Multi-threaded scanning for responsive UI
Requirements
Python 3.9+
Nmap installed on your system

Install dependencies:
pip install python-nmap

Install Nmap:

Linux:
sudo apt update
sudo apt install nmap

Windows:
Download and install Nmap from the official website.

Usage:
python hmap.py

Enter a target IP address, hostname, or network range, choose a scan profile, and start scanning.

Disclaimer:
This tool is intended for educational purposes and authorized security assessments only. Users are responsible for complying with all applicable laws and regulations. Unauthorized scanning of networks or systems without permission may be illegal.

Author:
yusuf.dzi

Built with Python, Tkinter, and Nmap.
