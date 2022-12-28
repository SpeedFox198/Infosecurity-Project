import { redirect } from '@sveltejs/kit';

export const actions = {
    forgotpassword: async ({request, cookies}) => {
        const data = await request.formData()
        const email = data.get("email")
        const response = await fetch("https://127.0.0.1:8443/api/auth/forgot-password", {   
            method: "POST",
            credentials: "include",
            headers: {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Cookie": request.headers.get("cookie")
            },
            body: JSON.stringify({"email": email})
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
