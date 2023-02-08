<script>
import { onMount } from "svelte";
import { getFlash } from "sveltekit-flash-message/client"
import { room_id, roomStorage } from "$lib/stores/room";
import { selectedMsgs } from "$lib/stores/select";
import { page } from "$app/stores"
import ChatSettings from "./ChatSettings.svelte";
import RightSlidingMenu from "./RightSlidingMenu.svelte";


export let socket;
export let encryption;
export let displayChatDetails;
export let closeChatDetails;
export let animateHideChatDetails;

const flash = getFlash(page);

const disappearingText = {
  "off": "Off",
  "5s": "5 seconds",
  "15s": "15 seconds",
  "24h": "24 hours",
  "7d": "7 days",
  "30d": "30 days"
};

let disappearing;
let displayNone = true;
let _displayDisappearing = false;
let _displayVerifyCode = false;
let securityCode = [];

$: currentChat = $roomStorage?.[$room_id] || {};
$: displayChatDetails ? (() => displayNone = false)() : setTimeout(() => displayNone = true, 150);
$: hide = animateHideChatDetails && !displayChatDetails;
$: displayDisappearing = _displayDisappearing && displayChatDetails;
$: displayVerifyCode = _displayVerifyCode && displayChatDetails && getSecurityCode();
$: !currentChat.encrypted && (() => _displayVerifyCode = false)();


const setDisappearing = () => socket.emit("set_disappearing", { disappearing, room_id: $room_id });
const blockUser = () => socket.emit("block_user", { block_id: currentChat.user_id, room_id: $room_id });
const unblockUser = () => socket.emit("unblock_user", { block_id: currentChat.user_id, room_id: $room_id });

async function getSecurityCode() {
  const rawCode = await encryption.generateSecurityCode($room_id);
  let temp, line;
  securityCode = [];
  for (let i=0; i<4; i++) {
    temp = rawCode.substring(i*16, (i*16)+16);
    line = [];
    for (let i=0; i<4; i++) {
      line.push(temp.substring(i*4, (i*4)+4))
    }
    securityCode.push(line);
  }
  return true;
}

function toggleDisappearing() {
  if (currentChat.blocked) {
    const action = currentChat.disappearing === "off" ? "on" : "off";
    const status = currentChat.blocked === "blocking" ? "this user is" : "you have been";
    $flash = { type: "failure", message: `You can't turn ${action} disappearing messages as ${status} blocked.` };
    return;
  }
  _displayDisappearing = !_displayDisappearing;
}

function toggleVerifyCode() {
  if (currentChat.encrypted) {
    _displayVerifyCode = !_displayVerifyCode;
  } else {
    // Do "Click to learn more" feature
  }
}

onMount(() => {
  socket.on("user_online", async data => roomStorage.updateOnlineStatus(data.user_id, true));
  socket.on("user_offline", async data => roomStorage.updateOnlineStatus(data.user_id, false));
});
</script>


