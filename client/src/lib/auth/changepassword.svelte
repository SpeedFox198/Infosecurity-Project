<script>
  export let errors
  
  let password = ""
  let confirmPassword = ""

  let requirementsDisplay = false
  let passwordMatchDisplay = false

  let lowerCaseFulfill, upperCaseFulfill, numberFulfill, specialCharFulfill, lengthFulfill
  $: requirementsFulfill = lowerCaseFulfill && upperCaseFulfill && numberFulfill && lengthFulfill && specialCharFulfill
  $: passwordsMatch = password === confirmPassword


  const toggleRequirements = () => {
    requirementsDisplay = !requirementsDisplay
  }
  
  const togglePasswordMatch = () => {
    passwordMatchDisplay = !passwordMatchDisplay
  }

  const checkPasswordRequirements = () => {
    const lowerCaseRegex = /[a-z]/g
    const upperCaseRegex = /[A-Z]/g
    const numberRegex = /[0-9]/g
    //const specialCharRegex = /[`!@#$%^&*()_+\-=\[\]{};':"\|,.<>\/?~]/g
    const specialCharRegex = /[\W_]/g
    
    lowerCaseFulfill = Boolean(password.match(lowerCaseRegex))
    upperCaseFulfill = Boolean(password.match(upperCaseRegex))
    numberFulfill = Boolean(password.match(numberRegex))
    specialCharFulfill = Boolean(password.match(specialCharRegex))
    lengthFulfill = password.length >= 8
  }
</script>

<div class="login card rounded-4 shadow">
    <div class=" p-5 pb-4 border-bottom-0">
      <h1 class="card-title fw-bold mb-0 fs-2">Enter your new password</h1>
    </div>
  
    <div class="card-body p-5 pt-0">
      <form method="POST">
        <!-- password -->
        <div class="form-floating mb-3">
          <input name="password" type="password"
            class="form-control rounded-3"
            on:focus={toggleRequirements}
            on:keyup={checkPasswordRequirements}
            on:blur={toggleRequirements}
            title="Must contain at least one number, one uppercase and lowercase letter, one special character, and at least 8 or more characters" 
            placeholder="Password" 
            required>
          <label for="floatingPassword">Password</label>
        </div>
        
        <!-- password requirements -->
        {#if requirementsDisplay}
          <div id="message">
            <h4 class="{(requirementsFulfill) ? "d-none" : ''}">Password must contain the following:</h4>
            <p class="{lowerCaseFulfill ? "d-none" : ''}">A <b>lowercase</b> letter</p>
            <p class="{upperCaseFulfill ? "d-none" : ''}">A <b>capital (uppercase)</b> letter</p>
            <p class="{numberFulfill ? "d-none" : ''}">1 <b>number (0-9)</b></p>
            <p class="{specialCharFulfill ? "d-none" : ''}">1 <b> Special Character (`!@#$%^&*()_+-=[]|&#123;&#125;;':"\|,.&lt;&gt;\/?~)</b></p>
            <p class="{lengthFulfill ? "d-none" : ''}">At least <b>8 characters</b></p>
          </div>
        {/if}

        <!-- confirm password -->
        <div class="form-floating mb-3 ">
          <input name="confirm-password" type="password"
          class="form-control rounded-3 {(!passwordsMatch) && passwordMatchDisplay ? "is-invalid" : ''}" 
          on:focus={togglePasswordMatch}
          on:blur={togglePasswordMatch}
          id="floatingPassword" 
          placeholder="Password" 
          required>
          <label for="floatingPassword">Confirm password</label>
        </div>

        {#if (!passwordsMatch) && passwordMatchDisplay}
          <p class="text-danger">Password and Confirm Password must be the same.</p>
        {/if}

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