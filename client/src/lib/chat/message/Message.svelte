<script>
import { beforeUpdate } from "svelte";
import { selectMode } from "$lib/stores/select";

export let blocked;
export let msg;
export let selected;
export let select;

// When msg is undefined, set it to empty object
beforeUpdate(() => msg = msg || {});


// Formating timestamp
const padZero = t => t < 10 ? "0" + t : t;

const t = new Date(msg.time * 1000);
let hours = t.getHours();
let ampm = hours < 12 ? "AM" : "PM";  // Display AM/PM
hours = hours % 12;
hours = hours ? hours : 12;

const time = `${hours}:${padZero(t.getMinutes())} ${ampm}`;


// Selecting message logic
let clicked = false;
function selectOption() {
  clicked = true;
  if (!$selectMode) select();
}
function selectMsg() {
  if ($selectMode && !clicked) select();
  clicked = false;
}
</script>


<!-- Messages Bubble -->
<div
  class="message d-flex"
  class:sent={msg.sent}
  class:selecting={$selectMode}
  class:selected
  class:consecutive={!msg.avatar}
  class:corner={msg.corner}
  class:not-blocked={!blocked}
  on:click={selectMsg} on:keydown
>
  {#if $selectMode}
    <i class="check fa-{selected ? "solid" : "regular"} fa-circle{selected ? "-check" : ""}"></i>
  {/if}

  <div class="info-section m{msg.sent ? "s" : "e"}-2">
    {#if msg.avatar}
      <img class="rounded-circle" src={msg.avatar} alt={msg.username}>
    {/if}
  </div>

  <div class="bubble-container d-flex justify-content-end flex-shrink-1">
    <div class="tail"></div>
    <div class="bubble">

      {#if !$selectMode}
        <button class="options" type="button" on:click={selectOption}>
          <i class="fa-solid fa-ellipsis"></i>
        </button>
      {/if}

      {#if !msg.sent && msg.avatar}
        <div class="username">{msg.username}</div>
      {/if}

      {#if msg.type === "image"}
        <div class="image-container img-wrapper" style="height: {msg.height}px; width: {msg.width}px;">
          <img src={msg.path} alt="" on:load={() => URL.revokeObjectURL((this || {}).src)}>
        </div>
      {/if}

      {#if msg.type === "video"}
        <div class="video-container video-wrapper" style="height: {msg.height}px; width: {msg.width}px;">
          <video src={msg.path} controls>
            <track kind="captions">
            Your browser does not support embedded videos
          </video>
        </div>
      {/if}
        
      {#if msg.type === "document"}
        <div class="file-container file-wrapper">
          <i class="fa-solid fa-file"></i>
          <div class="file-info">
          </div>
        </div>
      {/if}

      <div class="content-container d-flex" class:blocked={msg.blocked}>
        <div class="flex-grow-1">
          <span class="text-wrap text-break">
            {msg.content}
          </span>
          <span class="hidden" aria-hidden="true">{time}</span>
          <span class="time d-block">{time}</span>
        </div>
      </div>
    </div>
  </div>
  {#if msg.malicious && !msg.sent}
    <div class="malware-message d-flex align-items-center">
      <div class="rounded-pill py-1 px-2 mx-3 user-select-none">
        <i class="fa-solid fa-circle-exclamation me-1"></i>
        We have detected malware in this message. Do not click links or open attachments if you are unsure they are safe.
      </div>
    </div>
  {/if}
</div>


<style>
.message {
  padding: 0 3rem;
  overflow-anchor: none;
}

.sent {
  flex-direction: row-reverse;
}

.selected {
  background-color: var(--highlight-primary);
}

.not-blocked.selecting:hover {
  cursor: pointer;
  background-color: var(--highlight-primary);
}

.corner {
  padding-bottom: 0.2rem;
  margin-bottom: 0.6rem;
}

.content-container.blocked span {
  color: var(--red);
  text-shadow:
    0 0 2px var(--red-light-background),
    0 0 2px var(--red-light-background),
    0 0 2px var(--red-light-background);
  font-weight: bold;
}

.username {
  font-weight: bold;
  font-size: 0.85rem;
}

.bubble-container {
  max-width: 35rem;
  margin-top: 0.4rem;
  margin-bottom: 0.07rem;
}

.consecutive .bubble-container {
  margin-top: 0.07rem;
}

.sent .bubble-container {
  flex-direction: row-reverse;
}

.bubble {
  background-color: var(--white);
  text-align: left;
  padding: 0.5rem 0.6rem 0.65rem 0.8rem;
  border-radius: 0 1.3rem 1.3rem 0.7rem;
}

.sent .bubble {
  border-radius: 1.3rem 0 0.7rem 1.3rem;
  background-color: var(--primary);
  padding: 0.5rem 0.8rem 0.65rem 0.6rem;
  color: var(--white);
}

.consecutive .bubble {
  border-top-left-radius: 0.7rem;
}

.sent.consecutive .bubble {
  border-top-left-radius: 1.3rem;
  border-top-right-radius: 0.7rem;
}

.corner .bubble {
  border-bottom-left-radius: 1.3rem;
}

.sent.corner .bubble {
  border-bottom-right-radius: 1.3rem;
}

.tail {
  width: 0;
  height: 0;
  border-bottom: 10px solid transparent;
  border-right: 10px solid var(--white);
  color: var(--white);
}

.sent .tail {
  border-right: 0;
  border-left: 10px solid var(--primary);
  color: var(--primary);
}

.consecutive .tail {
  visibility: hidden;
}

.info-section {
  width: 3rem;
}

.time {
  font-size: 0.65rem;
  position: relative;
  float: right;
  margin: 0.8rem 0 -3rem -3rem;
  z-index: 10;
  color: var(--grey-dark);
}

.sent .time {
  color: var(--white);
}

.hidden {
  font-size: 0.68rem;
  visibility: hidden;
}

span {
  vertical-align: top;
}

.options {
  display: none;
  position: relative;
  float: right;
  padding: 0;
  margin: -0.3rem 0 -1rem -1rem;
  z-index: 10;
  height: 0;
  border: 0;
  color: var(--grey-dark);
}

.sent .options {
  color: var(--grey);
}

.options > i {
  border-radius: 0 100%;
  background-color: var(--white);
  box-shadow: -4px 0px 0px 5px var(--white), 4px 0px 0px 5px var(--white);
}

.sent .options > i {
  border-radius: 0 100%;
  background-color: var(--primary);
  box-shadow: -4px 0px 0px 5px var(--primary), 4px 0px 0px 5px var(--primary);
}


.not-blocked .bubble:hover .options, .not-blocked .tail:hover ~ .bubble .options {
  display: block;
}

.check {
  color: var(--primary);
  align-self: center;
  margin: 0 0.5rem;
  font-size: 20px;
}

.image-container ~ .content-container > div {
  width: 0;
}

.image-container {
  border-radius: 1rem;
  margin: -0.2rem -0.3rem 0 -0.5rem;
}

.sent .image-container {
  margin: -0.2rem -0.5rem 0 -0.3rem;
}

img {
  border-radius: 1rem;
  background-color: var(--white);
}

.malware-message {
  font-size: 0.9rem;
}

.malware-message > div {
  background-color: var(--red-light-background);
  color: var(--red);
  border: 1.5px solid var(--red);
}
</style>
