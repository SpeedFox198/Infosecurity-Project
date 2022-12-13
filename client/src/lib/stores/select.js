import { writable, derived } from "svelte/store";


export const selectedMsgs = (() => {
  const { subscribe, update } = writable(new Set());

  function toggle(message_id) {
    update(storage => {
      if (storage.has(message_id)) {
        storage.delete(message_id);
      } else {
        storage.add(message_id);
      }
      return storage;
    });
  }

  function clear(message_id) {
    update(storage => {
      storage.clear(message_id);
      return storage;
    });
  }

  return { subscribe, toggle, clear };
})();


export const selectMode = derived(
  selectedMsgs,
  $selectedMsgs => !!$selectedMsgs.size
);
