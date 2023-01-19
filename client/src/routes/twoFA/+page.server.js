//import { redirect } from '@sveltejs/kit'
import { redirect } from "sveltekit-flash-message/server"

export async function load({ cookies }) {
  if (!cookies.get("session")) {
    throw redirect(302, "/")
  }
}

export const actions = {
  twofA: async (event) => {
        const data = await event.request.formData()
        const twofA = data.get("twofA")
        const response = await fetch("https://127.0.0.1:8443/api/auth/2fa", {   
            method: "POST",
            credentials: "include",
            headers: {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Cookie": event.request.headers.get("cookie")
            },
            body: JSON.stringify({"twofacode": twofA})
        });  
        const result = await response.json();
        if (!response.ok) {
            return {
              TwoFAError: result.message
            }
        }
      
        event.cookies.delete("session")
        //throw redirect(302, "/")
        throw redirect(
          302,
          "/",
          { type: "success", message: "2FA sign in completed!" },
          event
        )
    }
}
