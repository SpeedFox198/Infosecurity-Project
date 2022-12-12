import { redirect } from '@sveltejs/kit';

/** @type {import('./$types').PageServerLoad} */
export async function load({ locals, fetch }) {
    if (!(locals.user)) {
        throw redirect(302, "/")
    }
   
    try {
        const deviceRes = await fetch("https://127.0.0.1:8443/api/devices/", {
            credentials: "include"
        })
        const devicesData = await deviceRes.json()
        if (!deviceRes.ok) {
            return {
                errors: "Error while retrieving devices",
                devices: []
            }
        }
    
        return {
            errors: null,
            devices: devicesData.devices
        }
    } catch (error) {
        console.error(error)
    }    
};