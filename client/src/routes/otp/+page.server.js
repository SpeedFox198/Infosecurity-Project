import { redirect } from '@sveltejs/kit';

export const actions = {
    otp: async ({request}) => {
        const data = await request.formData()
        const otp = data.get("otp")
        const response = await fetch("https://127.0.0.1:8443/api/auth/otp", {   
            method: "POST",
            credentials: "include",
            headers: {
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
            body: JSON.stringify({"otp": otp})
        });  
        const result = await response.json();
        if (!response.ok) {
            return {
              otpError: result.message
            }
        }
        throw redirect(302, "/")
    }
}
