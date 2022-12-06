import { writable } from "svelte/store";

export const room_id = (() => {
  // TODO(SpeedFox198): remove this temp value
  const { subscribe, set } = writable("");
  return { subscribe, set };
})();

export const allRooms = (() => {
  const { subscribe, set, update } = writable([]);

    async function addRoom(room) {
      update(storage => {
        storage.push(room);
        return storage;
    });
  }

return { subscribe, set, addRoom };
})();
