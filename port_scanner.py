#!/usr/bin/env python3
"""
Port Scanner - A multi-threaded port scanner with banner grabbing capabilities
"""

import socket
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from typing import Optional, Tuple


def get_banner(sock: socket.socket, timeout: float = 2.0) -> Optional[str]:
    """
    Attempts to retrieve banner information from an open socket connection.
    
    Args:
        sock: The connected socket object
        timeout: Timeout for receiving banner data (default: 2.0 seconds)
    
    Returns:
        Banner string if available, None otherwise
    """
    try:
        sock.settimeout(timeout)
        # Try to receive banner data
        banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
        return banner if banner else None
    except (socket.timeout, socket.error, UnicodeDecodeError):
        return None


def scan_port(target_ip: str, port: int, timeout: float = 1.0) -> Tuple[int, bool, Optional[str], Optional[str]]:
    """
    Scans a single port on the target IP address.
    
    Args:
        target_ip: The target IP address to scan
        port: The port number to scan
        timeout: Connection timeout in seconds (default: 1.0)
    
    Returns:
        Tuple containing (port, is_open, service_name, banner)
    """
    try:
        # Create a socket object
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        
        # Attempt to connect to the port
        result = sock.connect_ex((target_ip, port))
        
        if result == 0:
            # Port is open
            banner = get_banner(sock)
            service_name = get_service_name(port)
            sock.close()
            return (port, True, service_name, banner)
        else:
            # Port is closed or filtered
            sock.close()
            return (port, False, None, None)
            
    except socket.gaierror:
        # Hostname resolution error
        return (port, False, None, None)
    except socket.error:
        # Socket error
        return (port, False, None, None)
    except Exception as e:
        # Other unexpected errors
        return (port, False, None, None)


def get_service_name(port: int) -> Optional[str]:
    """
    Returns common service name for well-known ports.
    
    Args:
        port: Port number
    
    Returns:
        Service name if known, None otherwise
    """
    common_services = {
        20: "FTP Data",
        21: "FTP",
        22: "SSH",
        23: "Telnet",
        25: "SMTP",
        53: "DNS",
        80: "HTTP",
        110: "POP3",
        143: "IMAP",
        443: "HTTPS",
        445: "SMB",
        3306: "MySQL",
        3389: "RDP",
        5432: "PostgreSQL",
        8080: "HTTP-Proxy",
    }
    return common_services.get(port, None)


def parse_port_range(port_input: str) -> list:
    """
    Parses port range input from user.
    Supports single port, range (e.g., 1-100), or comma-separated ports.
    
    Args:
        port_input: User input string for ports
    
    Returns:
        List of port numbers to scan
    """
    ports = []
    
    # Split by comma for multiple ranges/ports
    parts = port_input.split(',')
    
    for part in parts:
        part = part.strip()
        
        if '-' in part:
            # Range format: start-end
            try:
                start, end = part.split('-')
                start = int(start.strip())
                end = int(end.strip())
                if start > end:
                    start, end = end, start
                ports.extend(range(start, end + 1))
            except ValueError:
                print(f"Invalid range format: {part}")
                continue
        else:
            # Single port
            try:
                ports.append(int(part))
            except ValueError:
                print(f"Invalid port number: {part}")
                continue
    
    # Remove duplicates and sort
    return sorted(list(set(ports)))


def display_results(results: list, target_ip: str, scan_time: float):
    """
    Displays scan results in a formatted table.
    
    Args:
        results: List of scan results (port, is_open, service, banner)
        target_ip: Target IP address that was scanned
        scan_time: Time taken for the scan
    """
    # Filter only open ports
    open_ports = [r for r in results if r[1]]
    
    print("\n" + "="*80)
    print(f"PORT SCAN RESULTS FOR {target_ip}")
    print("="*80)
    
    if not open_ports:
        print("\nNo open ports found.")
    else:
        print(f"\nFound {len(open_ports)} open port(s):\n")
        print(f"{'Port':<10} {'Status':<10} {'Service':<20} {'Banner':<40}")
        print("-" * 80)
        
        for port, is_open, service, banner in open_ports:
            port_str = str(port)
            status = "OPEN"
            service_str = service if service else "Unknown"
            banner_str = banner if banner else "No banner"
            
            # Truncate banner if too long
            if len(banner_str) > 38:
                banner_str = banner_str[:35] + "..."
            
            print(f"{port_str:<10} {status:<10} {service_str:<20} {banner_str:<40}")
    
    print("\n" + "="*80)
    print(f"Scan completed in {scan_time:.2f} seconds")
    print("="*80 + "\n")


def main():
    """
    Main function to run the port scanner.
    """
    print("\n" + "="*80)
    print("PORT SCANNER - Multi-threaded Port Scanner with Banner Grabbing")
    print("="*80 + "\n")
    
    # Get target IP address
    while True:
        target_ip = input("Enter target IP address or hostname: ").strip()
        if target_ip:
            # Validate IP or hostname
            try:
                socket.gethostbyname(target_ip)
                break
            except socket.gaierror:
                print("Invalid IP address or hostname. Please try again.")
        else:
            print("IP address cannot be empty. Please try again.")
    
    # Get port range
    while True:
        port_input = input("Enter port(s) to scan (e.g., 80, 443, 1-1000, or 22,80,443): ").strip()
        if port_input:
            ports = parse_port_range(port_input)
            if ports:
                break
            else:
                print("No valid ports found. Please try again.")
        else:
            print("Port range cannot be empty. Please try again.")
    
    # Get number of threads
    while True:
        try:
            num_threads = input("Enter number of threads (default: 50): ").strip()
            if not num_threads:
                num_threads = 50
            else:
                num_threads = int(num_threads)
            if num_threads > 0:
                break
            else:
                print("Number of threads must be greater than 0.")
        except ValueError:
            print("Invalid number. Please enter a valid integer.")
    
    # Get timeout
    while True:
        try:
            timeout_input = input("Enter connection timeout in seconds (default: 1.0): ").strip()
            if not timeout_input:
                timeout = 1.0
            else:
                timeout = float(timeout_input)
            if timeout > 0:
                break
            else:
                print("Timeout must be greater than 0.")
        except ValueError:
            print("Invalid number. Please enter a valid float.")
    
    print(f"\nScanning {len(ports)} port(s) on {target_ip}...")
    print(f"Using {num_threads} threads with {timeout}s timeout per connection\n")
    
    start_time = time.time()
    results = []
    
    # Use ThreadPoolExecutor for concurrent scanning
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        # Submit all port scan tasks
        future_to_port = {
            executor.submit(scan_port, target_ip, port, timeout): port 
            for port in ports
        }
        
        # Process completed tasks
        completed = 0
        for future in as_completed(future_to_port):
            completed += 1
            result = future.result()
            results.append(result)
            
            # Show progress
            if result[1]:  # If port is open
                print(f"[+] Port {result[0]} is OPEN - {result[2] or 'Unknown Service'}")
            
            # Progress indicator
            if completed % 50 == 0 or completed == len(ports):
                print(f"Progress: {completed}/{len(ports)} ports scanned...", end='\r')
    
    end_time = time.time()
    scan_time = end_time - start_time
    
    # Display results
    display_results(results, target_ip, scan_time)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nScan interrupted by user. Exiting...")
        sys.exit(0)
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        sys.exit(1)

