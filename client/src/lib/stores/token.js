import { writable } from "svelte/store";


export const gToken = (() => {
  const { subscribe, set } = writable({});

  /**
   * Initialise Google Access Token from localStorage
   * 
   * @returns {boolean} true if localStorage has no token
   */
  function init() {
    if (localStorage.gToken !== undefined) {
      initKeysFromJson(localStorage.gToken);
      return false;
    }
    return true;
  }


  function saveGToken(token) {
    set(token);
    _saveToLocalStorage(token);
  }


  function _saveToLocalStorage(token) {
    localStorage.gToken = JSON.stringify(token);
  }


  function initKeysFromJson(data) {
    set(JSON.parse(data));
  }

  return { subscribe, init, saveGToken, initKeysFromJson };
})();
