<script>
  import { friendRequestsStore } from "$lib/stores/friend-requests"
	import SlidingMenu from '$lib/settings/templates/SlidingMenu.svelte';
	import Option from '$lib/settings/templates/Option.svelte';
	import FriendsList from '$lib/friends/FriendsList.svelte';
	import FriendRequests from '$lib/friends/FriendRequests.svelte';

	export let displayFriends;
	export let toggleFriends;
  export let socket;

	let displayFriendsList = false;
	let displayFriendRequests = false;
  $: friendRequestCount = $friendRequestsStore.sent.length + $friendRequestsStore.received.length

	let toggleFriendsList = async () => displayFriendsList = !displayFriendsList;
  let toggleFriendRequests = async () => displayFriendRequests = !displayFriendRequests;
  
  const returnToMenuAfterMessage = async () => {
    await toggleFriendsList()
    await toggleFriends()
  }
</script>

<SlidingMenu title="Friends" display={displayFriends} on:click={toggleFriends}>
	<Option name="All" icon="user-group" on:click={toggleFriendsList} />
	<Option name="Pending Requests" icon="shield" on:click={toggleFriendRequests}>
    <div class="d-flex align-items-center ms-auto me-4">
      <span class="fs-5 friend-request-count text-center">{friendRequestCount}</span>
    </div>
  </Option>
</SlidingMenu>

<FriendsList {displayFriendsList} {toggleFriendsList} {socket} on:message-friend={returnToMenuAfterMessage} />
<FriendRequests {displayFriendRequests} {toggleFriendRequests} {socket} />

<style>
  .friend-request-count {
    border-radius: 50%;
    width: 2rem;
    height: 2rem;
    background-color: #ff6500;
    color: var(--white);
  }
</style>