<script>
  import Login from "$lib/auth/login.svelte"
  import Signup from "$lib/auth/signup.svelte"

  let signupDisplay = false

  const toggleSignupOn = () => {
    signupDisplay = !signupDisplay
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
        <Signup toggleSignupOn={toggleSignupOn}/>
        {:else}
        <!-- Login -->
        <Login toggleSignupOn={toggleSignupOn} />
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