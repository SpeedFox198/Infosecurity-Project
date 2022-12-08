<script>
  export let toggleSignupOn
  let loginError
  let username = ""
  let password = ""

  const loginSubmit = async () => {
    const response = await fetch("https://localhost:8443/api/auth/login", {
        method: "POST",
        credentials: "include",
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        body: JSON.stringify({"username": username, "password": password})
    })
    const result = await response.json()

    if (!response.ok) {
      loginError = result.message
      return
    }

    location.replace("/chat")
  }
  
</script>

<svelte:head>
    <script src="https://www.google.com/recaptcha/enterprise.js?render=6LcEnmMjAAAAAACQJ-aJ3Y9XQyMj7vlf23LpN5Kf"></script>
</svelte:head>

<div class="login card rounded-4 shadow">
  <div class=" p-5 pb-4 border-bottom-0">
    <h1 class="card-title fw-bold mb-0 fs-2">Log in and start chatting!</h1>
  </div>

  <div class="card-body p-5 pt-0">
    <form action="" on:submit|preventDefault={loginSubmit}>
      <div class="form-floating mb-3">
        <input
          type="text"
          class="form-control rounded-3"
          id="floatingInput"
          placeholder="name@example.com"
          bind:value={username}
          required
        >
        <label for="floatingInput">Email address or username</label>
      </div>
      <div class="form-floating mb-3">
        <input
          type="password"
          class="form-control rounded-3"
          id="floatingPassword"
          placeholder="Password"
          bind:value={password}
          required
        >
        <label for="floatingPassword">Password</label>
      </div>
      <button class="login-btn w-100 mb-2 btn btn-lg rounded-3 btn-primary" type="submit">
      Log in
      </button>
      {#if loginError}
        <p class="text-danger">Invalid credentials!</p>
      {/if}
      <a class="forgot-pw card-link text-center" href="/">Forgotten password?</a>

      <hr class="my-4" />
    </form>

    <h2 class="fs-5 fw-bold mb-3">Don't have an account yet?</h2>
      <button class="w-100 py-2 mb-2 btn btn-outline-dark rounded-3"
      type="button"
      on:click={toggleSignupOn}>
        Create new account
      </button>
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
