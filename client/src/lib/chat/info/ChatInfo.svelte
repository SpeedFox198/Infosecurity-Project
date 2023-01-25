<script>
import { createEventDispatcher } from "svelte";
import { room_id, roomStorage } from "$lib/stores/room";

$: currentChat = ($roomStorage || {})[$room_id] || undefined;

const dispatch = createEventDispatcher();

const onClickEvent = () => {
  if (currentChat !== undefined) dispatch("click");
}

</script>


<!-- Chat Info Section -->
<div
  class="chat-info d-flex user-select-none"
  class:has-chat={currentChat}
  on:click={onClickEvent} on:keydown
>
  <div class="d-flex flex-row">
    {#if currentChat !== undefined}

      <!-- Chat Icon -->
      <div class="icon d-flex ms-3 me-1">
        <div class="img-wrapper img-1-1">
          {#if !currentChat.icon.startsWith("media/")}
            <img class="rounded-circle p-2" src={currentChat.icon} alt="">
          {:else}
            <img class="rounded-circle p-2" src={`https://localhost:8443/api/${currentChat.icon}`} alt="">
          {/if}
        </div>
      </div>

      <!-- Chat Name -->
      <div class="d-flex align-items-center">
        <span class="name">{currentChat.name}</span>
      </div>

    {/if}
  </div>
</div>


<style>
.chat-info {
  height: var(--top-bar-height);
  background-color: var(--primary);
  border-left: 0.1rem solid var(--primary-shadow);
}

.chat-info.has-chat:hover {
  cursor: pointer;
}

.chat-info > .flex-row {
  height: var(--top-bar-height);
}

.icon {
  width: var(--top-bar-height);
}

.name {
  color: var(--white);
}
</style>
