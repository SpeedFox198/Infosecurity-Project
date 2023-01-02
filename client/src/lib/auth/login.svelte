<script>
  import { Turnstile } from "svelte-turnstile"
  export let toggleSignupOn
  export let errors
  export let googleLogin
</script>

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
      <a class="forgot-pw card-link text-center" href="/forgot-password">Forgotten password?</a>

      <hr class="my-4" />
    </form>

    <h2 class="fs-5 fw-bold mb-3">Don't have an account yet?</h2>
      <button class="w-100 py-2 mb-2 btn btn-outline-dark rounded-3"
      type="button"
      on:click={toggleSignupOn}>
        Create new account
      </button>
    <h2 class="fs-5 fw-bold mb-3">Or you can login with these</h2>
    <a href={googleLogin.url} class="btn btn-primary" role="button">
      Sign in with Google
    </a>
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