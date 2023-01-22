<script>
	import SlidingMenu from '$lib/settings/templates/SlidingMenu.svelte';
	import Option from '$lib/settings/templates/Option.svelte';
	import FriendsList from '$lib/friends/FriendsList.svelte';
	import FriendRequests from '$lib/friends/FriendRequests.svelte';

	export let displayFriends;
	export let toggleFriends;
  export let socket;

	let displayFriendsList = false;
	let displayFriendRequests = false;

	let toggleFriendsList = async () => displayFriendsList = !displayFriendsList;
  let toggleFriendRequests = async () => displayFriendRequests = !displayFriendRequests;
</script>

<SlidingMenu title="Friends" display={displayFriends} on:click={toggleFriends} right={false}>
	<Option name="All" icon="user-group" on:click={toggleFriendsList} />
	<Option name="Pending Requests" icon="shield" on:click={toggleFriendRequests} />
</SlidingMenu>

<FriendsList {displayFriendsList} {toggleFriendsList} {socket} />
<FriendRequests {displayFriendRequests} {toggleFriendRequests} />