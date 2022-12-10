<script>
import { beforeUpdate, afterUpdate } from "svelte";

import { msgStorage, allMsgs } from "$lib/stores/message";
import { room_id } from "$lib/stores/room";

import Message from "$lib/chat/message/Message.svelte";


$: roomMsgs = ($allMsgs || {})[$room_id] || [];

let chatDisplay;


// beforeUpdate(() => {
//   autoscroll = div && (div.offsetHeight + div.scrollTop) > (div.scrollHeight - 20);
// });

// afterUpdate(() => {
//   if (autoscroll) div.scrollTo(0, div.scrollHeight);
// });
</script>


<!-- Messages Display Section -->
<div class="chat" bind:this={chatDisplay}>
  <div class="my-2"></div>
  {#each roomMsgs as message_id}
    <Message msg={$msgStorage[message_id]}/>
  {/each}
  <div id="anchor"></div>
</div>


<style>
.chat {
  height: calc(100vh - 8rem);
  overflow-y: scroll;
  border-top: 0.1rem solid var(--grey-shadow);
  border-left: 0.1rem solid var(--grey-shadow);
}

/* TODO(SpeedFox198): Remove when unused */
#anchor {
  overflow-anchor: auto;
  height: 1rem;
}
</style>