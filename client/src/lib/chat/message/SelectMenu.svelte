<script>
import { createEventDispatcher } from "svelte";
import { room_id, roomList } from "$lib/stores/room";
import { selectedMsgs, counterNotSent } from "$lib/stores/select";

import { afterUpdate } from "svelte";
afterUpdate(() => console.log("hmm", $counterNotSent, invisible, $roomList, $room_id));

const dispatch = createEventDispatcher();

$: num = $selectedMsgs.size;
$: singular = num === 1;
$: currentRoom = ($roomList || {})[$room_id] || {};

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
<div class="container input-area">
  <div class="row justify-content-center align-items-center h-100">

    <!-- Attachments Input -->
    <div class="col-1 d-flex justify-content-center">
      <button class="btn p-0" type="button" on:click={selectedMsgs.clear}>
        <i class="icon-cross fa-solid fa-xmark"></i>
      </button>
    </div>

    <!-- Text Input -->
    <div class="col-10">
      <span>{num} message{singular ? "" : "s"} selected</span>
    </div>

    <!-- Submit Button -->
    <div class="col-1">
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
  height: 4rem;
  max-width: calc(100vw - var(--left-bar-length));
  background-color: var(--grey);
  border-left: 0.1rem solid var(--grey-shadow);
}

.icon-cross {
  font-size: 2rem;
}

.icon-trash {
  font-size: 1.5rem;
  color: var(--red-dark);
}
</style>
