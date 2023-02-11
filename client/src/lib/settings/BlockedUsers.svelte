<script>
import SlidingMenu from "$lib/settings/templates/SlidingMenu.svelte";
import { roomStorage, roomList } from "$lib/stores/room"

export let displayBlockedUsers;
export let toggleBlockedUsers;
export let socket;

let blockedSearchInput = "";
let selectedBlocked;
// TODO(low)(SpeedFox198): remove demo values

$: unfilteredRooms = $roomList.map(room_id => $roomStorage[room_id]);
$: currentBlocks = unfilteredRooms.filter(
  room =>
  room.blocked === "blocking" &&
  room.name.toLowerCase().includes(blockedSearchInput)
);

const unblockUser = (block_id, room_id) => socket.emit("unblock_user", { block_id, room_id });
const selectUser = block_id => selectedBlocked = block_id;
</script>


<SlidingMenu title="Blocked Users" display={displayBlockedUsers} on:click={toggleBlockedUsers}>
  <div class="input-group">
    <input
      type="search"
      class="form-control no-border m-3"
      placeholder="Search..." 
      aria-label="Search" 
      bind:value={blockedSearchInput}
    >
  </div>

  {#each currentBlocks as blocked}
    <div class="friend d-flex py-2 px-3 user-select-none align-items-center">
      {#if blocked.user_id !== selectedBlocked}

        <div class="icon p-2">
          <div class="img-wrapper img-1-1">
            <img
              class="rounded-circle"
              src={
                blocked.icon.startsWith("media/") ?
                `https://localhost:8443/api/${blocked.icon}` :
                blocked.icon
              }
              alt={blocked.name}
            >
          </div>
        </div>
        <div class="d-flex align-items-center">
          <span>{blocked.name}</span>
        </div>
        <button class="btn ms-auto unblock-button dark-green" on:click={() => selectUser(blocked.user_id)}>
          <i class="fa-solid fa-ban"></i> Unblock
        </button>

      {:else}

        <div class="d-flex align-items-center me-auto p-3">
          <span>Unblock <strong class="green">{blocked.name}</strong>?</span>
        </div>
        <button class="btn dark-green confirm-button"
          on:click={() => {unblockUser(blocked.user_id, blocked.room_id); setTimeout(selectUser, 500); }}>
          <i class="fa-solid fa-check fs-5"></i>
        </button>
        <button class="btn red cancel-button" on:click={() => selectUser("")}>
          <i class="fa-solid fa-xmark fs-5"></i>
        </button>
      {/if}
    </div>
  {/each}
</SlidingMenu>


<style>

.friend:has(> .unblock-button:hover) {
  background-color: var(--white-shadow);
}

.icon {
  height: 4.5rem;
  width: 4.5rem;
}

.no-border {
  border: 0;
}

.btn {
  background-color: transparent;
  border: none;
}

.green {
  color: var(--primary);
}

.dark-green {
  color: var(--primary-shadow);
}

.red {
  color: var(--red);
}

.unblock-button:hover {
  color: var(--primary-highlight);
}

.confirm-button:hover {
  color: var(--primary-highlight);
}

.cancel-button:hover {
  color: var(--red);
}
</style>
