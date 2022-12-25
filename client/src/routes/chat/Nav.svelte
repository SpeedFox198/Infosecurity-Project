<script>
  export let roomSearchInput

  let displayOptionsMenu = false
  
  const toggleOptionsMenu = () => {
    displayOptionsMenu = !displayOptionsMenu
  }

</script>

<div class="d-flex top-left align-items-center">
	<div class="p-2 input-group w-75">
    <span class="input-group-text search-icon">
      <i class="fa-solid fa-magnifying-glass"></i>
    </span>
		<input class="form-control no-border search-form"
      type="search"
      placeholder="Search" 
      aria-label="Search" 
      maxlength="20"
      bind:value={roomSearchInput} />
	</div>
	<button class="options-btn" title="Options" on:click={toggleOptionsMenu} type="button">
		<i class="fa-solid fa-ellipsis-vertical" />
	</button>
</div>

<style>
	.top-left {
		/* position: absolute;
  top: 0; */
		height: 4.6rem;
		width: var(--left-bar-length);
		background-color: var(--primary);
	}
  
  .options-btn {
    display: inline-block;
    text-decoration: none;
    border: none;
    background-color: var(--primary);
  }

  .options-btn:hover {
    cursor: pointer;
  }
  
  .search-icon {
    padding-right: 0.3rem;
  }
  
  .search-form {
    padding-left: 0.3rem;
  }
  
  .search-form:focus {
    box-shadow: none;
  }

  input[type="search"]::-webkit-search-cancel-button {
    cursor: pointer;
  }

  .no-border {
    border: 0;
  }
</style>
