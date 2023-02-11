<script>
import { page } from "$app/stores"

let currentUser = $page.data.user

export let gDriveHandleSignoutClick;
export let toggleSettings;
export let toggleNewGroup;
export let toggleFriends;
export let toggleBlockedUsers;
export let roomSearchInput

const logoutUser = async () => {
  if (gDriveHandleSignoutClick) gDriveHandleSignoutClick();
  localStorage.clear();
  await fetch("https://localhost:8443/api/auth/logout", {
    method: "POST",
    credentials: "include",
    headers: {
      "Accept": "application/json"
    }
  })

  location.replace("/")
};
</script>

<div class="d-flex top-left">
  <div class="nav-height d-flex flex-row align-items-center w-100">
    <img src={ currentUser.avatar || "default.png" } alt="avatar" class="rounded-circle h-100 p-2 user-select-none">
    <div class="input-group flex-grow p-2 h-100">
      <span class="input-group-text search-icon h-100">
        <i class="fa-solid fa-magnifying-glass"></i>
      </span>
      <input class="form-control no-border search-form h-100"
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
          <button on:click={toggleSettings} class="dropdown-item" type="button">
            <i class="fa-solid fa-cog"></i>
            Settings
          </button>
        </li>
        <li>
          <button on:click={toggleNewGroup} class="dropdown-item" type="button">
            <i class="fa-solid fa-plus"></i>
            New Group
          </button>
        </li>
        <li>
          <button on:click={toggleFriends} class="dropdown-item" type="button">
            <i class="fa-solid fa-user-group"></i>
            Friends
          </button>
        </li>
        <li>
          <button on:click={toggleBlockedUsers} class="dropdown-item" type="button">
            <i class="fa-solid fa-user-slash"></i>
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
</div>

<style>
  .nav-height {
    height: var(--top-bar-height);
  }

	.top-left {
		/* position: absolute;
  top: 0; */
		height: var(--top-bar-height);
		width: var(--side-bar-length);
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
