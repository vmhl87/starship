const crypto = require('crypto');
const fs = require('fs');

const FIXED_SALT = Buffer.from("fixed_salt_value_16"); // Fixed salt (16 bytes)

function deriveKey(password) {
    return new Promise((resolve, reject) => {
        crypto.pbkdf2(password, FIXED_SALT, 100000, 32, 'sha256', (err, key) => {
            if (err) reject(err);
            resolve(key);
        });
    });
}

async function encrypt(plaintext, password) {
    const iv = crypto.randomBytes(12); // Generate a random IV (12 bytes)
    const key = await deriveKey(password);
    
    const cipher = crypto.createCipheriv('aes-256-gcm', key, iv);
    let ciphertext = cipher.update(plaintext, 'utf8', 'base64');
    ciphertext += cipher.final('base64');
    const tag = cipher.getAuthTag(); // Get the authentication tag

    // Concatenate IV, tag, and ciphertext
    const combined = Buffer.concat([iv, tag, Buffer.from(ciphertext, 'base64')]);
    return combined.toString('base64'); // Return as base64
}

async function decrypt(ciphertext_b64, password) {
    const data = Buffer.from(ciphertext_b64, 'base64');
    
    const iv = data.slice(0, 12); // Extract the IV (first 12 bytes)
    const tag = data.slice(12, 28); // Extract the tag (next 16 bytes)
    const ciphertext = data.slice(28); // Extract the ciphertext (remaining bytes)
    
    const key = await deriveKey(password);
    
    const decipher = crypto.createDecipheriv('aes-256-gcm', key, iv);
    decipher.setAuthTag(tag); // Set the authentication tag
    let plaintext = decipher.update(ciphertext, undefined, 'utf8');
    plaintext += decipher.final('utf8');
    
    return plaintext;
}

// File I/O Functions
async function encryptFile(inputFilePath, outputFilePath, password) {
    // Read plaintext from input file
    const plaintext = fs.readFileSync(inputFilePath, 'utf8');
    const ciphertext = await encrypt(plaintext, password);
    
    // Write ciphertext to output file
    fs.writeFileSync(outputFilePath, ciphertext);
    console.log(`Encrypted text written to ${outputFilePath}`);
}

async function decryptFile(inputFilePath, outputFilePath, password) {
    // Read ciphertext from input file
    const ciphertext = fs.readFileSync(inputFilePath, 'utf8');
    const plaintext = await decrypt(ciphertext, password);
    
    // Write plaintext to output file
    fs.writeFileSync(outputFilePath, plaintext);
    console.log(`Decrypted text written to ${outputFilePath}`);
}

(async () => {
    const password = fs.readFileSync('/tmp/password.txt', 'utf8');  // Use a secure password
    const inputFilePath = '/tmp/input.txt';       // Input file containing plaintext
    const encryptedFilePath = '/tmp/encrypted.txt'; // Output file for ciphertext
    await encryptFile(inputFilePath, encryptedFilePath, password);
    const decryptedFilePath = '/tmp/decrypted.txt'; // Output file for ciphertext
    await decryptFile('/tmp/input2.txt', decryptedFilePath, password);
})();
