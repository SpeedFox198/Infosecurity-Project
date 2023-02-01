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
    setTimeout(removeFlash, flashTimeout)
  }
  
  const alertClass = {
    "success": "pos",
    "failure": "neg",
    "warning": "warn"
  }
  
  const alertType = {
    "success": "Success",
    "failure": "Error",
    "warning": "Warning"
  }
</script>

{#if $flash}
  <Toast 
    alertClass={alertClass[$flash.type]}
    alertType={alertType[$flash.type]}
    message={$flash.message}
    on:click={removeFlash}
  />
{/if}
<slot />
