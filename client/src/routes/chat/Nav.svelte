<script>
  export let roomSearchInput

  const logoutUser = async () => {
    await fetch("https://localhost:8443/api/auth/logout", {
      method: "POST",
      credentials: "include",
      headers: {
        "Accept": "application/json"
      }
    })
    
    location.replace("/")
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
      bind:value={roomSearchInput}
     />
	</div>

  <div class="dropdown flex-grow-1 pe-3 text-end">
    <button
     class="options-btn dropdown-toggle"
     title="Options"
     type="button"
     id="navOptionsDropdown"
     data-bs-toggle="dropdown"
     aria-expanded="false"
    >
      <i class="fa-solid fa-ellipsis-vertical" />
    </button>
    <ul class="dropdown-menu" aria-labelledby="navOptionsDropdown">
      <li>
        <button class="dropdown-item" type="button">
          <i class="fa-solid fa-plus"></i>
          New Chat
        </button>
      </li>
      <li>
        <button class="dropdown-item" type="button">
          <i class="fa-solid fa-user-group"></i>
          Friends
        </button>
      </li>
      <li>
        <button class="dropdown-item" type="button">
          <i class="fa-regular fa-circle-xmark"></i>
          Blocked Users
        </button>
      </li>
      <li>
        <button class="dropdown-item" type="button" on:click={logoutUser}>
          <i class="fa-solid fa-arrow-right-from-bracket"></i>
          Logout
        </button>
      </li>
    </ul>
  </div>
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
    color: #ffffff;
  }

  .options-btn:hover {
    cursor: pointer;
  }
  
  .search-icon {
    padding-right: 0.3rem;
    background-color: #ffffff;
    border-color: #ffffff;
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
  
  .dropdown-toggle::after {
    content: none;
  }
</style>
