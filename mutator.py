import hashlib
import binascii
from eth_utils import to_checksum_address

def private_key_to_address(private_key_hex):
    # Convert the private key from hex to bytes
    private_key_bytes = binascii.unhexlify(private_key_hex)
    
    # Generate the public key from the private key
    public_key = hashlib.sha3_256(private_key_bytes).digest()
    
    # Generate the Ethereum address from the public key
    address = hashlib.sha3_256(public_key).digest()[-20:]
    
    # Return the address as a lowercase hex string
    return address.hex()

def guided_search(target_address, starting_private_key):
    # Convert the target address to lowercase
    target_address = target_address.lower()

    # Initialize the current private key
    current_private_key = starting_private_key

    # Loop through possible private keys (you may want to implement a better algorithm here)
    for _ in range(1000000):  # You can adjust this range based on your needs
        # Generate an Ethereum address from the current private key
        generated_address = private_key_to_address(current_private_key)
        
        # Check if the generated address matches the target address
        if generated_address == target_address:
            print(f"Match found! Private key: {current_private_key}")
            return current_private_key
        
        # Optionally, print the current status for debugging
        print(f"Checking private key: {current_private_key} -> Address: {generated_address}")
        
        # Increment the private key (you may need a more sophisticated method)
        current_private_key = increment_private_key(current_private_key)

    print("No match found after guided search.")
    return None

def increment_private_key(private_key_hex):
    # Convert the private key from hex to integer, increment, and convert back to hex
    private_key_int = int(private_key_hex, 16) + 1
    return format(private_key_int, '064x')

# Example usage
if __name__ == "__main__":
    mode = input("Enter '1' to input a single target address or '2' to load a database of addresses: ")
    
    if mode == '1':
        target_address = input("Enter the target Ethereum address: ")
        starting_private_key = input("Enter the starting private key: ")
        guided_search(target_address, starting_private_key)
    else:
        print("Database mode is not implemented in this example.")
