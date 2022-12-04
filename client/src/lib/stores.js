import { derived, writable } from "svelte/store";


export const allMsgs = (() => {
  const { subscribe, update } = writable({});

  async function addMsg (msg, room_id) {
    update(storage => {

      // Get room messages array
      let roomMsgs = storage[room_id];
  
      // If room messages does not exist, create array for it
      if (!roomMsgs) {
        storage[room_id] = [];
        roomMsgs = storage[room_id];
      }
  
      // Add new message to array
      roomMsgs.push(msg);
      return storage;
    });
  }

  return {subscribe, addMsg};
})();


export const room_id = (() => {
  const { subscribe, set } = writable("<room_id>");
  return { subscribe, set }
})();


export const roomMsgs = derived(
  [allMsgs, room_id],
  ([$allMsgs, $room_id]) => {
    // Get room messages array
    let roomMsgs = $allMsgs[$room_id]

    // If room messages array does not exist
    if (!roomMsgs) roomMsgs = [];

    // Return room messages array
    return roomMsgs;
  }
);


export const user_id = (() => {
  const { subscribe, set } = writable("<user_id>");
  return { subscribe, set }
})();
