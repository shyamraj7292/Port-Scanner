# Port Scanner

A Python-based multi-threaded port scanner that identifies open ports on a target machine. This project demonstrates network scanning, socket programming, and multithreading for efficient scanning.

## Project Overview

Port scanning is a fundamental technique used in cybersecurity to detect open ports and running services on a networked system. This project implements a multi-threaded port scanner that scans a specified range of ports on a target IP, identifies open ports, and attempts to retrieve service banners. The scanner provides insights into potential security vulnerabilities by revealing exposed services.

## Features

- **Multi-threaded Scanning**: Uses Python's `ThreadPoolExecutor` for concurrent port scanning, significantly reducing scan time
- **Banner Grabbing**: Attempts to retrieve service banners from open ports to identify running services
- **Service Identification**: Automatically identifies common services based on well-known port numbers
- **Flexible Port Input**: Supports single ports, port ranges (e.g., 1-1000), and comma-separated lists (e.g., 22,80,443)
- **Formatted Output**: Displays results in a structured table format
- **Error Handling**: Robust error handling for network issues and invalid inputs
- **Progress Tracking**: Real-time progress updates during scanning

## How It Works

1. **Target Input**: The user enters the target IP address and the range of ports to scan
2. **Socket Connection**: The script attempts to establish a connection to each port
3. **Service Identification**: If a port is open, the scanner tries to identify the running service
4. **Banner Grabbing**: The scanner retrieves any available banner information from the open port
5. **Multithreading for Speed**: The scanning process is optimized using Python's `ThreadPoolExecutor`, allowing concurrent scanning of multiple ports for faster results
6. **Formatted Output**: The results are displayed in a structured table, highlighting open ports, detected services, and banners

## Key Concepts Covered

- **Socket Programming**: Using Python's `socket` module to establish connections
- **Banner Grabbing**: Extracting information about the service running on open ports
- **Multithreading**: Speeding up the scan by handling multiple ports simultaneously
- **Command-line Interaction**: Accepting user inputs for target IP and port range
- **Formatted Output Display**: Structuring scan results for readability

## Requirements

- Python 3.6 or higher
- Standard library modules only (no external dependencies required):
  - `socket`
  - `concurrent.futures`
  - `sys`
  - `time`
  - `typing`

## Installation

1. Clone or download this repository
2. Ensure Python 3.6+ is installed on your system
3. No additional packages need to be installed (uses only standard library)

## Usage

Run the port scanner using:

```bash
python port_scanner.py
```

The program will prompt you for:
1. **Target IP address or hostname**: The IP address or domain name of the target machine
2. **Port range**: Can be specified as:
   - Single port: `80`
   - Port range: `1-1000`
   - Multiple ports/ranges: `22,80,443,8000-8100`
3. **Number of threads**: Number of concurrent threads to use (default: 50)
4. **Connection timeout**: Timeout in seconds for each connection attempt (default: 1.0)

### Example Usage

```
Enter target IP address or hostname: 192.168.1.1
Enter port(s) to scan (e.g., 80, 443, 1-1000, or 22,80,443): 20-100
Enter number of threads (default: 50): 100
Enter connection timeout in seconds (default: 1.0): 0.5
```

## Sample Output

```
================================================================================
PORT SCAN RESULTS FOR 192.168.1.1
================================================================================

Found 3 open port(s):

Port       Status     Service              Banner                                
--------------------------------------------------------------------------------
22         OPEN       SSH                  SSH-2.0-OpenSSH_7.4
80         OPEN       HTTP                 HTTP/1.1 200 OK
443        OPEN       HTTPS                HTTP/1.1 200 OK

================================================================================
Scan completed in 2.45 seconds
================================================================================
```

## Implementation Details

### Core Functions

- `scan_port(target_ip, port, timeout)`: Scans a single port and returns its status
- `get_banner(sock, timeout)`: Attempts to retrieve banner information from an open socket
- `get_service_name(port)`: Returns common service names for well-known ports
- `parse_port_range(port_input)`: Parses various port input formats
- `display_results(results, target_ip, scan_time)`: Formats and displays scan results

### Threading Model

The scanner uses `ThreadPoolExecutor` from the `concurrent.futures` module to manage a pool of worker threads. Each thread independently scans a port, allowing for parallel execution and significantly improved performance compared to sequential scanning.

## Important Notes

⚠️ **Legal and Ethical Considerations**:
- Only scan systems you own or have explicit permission to scan
- Unauthorized port scanning may be illegal in many jurisdictions
- This tool is for educational purposes and authorized security testing only
- Always ensure you have proper authorization before scanning any network

## Error Handling

The scanner includes comprehensive error handling for:
- Invalid IP addresses or hostnames
- Network connection errors
- Socket timeouts
- Invalid port ranges
- Keyboard interrupts (Ctrl+C)

## Limitations

- Banner grabbing may not work for all services
- Some firewalls may block or filter port scan attempts
- Scanning large port ranges may take significant time even with multithreading
- Rate limiting may be necessary to avoid overwhelming target systems

## Future Enhancements

Potential improvements could include:
- UDP port scanning support
- Stealth scanning techniques (SYN scan, FIN scan)
- Export results to file (CSV, JSON)
- Command-line argument support
- Configuration file support
- More sophisticated service detection
- OS fingerprinting capabilities

## License

This project is provided for educational purposes only.

## Author

Developed as an educational project to demonstrate network scanning concepts, socket programming, and multithreading in Python.
