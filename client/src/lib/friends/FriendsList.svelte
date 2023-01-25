<script>
import { onMount } from "svelte";
import { getFlash } from "sveltekit-flash-message/client";

import { page } from "$app/stores";
import { invalidate } from "$app/navigation";
import SlidingMenu from "$lib/settings/templates/SlidingMenu.svelte";
import { friends } from "$lib/stores/friend"
import AddFriend from "$lib/friends/AddFriend.svelte";

export let displayFriendsList;
export let toggleFriendsList;
export let socket;

const flash = getFlash(page)
let displayAddFriend = false;

const toggleAddFriend = () => {
  displayAddFriend = !displayAddFriend
}

const removeFriend = async (user_id) => {
  socket.emit("remove_friend", {
    user: user_id
  })
}

const messageFriend = async (user_id) => {
  socket.emit("message_friend", {
    user: user_id  
  })
}

onMount(async () => {
  socket.on("remove_friend_failed", async (data) => {
    $flash = {type: 'failure', message: `Friend failed to remove! Reason: ${data.message}`}
  })
  
  socket.on("friend_removed", async () => {
    invalidate("app:friends")
  })
  
  socket.on("message_friend_error", async (data) => {
    $flash = {type: 'failure', message: `Failed to message friend! Reason: ${data.message}`}
  })
})
</script>


<SlidingMenu title="Friends List" display={displayFriendsList} on:click={toggleFriendsList} right={false}>
  {#each $friends as friend (friend.user_id)}
    <div class="friend d-flex py-2 user-select-none align-items-center">
      <div class="icon p-2">
        <div class="img-wrapper img-1-1">
          <img class="rounded-circle" src={friend.avatar} alt="{friend.username} avatar">
        </div>
      </div>
      <div class="d-flex align-items-center">
        <span>{friend.username}</span>
      </div>
      
      <!-- Friend dropdown -->
      <div class="dropdown flex-grow-1 pe-3 text-end">
        <button
         class="options-btn dropdown-toggle"
         title="Options"
         type="button"
         id="{friend.user_id}-dropdown"
         data-bs-toggle="dropdown"
         aria-expanded="false"
        >
          <i class="fa-solid fa-ellipsis-vertical" />
        </button>

        <ul class="dropdown-menu" aria-labelledby="{friend.user_id}-dropdown">
          <li>
            <button class="dropdown-item" on:click={messageFriend(friend.user_id)}>
              <i class="fa-solid fa-message"></i>
              Message
            </button>
          </li>
          <li>
            <button on:click class="dropdown-item" type="button">
              <i class="fa-solid fa-user-slash"></i>
              Block
            </button>
          </li>
          <li>
            <button class="dropdown-item" type="button" on:click={removeFriend(friend.user_id)}>
              <i class="fa-solid fa-xmark"></i>
              Remove Friend
            </button>
          </li>
        </ul>
      </div>

    </div>
  {/each}
  <div class="position-absolute bottom-0 end-0 pe-3 mb-3">
    <button type="button" class="btn friend-req" on:click={toggleAddFriend}>
      <i class="fa-solid fa-user-plus fs-4"></i>
    </button>
  </div>

</SlidingMenu>

<AddFriend {displayAddFriend} {toggleAddFriend} {socket} />

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

.options-btn {
  display: inline-block;
  text-decoration: none;
  border: none;
  background-color: inherit;
  color: #000000;
}

.options-btn:hover {
  cursor: pointer;
  background-color: inherit;
}

.dropdown-toggle::after {
  content: none;
}

.friend-req {
  border-radius: 50%;
  background-color: var(--primary);
  color: var(--white);
  width: 4rem;
  height: 4rem;
}

.friend-req:active {
  background-color: var(--primary-shadow);
  color: var(--white);
}

</style>
