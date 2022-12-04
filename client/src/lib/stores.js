import { writable } from "svelte/store";

export const allMsgs = (() => {
  const { subscribe, update } = writable({});

  return {
    subscribe,
    addMsg: (msg, room_id) => update(val => val[room_id].push(msg))
  }
})();

export const room_id = (() => {
  const { subscribe, set } = writable("<room_id>");
  return { subscribe, set }
})();

export const user_id = (() => {
  const { subscribe, set } = writable("<user_id>");
  return { subscribe, set }
})();
