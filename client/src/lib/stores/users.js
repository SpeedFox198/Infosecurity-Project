import { derived, writable } from "svelte/store";

export const user_id = (() => {
  // TODO(SpeedFox198): remove this temp value
  const { subscribe, set } = writable("<user_id>");
  return { subscribe, set }
})();


export const allUsers = (() => {
  const { subscribe, update } = writable({})

  async function addUser(user_id, user) {
    update(storage => storage[user_id] = user);
  }

  return {subscribe, addUser}
})();
