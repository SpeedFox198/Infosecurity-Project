<script>
	import SlidingMenu from '$lib/settings/templates/SlidingMenu.svelte';
	import Friend from './Friend.svelte';

	export let displayFriendRequests;
	export let toggleFriendRequests;

  let friend = {}
</script>

<SlidingMenu
	title="Friend Requests"
	display={displayFriendRequests}
	on:click={toggleFriendRequests}
	right="false"
>
  <div class="m-3">
    <div class="mb-4">
      <span class="fw-bold fs-4">Sent</span>
      <Friend {friend}>
        <div class="ms-auto">
          <button type="button" class="btn btn-danger">Cancel</button>
        </div>
      </Friend>
    </div>
    <div>
      <span class="fw-bold fs-4">Received</span>
      <Friend {friend}>
        <div class="ms-auto">
          <button type="button" class="circle-btn me-2 pos">
            <i class="fa-solid fa-check fs-3"></i>
          </button>
          <button type="button" class="circle-btn neg">
            <i class="fa-solid fa-xmark fs-3"></i>
          </button>
        </div>
      </Friend>
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
</style>
