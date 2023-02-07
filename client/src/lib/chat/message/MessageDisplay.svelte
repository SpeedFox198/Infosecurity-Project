<script>
import { beforeUpdate, afterUpdate, onMount } from "svelte";

import { msgStorage, allMsgs } from "$lib/stores/message";
import { room_id } from "$lib/stores/room";
import { user_id } from "$lib/stores/user"
import { count } from "$lib/stores/count";
import { lockScroll } from "$lib/stores/scroll";
import { selectedMsgs } from "$lib/stores/select";

import Message from "$lib/chat/message/Message.svelte";
import LoadingMessage from "$lib/chat/LoadingMessage.svelte";


export let getRoomMsgs;
export let ocrLoading;
export let blocked;

$: roomMsgs = $allMsgs?.[$room_id] || [];

let display;
let autoScroll = true;
let loadingMsgs = false;
let currentScroll;


onMount(() => {
  autoScroll = true;  // Scroll the first time it is loaded
});


beforeUpdate(() => {
  if (loadingMsgs) {  // When loading older messages
    if (!$lockScroll) currentScroll = display.scrollHeight - display.scrollTop;
    autoScroll = false;
  } else {            // Check if need to autoscroll to latest message
    autoScroll = display && display.scrollTop + display.clientHeight === display.scrollHeight;
  }
});


afterUpdate(() => {
  if (loadingMsgs && !$lockScroll) {  // If loading old messages
    display.scrollTo(0, display.scrollHeight - currentScroll);
    loadingMsgs = false;
  } else if (autoScroll) {  // Scroll if at bottom of screen
    display.scrollTo(0, display.scrollHeight);
  }
});


function loadOldMsgs() {
  if (!loadingMsgs && display && display.scrollTop < 333) {
    loadingMsgs = true;
    const { n, extra } = count.nextN($room_id);
    getRoomMsgs($room_id, n, extra);
  }
}


function selectMsg(message_id, user_id_) {
  selectedMsgs.toggle(message_id, user_id_ === $user_id);
}
</script>


<!-- Messages Display Section -->
<div class="chat" bind:this={display} on:scroll={loadOldMsgs}>
  <div class="my-2"></div>

  <!-- Load each message in the room -->
  {#each roomMsgs as messageInfo}
    <Message
      {blocked}
      msg={$msgStorage[messageInfo.message_id]}
      selected={$selectedMsgs.has(messageInfo.message_id)}
      select={() => selectMsg(messageInfo.message_id, messageInfo.user_id)}/>
  {/each}
  
  {#if ocrLoading}
    <LoadingMessage />
  {/if}

  <!-- Anchor page to bottom when at bottom -->
  <div id="anchor"></div>
</div>


<style>
.chat {
  height: calc(100vh - var(--top-bar-height) - var(--bottom-bar-height));
  background-color: var(--primary-light);
  overflow-y: scroll;
  border-top: 0.1rem solid var(--highlight-primary);
  border-left: 0.1rem solid var(--grey-shadow);
}

#anchor {
  overflow-anchor: auto;
  height: 1px;
}
</style>
