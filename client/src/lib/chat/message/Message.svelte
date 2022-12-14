<script>
import { afterUpdate, beforeUpdate } from "svelte";
import { selectMode } from "$lib/stores/select";


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
  on:click={selectMsg} on:keydown
>
  {#if $selectMode}
    <i class="check fa-{selected ? "solid" : "regular"} fa-circle{selected ? "-check" : ""}"></i>
  {/if}

  <div class="info-section m{msg.sent ? "s" : "e"}-2">
    {#if msg.avatar}
      <img class="rounded-circle" src={msg.avatar} alt="{msg.username}">
    {/if}
  </div>

  <div class="bubble-container d-flex justify-content-end flex-shrink-1">

    <div class="tail"></div>

    <div class="bubble">

      {#if !$selectMode}
        <button class="options" type="button" on:click={selectOption}><i class="fa-solid fa-ellipsis"></i></button>
      {/if}

      {#if !msg.sent && msg.avatar}
        <div class="username">{msg.username}</div>
      {/if}
      <span class="text-wrap text-break">
        {msg.content}
      </span>
      <span class="hidden" aria-hidden="true">{time}</span>
      <span class="time d-block">{time}</span>
    </div>

  </div>

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

.selecting:hover {
  cursor: pointer;
  background-color: var(--highlight-primary);
}

.corner {
  padding-bottom: 0.2rem;
  margin-bottom: 0.6rem;
}

.username {
  font-weight: bold;
  font-size: 0.85rem;
}

.bubble-container {
  max-width: 75%;
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
  background-color: var(--grey);
  text-align: left;
  padding: 0.5rem 0.6rem 0.65rem 0.8rem;
  border-radius: 0 1.1rem 1.1rem 0.7rem;
}

.sent .bubble {
  border-radius: 1.1rem 0 0.7rem 1.1rem;
  background-color: var(--primary);
  padding: 0.5rem 0.8rem 0.65rem 0.6rem;
  color: var(--white);
}

.consecutive .bubble {
  border-top-left-radius: 0.7rem;
}

.sent.consecutive .bubble {
  border-top-left-radius: 1.1rem;
  border-top-right-radius: 0.7rem;
}

.corner .bubble {
  border-bottom-left-radius: 1.1rem;
}

.sent.corner .bubble {
  border-bottom-right-radius: 1.1rem;
}

.tail {
  width: 0;
  height: 0;
  border-bottom: 10px solid transparent;
  border-right: 10px solid var(--grey);
  color: var(--grey);
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
  color: var(--grey);
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

.bubble:hover .options, .tail:hover ~ .bubble .options {
  display: block;
}

.check {
  color: var(--primary);
}
</style>
