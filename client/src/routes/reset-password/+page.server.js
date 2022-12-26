import { redirect } from '@sveltejs/kit';

export const actions = {
    changepassword: async ({request, cookies}) => {
        const data = await request.formData()
        const changepassword = data.get("password")
        const changepasswordconfirm = data.get("password_confirm")
        const response = await fetch("https://127.0.0.1:8443/api/auth/reset-password?token=<token>", {   
            method: "POST",
            credentials: "include",
            headers: {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Cookie": request.headers.get("cookie")
            },
            body: JSON.stringify({"password": changepassword, "password_confirm": changepasswordconfirm})
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
