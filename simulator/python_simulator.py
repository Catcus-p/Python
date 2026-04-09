#!/usr/bin/env python3
"""
Enhanced Thermal Printer Simulator with ESC/POS Decoding
Listens on TCP port 9100 and displays formatted receipt text
"""

import socket
import re

HOST = '0.0.0.0'
PORT = 9100

def decode_escpos(data: bytes) -> str:
    """Decode ESC/POS byte data into readable formatted text"""
    try:
        # Remove common ESC/POS control codes
        text = data.decode('utf-8', errors='ignore')
    except:
        text = data.decode('latin-1', errors='ignore')
    
    # ESC/POS command patterns to strip
    # ESC @ - Initialize printer
    # ESC a n - Alignment (0=left, 1=center, 2=right)
    # ESC E n - Bold on/off
    # ESC ! n - Print mode
    # GS V - Cut paper
    # LF - Line feed
    
    lines = []
    current_line = ""
    alignment = "left"  # Track current alignment
    
    i = 0
    while i < len(data):
        b = data[i]
        
        # ESC (0x1B) commands
        if b == 0x1B:
            if i + 1 < len(data):
                cmd = data[i + 1]
                
                # ESC @ - Initialize
                if cmd == ord('@'):
                    i += 2
                    continue
                
                # ESC a n - Alignment
                elif cmd == ord('a') and i + 2 < len(data):
                    align_code = data[i + 2]
                    if align_code == 0:
                        alignment = "left"
                    elif align_code == 1:
                        alignment = "center"
                    elif align_code == 2:
                        alignment = "right"
                    i += 3
                    continue
                
                # ESC E n - Bold
                elif cmd == ord('E') and i + 2 < len(data):
                    i += 3
                    continue
                
                # ESC ! n - Print mode
                elif cmd == ord('!') and i + 2 < len(data):
                    i += 3
                    continue
                
                # ESC d n - Print and feed n lines
                elif cmd == ord('d') and i + 2 < len(data):
                    n = data[i + 2]
                    if current_line:
                        lines.append((alignment, current_line))
                        current_line = ""
                    for _ in range(n):
                        lines.append((alignment, ""))
                    i += 3
                    continue
                
                # ESC M n - Character font
                elif cmd == ord('M') and i + 2 < len(data):
                    i += 3
                    continue
                
                # Other ESC commands - skip 2 bytes
                else:
                    i += 2
                    continue
        
        # GS (0x1D) commands
        elif b == 0x1D:
            if i + 1 < len(data):
                cmd = data[i + 1]
                
                # GS V - Cut
                if cmd == ord('V'):
                    if i + 2 < len(data):
                        i += 3
                    else:
                        i += 2
                    continue
                
                # GS ! n - Character size
                elif cmd == ord('!') and i + 2 < len(data):
                    i += 3
                    continue
                
                # Other GS commands
                else:
                    i += 2
                    continue
        
        # LF (0x0A) - Line feed
        elif b == 0x0A:
            lines.append((alignment, current_line))
            current_line = ""
            i += 1
            continue
        
        # CR (0x0D) - Carriage return
        elif b == 0x0D:
            i += 1
            continue
        
        # Printable ASCII
        elif 32 <= b <= 126:
            current_line += chr(b)
            i += 1
            continue
        
        # Skip other control characters
        else:
            i += 1
            continue
    
    # Add remaining text
    if current_line:
        lines.append((alignment, current_line))
    
    return lines


def format_output(lines: list, width: int = 48) -> str:
    """Format lines with proper alignment for display"""
    output = []
    output.append("=" * width)
    output.append("        THERMAL PRINTER OUTPUT")
    output.append("=" * width)
    
    for alignment, text in lines:
        if not text:
            output.append("")
            continue
        
        if alignment == "center":
            output.append(text.center(width))
        elif alignment == "right":
            output.append(text.rjust(width))
        else:
            output.append(text)
    
    output.append("=" * width)
    return "\n".join(output)


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Enhanced Thermal Printer Simulator')
    parser.add_argument('--port', type=int, default=PORT, help='Port to listen on')
    args = parser.parse_args()
    
    port = args.port

    print(f"🖨️  Enhanced Thermal Printer Simulator")
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # Try to bind to the requested port first, then fallback to a range
        ports_to_try = [port] + [p for p in range(9100, 9110) if p != port]
        bound_port = None
        
        for p in ports_to_try:
            try:
                s.bind((HOST, p))
                bound_port = p
                break
            except OSError as e:
                if e.errno == 98:  # Address already in use
                    continue
                else:
                    raise e
        
        if bound_port is None:
            print(f"❌ Error: Could not find an available port in range 9100-9109.")
            return

        print(f"📡 Listening on port {bound_port}...")
        print("-" * 50)
        s.listen(1)
        
        while True:
            print("\n⏳ Waiting for print job...")
            conn, addr = s.accept()
            
            with conn:
                print(f"✅ Connected from {addr}")
                
                # Receive all data
                data = b""
                while True:
                    chunk = conn.recv(4096)
                    if not chunk:
                        break
                    data += chunk
                
                if data:
                    print(f"🎉 Print Job Received! Size: {len(data)} bytes")
                    print()
                    
                    # Decode and format
                    lines = decode_escpos(data)
                    formatted = format_output(lines)
                    print(formatted)
                    print()


if __name__ == "__main__":
    main()