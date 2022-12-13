import { writable } from "svelte/store";


// TODO(SpeedFox198): add documentations and comments
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
  function minusExtra(room_id) {
    let n, extra;
  
    update(storage => {
      const room_count = _get(storage, room_id);
      n = room_count.n;
      // When room messages are not loaded yet, do not modify extra value
      extra = n ? room_count.extra-- : 0;
      return storage;
    });

    return { n, extra };
  }

  return { subscribe, nextN, nextExtra };
})();
