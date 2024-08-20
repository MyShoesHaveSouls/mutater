import os
import binascii
import hashlib
import concurrent.futures
import time
from datetime import timedelta

def private_key_to_address(private_key):
    private_key_bytes = binascii.unhexlify(private_key)
    blake2b_hash = hashlib.blake2b(digest_size=32)
    blake2b_hash.update(private_key_bytes)
    return '0x' + blake2b_hash.hexdigest()[-40:]

def mutate_private_key(private_key, position, new_char):
    return private_key[:position] + new_char + private_key[position+1:]

def guided_search_worker(target_address, start_private_key, position, char_set):
    current_key = start_private_key
    current_address = private_key_to_address(current_key)

    for char in char_set:
        new_key = mutate_private_key(current_key, position-2, char)
        new_address = private_key_to_address(new_key)
        if new_address[:position+1] == target_address[:position+1]:
            return new_key, new_address

    return None

def parallel_guided_search(target_address, start_private_key, num_workers):
    current_key = start_private_key
    current_address = private_key_to_address(current_key)

    for i in range(2, len(target_address)):
        if current_address[i] == target_address[i]:
            continue

        char_set = '0123456789abcdef'
        with concurrent.futures.ProcessPoolExecutor(max_workers=num_workers) as executor:
            futures = [executor.submit(guided_search_worker, target_address, current_key, i, char_set) for _ in range(num_workers)]

            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result:
                    current_key, current_address = result
                    break

        # Progress reporting
        if i % 100 == 0 or i == len(target_address) - 1:
            print(f"Currently matching character {i+1} of the target address: {target_address[i]}")

        if current_address == target_address:
            print(f"Match found! Address: {current_address}, Private Key: {current_key}")
            return current_key, current_address

    print(f"No match found after guided search for {target_address}.")
    return None

def process_addresses(target_addresses, start_private_key, num_workers):
    start_time = time.time()

    for target_address in target_addresses:
        print(f"Starting guided search for target address: {target_address}")
        parallel_guided_search(target_address, start_private_key, num_workers)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Total execution time: {timedelta(seconds=elapsed_time)}")

def load_addresses(file_path):
    with open(file_path, 'r') as file:
        addresses = [line.strip().lower() for line in file]
    return addresses

def main():
    option = input("Enter '1' to input a single target address or '2' to load a database of addresses: ").strip()
    
    if option == '1':
        target_address = input("Enter the target Ethereum address: ").strip().lower()
        target_addresses = [target_address]
    elif option == '2':
        addresses_file = input("Enter the path to the addresses database file: ").strip()
        target_addresses = load_addresses(addresses_file)
    else:
        print("Invalid option. Exiting...")
        return

    start_private_key = binascii.hexlify(os.urandom(32)).decode('utf-8')  # Generate a random starting key
    print(f"Starting private key: {start_private_key}")

    num_workers = os.cpu_count()  # Adjust this based on your hardware
    process_addresses(target_addresses, start_private_key, num_workers)

if __name__ == "__main__":
    main()
