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
    if (localStorage.masterKey === undefined) {
      return true;
    }
    initFromJson(localStorage.masterKey);
    return false;
  }


  function saveMasterKey(key) {
    set(key);
    _saveToLocalStorage(key);
  }


  function _saveToLocalStorage(key) {
    localStorage.masterKey = JSON.stringify(key);
  }


  function initFromJson(data, store) {
    set(JSON.parse(data));
    if (store) {
      localStorage.masterKey = data;
    }
  }

  return { subscribe, init, initFromJson, saveMasterKey };
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
    if (localStorage.roomKeys === undefined) {
      return true;
    }
    initFromJson(localStorage.roomKeys);
    return false;
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

  function initFromJson(data, store) {
    set(JSON.parse(data));
    if (store) {
      localStorage.roomKeys = data;
    }
  }

  return { subscribe, init, initFromJson, saveNewKey };
})();
