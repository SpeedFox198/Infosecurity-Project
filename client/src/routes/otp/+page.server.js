import { redirect } from '@sveltejs/kit'

export async function load({ cookies }) {
  if (!cookies.get("session")) {
    throw redirect(302, "/")
  }
}

export const actions = {
    otp: async ({request, cookies}) => {
        const data = await request.formData()
        const otp = data.get("otp")
        const response = await fetch("https://127.0.0.1:8443/api/auth/otp", {   
            method: "POST",
            credentials: "include",
            headers: {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Cookie": request.headers.get("cookie")
            },
            body: JSON.stringify({"otp": otp})
        });  
        const result = await response.json();
        if (!response.ok) {
            return {
              otpError: result.message
            }
        }
      
        cookies.delete("session")
        throw redirect(302, "/")
    }
}
