import { writable } from "svelte/store"

/** @type {import('svelte/store').Writable<number>} */
export const ocrStatus = writable(0)