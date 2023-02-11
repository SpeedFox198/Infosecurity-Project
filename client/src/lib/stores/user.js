import { writable } from "svelte/store";

// user_id of currently logged in user
export const user_id = (() => {
  const { subscribe, set } = writable("");
  return { subscribe, set };
})();


export const globalUser = (() => {
  const { subscribe, update, set } = writable({});
  async function enableEncryption() {
    update(storage => {
      storage.e2ee = true;
      return storage;
    });
  }
  return { subscribe, enableEncryption, set };
})();


// Collection of all users known/used
export const allUsers = (() => {
  const { subscribe, update } = writable({});

  /* Adds a user entry into the collection
   * Also works with adding multiple users
   * When user_id is specified, assume adding of single user
   * When user_id is unspecified, assume adding of multiple users
   * Good luck using this function (Sorry for making it complicated)
   * TODO(low)(SpeedFox198): if possible in future, simplify this proccess
   */
  async function addUser(user, user_id) {
    update(storage => {
      if (user_id) {
        storage[user_id] = user;
      } else {
        Object.assign(storage, user);
      }
      return storage;
    });
  }

  return { subscribe, addUser };
})();
