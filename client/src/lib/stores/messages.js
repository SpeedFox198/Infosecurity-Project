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

  async function changeId(temp_id, message_id, time) {
    update(storage => {
      // Change temp_id to message_id
      storage[message_id] = storage[temp_id];
      delete storage[temp_id];

      // Add time attribute
      storage[message_id].time = time;

      return storage;
    });
  }

  return { subscribe, updateMsg, changeId };
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

  async function initRooms(rooms) {
    update(storage => {
      for (let i; i < rooms.length; i++) {
        storage[rooms[i].room_id] = [];
      }
      return storage;
    });
  }

  async function changeId(temp_id, message_id, room_id) {
    update(storage => {

      // Get index of temp_id in storage
      const index = storage[room_id].indexOf(temp_id);

      // Replace temp_id with message_id
      if (index > -1) storage[room_id][index] = message_id;

      return storage;
    });
  }

  return { subscribe, addMsg, initRooms, changeId };
})();
