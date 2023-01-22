<script>
	import SlidingMenu from '$lib/settings/templates/SlidingMenu.svelte';
	import Friend from '$lib/friends/Friend.svelte';
  import { friendRequestsStore } from '$lib/stores/friend-requests'

	export let displayFriendRequests;
	export let toggleFriendRequests;

</script>

<SlidingMenu
	title="Friend Requests"
	display={displayFriendRequests}
	on:click={toggleFriendRequests}
	right="false"
>
  <div class="mb-4">
    <span class="fw-bold fs-4 mx-3">Sent</span>
    {#each $friendRequestsStore.sent as user}
      <Friend friend={user}>
        <div class="ms-auto">
          <button type="button" class="btn btn-danger">Cancel</button>
        </div>
      </Friend>  
    {/each}
  </div>
  <div>
    <span class="fw-bold fs-4 mx-3">Received</span>
    {#each $friendRequestsStore.received as user}
      <Friend friend={user}>
        <div class="ms-auto">
          <button type="button" class="circle-btn me-2 pos">
            <i class="fa-solid fa-check fs-3"></i>
          </button>
          <button type="button" class="circle-btn neg">
            <i class="fa-solid fa-xmark fs-3"></i>
          </button>
        </div>
      </Friend>  
    {/each}
    
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
</style>
