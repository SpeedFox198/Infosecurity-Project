import { redirect } from '@sveltejs/kit';

/** @type {import('./$types').PageServerLoad} */
export async function load({locals}) {
    if (!(locals.user && locals.user.verified)) {
        throw redirect(302, "/")
    }
};