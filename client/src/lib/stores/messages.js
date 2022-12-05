import { derived, writable } from "svelte/store";

export const allMsgs = (() => {
  const { subscribe, update } = writable({});

  async function addMsg (msg, room_id, add_prev) {
    update(storage => {

      // Get room messages array
      let roomMsgs = storage[room_id];

      // If room messages does not exist, create array for it
      if (!roomMsgs) {
        roomMsgs = [];
        storage[room_id] = roomMsgs;
      }

      if (!add_prev) {  // Add new message to array
        roomMsgs.push(msg);
      }
      else {  // Add older(previous) messages to front of array
        roomMsgs.unshift.apply(msg, roomMsgs);
      }

      return storage;
    });
  }

  return { subscribe, addMsg };
})();


export const room_id = (() => {
  // TODO(SpeedFox198): remove this temp value
  const { subscribe, set } = writable("");
  return { subscribe, set }
})();


// TODO(SpeedFox198): consider removing this later
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
