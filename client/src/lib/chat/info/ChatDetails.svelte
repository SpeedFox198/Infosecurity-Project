<script>
import { room_id, roomStorage } from "$lib/stores/room";
import ChatSettings from "./ChatSettings.svelte";

export let displayChatDetails;
export let closeChatDetails;
export let animateHideChatDetails;

let displayNone = true;
$: currentChat = ($roomStorage || {})[$room_id] || {};
$: displayChatDetails ? (() => displayNone=false)() : setTimeout(() => displayNone=true, 500);
</script>


<!-- Chat Details Section -->
<div class="chat-details-section" class:hide={animateHideChatDetails && !displayChatDetails} class:d-none={displayNone}>
  <div class="main">

    <!-- Profile -->
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

    <!-- Content -->
    <div class="content">
  
      <div class="section px-4 pb-2 mb-3">
        <div class="img-wrapper img-1-1">
          <img class="rounded-circle p-4" src={currentChat.icon} alt="">
        </div>
        <div class="d-flex flex-row justify-content-center">
          <span class="chat-name fs-5 user-select-none">{currentChat.name}</span>
        </div>
      </div>
  
      <div class="section mb-3">
        <!-- encrypted? -->
        <ChatSettings icon={"lock"} name="Encryption" on:click>
          {"Messages in this chat are end-to-end encrypted. Click to learn more."}
        </ChatSettings>
        <!-- disappearing messages settings -->
        <ChatSettings icon="stopwatch" name="Disappearing Messages" on:click>
          {"Off"}
        </ChatSettings>
      </div>
      
      <div class="section mb-3">
        <!-- Direct -->
        <!-- {#each getGroupsInCommon() as groups}
          ...
        {/each} -->
        <!-- groups in common -->
        <!-- Group -->
        <!-- participants -->
      </div>
  
      <div class="section mb-3">
        <!-- Direct -->
        <!-- block, delete -->
        <ChatSettings icon="ban" name="Block" red on:click/>
        <ChatSettings icon="trash" name="Delete chat" red on:click/>
        <!-- Group -->
        <ChatSettings icon="arrow-right-from-bracket" name="Exit Group" red on:click/>
        <!-- exit -->
      </div>
  
    </div>

  </div>
</div>


<style>
.chat-details-section {
  width: var(--side-bar-length);
  background-color: var(--white);
  overflow-x: hidden;
  -webkit-animation-name: display-chat-details;
  -webkit-animation-duration: 0.5s;
  animation-name: display-chat-details;
  animation-duration: 0.5s;
}

.chat-details-section.hide {
  width: 0;
  overflow-x: hidden;
  -webkit-animation-name: display-none;
  -webkit-animation-duration: 0.5s;
  animation-name: display-none;
  animation-duration: 0.5s;
}

.main {
  width: var(--side-bar-length);
}

.chat-profile {
  height: var(--top-bar-height);
  background-color: var(--primary);
  color: var(--white);
}

.section {
  background-color: var(--white);
  box-shadow: 0 2px 2px var(--grey-shadow);
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
  overflow-y: scroll;
  background-color: var(--grey);
}


/* Animations */
@-webkit-keyframes display-chat-details {
  from {
    width: 0;
  }
  to {
    width: var(--side-bar-length);
  }
}

@keyframes display-chat-details {
  from {
    width: 0;
  }
  to{
    width: var(--side-bar-length);
  }
}

@-webkit-keyframes display-none {
  from {
    width: var(--side-bar-length);
  }
  to {
    width: 0;
  }
}

@keyframes display-none {
  from {
    width: var(--side-bar-length);
  }
  to {
    width: 0;
  }
}
</style>
