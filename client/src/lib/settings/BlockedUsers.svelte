<script>
    
    import SlidingMenu from "$lib/settings/templates/SlidingMenu.svelte";
    import { friends } from "$lib/stores/friend"
    
    export let displayBlockedUsers;
    export let toggleBlockedUsers;
    
    let friendSearchInput = "";
    let selectedFriends = [];
    // TODO(low)(SpeedFox198): remove demo values

    $: currentFriends = $friends.filter(friend => friend.username
                                                    .toLowerCase()
                                                    .includes(friendSearchInput));
    
    /** @type {?File} */
    
    const Unblock = () => {
      console.log(selectedFriends);
    }

    </script>
    
    
    <SlidingMenu title="Blocked Users" display={displayBlockedUsers} on:click={toggleBlockedUsers}>
      <div class="input-group">
        <input
         type="search"
         class="form-control no-border m-3"
         placeholder="Search..." 
         aria-label="Search" 
         bind:value={friendSearchInput}
        >  
      </div>
    
      {#each currentFriends as friend}
        <div class="friend d-flex py-2 user-select-none align-items-center">
          <input type="checkbox"
          class="form-check-input ms-3 me-1 p-2"
          title="Add { friend.username } to group" 
          bind:group={selectedFriends} 
          value={friend}
          >
          <div class="icon p-2">
            <div class="img-wrapper img-1-1">
              <img class="rounded-circle" src={friend.avatar} alt="{friend.username} avatar">
            </div>
          </div>
          <div class="d-flex align-items-center">
            <span>{friend.username}</span>
          </div>
        </div>
      {/each}

      <div class="d-grid m-3">
        <button 
        on:click={ Unblock }
        class="btn btn-primary btn-block"
        type="button"
        disabled={ selectedFriends.length === 0 ? 'true' : '' }
        aria-disabled={ selectedFriends.length === 0 ? 'true' : 'false' }
        >
          Unblock
        </button>
      </div>

    </SlidingMenu>
    
       
    <style>
    .friend {
      border-bottom: 0.1rem solid var(--primary-light-shadow);
    }
    
    .friend:hover {
      cursor: pointer;
      background-color: var(--primary-light-shadow);
    }
    
    .icon {
      height: 4.5rem;
      width: 4.5rem;
    }
    
    .no-border {
      border: 0;
    }
    
    </style>