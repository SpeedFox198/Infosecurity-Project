<script>
import { createEventDispatcher } from "svelte";
import { room_id, roomStorage } from "$lib/stores/room";
import { selectedMsgs, counterNotSent } from "$lib/stores/select";

const dispatch = createEventDispatcher();

$: num = $selectedMsgs.size;
$: singular = num === 1;
$: currentRoom = ($roomStorage || {})[$room_id] || {};

$: invisible = $counterNotSent &&
  (
    (currentRoom.type === "direct") ||
    (currentRoom.type === "group" && !currentRoom.is_admin)
  );


async function deleteMsgs(event) {
  // Trigger deletion of the selected messages
  dispatch("delete", {
    "messages": Array.from($selectedMsgs),
    "room_id": $room_id
  });

  // Clear any selected messages that are to be deleted
  selectedMsgs.clear();
}
</script>


<!-- Texting Input Section -->
<div class="d-flex flex-container w-100 input-area">
  <div class="d-flex flex-row justify-content-center align-items-center h-100 w-100">

    <!-- Attachments Input -->
    <div class="icon-container d-flex justify-content-center">
      <button class="btn p-0" type="button" on:click={selectedMsgs.clear}>
        <i class="icon-cross fa-solid fa-xmark"></i>
      </button>
    </div>

    <!-- Text Input -->
    <div class="flex-grow-1 mx-4">
      <span>{num} message{singular ? "" : "s"} selected</span>
    </div>

    <!-- Submit Button -->
    <div class="icon-container">
      <button class="btn" class:invisible type="button" on:click={deleteMsgs}>
        <i class="icon-trash fa-solid fa-trash"></i>
      </button>
    </div>
  </div>
</div>


<style>
.input-area {
  position: absolute;
  bottom: 0;
  height: var(--bottom-bar-height);
  background-color: var(--grey);
  border-left: 0.1rem solid var(--grey-shadow);
}

.icon-container {
  width: 5rem;
}

.icon-cross {
  font-size: 2rem;
}

.icon-trash {
  font-size: 1.5rem;
  color: var(--red);
}
</style>
