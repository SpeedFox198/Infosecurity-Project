<script>
	import SlidingMenu from '$lib/settings/templates/SlidingMenu.svelte';
	import Friend from '$lib/friends/Friend.svelte';
  import { friendRequestsStore } from '$lib/stores/friend-requests'
	import { onMount } from 'svelte';
	import { invalidate } from '$app/navigation';

	export let displayFriendRequests;
	export let toggleFriendRequests;
  /** @type {import('socket.io-client').Socket}*/
  export let socket;

  const cancelSentFriendRequest = async (user_id) => {
    socket.emit("cancel_sent_friend_request", {
      user: user_id
    })
  }
  
  const acceptFriendRequest = async (user_id) => {
    socket.emit("accept_friend_request", {
      user: user_id
    })
  }
  
  const cancelReceivedFriendRequest = async (user_id) => {
    socket.emit("cancel_received_friend_request", {
      user: user_id
    })
  }

  onMount(async () => {
    socket.on("friend_requests_update", async () => {
      invalidate("app:friend-requests")
    })
  })
</script>

<SlidingMenu
	title="Friend Requests"
	display={displayFriendRequests}
	on:click={toggleFriendRequests}
>
  <div class="req-partition d-flex flex-column">
    <span class="fw-bold fs-4 mx-3">Sent</span>
    <div class="flex-grow-1 requests">
      {#each $friendRequestsStore.sent as user (user.user_id)}
        <Friend friend={user}>
          <div class="ms-auto">
            <button type="button" class="btn btn-danger" on:click={cancelSentFriendRequest(user.user_id)}>Cancel</button>
          </div>
        </Friend>  
      {/each}
    </div>
  </div>

  <div class="req-partition d-flex flex-column">
    <span class="fw-bold fs-4 mx-3">Received</span>
    <div class="flex-grow-1 requests">
      {#each $friendRequestsStore.received as user (user.user_id)}
        <Friend friend={user}>
          <div class="ms-auto">
            <button type="button" class="circle-btn me-2 pos" on:click={acceptFriendRequest(user.user_id)}>
              <i class="fa-solid fa-check fs-3"></i>
            </button>
            <button type="button" class="circle-btn neg" on:click={cancelReceivedFriendRequest(user.user_id)}>
              <i class="fa-solid fa-xmark fs-3"></i>
            </button>
          </div>
        </Friend>  
      {/each}
    </div>
  </div>
</SlidingMenu>

<style>
  .circle-btn {
    border: 0;
    border-radius: 50%;
    width: 3rem;
    height: 3rem;
  }

  .pos {
    background-color: #39ff14;
    color: var(--white);
  }

  .neg {
    background-color: #E10600;
    color: var(--white);
  }
  
  .req-partition {
    height: 50%;
  }

  .requests {
    overflow-y: auto;
  }
</style>
