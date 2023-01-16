import { writable } from "svelte/store";


/**
 * Stores the master key for end-to-end encryption
 * 
 * Structure:
 * {
 *   privKey: string;  - Base64 encoded string of private key
 *   pubKey: string;
 *   auth(something idk)
 * }
 */
export const masterKey = (() => {
  const { subscribe, set } = writable({});

  /**
   * Initialise keys from localStorage
   * 
   * @returns {boolean} true if localStorage has no keys
   */
  function init() {
    if (localStorage.masterKey !== undefined) {
      initKeysFromJson(localStorage.masterKey);
      return false;
    }
    return true;
  }


  function saveMasterKey(key) {
    set(key);
    _saveToLocalStorage(key);
  }


  function _saveToLocalStorage(key) {
    localStorage.masterKey = JSON.stringify(key);
  }


  function initKeysFromJson(data) {
    set(JSON.parse(data));
  }

  return { subscribe, init, saveMasterKey, initKeysFromJson };
})();


/**
 * Stores a collection of encryption keys for end-to-end encryption
 * 
 * Structure:
 * {
 *   room_id <string>: string;  - Base64 encoded string of encryption key
 * }
 */
export const roomKeys = (() => {
  const { subscribe, set, update } = writable({});

  /**
   * Initialise keys from localStorage
   * 
   * @returns {boolean} true if localStorage has no keys
   */
  function init() {
    if (localStorage.roomKeys !== undefined) {
      initKeysFromJson(localStorage.roomKeys);
      return false;
    }
    return true;
  }


  function saveNewKey(room_id, key) {
    update(storage => {
      storage[room_id] = key;
      _saveToLocalStorage(storage);
      return storage;
    });
  }


  function _saveToLocalStorage(roomKeys) {
    localStorage.roomKeys = JSON.stringify(roomKeys);
  }


  function initKeysFromJson(data) {
    set(JSON.parse(data));
  }

  return { subscribe, init, saveNewKey, initKeysFromJson };
})();
