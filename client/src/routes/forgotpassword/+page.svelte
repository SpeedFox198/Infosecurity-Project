<script>
    import OTP from '$lib/auth/otp.svelte'
    export let form
    
    let errors

    if (form?.otpError) {
      errors = form.otpError
    }
  </script>
  
  
  <svelte:head>
    <title>Bubbles | Forgot Password</title>
  </svelte:head>
  
  <main class="background h-100">
    <div class="container-fluid">
      <div class="row">
        <!-- Bubbles Logo -->
        <div class="bubbles-name col-md-6">
          <img class="logo-with-text" src="/with-text.svg" alt="Bubbles">
        </div>
        <div class="col-md-6">
          <OTP errors={errors}/>
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