import { writable, derived } from "svelte/store";

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


// True if friend list has not  been initialised yet
export const friendsNeedInit = derived(
  friends,
  $friends => Object.keys($friends).length === 0
);