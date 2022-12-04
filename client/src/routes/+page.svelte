<script>
  import Login from "$lib/login.svelte"
  import Signup from "$lib/login.svelte"
  let signupDisplay = false

  const toggleSignupOn = () => {
    signupDisplay = !signupDisplay
  }

</script>


<svelte:head>
  <title>Bubbles | Login</title>
</svelte:head>
<main class="background h-100">
  <div class="container-fluid">
    <div class="row">
      <!-- Bubbles Logo -->
      <div class="bubbles-name col-md-6">
        <img class="logo-with-text" src="/with-text.svg" alt="Bubbles">
      </div>

      <!-- Login -->
      <Login toggleSignupOn={toggleSignupOn} signupDisplay={signupDisplay}/>
      
      <!-- Sign up -->
      <Signup toggleSignupOn={toggleSignupOn} signupDisplay={signupDisplay}/>
      
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