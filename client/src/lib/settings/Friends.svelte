<script>
	import SlidingMenu from '$lib/settings/templates/SlidingMenu.svelte';
	import Option from '$lib/settings/templates/Option.svelte';
	import FriendsList from '$lib/friends/FriendsList.svelte';

	export let displayFriends;
	export let toggleFriends;

	let displayFriendsList = false;
	let toggleFriendsList = async () => (displayFriendsList = !displayFriendsList);
  let togglePendingList = async () => {}
</script>

<SlidingMenu title="Friends" display={displayFriends} on:click={toggleFriends} right={false}>
	<Option name="All" icon="user-group" on:click={toggleFriendsList} />
	<Option name="Pending Requests" icon="shield" on:click={togglePendingList} />
</SlidingMenu>

<FriendsList {displayFriendsList} {toggleFriendsList} />