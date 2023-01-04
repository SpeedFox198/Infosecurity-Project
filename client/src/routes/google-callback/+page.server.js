import { redirect } from '@sveltejs/kit'
import tough from "tough-cookie"

const Cookie = tough.Cookie

/** @type {import('./$types').PageServerLoad} */
export async function load({ url, cookies, request }) {
  const response = await fetch("https://127.0.0.1:8443/api/auth/google-callback", {
    method: "POST",
    headers: {
      "Accept": "application/json",
      "Content-Type": "application/json",
      "Cookie": request.headers.get("cookie"),
      "User-Agent": request.headers.get("User-Agent")
    },
    credentials: "include",
    body: JSON.stringify({"parameters": url.search}),
  })
  
  if (!response.ok) {
    throw redirect(302, "/")
  }
  
  const quartCookie = Cookie.parse(response.headers.get("set-cookie"))
  cookies.set(quartCookie.key, quartCookie.value, {
    path: quartCookie.path,
    httpOnly: quartCookie.httpOnly,
    sameSite: quartCookie.sameSite,
    maxAge: 60 * 24 * 60 * 60, // formatted as (days * hours * minutes * seconds)
  })

  throw redirect(302, "/chat")
};