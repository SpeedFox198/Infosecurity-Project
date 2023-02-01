<script>
  import { initFlash } from "sveltekit-flash-message/client"
  import { page } from "$app/stores"
	import Toast from '$lib/general/Toast.svelte';
  
  const flash = initFlash(page)
  const flashTimeout = 5000
  
  const removeFlash = () => {
    $flash = undefined
  }
  
  $: if ($flash) {
    // Auto remove flash if user does not click x
    setTimeout(removeFlash, flashTimeout)
  }
  
  const alert = {
    "success": {
      type: "Success",
      class: "pos"
    },
    "failure": {
      type: "Error",
      class: "neg"
    },
    "warning": {
      type: "Warning",
      class: "warn"
    }
  }
</script>

{#if $flash}
  <Toast 
    alertClass={alert[$flash.type].class}
    alertType={alert[$flash.type].type}
    message={$flash.message}
    on:click={removeFlash}
  />
{/if}
<slot />