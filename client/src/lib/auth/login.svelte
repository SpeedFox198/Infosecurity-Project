<script>
  import { Turnstile } from "svelte-turnstile"

  import { browser } from "$app/environment"
  export let toggleSignupOn
  export let errors

  async function handleCredentialResponse(response) {
    console.log("Encoded JWT ID token: " + response.credential);
    await fetch("https://127.0.0.1:8443/api/auth/login-callback", {
    method: "POST",
    credentials: "include",
    headers: {
      "Accept": "application/json",
      "Content-Type": "application/json"
    },
    body: JSON.stringify({"token": response.credential})
  });

  }

  if (browser) {
    window.onload = function () {
      google.accounts.id.initialize({
        client_id: "758319541478-uflvh47eoagk6hl73ss1m2hnj35vk9bq.apps.googleusercontent.com",
        callback: handleCredentialResponse
      });
      google.accounts.id.renderButton(
        document.getElementById("buttonDiv"),
        { theme: "outline", size: "large" }  // customization attributes
      );
      google.accounts.id.prompt(); // also display the One Tap dialog
    }
  }

</script>

<svelte:head>
  <meta name="google-signin-client_id" content="758319541478-uflvh47eoagk6hl73ss1m2hnj35vk9bq.apps.googleusercontent.com">
  <script src="https://accounts.google.com/gsi/client" async defer></script>
</svelte:head>

<div class="login card rounded-4 shadow">
  <div class=" p-5 pb-4 border-bottom-0">
    <h1 class="card-title fw-bold mb-0 fs-2">Log in and start chatting!</h1>
  </div>

  <div class="card-body p-5 pt-0">
    <form method="POST" action="?/login">
      <div class="form-floating mb-3">
        <input
          type="text"
          name="username"
          class="form-control rounded-3"
          id="floatingInput"
          placeholder="name@example.com"
          required
        >
        <label for="floatingInput">Email address or username</label>
      </div>
      <div class="form-floating mb-3">
        <input
          type="password"
          name="password"
          class="form-control rounded-3"
          id="floatingPassword"
          placeholder="Password"
          required
        >
        <label for="floatingPassword">Password</label>
      </div>
      <Turnstile siteKey="0x4AAAAAAABjATniBKt9vZiC"/>
      {#if errors}
        <p class="text-danger">{errors}</p>
      {/if}
      <button class="login-btn w-100 mb-2 btn btn-lg rounded-3 btn-primary" type="submit">
      Log in
      </button>
      <a class="forgot-pw card-link text-center" href="/">Forgotten password?</a>

      <hr class="my-4" />
    </form>

    <h2 class="fs-5 fw-bold mb-3">Don't have an account yet?</h2>
      <button class="w-100 py-2 mb-2 btn btn-outline-dark rounded-3"
      type="button"
      on:click={toggleSignupOn}>
        Create new account
      </button>
    <h2 class="fs-5 fw-bold mb-3">Or you can login with these</h2>
    <div id="buttonDiv"></div> 
    <div id="g_id_onload"
    data-client_id="758319541478-uflvh47eoagk6hl73ss1m2hnj35vk9bq.apps.googleusercontent.com"
    data-login_uri="https://localhost/"
    data-auto_prompt="false">
    </div>
    <div class="g_id_signin"
        data-type="standard"
        data-size="large"
        data-theme="outline"
        data-text="sign_in_with"
        data-shape="rectangular"
        data-logo_alignment="left">
    </div>
  </div>
</div>

<style>
  .forgot-pw{
    color: var(--primary-light)
  }

  .login{
    background-color: var(--white);
    margin: 8rem
  }
  
  .login-btn{
    background-color: var(--primary-dark)
  }
  
  @media(max-width: 576px) {
    .login {
      margin: 0rem
    }
  }
</style>