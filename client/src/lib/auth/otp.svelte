<div class="login card rounded-4 shadow">
    <div class=" p-5 pb-4 border-bottom-0">
      <h1 class="card-title fw-bold mb-0 fs-2">Submit your OTP from your registered email.</h1>
    </div>
  
    <div class="card-body p-5 pt-0">
      <form method="POST" action="?/otp">
        <div class="form-floating mb-3">
          <input
            type="text"
            name="otp"
            class="form-control rounded-3"
            id="floatingInput"
            placeholder="123456"
            required
          >
          <label for="floatingInput">OTP</label>
        </div>
        <button class="login-btn w-100 mb-2 btn btn-lg rounded-3 btn-primary" type="submit">
        Submit
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