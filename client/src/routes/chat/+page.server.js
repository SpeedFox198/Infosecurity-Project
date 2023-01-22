import { redirect } from '@sveltejs/kit';

/** @type {import('./$types').PageServerLoad} */
export async function load({locals, fetch, depends}) {
    if (!(locals.user)) {
      throw redirect(302, "/")
    }
  
    const getDevices = async () => {
      depends("app:devices")
      const deviceRes = await fetch("https://127.0.0.1:8443/api/devices/")
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
  
    const getFriends = async () => {
      const response = await fetch("https://127.0.0.1:8443/api/friends/")
      const data = await response.json()
      if (!response.ok) {
        return {
          errors: "Error while retrieving devices",
          friendsList: []
        }
      }

      return {
        errors: null,
        friendsList: data.friends
      }
    }
    
    const getFriendRequests = async () => {
      const response = await fetch("https://127.0.0.1:8443/api/friends/requests")
      const data = await response.json()
      if (!response.ok) {
        return {
          errors: "Error while retrieving friend requests",
          friendRequestsList: []
        }
      }
      
      return {
        errors: null,
        friendRequestsList: data
      }

    }
  
    return {
      devices: getDevices(),
      friends: getFriends(),
      friendRequests: getFriendRequests()
    }
};