import { writable } from "svelte/store"

/** @type {import('svelte/store').Writable<Map<string, number>} */
export const ocrStatus = writable(new Map())