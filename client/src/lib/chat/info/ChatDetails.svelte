<script>
import { room_id, roomStorage, roomList } from "$lib/stores/room";

export let displayChatDetails;
export let closeChatDetails;

$: currentChat = ($roomStorage || {})[$room_id] || {};



</script>

<div class:d-none={!displayChatDetails} class="chat-details-section">
  <div class="chat-profile d-flex flex-row align-items-center p-2">
    <div class="d-flex">
      <button
        class="back d-flex align-items-center justify-content-center rounded-circle"
        type="button" on:click={closeChatDetails}
      >
        <i class="fa-solid fa-times fs-5"></i>
      </button>
    </div>
    <div class="d-flex">
      <div class="ms-4 fs-5 fw-bold user-select-none">{"Contact"} Info</div>
    </div>
  </div>
  <div class="content">

    <div class="section p-4 mb-2">
      <div class="img-wrapper img-1-1">
        <img class="rounded-circle p-3" src={currentChat.icon} alt="">
      </div>
      <div class="d-flex flex-row justify-content-center">
        <span class="chat-name fs-5">{currentChat.name}</span>
      </div>
    </div>

    <div class="section">
      <!-- encrypted? -->
      <!-- disappearing messages settings -->
    </div>

    <div class="section">
      <!-- Direct -->
      <!-- groups in common -->
      <!-- Group -->
      <!-- participants -->
    </div>

    <div class="section">
      <!-- Direct -->
      <!-- block, delete -->
      <!-- Group -->
      <!-- exit -->
    </div>

  </div>
</div>


<style>
.chat-details-section {
  height: 100%;
  width: var(--side-bar-length);
  right: initial;
  background-color: var(--white);
  overflow-x: hidden;
  transition: 0.15s;
}

.chat-profile {
  height: var(--top-bar-height);
  background-color: var(--primary);
  color: var(--white);
}

.section {
  background-color: var(--white);
  box-shadow: 0 3px 4px var(--grey-shadow);
}

.back {
  background-color: inherit;
  border: 0;
  width: 3rem;
  height: 3rem;
  color: var(--grey); 
}

.back:hover {
  background-color: var(--primary-highlight);
}

.content {
  height: calc(100vh - var(--top-bar-height));
  overflow-y: auto;
  background-color: var(--grey);
}
</style>
