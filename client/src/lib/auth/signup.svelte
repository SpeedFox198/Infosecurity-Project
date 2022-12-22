<script>
    import { Turnstile } from "svelte-turnstile"

    export let toggleSignupOn
    export let errors

    let password
    let confirmPassword
    let requirementsDisplay
    let lowerCaseFulfill
    let upperCaseFulfill
    let numberFulfill
    let specialCharFulfill
    let lengthFulfill
    $: requirementsFulfill = lowerCaseFulfill && upperCaseFulfill && numberFulfill && lengthFulfill && specialCharFulfill


    const showRequirements = () => {
        requirementsDisplay = true
    }
  
    const hideRequirements = () => {
        requirementsDisplay = false
    }
    
    const checkPasswordRequirements = () => {
        const lowerCaseRegex = /[a-z]/g
        const upperCaseRegex = /[A-Z]/g
        const numberRegex = /[0-9]/g
        const specialCharRegex = /[`!@#$%^&*()_+\-=\[\]{};':"\|,.<>\/?~]/g
        
        lowerCaseFulfill = Boolean(password.match(lowerCaseRegex))
        upperCaseFulfill = Boolean(password.match(upperCaseRegex))
        numberFulfill = Boolean(password.match(numberRegex))
        specialCharFulfill = Boolean(password.match(specialCharRegex))
        lengthFulfill = password.length >= 8
    }
</script>


<div class="signup card rounded-4 shadow">
        <div class=" p-5 pb-4 border-bottom-0">
          <h1 class="card-title fw-bold mb-0 fs-2">Sign up and start chatting!</h1>
        </div>

        <div class="card-body p-5 pt-0">
          <form method="POST" action="?/signup">
            <!-- email address -->
            <div class="form-floating mb-3">
              <input name="email" type="email" class="form-control rounded-3" id="floatingInput" placeholder="name@example.com" required>
              <label for="floatingInput">Email address</label>
            </div>

            <!-- username -->
            <div class="form-floating mb-3">
              <input name="username"
               type="text"
               class="form-control rounded-3" 
               id="floatingInput" 
               placeholder="username" 
               required>
              <label for="floatingInput">Username</label>
            </div>

            <!-- password -->
            <div class="form-floating mb-3">
              <input name="password" type="password"
               class="form-control rounded-3"
               bind:value={password}
               on:focus={showRequirements}
               on:keyup={checkPasswordRequirements}
               on:blur={hideRequirements}
               title="Must contain at least one number, one uppercase and lowercase letter, one special character, and at least 8 or more characters" 
               placeholder="Password" 
               required>
              <label for="floatingPassword">Password</label>
            </div>
            
            <!-- password requirements -->
            {#if requirementsDisplay}
              <div id="message">
                <h4 class="{(requirementsFulfill) ? "d-none" : ''}">Password must contain the following:</h4>
                <p class="{lowerCaseFulfill === true ? "d-none" : ''}">A <b>lowercase</b> letter</p>
                <p class="{upperCaseFulfill === true ? "d-none" : ''}">A <b>capital (uppercase)</b> letter</p>
                <p class="{numberFulfill === true ? "d-none" : ''}">1 <b>number (0-9)</b></p>
                <p class="{specialCharFulfill === true ? "d-none" : ''}">1 <b> Special Character (`!@#$%^&*()_+-=[]|&#123;&#125;;':"\|,.&lt;&gt;\/?~)</b></p>
                <p class="{lengthFulfill === true ? "d-none" : ''}">At least <b>8 characters</b></p>
              </div>
            {/if}

            <!-- confirm password -->
            <div class="form-floating mb-3">
              <input name="confirmpassword" type="password"
              class="form-control rounded-3" 
              bind:value={confirmPassword}
              id="floatingPassword" 
              placeholder="Password" 
              required>
              <label for="floatingPassword">Confirm password</label>
            </div>
            <Turnstile siteKey="0x4AAAAAAABjATniBKt9vZiC"/>
            {#if errors}
              <p class="text-danger">{errors}</p>
            {/if}
            <button class="login-btn w-100 mb-2 btn btn-lg rounded-3 btn-primary" type="submit">Sign up</button>
            <small class="text-muted">By clicking Sign up, you agree to our <a href="https://discord.com/terms">terms of service</a>.</small>
              
            <hr class="my-4">
          </form>
          
            <h2 class="fs-5 fw-bold mb-3">Already have an account?</h2>
            <button class="w-100 py-2 mb-2 btn btn-outline-dark rounded-3" 
            type="button"
            on:click={toggleSignupOn}>
              Log in here
            </button>
        </div>
      </div>



<style>

.signup{
  background-color: var(--white);
  margin: 8rem
}

.login-btn{
  background-color: var(--primary-dark)
}

@media (max-width: 576px) {
  .signup {
    margin: 0rem
  }
}

</style>