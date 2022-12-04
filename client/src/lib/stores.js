import { derived, writable } from "svelte/store";

export const allMsgs = (() => {
  const { subscribe, update } = writable({'a':3});

  return {
    subscribe,
    addMsg: (msg, room_id) => update(val => {
      let roomMsgs = val[room_id];
      if (!roomMsgs) roomMsgs = [];
      roomMsgs.push(msg);
      return roomMsgs;
    })
  }
})();

export const room_id = (() => {
  const { subscribe, set } = writable("a");
  return { subscribe, set }
})();

export const roomMsgs = derived(
  [allMsgs, room_id],
  ([$allMsgs, $room_id]) => {
    let roomMsgs = $allMsgs[$room_id];
    if (!roomMsgs) roomMsgs = [];
    return roomMsgs;
  }
);

export const user_id = (() => {
  const { subscribe, set } = writable("<user_id>");
  return { subscribe, set }
})();
