import { redirect } from '@sveltejs/kit';
import tough from "tough-cookie"


const Cookie = tough.Cookie

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
    
    const { cfSuccess } = await validateCfToken(cfToken, "0x4AAAAAAABjATgnTcCbttib5rnrNUIazOg")

    if (!cfSuccess) {
      return {
        cfError: "Invalid CAPTCHA"
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
    
    const quartCookie = Cookie.parse(response.headers.get("set-cookie"))
    cookies.set(quartCookie.key, quartCookie.value, {
      path: quartCookie.path,
      httpOnly: quartCookie.httpOnly,
      sameSite: quartCookie.sameSite,
      maxAge: quartCookie.maxAge,
    })

    throw redirect(302, "/chat")
  },
  signup: async ({request, cookies}) => {
    const data = await request.formData()
    const username = data.get("username")
    const email = data.get("email")
    const password = data.get("password")
    const confirmPassword = data.get("confirmpassword")
    const cfToken = data.get("cf-turnstile-response")
    
    const { cfSuccess } = await validateCfToken(cfToken, "0x4AAAAAAABjATgnTcCbttib5rnrNUIazOg")
  
    if (!cfSuccess) {
      return {
        cfError: "Invalid CAPTCHA"
      }
    }

    if (password !== confirmPassword) {
      return {
        signupError: "Passwords do not match"
      }
    }

    const response = await fetch("https://127.0.0.1:8443/api/auth/sign-up", {
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

    const otpCookie = Cookie.parse(response.headers.get("set-cookie"))
    cookies.set(otpCookie.key, otpCookie.value, {
      path: otpCookie.path,
      httpOnly: otpCookie.httpOnly,
      sameSite: otpCookie.sameSite,
      maxAge: otpCookie.maxAge,
    })

    throw redirect(302, "/otp")
  }
}

async function validateCfToken(token, secret) {
  const response = await fetch("https://challenges.cloudflare.com/turnstile/v0/siteverify", {
    method: "POST",
    headers: {
      "content-type": "application/json",
    },
    body: JSON.stringify({
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