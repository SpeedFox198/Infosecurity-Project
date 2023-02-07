<script>
  import { fly, fade } from "svelte/transition"
  export let alertClass
  export let alertType
  export let message
</script>

<div
	class="b-toast d-flex flex-column"
	in:fly={{ y: -200, duration: 1000 }}
	out:fade
	role="alert"
>
	<div class="{alertClass} header">
		<div class="d-flex p-2">
			<span class="flex-grow-1 align-items-center">{alertType}</span>
			<button type="button" on:click class="remove-btn">
				<i class="fa-solid fa-xmark" />
			</button>
		</div>
	</div>
	<div class="p-2">
		{message}
	</div>
</div>

<style>
  .b-toast {
    width: 400px;
    max-width: 100%;
    background-color: rgba(255, 255, 255, .85);
    border-radius: 0.5rem;
    position: fixed;
    left: 50%;
    transform: translateX(-50%);
    top: 2rem;
    z-index: 11;
  }
  
  .header {
    color: var(--white);
    border-top-left-radius: 0.5rem;
    border-top-right-radius: 0.5rem;
  }
  
  .pos {
    background-color: #39ff14;
  } 
  
  .neg {
    background-color: #E10600;
  }
  
  .warn {
    background-color: yellow;
    color: black;
  }
  
  .remove-btn {
    border: 0;
    color: inherit;
    background-color: inherit;
  }
</style>