<script>
import SlidingMenu from "$lib/settings/templates/SlidingMenu.svelte";
import Option from "$lib/settings/templates/Option.svelte";
import { friends } from "$lib/stores/friend";

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
            <button class="dropdown-item">
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
            <button class="dropdown-item" type="button" on:click>
              <i class="fa-solid fa-xmark"></i>
              Remove Friend
            </button>
          </li>
        </ul>
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
</style>
