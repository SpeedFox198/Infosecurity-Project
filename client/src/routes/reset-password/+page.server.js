import { redirect } from '@sveltejs/kit';

export const actions = {
    default: async ({request, url}) => {
        const data = await request.formData()
        const changePassword = data.get("password")
        const changePasswordConfirm = data.get("confirm-password")
        const changePasswordToken = url.searchParams.get("token")

        const response = await fetch("https://127.0.0.1:8443/api/auth/reset-password", {   
            method: "POST",
            headers: {
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
              "token": changePasswordToken,
              "password": changePassword,
              "confirm_password": changePasswordConfirm
            })
        });  

        const result = await response.json();
        if (!response.ok) {
            return {
              error: result.message
            }
        }
      
        throw redirect(302, "/")
    }
}
