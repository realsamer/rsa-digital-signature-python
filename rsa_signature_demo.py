"""Demonstrate RSA digital signing and verification with SHA-256 and RSA-PSS.

Run this educational example with: python rsa_signature_demo.py
The RSA key pair is generated in memory for each execution.
"""

import hashlib

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa


ORIGINAL_MESSAGE = b"Send message to Dr. Abdelkareem Alashqar"
MODIFIED_MESSAGE = b"Transfer message to Dr. Abdelkareem Alashqar"
RSA_KEY_SIZE = 2048


def pss_padding() -> padding.PSS:
    """Return identical RSA-PSS parameters for signing and verification."""
    return padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH,
    )


def verify_signature(
    public_key: rsa.RSAPublicKey, message: bytes, signature: bytes
) -> bool:
    """Verify an RSA-PSS signature; return False for an invalid signature."""
    try:
        public_key.verify(signature, message, pss_padding(), hashes.SHA256())
        return True
    except InvalidSignature:
        return False


def main() -> int:
    """Sign once, run three verification checks, and report their results."""
    # 1. Generate a fresh RSA key pair. The private key is never exported.
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=RSA_KEY_SIZE,
    )
    public_key = private_key.public_key()

    # 2. Sign the original message with the private key.
    signature = private_key.sign(
        ORIGINAL_MESSAGE,
        pss_padding(),
        hashes.SHA256(),
    )

    # 3. Verify the genuine message and signature with the public key.
    original_valid = verify_signature(public_key, ORIGINAL_MESSAGE, signature)

    # 4. Change the message while keeping the original signature.
    modified_message_valid = verify_signature(
        public_key, MODIFIED_MESSAGE, signature
    )

    # 5. Corrupt one bit of the signature while keeping the original message.
    corrupted_signature = bytes([signature[0] ^ 0x01]) + signature[1:]
    modified_signature_valid = verify_signature(
        public_key, ORIGINAL_MESSAGE, corrupted_signature
    )

    print("RSA DIGITAL SIGNATURE DEMONSTRATION")
    print("-----------------------------------")
    print(f"RSA key size         : {private_key.key_size} bits")
    print("Hash algorithm       : SHA-256")
    print("Signature padding    : RSA-PSS (MGF1 with SHA-256)")
    print(f"Original message     : {ORIGINAL_MESSAGE.decode('utf-8')}")
    print(f"SHA-256 digest       : {hashlib.sha256(ORIGINAL_MESSAGE).hexdigest()}")
    print(f"Signature length     : {len(signature)} bytes")
    print(f"Signature preview    : {signature.hex()[:48]}...")
    print()
    print("VERIFICATION RESULTS")
    print("--------------------")
    print(f"1. Original message  : {'VALID' if original_valid else 'INVALID'}")
    print(f"2. Modified message  : {'VALID' if modified_message_valid else 'INVALID'}")
    print(f"3. Changed signature : {'VALID' if modified_signature_valid else 'INVALID'}")

    all_passed = (
        original_valid
        and not modified_message_valid
        and not modified_signature_valid
    )
    print(f"\n{'All three tests passed.' if all_passed else 'One or more tests failed.'}")
    return 0 if all_passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
