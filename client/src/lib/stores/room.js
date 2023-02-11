import { writable } from "svelte/store";


export const room_id = (() => {
  const { subscribe, set } = writable("");
  return { subscribe, set };
})();


/*
 * Stores a collection of room objects identified by their room_id
 * 
 * Structure:
 * {
 *   <room_id>: {
 *     room_id: string;
 *     disappearing: string;
 *     type: string;
 *     encrypted: boolean;
 *     is_admin: boolean;
 *     icon: string;
 *     name: string;
 *     user_id?: string;
 *     online?: boolean;
 *     blocked?: string;
 *     "blocked" if current user is blocked by other user or "blocking" if current user is blocking other user
 *   },
 *   ...
 * }
 */
export const roomStorage = (() => {
  const { subscribe, set, update } = writable({});

  async function addRoom(room_id, room) {
    update(storage => {
      storage[room_id] = room;
      return storage;
    });
  }

  /**
   * Update online status of user
   * @param {string} user_id user id of user that went offline
   * @param {boolean} status True if user is online
   */
  async function updateOnlineStatus(user_id, status) {
    update(storage => {
      Object.keys(storage).forEach(room_id => {
        if (storage[room_id].user_id === user_id) {
          storage[room_id].online = status;
        }
      });
      return storage;
    });
  }

  return { subscribe, set, addRoom, updateOnlineStatus };
})();


/*
 * Stores a list of room_id
 * 
 * Structure:
 * [<room_id>, ...]
 * 
 * room_id are sorted by most recently active time
 * (Most recently active at index 0, least recently active at final index)
 */
export const roomList = (() => {
  const { subscribe, set, update } = writable([]);

  async function addRoom(room_id) {
    update(storage => {
      storage.push(room_id);
      return storage;
    });
  }

  return { subscribe, set, addRoom };
})();
