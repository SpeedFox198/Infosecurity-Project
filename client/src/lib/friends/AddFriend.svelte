<script>
  import { createEventDispatcher } from "svelte";

  import SlidingMenu from "$lib/settings/templates/SlidingMenu.svelte";
	import Friend from "$lib/friends/Friend.svelte";
  import { friends } from "$lib/stores/friend"
  import { page } from "$app/stores"
  
  export let displayAddFriend
  export let toggleAddFriend
  
  const dispatch = createEventDispatcher()
	let currentUser = $page.data.user;
  let searchInput = "";
  let searchResults;
  let searchError;
  let loading = false;

  const searchUser = async () => {
    loading = true
    const response = await fetch(`https://localhost:8443/api/user/find`, {
      method: "POST",
      credentials: "include",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        "username": searchInput
      })
    })
    const data = await response.json()
    
    if (!response.ok) {
      loading = false
      searchError = data.message
      return
    }
    
    searchResults = data.user_search_results
    loading = false
  }
  
  const isFriendOrSelf = (user) => {
    const friends_user_ids = $friends.map(friend => friend.user_id)
    return (friends_user_ids.includes(user.user_id) || (currentUser.user_id === user.user_id))
  }
  
  const createFriendRequest = async (user_id) => {
    dispatch(
      'create-friend-request', {
        user: user_id
      }
    ) 
  }
</script>

<SlidingMenu title="Add A Friend" display={displayAddFriend} on:click={toggleAddFriend} right={false}>
  <div class="m-3">
    <form on:submit={searchUser}>
      <div class="input-group mb-3">
        <input type="text" class="form-control search-bar py-2" placeholder="Search for a user by their username" required bind:value={searchInput}>
        <span class="input-group-text search-btn-platform">
          <button type="submit" class="btn search-btn" title="Search for a user">
            <i class="fa-solid fa-magnifying-glass"></i>
          </button>
        </span>
      </div>
    </form>
  </div>
    
  {#if loading}
    <span class="position-absolute top-50 start-50 translate-middle fs-4">
      Loading...
    </span>
  {:else}

    {#if searchError}
      <span class="position-absolute top-50 start-50 translate-middle fs-4">{searchError}</span>
    {/if}

    {#if searchResults}
      {#each searchResults as user (user.user_id)}
        <Friend friend={user}>

          {#if !isFriendOrSelf(user)}
            <div class="ms-auto">
              <button class="btn btn-primary" on:click={createFriendRequest(user.user_id)}>
                <i class="fa-solid fa-user-plus"></i>
                Add friend
              </button>
            </div>
          {/if}

        </Friend>
      {/each}
    {/if}
    
  {/if}
</SlidingMenu>

<style>
  .search-bar:focus {
    box-shadow: none;
  }

  .search-btn-platform {
    background-color: var(--white);
    padding: 0;
  }
  
  .search-btn:focus {
    outline: none;
  }
</style>