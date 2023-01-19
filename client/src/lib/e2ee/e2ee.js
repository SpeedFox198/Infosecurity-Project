import { encode, decode } from "base64-arraybuffer";

const SEPARATOR = ";";
const SubtleCrypto = crypto.subtle;
const AES_MODE = "AES-GCM";
const EcKeyGenParams = {
  name: "ECDH",
  namedCurve: "P-256"
};


/**
 * Derive the shared secret key,
 * given the current client's private key,
 * and the other client's public key.
 * 
 * @param {CryptoKey} privateKey private ECDH key
 * @param {CryptoKey} publicKey public ECDH key
 * @returns {Promise<CryptoKey>}
 */
function deriveSecretKey(privateKey, publicKey) {
  return SubtleCrypto.deriveKey(
    {
      name: "ECDH",
      public: publicKey
    },
    privateKey,
    {
      name: AES_MODE,
      length: 256
    },
    true,
    ["encrypt", "decrypt"]
  );
}


/**
 * Generate a new pair of private and public keys
 * 
 * @returns {Promise<CryptoKeyPair} private and public keys generated
 */
async function generateKeyPair() {
  return await SubtleCrypto.generateKey(EcKeyGenParams, true, ["deriveKey"]);
}


/**
 * Exports the provided key to a JSON string
 * @param {CryptoKey} key key to be exported
 * @returns {Promise<string>}
 */
async function exportPrivateKey(key) {
  return JSON.stringify(await SubtleCrypto.exportKey("jwk", key));
}

/**
 * Exports the provided key to a Base64 string
 * @param {CryptoKey} key key to be exported
 * @returns {Promise<string>}
 */
async function exportPublicKey(key) {
  return encode(await SubtleCrypto.exportKey("raw", key));
}


/**
 * Imports the JSON string private key
 * @param {string} jwk JSON string key to be imported
 * @returns {Promise<CryptoKey>}
 */
async function importPrivateKey(keyData) {
  return await _importKey("jwk", JSON.parse(keyData), ["deriveKey"]);
}


/**
 * Imports the JSON string public key
 * @param {string} jwk JSON string key to be imported
 * @returns {Promise<CryptoKey>}
 */
async function importPublickey(keyData) {
  return await _importKey("raw", decode(keyData), []);
}


/**
 * Imports the key from keyData using specified format
 * @param {"jwk" | "raw"} format format of key to be imported
 * @param {object} keyData data of key to be imported
 * @param {Array} usage usage of key to be imported
 * @returns {Promise<CryptoKey>}
 */
async function _importKey(format, keyData, usage) {
  return await SubtleCrypto.importKey(format, keyData, EcKeyGenParams, true, usage);
}


function _encodeMessage(message) {
  return (new TextEncoder()).encode(message);
}

function _decodeMessage(encoded) {
  return (new TextDecoder()).decode(encoded);
}


/**
 * Encrypts message using key
 * 
 * @param {*} message message to be encrypted
 * @param {CryptoKey} key key used for encryption
 * @returns {Promise<string>} encrypted message and IV separated by a separator
 */
async function encryptMessage(message, key) {
  const encoded = _encodeMessage(message);
  const iv = crypto.getRandomValues(new Uint8Array(12));
  const encrypted = await SubtleCrypto.encrypt({ name: AES_MODE, iv }, key, encoded);
  return encode(encrypted) + SEPARATOR + encode(iv);
}


/**
 * Decrypts ciphertext using key
 * 
 * @param {string} ciphertext Base64 encoded ciphertext to be decrypted
 * @param {CryptoKey} key key used for decryption
 * @returns {Promise<string>} encrypted message and IV separated by a separator
 */
async function decryptMessage(ciphertext, key) {
  let [encrypted, iv] = ciphertext.split(SEPARATOR);
  iv = decode(iv);
  encrypted = decode(encrypted);
  const decrypted = await SubtleCrypto.decrypt({ name: AES_MODE, iv }, key, encrypted);
  return _decodeMessage(decrypted);
}


// Export functions for svelte components to use
export const e2ee = {
  generateKeyPair,
  exportPrivateKey,
  exportPublicKey,
  importPrivateKey,
  importPublickey,
  deriveSecretKey,
  encryptMessage,
  decryptMessage
};
