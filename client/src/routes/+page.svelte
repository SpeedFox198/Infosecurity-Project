<svelte:head>
  <title>Bubbles | Login</title>
</svelte:head>

<script>
  import Login from "$lib/login.svelte"
  let email = ""
  let username = ""
  let password = ""
  let confirmPassword = ""
  let requirementsDisplay
  let lowerCaseFulfill
  let upperCaseFulfill
  let numberFulfill
  let lengthFulfill
  $: requirementsFulfill = lowerCaseFulfill && upperCaseFulfill && numberFulfill && lengthFulfill

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
    
    lowerCaseFulfill = Boolean(password.match(lowerCaseRegex))
    upperCaseFulfill = Boolean(password.match(upperCaseRegex))
    numberFulfill = Boolean(password.match(numberRegex))
    lengthFulfill = password.length >= 8
  }
</script>

<style>
.background{
  background-color: var(--grey);
}

.logo-with-text{
  padding: 8rem
}

.login{
  background-color: var(--white);
  margin: 8rem
}

.login-btn{
  background-color: var(--primary-dark)
}


</style>

<main class="background h-100">
  <div class="container-fluid">
    <div class="row">
      <!-- Bubbles Logo -->
      <div class="bubbles-name col-md-6">
        <img class="logo-with-text" src="/with-text.svg" alt="Bubbles">
      </div>

      <!-- Login -->
      <Login />
      
      <!-- Sign up -->
      <div class="login col-md-4 card rounded-4 shadow">
        <div class=" p-5 pb-4 border-bottom-0">
          <h1 class="card-title fw-bold mb-0 fs-2">Sign up and start chatting!</h1>
        </div>

        <div class="card-body p-5 pt-0">
          <form class="">
            <!-- email address -->
            <div class="form-floating mb-3">
              <input type="email" class="form-control rounded-3" id="floatingInput" placeholder="name@example.com" bind:value={email} required>
              <label for="floatingInput">Email address</label>
            </div>

            <!-- username -->
            <div class="form-floating mb-3">
              <input type="text" class="form-control rounded-3" id="floatingInput" placeholder="username" bind:value={username} required>
              <label for="floatingInput">Username</label>
            </div>

            <!-- password -->
            <div class="form-floating mb-3">
              <input type="password"
               class="form-control rounded-3"
               bind:value={password}
               on:click={showRequirements}
               on:keyup={checkPasswordRequirements}
               on:blur={hideRequirements}
               title="Must contain at least one number and one uppercase and lowercase letter, and at least 8 or more characters" 
               placeholder="Password" 
               required>
              <label for="floatingPassword">Password</label>
            </div>
            <!-- confirm password -->
            <div class="form-floating mb-3">
              <input type="password"
              class="form-control rounded-3" 
              bind:value={confirmPassword}
              id="floatingPassword" 
              placeholder="Password" 
              required>
              <label for="floatingPassword">Confirm password</label>
            </div>

            <!-- password requirements -->
            {#if requirementsDisplay}
              <div id="message">
                <h3 class="{(requirementsFulfill) ? "d-none" : ''}">Password must contain the following:</h3>
                <p class="{lowerCaseFulfill === true ? "d-none" : ''}">A <b>lowercase</b> letter</p>
                <p class="{upperCaseFulfill === true ? "d-none" : ''}">A <b>capital (uppercase)</b> letter</p>
                <p class="{numberFulfill === true ? "d-none" : ''}">A <b>number</b></p>
                <p class="{lengthFulfill === true ? "d-none" : ''}">Minimum <b>8 characters</b></p>
              </div>
            {/if}
            

            <button class="login-btn w-100 mb-2 btn btn-lg rounded-3 btn-primary" type="submit">Sign up</button>
            <small class="text-muted">By clicking Sign up, you agree to the terms of use.</small>
            
            <hr class="my-4">
            <h2 class="fs-5 fw-bold mb-3">Already have an account?</h2>
            <button class="w-100 py-2 mb-2 btn btn-outline-dark rounded-3" type="submit">
              Log in here
            </button>
          </form>
        </div>
      </div>
    </div>
  </div>
</main>