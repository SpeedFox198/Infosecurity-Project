import { writable } from "svelte/store";


// Generates and returns an increasing temp_id
export const getTempId = (() => {
  const { update } = writable(0);

  return () => {
    let n;
    update(storage => {
      n = ++storage;
      return storage;
    });
    return n;
  }
})();


/*
 * Stores a collection of message objects identified by their message_id
 *
 * Structure:
 * {
 *   <message_id>: {
 *     sent: boolean;      - True if message was sent by current user
 *     time: int;          - Timestamp in unix time format
 *     content: string;    - Content of message
 *     reply_to: string;   - message_id of message being replied to TODO(low)(SpeedFox198): remove when unsused
 *     type: string;       - Type of message
 *     corner?: boolean;   - True if message is last of consecutive messages sent by same user
 *     username?: string;  - Username of user that sent the message
 *     avatar?: string;    - Path to image of avatar of user
 *   },
 *   ...
 * }
 */
export const msgStorage = (() => {
  const { subscribe, update } = writable({});

  // Adds a new message or updates an existing message
  async function updateMsg(msg, message_id) {
    update(storage => {
      // Read documentation for function in user.js for how this logic works
      if (message_id) {
        storage[message_id] = msg;  // Add new message to storage
      } else {
        Object.assign(storage, msg);
      }
      return storage;
    });
  }

  // Change message_id from temp_id to new id received from server
  async function changeId(temp_id, message_id, time, filename) {
    update(storage => {
      // Change temp_id to message_id
      storage[message_id] = storage[temp_id];
      delete storage[temp_id];

      // Add time attribute
      storage[message_id].time = time;

      let path = storage[message_id].path;
      if (path && filename) {
        storage[message_id].path = _changeMediaPath(path, message_id, filename);
        console.log("changed:", storage[message_id].path)
      }

      return storage;
    });
  }

  async function deleteMsg(message_id) {
    let msg;
    update(storage => {
      msg = storage[message_id];
      delete storage[message_id];
      return storage;
    });
    return msg;
  }

  function _changeMediaPath(path, message_id, filename) {
    let parts = path.split("/");
    parts[parts.length-2] = message_id;
    parts[parts.length-1] = filename;
    return parts.join("/");
  }

  return { subscribe, updateMsg, changeId, deleteMsg };
})();


/*
 * Stores a collection of list of message_id and user_id for each room
 *
 * Structure:
 * {
 *   <room_id>: [{
 *     message_id: <message_id>;
 *     user_id: <user_id>;
 *   }, ...],
 *   ...
 * }
 * 
 * message_id are sorted in ascending order by time
 * (Earliest message at index 0, latest message at final index)
 */
export const allMsgs = (() => {
  const { subscribe, update } = writable({});

  async function addMsg(msgInfo, room_id, add_prev) {
    update(storage => {

      // Get room messages array
      let roomMsgs = storage[room_id];

      // If room messages does not exist, create array for it
      if (!roomMsgs) {
        roomMsgs = [];
        storage[room_id] = roomMsgs;
      }

      if (!add_prev) {  // Add new message to array
        roomMsgs.push(msgInfo);
      } else {  // Add older(previous) messages to front of array
        roomMsgs.unshift.apply(roomMsgs, msgInfo);
      }

      return storage;
    });
  }

  async function initRooms(rooms) {
    update(storage => {
      for (let i=0; i < rooms.length; i++) {
        storage[rooms[i]] = [];
      }
      return storage;
    });
  }

  async function changeId(temp_id, message_id, room_id) {
    update(storage => {

      // Get index of temp_id in storage
      const index = storage[room_id].findIndex(msgInfo => msgInfo.message_id === temp_id);

      // Replace temp_id with message_id
      if (index > -1) storage[room_id][index].message_id = message_id;

      return storage;
    });
  }

  async function deleteMsg(room_id, message_id) {
    let user_id, index;
    update(storage => {
      let roomMsgs = storage[room_id];
      if (roomMsgs) {
        // Get index of message_id in storage
        index = roomMsgs.findIndex(msgInfo => msgInfo.message_id === message_id);
        
        // Delete message if found
        if (index > -1); {
          ({user_id} = roomMsgs[index]);  // Get user_id of message
          roomMsgs.splice(index, 1);
        }
      }
      return storage;
    });
    return { index, user_id };
  }

  return { subscribe, addMsg, initRooms, changeId, deleteMsg };
})();
