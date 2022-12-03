import { browser } from "$app/environment";
import { onDestroy } from "svelte/internal";
import { writable } from "svelte/store";


export function messages() {
  const allMsgs = writable(Array());
  const { subscribe, set, update } = allMsgs;
  
  if (browser && localStorage.messages) {
    set(JSON.parse(localStorage.getItem("messages")));
  }
  const unsubscribe = subscribe(async messages => {
    if (browser) localStorage.messages = JSON.stringify(messages);
  });

  onDestroy(unsubscribe);

  return {
    subscribe,
    addMsg: async msg => update(val => val.concat(msg))
  }
}
