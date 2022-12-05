import { writable } from "svelte/store";

// user_id of currently logged in user
export const user_id = (() => {
  // TODO(SpeedFox198): remove this temp value
  const { subscribe, set } = writable("<user_id>");
  return { subscribe, set }
})();


// Collection of all users known/used
export const allUsers = (() => {
  const { subscribe, update } = writable({});

  /* Adds a user entry into the collection
   * Also works with adding multiple users
   * When user_id is specified, assume adding of single user
   * When user_id is unspecified, assume adding of multiple users
   * Good luck using this function (Sorry for making it complicated)
   * TODO(SpeedFox198): if possible in future, simplify this proccess
   */
  async function addUser(user, user_id) {
    update(storage => {
      if (user_id) {
        storage[user_id] = user;
      }
      else {
        Object.assign(storage, user);
      }
      return storage;
    });
  }

  return { subscribe, addUser }
})();
