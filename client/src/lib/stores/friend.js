import { writable } from "svelte/store";

export const friends = (() => {
  const { subscribe, set, update } = writable([]);

  async function addFriend(user) {
    update(storage => {
      storage.push(user)
      return storage;
    });
  }

  return { subscribe, set, addFriend };
})();