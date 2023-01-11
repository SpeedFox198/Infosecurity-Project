//import { redirect } from '@sveltejs/kit'
import { redirect } from "sveltekit-flash-message/server"

export async function load({ cookies }) {
  if (!cookies.get("session")) {
    throw redirect(302, "/")
  }
}

export const actions = {
    otp: async (event) => {
        const data = await event.request.formData()
        const otp = data.get("otp")
        const response = await fetch("https://127.0.0.1:8443/api/auth/otp", {   
            method: "POST",
            credentials: "include",
            headers: {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Cookie": event.request.headers.get("cookie")
            },
            body: JSON.stringify({"otp": otp})
        });  
        const result = await response.json();
        if (!response.ok) {
            return {
              otpError: result.message
            }
        }
      
        event.cookies.delete("session")
        //throw redirect(302, "/")
        throw redirect(
          302,
          "/",
          { type: "success", message: "Sign up completed!" },
          event
        )
    }
}
