import { writable, derived } from "svelte/store";


export const counterNotSent = (() => {
  const { subscribe, set, update } = writable(0);

  async function addCount(n) {
    update(storage => {
      storage += n;
      return storage;
    });
  }

  async function clear() {
    set(0);
  }

  return { subscribe, addCount, clear };
})();


export const selectedMsgs = (() => {
  const { subscribe, update } = writable(new Set());

  async function toggle(message_id, sent) {
    update(storage => {
      if (storage.has(message_id)) {
        storage.delete(message_id);
        counterNotSent.addCount(-!sent);
      } else {
        storage.add(message_id);
        counterNotSent.addCount(!sent);
      }
      return storage;
    });
  }

  async function remove(message_id, sent) {
    update(storage => {
      if (storage.has(message_id)) {
        storage.delete(message_id);
        counterNotSent.addCount(-!sent);
      }
      return storage;
    });
  }

  async function clear() {
    counterNotSent.clear();
    update(storage => {
      storage.clear();
      return storage;
    });
  }

  return { subscribe, toggle, remove, clear };
})();


export const selectMode = derived(
  selectedMsgs,
  $selectedMsgs => !!$selectedMsgs.size
);
