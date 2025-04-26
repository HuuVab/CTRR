import time
import random
import matplotlib.pyplot as plt
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes

def generate_rsa_keys(key_size=2048):
    """Generate RSA public and private keys."""
    # Start key generation time measurement
    start_time = time.time()
    
    # Generate a private key with the specified key size
    private_key = rsa.generate_private_key(
        public_exponent=65537,  # Standard value for e
        key_size=key_size
    )
    
    # Extract the public key from the private key
    public_key = private_key.public_key()
    
    # End key generation time measurement
    generation_time = time.time() - start_time
    print(f"Key generation time: {generation_time:.4f} seconds")
    
    return private_key, public_key

def encrypt_message(message, public_key):
    """Encrypt a message using RSA public key."""
    # Convert string message to bytes if necessary
    if isinstance(message, str):
        message = message.encode('utf-8')
    
    # Encrypt the message using OAEP padding
    ciphertext = public_key.encrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    
    return ciphertext

def decrypt_message(ciphertext, private_key):
    """Decrypt a message using RSA private key."""
    # Decrypt the ciphertext using OAEP padding
    plaintext = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    
    # Convert decrypted bytes back to string
    return plaintext.decode('utf-8')

def test_rsa_encryption_decryption():
    """Test RSA encryption and decryption with a sample message."""
    # Generate RSA keys
    private_key, public_key = generate_rsa_keys()
    
    # Sample message
    original_message = "This is a test message for RSA encryption and decryption."
    
    # Encrypt the message
    print(f"Original message: {original_message}")
    encrypted_message = encrypt_message(original_message, public_key)
    print(f"Encrypted message (bytes): {encrypted_message[:50]}... (truncated)")
    
    # Decrypt the message
    decrypted_message = decrypt_message(encrypted_message, private_key)
    print(f"Decrypted message: {decrypted_message}")
    
    # Verify decryption
    assert original_message == decrypted_message, "Decryption failed!"
    print("Verification: The decrypted message matches the original message.")

