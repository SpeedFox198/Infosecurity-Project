<div class="login col-md-4 card rounded-4 shadow">
  <div class=" p-5 pb-4 border-bottom-0">
    <h1 class="card-title fw-bold mb-0 fs-2">Log in and start chatting!</h1>
  </div>

  <div class="card-body p-5 pt-0">
    <form class="">
      <div class="form-floating mb-3">
        <input
          type="text"
          class="form-control rounded-3"
          id="floatingInput"
          placeholder="name@example.com"
          required
        />
        <label for="floatingInput">Email address or username</label>
      </div>
      <div class="form-floating mb-3">
        <input
          type="password"
          class="form-control rounded-3"
          id="floatingPassword"
          placeholder="Password"
          required
        />
        <label for="floatingPassword">Password</label>
      </div>
      <button class="login-btn w-100 mb-2 btn btn-lg rounded-3 btn-primary" type="submit"
        >Log in</button
      >
      <a class="forgot-pw card-link text-center" href="/">Forgotten password?</a>

      <hr class="my-4" />
      <h2 class="fs-5 fw-bold mb-3">Don't have an account yet?</h2>
      <button class="w-100 py-2 mb-2 btn btn-outline-dark rounded-3" type="submit">
        Create new account
      </button>
    </form>
  </div>
</div>

<style>
  .forgot-pw{
    color: var(--primary-light)
  }

  .login{
    background-color: var(--white);
    margin: auto
  }
  
  .login-btn{
    background-color: var(--primary-dark)
  }
</style>
