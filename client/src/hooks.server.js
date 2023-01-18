/** @type {import('@sveltejs/kit').Handle} */
export const handle = async ({event, resolve}) => {
    // Get cookie
    const session = event.cookies.get("QUART_AUTH")
    
    if (!session) {
      return await resolve(event)
    }
    
    // Check if cookie is valid
    const response = await fetch("https://127.0.0.1:8443/api/auth/is-logged-in", {
        headers: {
            Cookie: `QUART_AUTH=${session}`,
        },
    })
    const userResponse = await response.json()

    if (userResponse.message === "Not authenticated") {
      event.cookies.delete("QUART_AUTH")
      return await resolve(event)
    }
 
    event.locals.user = userResponse    
    return await resolve(event)    
}

/** @type {import('@sveltejs/kit').HandleFetch} */
export async function handleFetch({ event, request, fetch }) {
    // for some reason fetches are not sent with cookies so this will handle it
    if (request.url.startsWith("https://127.0.0.1:8443/")) {
        request.headers.set('cookie', `QUART_AUTH=${event.cookies.get("QUART_AUTH")}`)
    }
    
    return fetch(request)
}