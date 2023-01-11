<script>
import SlidingMenu from "$lib/settings/templates/SlidingMenu.svelte";
import { friends } from "$lib/stores/friend"

export let displayNewGroup;
export let toggleNewGroup;

//let displayMagic = false;     // Disappearing messages menu, *MAGIC! POOF!* (๑°༥°๑)
let displayCustomizeGroup = false;
let friendSearchInput = "";
let groupName = "";
let disappearing;
let selectedFriends = []; // IDs of users to be sent to API

$: currentFriends = $friends.filter(friend => friend.username
                                                .toLowerCase()
                                                .includes(friendSearchInput));

//const toggleMagic = async () => displayMagic = !displayMagic;
const toggleCustomizeGroup = async () => displayCustomizeGroup = !displayCustomizeGroup;

const createGroup = async () => {
  // TODO Implement submitting and backend logic
  const groupData = {
    group_name: groupName,
    disappearing: disappearing, 
    users: selectedFriends.map(users => users.user_id)
  }
  console.log(groupData)
}
</script>


<SlidingMenu title="Add Group Members" display={displayNewGroup} on:click={toggleNewGroup} right={false}>
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
      name={friend.username}
      title="Add friend to group" 
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
    on:click={ toggleCustomizeGroup }
    class="btn btn-primary btn-block"
    type="button"
    disabled={ selectedFriends.length === 0 ? 'true' : '' }
    aria-disabled={ selectedFriends.length === 0 ? 'true' : 'false' }
    >
      Next
    </button>
  </div>
</SlidingMenu>

<SlidingMenu title="Customize group" display={ displayCustomizeGroup } on:click={ toggleCustomizeGroup } right={false}>
  <div class="m-3">
    <!--TODO FilePond Here-->
    <h3>Group Icon</h3>

    <div class="form-floating mb-3">
      <input type="text" class="form-control" bind:value={groupName} id="floatingGroupName" placeholder="Group Name">
      <label for="floatingGroupName">Group Name</label>
    </div>

    <div class="mb-3 d-flex">
      <div class="align-items-center d-flex ">
        <i class="fa-solid fa-stopwatch fs-2"></i>
      </div>

      <span class="text-nowrap p-3 d-flex align-items-center">
        Disappearing messages
      </span>

      <div class="flex-grow-1 align-items-center d-flex">
        <select bind:value={disappearing} id="disappearingSelect" class="form-select" aria-label="Select the duration of disappearing messages">
          <option value="off" selected>Off</option>
          <option value="24h">1 Day</option>
          <option value="7d">1 Week</option>
          <option value="30d">1 Month</option>
        </select>  
      </div>
    </div>

    <div class="row">
      <span class="mb-2">Participants: { selectedFriends.length }</span>
      {#each selectedFriends as friend}
        <!-- The gap between each participant very not nice, need to improve on the values-->
        <div class="col-3 mb-5 ms-2">
          <div class="icon">
            <div class="img-wrapper img-1-1">
              <img class="rounded-circle" src={ friend.avatar } alt="{ friend.username } avatar">
            </div>
            <p class="text-center">{ friend.username }</p>
          </div>
        </div>
      {/each} 
    </div>

    <div class="d-grid">
      <button type="submit" class="btn btn-primary btn-block" on:click={createGroup}>Create Group</button>
    </div>  
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
