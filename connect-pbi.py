#!/usr/bin/env python3
"""
Connect to Power BI Desktop XMLA Endpoint at localhost:63159
"""

import socket
import json

def test_connection(host="localhost", port=63159):
    """Test connection to XMLA endpoint"""
    try:
        print(f"Connecting to {host}:{port}...")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((host, port))
        sock.close()
        
        if result == 0:
            print(f"✓ Connection successful!")
            print(f"✓ XMLA endpoint is listening on {host}:{port}")
            return True
        else:
            print(f"✗ Connection failed: {result}")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def get_connection_info():
    """Display connection information"""
    print("\n=== Power BI Desktop XMLA Connection Info ===")
    print("Server: localhost:63159")
    print("Protocol: XMLA (XML for Analysis)")
    print("\nAccess methods:")
    print("  • DAX Studio: Connect to localhost:63159")
    print("  • SSMS: Connect to localhost:63159 (as Analysis Services)")
    print("  • Tabular Editor 3: Create external connection")
    print("  • Power BI Desktop: Open main.pbip")
    print("\nPython libraries for XMLA:")
    print("  pip install xmla2")
    print("  pip install 'pyodbc' for OLEDB connections")

if __name__ == "__main__":
    print("=== Power BI Local XMLA Connection Test ===\n")
    if test_connection():
        get_connection_info()
    else:
        print("\n✗ Unable to connect. Ensure Power BI Desktop is running.")
