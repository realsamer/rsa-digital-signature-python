# RSA Digital Signature — Python

A small, reproducible demonstration of **RSA digital signatures** for the
**Software Security (SDEV 4303)** course, Chapter 2: *Cryptographic Tools*.

The program generates an RSA key pair, signs a message with the private key, and
verifies its signature with the public key. It also tests how verification
responds if the message or signature is changed.

## Features

- Generates a fresh **2048-bit RSA key pair** in memory.
- Signs data using **RSA-PSS**, **SHA-256**, and **MGF1(SHA-256)**.
- Verifies a valid message/signature pair using the public key.
- Demonstrates that changes to the message or signature invalidate verification.
- Displays readable results and exits with a nonzero status if any check fails.

## Requirements

- Python 3.10 or newer
- The [`cryptography`](https://cryptography.io/) package

## Getting started

Download or clone this repository using the **Code** menu on GitHub, then
open a terminal in the `rsa-digital-signature-python` directory.

Create and activate a virtual environment (recommended):

**Windows PowerShell**

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies and run the example:

```bash
python -m pip install -r requirements.txt
python rsa_signature_demo.py
```

If you are using Windows without an activated environment, you can use `py`
instead of `python`.

## Example output

```text
RSA DIGITAL SIGNATURE DEMONSTRATION
-----------------------------------
RSA key size         : 2048 bits
Hash algorithm       : SHA-256
Signature padding    : RSA-PSS (MGF1 with SHA-256)
Original message     : Transfer $1000 to Mark
SHA-256 digest       : e7fee622d165ba8d68be84c42b94612918caa37b57e5b43aa363abac6d74d7cc
Signature length     : 256 bytes
Signature preview    : <hexadecimal value varies between runs>...

VERIFICATION RESULTS
--------------------
1. Original message  : VALID
2. Modified message  : INVALID
3. Changed signature : INVALID

All three tests passed.
```

The signature bytes vary from run to run because each execution generates a new
RSA key pair and RSA-PSS introduces randomness. The verification outcomes should
remain the same.

## How it works

1. **Key generation:** Create a 2048-bit RSA private key and derive its public key.
2. **Signing:** Compute an RSA-PSS signature over the original message using the
   private key and SHA-256.
3. **Valid verification:** Confirm that the original message passes verification
   with the corresponding public key.
4. **Changed message:** Reuse the signature with an altered message. Verification fails.
5. **Changed signature:** Flip one bit of the signature. Verification also fails.

In this example, `verify_signature()` returns `True` for a valid signature and
`False` if `cryptography` raises `InvalidSignature`.

## Expected results

| Scenario | Expected result | Explanation |
| --- | --- | --- |
| Original message and original signature | `VALID` | The signature matches the message and public key. |
| Modified message and original signature | `INVALID` | The signed content no longer matches. |
| Original message and modified signature | `INVALID` | The signature bytes have been altered. |

## Project structure

```text
rsa-digital-signature-python/
├── rsa_signature_demo.py   # RSA signing, verification, and checks
├── requirements.txt        # Python dependency
├── .gitignore              # Excludes local files and secrets
└── README.md               # Project documentation
```

## Security notes

- A **private key** signs; the matching **public key** verifies.
- Digital signatures support message integrity and signer authentication when
  the verifying party can trust the public key's ownership. They **do not
  encrypt or conceal the message**.
- This example creates keys in memory and does not store or print the private key.
- This project is for learning, not a complete production key-management or
  certificate-validation system.

## Academic context

Course: **Software Security — SDEV 4303**  
Chapter: **02 — Cryptographic Tools**  
Instructor: **Dr. Abdelkareem Alashqar**  
Academic year: **2026/2027**
