import { redirect } from '@sveltejs/kit';

/** @type {import('./$types').PageServerLoad} */
export async function load({locals, fetch, depends}) {
    if (!(locals.user)) {
        throw redirect(302, "/")
    }
  
    const getDevices = async () => {
      depends("app:devices")
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
    }
  
    return {
      devices: getDevices(),
    }
};