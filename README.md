# IB-EdDSA Digital Signature (Learning Project)

This project helps you understand and visualize how an **Identity-Based EdDSA (IB-EdDSA)** digital signature scheme works in practice.  
It is designed **purely for educational purposes**, aiming to help learners grasp the signing workflow rather than providing a production-ready security system.

---

## Overview

To use this project, you first need a **master secret**.  
The master secret is used as the key for an **HMAC-based hash function** (similar to a normal hash function, but with an additional secret key).

In this repository, the master secret is defined inside the file `IB-EdDSA.py`.  
You need to locate the variable named `mastersecret` and replace it with your own value.

For demonstration purposes, a custom master secret is already provided.  
In real-world systems, companies generate this master secret using highly secure processes.

You may also choose any value for learning and testing, **as long as the master secret is exactly 64 bytes long**.  
You can verify the length of your master secret using the provided script `master_secret.py`.

---

## IB-EdDSA Signing Process

The IB-EdDSA signature scheme in this project consists of **three main steps**:

1. **Key Generation**
2. **Signing**
3. **Verification**

---

### 1. Key Generation

To generate keys, you need a file named `ID.txt`.  
This file can contain **any identity information**, such as:
- An email address  
- A home address  
- A role or position within a company  

You can freely modify the content of `ID.txt` for testing purposes.

After the key generation step, the system produces:
- A **private key**
- A **public key**

These keys can be reused multiple times to sign different documents.

---

### 2. Signing

For the signing step, you need:
- A document to be signed (PDF, DOCX, PPT, or any other file, preferably text-based)
- A **private key** generated in the previous step

After signing, the program outputs a file with the extension `.sig`, which represents the **digital signature** of the document.

---

### 3. Verification

For verification, you need:
- A **public key**
- A **private key**
- The original document
- The corresponding `.sig` signature file

The program verifies the signature using the IB-EdDSA algorithm.

If **any component is altered**, including:
- Using a different key pair  
- Modifying the signature file  
- Changing the original document (even a single character, space, or punctuation mark)

the verification process will fail, indicating that the document has been modified and is no longer trustworthy.

---

## Cryptographic Details

This project uses the **Ed25519 elliptic curve**, which is a modern and widely trusted curve standardized by NIST and commonly used in secure cryptographic systems.

---

## Setup and Execution

First, create a Python virtual environment in the project directory using:

python -m venv venv

Then activate the virtual environment:

source venv/bin/activate   # Linux / macOS

venv\Scripts\Activate      # Windows (PowerShell)

After activation, install the required library:

pip install cryptography

Once the environment is ready, run the program:

python IB-EdDSA.py

## How to Run

When running the program, simply follow the instructions displayed in the terminal.  
The program will guide you step by step through the process of key generation, signing, and verification.

---

## Intended Use and Limitations

This project can also be used for fun experiments, such as:
- Signing a file and letting a friend verify whether you were the signer

While this can be an interesting learning experience, **it is not recommended for real business or production environments**.  
The primary goal of this project is to help learners understand **how digital signature workflows operate**.

For deeper understanding, you are encouraged to study:
- Elliptic curve cryptography
- Digital signature algorithms
- Identity-based cryptographic systems

It is very likely that elliptic curve cryptography will continue to grow and gradually replace some traditional RSA-based signature schemes in the near future.

---

Happy learning!

**Nguyễn Lê Anh Tuấn**
