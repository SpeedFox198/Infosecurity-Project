import { writable } from "svelte/store";


// Generates and returns an increasing temp_id
export const getTempId = (() => {
  const { update } = writable(0);

  return () => {
    let n;
    update(update => {
      n = update;
      return n + 1;
    });
    return n;
  }
})();


export const msgStorage = (() => {
  const { subscribe, update } = writable({});

  // Adds a new message or updates an existing message
  async function updateMsg(message_id, msg) {
    update(storage => {
      storage[message_id] = msg;  // Add new message to storage
      return storage;
    });
  }

  return { subscribe, updateMsg };
})();


export const allMsgs = (() => {
  const { subscribe, update } = writable({});

  async function addMsg(message_id, room_id, add_prev) {
    update(storage => {

      // Get room messages array
      let roomMsgs = storage[room_id];

      // If room messages does not exist, create array for it
      if (!roomMsgs) {
        roomMsgs = [];
        storage[room_id] = roomMsgs;
      }

      if (!add_prev) {  // Add new message to array
        roomMsgs.push(message_id);
      }
      else {  // Add older(previous) messages to front of array
        roomMsgs.unshift.apply(message_id, roomMsgs);
      }

      return storage;
    });
  }

  return { subscribe, addMsg };
})();
