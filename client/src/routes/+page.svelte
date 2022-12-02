<svelte:head>
  <title>{"Bubbles"}</title>
</svelte:head>



<style>
.background{
  background-color: var(--grey);
}

.login{
  background-color: var(--white);
}

.login-btn{
  background-color: var(--primary-dark)
}

.forgot-pw{
  color: var(--primary-light)
}

</style>
<main class="background">
  <div class="container-fluid">
    <div class="row">
      <!-- Bubbles Logo -->
      <div class="bubbles-name col-md-6">
        <img class="logo-with-text" src="/with-text.svg" alt="Bubbles">
      </div>

      <!-- Login -->
      <div class="login col-md-6 modal-content rounded-4 shadow">
        <div class="modal-header p-5 pb-4 border-bottom-0">
          <h1 class="fw-bold mb-0 fs-2">Log in and start chatting!</h1>
        </div>

        <div class="modal-body p-5 pt-0">
          <form class="">
            <div class="form-floating mb-3">
              <input type="email" class="form-control rounded-3" id="floatingInput" placeholder="name@example.com">
              <label for="floatingInput">Email address or username</label>
            </div>
            <div class="form-floating mb-3">
              <input type="password" class="form-control rounded-3" id="floatingPassword" placeholder="Password">
              <label for="floatingPassword">Password</label>
            </div>
            <button class="login-btn w-100 mb-2 btn btn-lg rounded-3 btn-primary" type="submit">Log in</button>
            <a class="forgot-pw" href="/">Forgotten password?</a>
            
            <hr class="my-4">
            <h2 class="fs-5 fw-bold mb-3">Don't have an account yet?</h2>
            <button class="w-100 py-2 mb-2 btn btn-outline-dark rounded-3" type="submit">
              Create new account
            </button>
            
          </form>
        </div>
      </div>
    </div>
  </div>
</main>