<!-- Chat Details Section -->
<div class="chat-details-section" class:hide class:d-none={displayNone}>
  <div class="section-container">

    <!-- Section Header -->
    <div class="title d-flex flex-row align-items-center p-2">
      <div class="d-flex">
        <button
          class="back d-flex align-items-center justify-content-center rounded-circle"
          type="button" on:click={closeChatDetails}
        >
          <i class="fa-solid fa-times fs-5"></i>
        </button>
      </div>
      <div class="d-flex">
        <div class="ms-4 fs-5 fw-bold user-select-none">{currentChat.type === "direct" ? "User" : "Group"} Info</div>
      </div>
    </div>

    <!-- Content -->
    <div class="content">

      <div class="section px-4 pb-2 mb-3">
        <div class="img-wrapper img-1-1">
          <img
            class="rounded-circle p-4" alt=""
            src={
              currentChat.icon?.startsWith("media/") ?
              `https://localhost:8443/api/${currentChat.icon}` :
              currentChat.icon
            }
          >
        </div>
        <div class="d-flex flex-row justify-content-center">
          <span class="chat-name fs-5 user-select-none">{currentChat.name}</span>
        </div>
      </div>

      <div class="section mb-3">
        <ChatSettings
          icon={currentChat.encrypted ? "lock" : "unlock"}
          name="Encryption"
          green={currentChat.encrypted}
          orange={!currentChat.encrypted}
          on:click={toggleVerifyCode}
        >
          {#if currentChat.type === "group"}
            End-to-end encryption is not available for group chats yet. Click to learn more.
          {:else if currentChat.encrypted}
            Messages in this chat are end-to-end encrypted. Click to learn verify.
          {:else}
            End-to-end encryption is not enabled for this chat. Click to learn more.
          {/if}
        </ChatSettings>
        {#if currentChat.type === "direct" || currentChat.is_admin}
          <ChatSettings icon="stopwatch" name="Disappearing Messages" arrow on:click={toggleDisappearing}>
            {disappearingText[currentChat.disappearing]}
          </ChatSettings>
        {/if}
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
        {#if currentChat.type === "direct"}
          {#if currentChat.blocked === "blocking"}
            <ChatSettings icon="ban" name="Unblock {currentChat.name}" green on:click={unblockUser}/>
          {:else if currentChat.blocked === "blocked"}
            <ChatSettings icon="ban" name="You have been blocked by {currentChat.name}" red unclickable/>
          {:else}
            <ChatSettings icon="ban" name="Block {currentChat.name}" red on:click={()=>{blockUser();selectedMsgs.clear();}}/>
          {/if}
        {:else}
          {#if currentChat.is_admin}
            <ChatSettings icon="trash" name="Delete Group" red on:click={null}/>
          {:else}
            <ChatSettings icon="arrow-right-from-bracket" name="Exit Group" red on:click={null}/>
          {/if}
        {/if}
      </div>

    </div>

  </div>
</div>

<RightSlidingMenu
  title="Disappearing Messages"
  display={displayDisappearing}
  on:click={toggleDisappearing}
>
  <div class="d-flex flex-column p-4">
    <div class="mb-3 green">
      Enabling this feature makes messages in this chat disappear after the set amount of time.
    </div>
    <div class="mb-3">Anyone in the chat can change this setting.</div>
    <form on:submit|preventDefault={setDisappearing}>
      {#each [
        { value: "off", text: "Off" },
        { value: "5s", text: "5 seconds" },
        { value: "15s", text: "15 seconds" },
        { value: "24h", text: "24 hours" },
        { value: "7d", text: "7 days" },
        { value: "30d", text: "30 days" }
      ] as item}
        <div class="form-check">
          <input
          class="form-check-input" type="radio" name="disappearing" id="disappearing"
          value={item.value} checked={currentChat.disappearing === item.value}
          bind:group={disappearing}>
          <label class="form-check-label" for="disappearing">
            {item.text}
          </label>
        </div>
      {/each}
      <button
        type="submit" class="btn mb-3"
        disabled={disappearing === undefined || disappearing === currentChat.disappearing}
      >Set disappearing time</button>
    </form>
  </div>
</RightSlidingMenu>


<RightSlidingMenu
  title="Verify Security Code"
  display={displayVerifyCode}
  on:click={toggleVerifyCode}
>
  <div class="d-flex flex-column justify-content-center p-4">
    <div class="smaller-text user-select-none mb-4">
      Compare the number below with <strong class="green">{currentChat.name}</strong>
      to verify that messages sent in this chat are end-to-end encrypted:
    </div>
    <div class="text-center">
      {#each securityCode as a}
        <div class="space-a">
          {#each a as b}
            <span class="space-b">
              {#each b as c}
                <span class="space-c">{c}</span>
              {/each}
            </span>
          {/each}
        </div>
      {/each}
    </div>
  </div>
</RightSlidingMenu>


<style>
.chat-details-section {
  width: var(--side-bar-length);
  background-color: var(--white);
  overflow-x: hidden;
  -webkit-animation-name: display-chat-details;
  -webkit-animation-duration: 0.15s;
  animation-name: display-chat-details;
  animation-duration: 0.15s;
}

.chat-details-section.hide {
  width: 0;
  overflow-x: hidden;
  -webkit-animation-name: display-none;
  -webkit-animation-duration: 0.15s;
  animation-name: display-none;
  animation-duration: 0.15s;
}

.section-container {
  width: var(--side-bar-length);
}

.title {
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

.btn {
  background-color: var(--primary);
  color: var(--white);
}

.smaller-text {
  font-size: 90%;
}

.space-a {
  display: inline-block;
  margin: 0.1em auto;
}

.space-b {
  padding: 0 0.5em;
}

.space-c {
  padding: 0 0.1em;
}

.green {
  color: var(--primary);
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
