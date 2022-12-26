<script>
  export let errors;
</script>

<div class="login card rounded-4 shadow">
    <div class=" p-5 pb-4 border-bottom-0">
      <h1 class="card-title fw-bold mb-0 fs-2">Enter your new password</h1>
    </div>
  
    <div class="card-body p-5 pt-0">
      <form method="POST" action="?/changepassword">
        <div class="form-floating mb-3">
          <input
            type="password"
            name="password"
            class="form-control rounded-3"
            id="floatingInput"
            placeholder="Password"
            required
          >
          <label for="floatingInput">New Password</label>
        </div>
        <div class="form-floating mb-3">
          <input
            type="password"
            name="change_password"
            class="form-control rounded-3"
            id="floatingPassword"
            placeholder="Confirm Password"
            required
          >
          <label for="floatingPassword">Confirm Password</label>
        </div>
        {#if errors}
          <p class="text-danger">{errors}</p>
        {/if}
        <button class="login-btn w-100 mb-2 btn btn-lg rounded-3 btn-primary" type="submit">
            Change Password
        </button>
        <hr class="my-4" />
      </form>
    </div>
  </div>
  
  <style>
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