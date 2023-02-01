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
 * Exports the provided private key to a JSON string
 * @param {CryptoKey} key private key to be exported
 * @returns {Promise<string>}
 */
async function exportPrivateKey(key) {
  return JSON.stringify(await SubtleCrypto.exportKey("jwk", key));
}


/**
 * Exports the provided public key to a Base64 string
 * @param {CryptoKey} key public key to be exported
 * @returns {Promise<string>}
 */
async function exportPublicKey(key) {
  return encode(await SubtleCrypto.exportKey("raw", key));
}


/**
 * Exports the provided room key to a Base64 string
 * @param {CryptoKey} key room key to be exported
 * @returns {Promise<string>}
 */
async function exportRoomKey(key) {
  return encode(await SubtleCrypto.exportKey("raw", key));
}

/**
 * Imports the JSON string private key
 * @param {string} keyData JSON string key to be imported
 * @returns {Promise<CryptoKey>}
 */
async function importPrivateKey(keyData) {
  return await _importKey("jwk", JSON.parse(keyData), ["deriveKey"]);
}


/**
 * Imports the Base64 string public key
 * @param {string} keyData Base64 string key to be imported
 * @returns {Promise<CryptoKey>}
 */
async function importPublickey(keyData) {
  return await _importKey("raw", decode(keyData), []);
}


/**
 * Imports the Base64 string room key
 * @param {string} keyData Base64 string key to be imported
 * @returns {Promise<CryptoKey>}
 */
async function importRoomKey(keyData) {
  return await SubtleCrypto.importKey("raw", decode(keyData), "AES-GCM", true, ["encrypt", "decrypt"]);
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
 * Returns the array buffer of a file
 * @param {File} file object
 * @returns {Promise<ArrayBuffer>} array buffer of file
 */
async function _encodeFile(file) {
  return await file.arrayBuffer();
}

/**
 * Encrypts data using key
 * 
 * @param {ArrayBuffer} data data to be encrypted
 * @param {CryptoKey} key key used for encryption
 * @returns {Promise<string>} encrypted data and IV separated by a separator
 */
async function _encrypt(data, key) {
  const iv = crypto.getRandomValues(new Uint8Array(12));
  const encrypted = await SubtleCrypto.encrypt({ name: AES_MODE, iv }, key, data);
  return encode(encrypted) + SEPARATOR + encode(iv);
}


/**
 * Decrypts ciphertext using key
 * 
 * @param {string} ciphertext Base64 encoded ciphertext to be decrypted
 * @param {CryptoKey} key key used for decryption
 * @returns {Promise<ArrayBuffer>} decrypted message
 */
async function _decrypt(ciphertext, key) {
  let [encrypted, iv] = ciphertext.split(SEPARATOR);
  iv = decode(iv);
  encrypted = decode(encrypted);
  return _decryptRaw(encrypted, key, iv);
}


/**
 * Decrypts encrypted content using key and iv
 * 
 * @param {BufferSource} encrypted string to be decoded
 * @param {CryptoKey} key key used for decryption
 * @param {ArrayBuffer} iv iv used for decryption
 * @returns {Promise<ArrayBuffer>} decrypted content
 */
async function _decryptRaw(encrypted, key, iv) {
  return await SubtleCrypto.decrypt({ name: AES_MODE, iv }, key, encrypted);
}


/**
 * Encrypts message using key
 * 
 * @param {string} message message to be encrypted
 * @param {CryptoKey} key key used for encryption
 * @returns {Promise<string>} encrypted message and IV separated by a separator
 */
async function encryptMessage(message, key) {
  return await _encrypt(_encodeMessage(message), key);
}


/**
 * Decrypts ciphertext using key
 * 
 * @param {string} ciphertext Base64 encoded ciphertext to be decrypted
 * @param {CryptoKey} key key used for decryption
 * @returns {Promise<string>} decrypted message
 */
async function decryptMessage(ciphertext, key) {
  return _decodeMessage(await _decrypt(ciphertext, key));
}


/**
 * Decrypts encrypted image using key
 * 
 * @param {Blob} encryptedImage Blob image file object
 * @param {CryptoKey} key key used for decryption
 * @returns {Promise<Blob>} decrypted image
 */
async function decryptImage(encryptedImage, key) {
  // TODO(high)(SpeedFox198): change the iv from hardcoded
  let content = await _encodeFile(encryptedImage)
  content = await _decryptRaw(content, key, decode("yv7K/sr+"));
  return new Blob([content], {type: "image/png"});
}


// Export functions for svelte components to use
export const e2ee = {
  generateKeyPair,
  exportPrivateKey,
  exportPublicKey,
  exportRoomKey,
  importPrivateKey,
  importPublickey,
  importRoomKey,
  deriveSecretKey,
  encryptMessage,
  decryptMessage,
  decryptImage
};