def measure_rsa_performance(max_length=180, step=20):
    """Measure RSA encryption and decryption performance for different message lengths.
    Note: Using conservative max_length to avoid encryption errors."""
    # Generate RSA keys
    private_key, public_key = generate_rsa_keys()
    
    # Get approximate maximum message size for this key
    # For 2048-bit key with OAEP padding using SHA-256, max size is typically around 190 bytes
    # We'll use a conservative value to be safe
    key_size = private_key.key_size
    max_safe_length = (key_size // 8) - 66  # Very conservative estimate for OAEP with SHA-256
    
    print(f"Using RSA key size: {key_size} bits")
    print(f"Maximum safe message length: ~{max_safe_length} bytes (conservative estimate)")
    
    # Limit max_length to be safe
    if max_length > max_safe_length:
        max_length = max_safe_length
        print(f"Limiting maximum test length to {max_length} bytes to prevent encryption errors")
    
    # Initialize lists to store results
    message_lengths = []
    encryption_times = []
    decryption_times = []
    
    for length in range(step, max_length + 1, step):
        # Generate a random message of specified length
        message = ''.join(random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') 
                         for _ in range(length))
        
        try:
            # Measure encryption time
            start_time = time.time()
            encrypted_message = encrypt_message(message, public_key)
            encryption_time = time.time() - start_time
            
            # Measure decryption time
            start_time = time.time()
            decrypted_message = decrypt_message(encrypted_message, private_key)
            decryption_time = time.time() - start_time
            
            # Verify decryption worked
            if message != decrypted_message:
                print(f"Warning: Decryption failed for message length {length}!")
                continue
                
            # Add to results
            message_lengths.append(length)
            encryption_times.append(encryption_time)
            decryption_times.append(decryption_time)
            
            print(f"Message length: {length}, Encryption time: {encryption_time:.6f}s, Decryption time: {decryption_time:.6f}s")
        
        except Exception as e:
            print(f"Error with message length {length}: {e}")
            break
    
    # Demonstrate RSA message size limitation
    print("\nDemonstrating RSA message size limitation:")
    boundary_test(public_key, max_safe_length)
    
    return message_lengths, encryption_times, decryption_times

def boundary_test(public_key, estimated_max):
    """Test message sizes around the boundary to demonstrate RSA limitations."""
    sizes_to_test = [
        estimated_max - 20,
        estimated_max - 10,
        estimated_max,
        estimated_max + 10,
        estimated_max + 20,
        estimated_max + 50
    ]
    
    for size in sizes_to_test:
        message = 'A' * size
        try:
            start_time = time.time()
            encrypt_message(message, public_key)
            encryption_time = time.time() - start_time
            print(f"Size {size} bytes: Successfully encrypted in {encryption_time:.6f}s")
        except Exception as e:
            print(f"Size {size} bytes: Encryption failed - {str(e)}")

def plot_rsa_performance(message_lengths, encryption_times, decryption_times):
    """Plot RSA encryption and decryption performance."""
    plt.figure(figsize=(10, 6))
    
    plt.plot(message_lengths, encryption_times, 'b-o', label='Encryption Time')
    plt.plot(message_lengths, decryption_times, 'r-o', label='Decryption Time')
    
    plt.xlabel('Message Length (characters)')
    plt.ylabel('Time (seconds)')
    plt.title('RSA Encryption and Decryption Performance')
    plt.legend()
    plt.grid(True)
    
    plt.savefig('rsa_performance.png')
    print("Performance plot saved as 'rsa_performance.png'")

def demonstrate_hybrid_encryption():
    """Demonstrate a simplified version of hybrid encryption (RSA + simulated symmetric)."""
    print("\nDemonstrating Hybrid Encryption Approach:")
    print("-" * 60)
    
    # 1. Generate RSA keys
    private_key, public_key = generate_rsa_keys()
    
    # 2. Generate a random symmetric key (in a real system, this would be an AES key)
    symmetric_key = ''.join(random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') 
                           for _ in range(32))
    print(f"Generated symmetric key: {symmetric_key[:10]}... (truncated)")
    
    # 3. Encrypt the symmetric key with RSA
    start_time = time.time()
    encrypted_sym_key = encrypt_message(symmetric_key, public_key)
    rsa_time = time.time() - start_time
    print(f"RSA-encrypted symmetric key (bytes): {encrypted_sym_key[:20]}... (truncated)")
    print(f"RSA encryption time for key: {rsa_time:.6f}s")
    
    # 4. Simulate encrypting a large message with the symmetric key
    large_message = "This is a very large message that would be too big for RSA encryption. " * 20
    print(f"Large message length: {len(large_message)} characters")
    
    # Simulate symmetric encryption (just XOR with key for demonstration)
    start_time = time.time()
    # This is NOT secure encryption - just a simulation!
    simulated_encrypted = ''.join(chr(ord(m) ^ ord(symmetric_key[i % len(symmetric_key)])) 
                                 for i, m in enumerate(large_message))
    sym_encryption_time = time.time() - start_time
    print(f"Simulated symmetric encryption time: {sym_encryption_time:.6f}s")
    print(f"Total encryption time: {rsa_time + sym_encryption_time:.6f}s")
    
    # 5. Decryption process
    # First decrypt the symmetric key using RSA
    start_time = time.time()
    decrypted_sym_key = decrypt_message(encrypted_sym_key, private_key)
    rsa_decryption_time = time.time() - start_time
    
    # Then simulate decrypting the message using the symmetric key
    start_time = time.time()
    simulated_decrypted = ''.join(chr(ord(c) ^ ord(decrypted_sym_key[i % len(decrypted_sym_key)])) 
                                 for i, c in enumerate(simulated_encrypted))
    sym_decryption_time = time.time() - start_time
    
    print(f"RSA decryption time for key: {rsa_decryption_time:.6f}s")
    print(f"Simulated symmetric decryption time: {sym_decryption_time:.6f}s")
    print(f"Total decryption time: {rsa_decryption_time + sym_decryption_time:.6f}s")
    
    # Verify
    assert symmetric_key == decrypted_sym_key
    assert large_message == simulated_decrypted
    print("Verification: Hybrid encryption/decryption successful")

def main():
    # Test RSA encryption and decryption
    print("\nTesting RSA Encryption and Decryption:")
    print("-" * 60)
    test_rsa_encryption_decryption()
    
    # Measure and plot performance
    print("\nMeasuring RSA Performance:")
    print("-" * 60)
    message_lengths, encryption_times, decryption_times = measure_rsa_performance()
    
    # Only plot if we have data
    if message_lengths:
        plot_rsa_performance(message_lengths, encryption_times, decryption_times)
    
    # Demonstrate hybrid approach
    demonstrate_hybrid_encryption()
    
    # Discuss limitations and recommendations
    print("\nLimitations of RSA Cryptosystem:")
    print("-" * 60)
    print("1. Performance: RSA is significantly slower than symmetric encryption algorithms")
    print("2. Message Size Limitation: RSA can only encrypt data up to the key size minus padding (as demonstrated)")
    print("3. Security Concerns: Vulnerable to quantum computing attacks")
    print("4. Key Management: RSA requires secure key distribution mechanisms")
    print("5. Computational Intensity: RSA operations are computationally expensive")
    
    print("\nRecommendations for Improvement:")
    print("-" * 60)
    print("1. Hybrid Encryption: Use RSA for key exchange and symmetric encryption for data")
    print("2. Increase Key Size: Use 3072 or 4096-bit keys for long-term security")
    print("3. Implement Proper Padding: Always use secure padding schemes like OAEP")
    print("4. Consider Elliptic Curve Cryptography (ECC) as an alternative to RSA")
    print("5. Implement secure random number generation for key generation")
    print("6. Use chunking for large messages if hybrid encryption is not an option")

if __name__ == "__main__":
    main()