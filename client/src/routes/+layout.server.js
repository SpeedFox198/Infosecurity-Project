import { loadFlashMessage } from "sveltekit-flash-message/server"

export const load = loadFlashMessage(async ({ locals }) => {
    return {
      user: await locals.user
    }
})