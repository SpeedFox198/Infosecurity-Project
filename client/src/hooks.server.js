
export const handle = async ({event, resolve}) => {
    // Get cookie
    const session = event.cookies.get("QUART_AUTH")
    console.log(session)
    
    if (!session) {
        return await resolve(event)
    }
    
    // Check if cookie is valid
    const response = await fetch("https://127.0.0.1:8443/api/auth/is-logged-in", {
        headers: {
            Cookie: `QUART_AUTH=${session}`
        }
    })
    const userResponse = await response.json()

    if (userResponse.message === "not authenticated") {
     return await resolve(event)
    }
    
    event.locals.user = userResponse    
    return await resolve(event)
}
