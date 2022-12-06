import { derived, writable } from "svelte/store";
import { room_id } from "./rooms";

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

// TODO(SpeedFox198): consider removing this later
// especially since it seems like it's only used once
// and if it's removed, rmb to remove the import
export const roomMsgs = derived(
  [allMsgs, room_id],
  ([$allMsgs, $room_id]) => {
    // Get room messages array
    let roomMsgs = $allMsgs[$room_id];

    // If room messages array does not exist
    if (!roomMsgs) roomMsgs = [];

    // Return room messages array
    return roomMsgs;
  }
);
