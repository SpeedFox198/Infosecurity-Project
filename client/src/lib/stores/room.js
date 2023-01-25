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
 *     disappearing: boolean;
 *     type: string;
 *     encrypted: boolean;
 *     is_admin: boolean;
 *     icon: string;
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

  return { subscribe, set, addRoom };
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
