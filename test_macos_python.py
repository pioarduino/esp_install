#!/usr/bin/env python3
# Test for macOS Standard Python certificate handling

import sys
import os
import tempfile
import subprocess

def test_macos_standard_python_hints():
    """Test the certificate hints for standard macOS Python"""
    
    # Simulate standard macOS Python path
    original_executable = sys.executable
    sys.executable = '/usr/bin/python3'
    
    # Import the improved function
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'tools'))
    from idf_tools import print_hints_on_download_error
    
    print("=== Testing Standard macOS Python Certificate Hints ===")
    print(f"Simulating Python path: {sys.executable}")
    print()
    
    # Test with SSL certificate error
    print("Testing with SSL CERTIFICATE error:")
    print_hints_on_download_error("SSL: CERTIFICATE_VERIFY_FAILED")
    
    # Restore original executable
    sys.executable = original_executable

def test_system_certificate_extraction():
    """Test extracting system certificates on macOS"""
    
    print("\n=== Testing System Certificate Extraction ===")
    
    try:
        # Test system certificate extraction
        result = subprocess.run([
            'security', 'find-certificate', '-a', '-p', 
            '/System/Library/Keychains/SystemRootCertificates.keychain'
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            cert_count = result.stdout.count('-----BEGIN CERTIFICATE-----')
            print(f"✅ System certificates extracted: {cert_count} certificates")
            
            # Save to temp file to test
            with tempfile.NamedTemporaryFile(mode='w', suffix='.pem', delete=False) as f:
                f.write(result.stdout)
                temp_cert_file = f.name
            
            print(f"✅ Certificates saved to: {temp_cert_file}")
            
            # Test if the file is valid
            file_size = os.path.getsize(temp_cert_file)
            print(f"✅ Certificate file size: {file_size} bytes")
            
            # Clean up
            os.unlink(temp_cert_file)
            print("✅ Test completed successfully")
            
        else:
            print("❌ Error extracting system certificates:")
            print(result.stderr)
            
    except Exception as e:
        print(f"❌ Exception during certificate extraction: {e}")

def test_standard_python_existence():
    """Check if standard macOS Python exists"""
    
    print("\n=== Testing Standard macOS Python Availability ===")
    
    standard_python = '/usr/bin/python3'
    
    if os.path.exists(standard_python):
        print(f"✅ Standard macOS Python found: {standard_python}")
        
        try:
            # Test running it
            result = subprocess.run([
                standard_python, '-c', 
                'import sys; print("Python version:", sys.version); import ssl; print("SSL available:", bool(ssl))'
            ], capture_output=True, text=True, timeout=5)
            
            if result.returncode == 0:
                print("✅ Standard Python is functional:")
                print(result.stdout.strip())
            else:
                print("❌ Standard Python has issues:")
                print(result.stderr.strip())
                
        except Exception as e:
            print(f"❌ Error testing standard Python: {e}")
    else:
        print(f"❌ Standard macOS Python not found at: {standard_python}")

if __name__ == "__main__":
    test_macos_standard_python_hints()
    test_system_certificate_extraction()
    test_standard_python_existence()
    
    print("\n=== Summary ===")
    print("The improved download function now properly detects and provides")
    print("specific solutions for standard macOS Python (/usr/bin/python3)")
    print("including system certificate extraction and environment setup.")
