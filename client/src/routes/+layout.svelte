<script>
  import { initFlash } from "sveltekit-flash-message/client"
  import { page } from "$app/stores"
  
  const flash = initFlash(page)
  const flashTimeout = 5000
  
  const removeFlash = () => {
    $flash = undefined
  }
  
  $: if ($flash) {
    setTimeout(removeFlash, flashTimeout)
  }
  
</script>

{#if $flash}
  <!-- Flash messages-->
  <div class="alert alert-dismissible flash fade show {$flash.type === 'success' ? 'alert-success' : 'alert-danger'}" role="alert">
    {$flash.message}
    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close" on:click={removeFlash}></button>
  </div>
{/if}
<slot />

<style>
  .flash {
    margin-bottom: 0;
  }
</style>