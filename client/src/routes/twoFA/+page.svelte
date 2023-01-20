<script>
    import TwoFA from '$lib/auth/twoFA.svelte'
    export let form
    
    let errors

    if (form?.TwoFAError) {
      errors = form.TwoFAError
    }
</script>
  
  
<svelte:head>
  <title>Bubbles | 2FA </title>
</svelte:head>

<main class="background h-100">
  <div class="container-fluid">
    <div class="row">
      <!-- Bubbles Logo -->
      <div class="bubbles-name col-md-6">
        <img class="logo-with-text" src="/with-text.svg" alt="Bubbles">
      </div>
      <div class="col-md-6">
        <TwoFA errors={errors}/>
        <br>
        <div class="text-center">
          <a href="/backupcode">Use Backup Code</a>
        </div>
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