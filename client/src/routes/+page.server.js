import { redirect } from '@sveltejs/kit';

/** @type {import('./$types').PageServerLoad} */
export async function load({locals}) {
    if (locals.user) {
        throw redirect(302, "/chat")
    }
};

/** @type {import('./$types').Actions} */
export const actions = {
  login: async ({cookies, request}) => {
    const data = await request.formData()
    const username = data.get("username")
    const password = data.get("password")
    const cfToken = data.get("cf-turnstile-response")
    
    const { cfSuccess, cfError } = await validateCfToken(cfToken, "0x4AAAAAAABjATgnTcCbttib5rnrNUIazOg")

    if (!cfSuccess) {
      return {
        cfError: cfError || "Invalid CAPTCHA"
      }
    }
    
    const response = await fetch("https://127.0.0.1:8443/api/auth/login", {
        method: "POST",
        credentials: "include",
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": request.headers.get("User-Agent")
        },
        body: JSON.stringify({"username": username, "password": password})
    });
    const result = await response.json();
    
    if (!response.ok) {
      return {
        loginError: result.message
      }
    }
    
    const cookie = response.headers.get("set-cookie").split("=")[1]
    cookies.set("QUART_AUTH", cookie)
    throw redirect(302, "/chat")
  },
  signup: async ({request}) => {
    const data = await request.formData()
    const username = data.get("username")
    const email = data.get("email")
    const password = data.get("password")
    const confirmPassword = data.get("confirmPassword")
    const cfToken = data.get("cf-turnstile-response")
    
    const { cfSuccess, cfError } = await validateCfToken(cfToken, "0x4AAAAAAABjATgnTcCbttib5rnrNUIazOg")
  
    if (!cfSuccess) {
      return {
        cfError: cfError || "Invalid CAPTCHA"
      }
    }

    if (password !== confirmPassword) {
      return {
        signupError: "Passwords do not match"
      }
    }

    const response = await fetch("https://127.0.0.1:8443/api/auth/signup", {
      method: "POST",
      credentials: "include",
      headers: {
          "Accept": "application/json",
          "Content-Type": "application/json",
      },
      body: JSON.stringify({"username": username, "password": password, "email": email})
    });
    const result = await response.json();
    if (!response.ok) {
      return {
        signupError: result.message
      }
    }
    throw redirect(302, "/OTP")
  }
}

async function validateCfToken(token, secret) {
  const response = await fetch("https://challenges.cloudflare.com/turnstile/v0/siteverify", {
    method: "POST",
    headers: {
      "content-type": "application/x-www-form-urlencoded",
    },
    body: new URLSearchParams({
      response: token,
      secret: secret
    })
  })

  const data = await response.json()
  
  return {
    cfSuccess: data.success,
    // Return the first error if it exists
    cfError: data['error-codes']?.length ? data['error-codes'][0] : null,
  }
}