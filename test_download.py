#!/usr/bin/env python3
# Test script for the improved download function

import os
import sys
import tempfile

# Add the tools directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'tools'))

from idf_tools import download, print_hints_on_download_error

def test_download():
    """Test the improved download function with various scenarios"""
    
    # Test URLs
    test_urls = [
        'https://dl.espressif.com/dl/idf-installer/esp-idf-tools-setup-offline-5.4.2.exe',  # Should work with custom cert
        'https://github.com/espressif/esp-idf/archive/refs/heads/master.zip',  # Should work with custom cert
        'https://httpbin.org/status/200',  # Simple test URL
    ]
    
    for url in test_urls:
        print(f"\n=== Testing download from: {url} ===")
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            temp_path = tmp_file.name
        
        try:
            # Test download
            error = download(url, temp_path)
            
            if error is None:
                # Check if file was created and has content
                if os.path.exists(temp_path) and os.path.getsize(temp_path) > 0:
                    print(f"✅ Download erfolgreich! Dateigröße: {os.path.getsize(temp_path)} bytes")
                else:
                    print("❌ Download fehlgeschlagen: Datei ist leer oder existiert nicht")
            else:
                print(f"❌ Download fehlgeschlagen mit Fehler: {error}")
                print("Hinweise zur Fehlerbehebung:")
                print_hints_on_download_error(str(error))
                
        except Exception as e:
            print(f"❌ Unerwarteter Fehler: {e}")
        
        finally:
            # Clean up
            if os.path.exists(temp_path):
                os.unlink(temp_path)

if __name__ == "__main__":
    print("🔧 Teste verbesserte Download-Funktion...")
    test_download()
    print("\n✅ Test abgeschlossen!")
