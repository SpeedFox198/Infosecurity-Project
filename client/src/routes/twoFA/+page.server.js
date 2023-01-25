//import { redirect } from '@sveltejs/kit'
import { redirect } from "sveltekit-flash-message/server"


import tough from "tough-cookie"


const Cookie = tough.Cookie

export async function load({ cookies }) {
  if (!cookies.get("session")) {
    throw redirect(302, "/")
  }
}

export const actions = {
  twoFA: async (event) => {
        const data = await event.request.formData()
        const twoFA = data.get("twoFA")
        console.log(twoFA)
        const response = await fetch("https://127.0.0.1:8443/api/auth/2fa", {   
            method: "POST",
            credentials: "include",
            headers: {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Cookie": event.request.headers.get("cookie")
            },
            body: JSON.stringify({"twofacode": twoFA})
        });  
        const result = await response.json();
        if (!response.ok) {
            return {
              TwoFAError: result.message
            }
        }
      
        const quartCookie = Cookie.parse(response.headers.get("set-cookie"))
        event.cookies.set(quartCookie.key, quartCookie.value, {
          path: quartCookie.path,
          httpOnly: quartCookie.httpOnly,
          sameSite: quartCookie.sameSite,
          maxAge: 60 * 24 * 60 * 60, // formatted as (days * hours * minutes * seconds)
        })

        //throw redirect(302, "/")
        throw redirect(
          302,
          "/chat",
          { type: "success", message: "Login Successful!" },
          event
        )
    }
}
