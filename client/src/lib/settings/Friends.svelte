
<script>
import SlidingMenu from "$lib/settings/templates/SlidingMenu.svelte";
import Option from "$lib/settings/templates/Option.svelte";
import { friends } from "$lib/stores/friend"

export let displayFriends;
export let toggleFriends;

</script>


<SlidingMenu title="Friends" display={displayFriends} on:click={toggleFriends} right={false}>
  {#each $friends as friend}
    <div class="friend d-flex py-2 user-select-none align-items-center">
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
</style>
