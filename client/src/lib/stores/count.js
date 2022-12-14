import { writable } from "svelte/store";


/*
 * Counts offset for requesting past undisplayed messages
 * Each room stores 2 counting variables:
 *   n:
 *     - Represents the "nth" 20-blocks of messages that has been received
 *     - E.g.: n=0 offset=0, n=1 offset=20, n=2 offset=40
 *   extra:
 *     - Represents the extra amount of offset needed due to sending/deleting messages
 * 
 * Example:
 * n=0, extra= 0, offset = 0
 * n=2, extra= 5, offset = 2*20 +5 = 45
 * n=3, extra=-2, offset = 3*20 -2 = 58
 * 
 * Structure:
 * {
 *   <room_id>: { n, extra },
 *   ...
 * }
 */
export const count = (() => {
  const { subscribe, update } = writable({});

  function _get(storage, key) {
    let result = storage[key];
    if (!result) {
      result = { n:0, extra:0 };
      storage[key] = result;
    }
    return result;
  }

  function nextN(room_id) {
    let n, extra;
  
    update(storage => {
      const room_count = _get(storage, room_id);
      n = room_count.n++;
      extra = room_count.extra;
      return storage;
    });

    return { n, extra };
  }

  function nextExtra(room_id) {
    let n, extra;
  
    update(storage => {
      const room_count = _get(storage, room_id);
      n = room_count.n;
      extra = room_count.extra++;
      return storage;
    });

    return { n, extra };
  }

  // TODO(SpeedFox198): rename them to proper names
  function decreaseExtra(room_id, amount) {
    let n, extra;
  
    update(storage => {
      const room_count = _get(storage, room_id);
      n = room_count.n;
      room_count.extra -= amount;
      return storage;
    });

    return { n, extra };
  }

  return { subscribe, nextN, nextExtra, decreaseExtra };
})();
