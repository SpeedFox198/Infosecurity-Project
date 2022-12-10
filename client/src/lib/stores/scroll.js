import { writable } from "svelte/store";


export const lockScroll = (() => {
  const { subscribe, set } = writable(true);

  return {
    subscribe,
    lock: () => set(true),
    unlock: () => set(false)
  };
})();
