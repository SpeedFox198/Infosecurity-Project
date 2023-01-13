<script>
import SlidingMenu from "$lib/settings/templates/SlidingMenu.svelte";
import { friends } from "$lib/stores/friend"
import { page } from "$app/stores"
import { getFlash } from "sveltekit-flash-message/client"

export let displayNewGroup;
export let toggleNewGroup;

const flash = getFlash(page)

let displayCustomizeGroup = false;
let friendSearchInput = "";

let showPhoto;
let photoUpload;
let photoPreview;

let groupName = "";
let disappearing;
let selectedFriends = [];

$: currentFriends = $friends.filter(friend => friend.username
                                                .toLowerCase()
                                                .includes(friendSearchInput));

const toggleCustomizeGroup = async () => displayCustomizeGroup = !displayCustomizeGroup;

const setGroupPhoto = () => {
  const photo = photoUpload[0]

  if (photo) {
    showPhoto = true
  
    const reader = new FileReader()
    reader.addEventListener("load", () => {
      photoPreview.setAttribute("src", reader.result)
    })
    reader.readAsDataURL(photo)

    return
  }
  showPhoto = false
}

const createGroup = async () => {
  const photoToSend = photoUpload ? photoUpload[0] : null

  const req = new FormData()
  req.append("group_icon", photoToSend)
  req.append("metadata", JSON.stringify({
    name: groupName,
    disappearing: disappearing,
    users: selectedFriends.map(user => user.user_id)
  }))

  const response = await fetch("https://localhost:8443/api/group/new", {
    method: "POST",
    credentials: "include",
    headers: {
      "Accept": "application/json",
    },
    body: req
  })

  if (!response.ok) {
    console.error(await response.json())
  }

  $flash = { type: 'success', message: "Group created!"}
  await toggleCustomizeGroup()
  await toggleNewGroup()
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

    {#if showPhoto}
      <img bind:this={ photoPreview } src="" alt="Group Preview" class="rounded-circle d-block mx-auto" style="width: 400px; length: 400px;">
    {/if}    


    <div class="mb-3">
      <label for="groupPhoto" class="form-label">Group Photo</label>
      <input class="form-control" type="file" id="groupPhoto" bind:files={photoUpload} on:change={setGroupPhoto}>
    </div>

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
        <select bind:value={disappearing}
         id="disappearingSelect"
         class="form-select"
         aria-label="Select the duration of disappearing messages"
         >
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
      <button type="submit" class="btn btn-primary btn-block" on:click={ createGroup }>Create Group</button>
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
