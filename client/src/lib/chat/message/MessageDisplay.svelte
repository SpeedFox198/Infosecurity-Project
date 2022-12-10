<script>
import { beforeUpdate, afterUpdate, onMount } from "svelte";

import { msgStorage, allMsgs } from "$lib/stores/message";
import { room_id } from "$lib/stores/room";
import { count } from "$lib/stores/count";

import Message from "$lib/chat/message/Message.svelte";


export let getRoomMsgs;

$: roomMsgs = ($allMsgs || {})[$room_id] || [];

let display;
let autoScroll = true;
let loadingMsgs = false;
let currentScroll;


onMount(() => {
  autoScroll = true;  // Scroll the first time it is loaded
})


beforeUpdate(() => {
  if (loadingMsgs) {  // If loading old messages
    currentScroll = display.scrollHeight - display.scrollTop;
  } else {            // Check if need to autoscroll to latest message
    autoScroll = display && display.scrollTop + display.clientHeight === display.scrollHeight;
  }
});


afterUpdate(() => {
  if (loadingMsgs) {        // If loading old messages
  console.log('then height', display.scrollHeight)
    console.log('currentscroll ',currentScroll);
    display.scrollTo(0, display.scrollHeight - currentScroll);
    loadingMsgs = false;
  } else if (autoScroll) {  // Scroll if at bottom of screen
    display.scrollTo(0, display.scrollHeight);
  }
});


async function loadOldMsgs() {
  console.log('scroll height', display.scrollHeight)
  if (!loadingMsgs && display && display.scrollTop < 500) {
    loadingMsgs = true;
    const { n, extra } = count.nextN($room_id);
    getRoomMsgs($room_id, n, extra);
  }
}
</script>


<!-- Messages Display Section -->
<div class="chat" bind:this={display} on:scroll={loadOldMsgs}>
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
