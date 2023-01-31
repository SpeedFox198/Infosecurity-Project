<script>
  import { fly, fade } from 'svelte/transition';
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
  <div class="b-toast p-3 d-flex flex-column" in:fly="{{ y: -200, duration: 1000 }}" out:fade role="alert">
    <div class="{alertClass[$flash.type]} p-2 header">
      <div class="d-flex">
        <span class="flex-grow-1 align-items-center">{alertType[$flash.type]}</span>
        <button type="button" on:click={removeFlash} class="remove-btn">
          <i class="fa-solid fa-xmark"></i>
        </button>
      </div>
    </div>
    <div>
      {$flash.message}
    </div>
  </div> 
{/if}
<slot />

<style>
  .b-toast {
    width: 400px;
    max-width: 100%;
    background-color: rgba(255, 255, 255, .85);
    border-radius: 0.5rem;
    position: fixed;
    left: 50%;
    top: 2rem;
    z-index: 5;
  }
  
  .header {
    color: var(--white);
    border-radius: 0.5rem;
  }
  
  .pos {
    background-color: #39ff14;
  } 
  
  .neg {
    background-color: #E10600;
  }
  
  .warn {
    background-color: yellow;
  }
  
  .remove-btn {
    border: 0;
    color: inherit;
    background-color: inherit;
  }
</style>