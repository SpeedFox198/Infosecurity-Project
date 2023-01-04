<script>
  import Login from "$lib/auth/login.svelte"
  import Signup from "$lib/auth/signup.svelte"
  export let form
  export let data

  let signupDisplay = false
  let errors
  
  const toggleSignupOn = () => {
    signupDisplay = !signupDisplay
  }

  if (form?.loginError) {
    errors = form.loginError
  }
  
  if (form?.signupError) {
    errors = form.signupError
    toggleSignupOn()
  }
  
  if (form?.loginCfError) {
    errors = form.loginCfError
  }
  
  if (form?.signupCfError) {
    errors = form.signupCfError
    toggleSignupOn()
  }
  
</script>


<svelte:head>
  <title>Bubbles | Home</title>
</svelte:head>

<main class="background h-100">
  <div class="container-fluid">
    <div class="row">
      <!-- Bubbles Logo -->
      <div class="bubbles-name col-md-6">
        <img class="logo-with-text" src="/with-text.svg" alt="Bubbles">
      </div>
      <div class="col-md-6">
        {#if (signupDisplay)}
        <!-- Sign up -->
        <Signup toggleSignupOn={toggleSignupOn} errors={errors}/>
        {:else}
        <!-- Login -->
        <Login toggleSignupOn={toggleSignupOn} errors={errors} googleLogin={data.googleLogin}/>
        {/if}
      </div>
    </div>
  </div>
</main>

<style>
.background{
  background-color: var(--grey);
}

.logo-with-text{
  padding: 8rem
}

</style>