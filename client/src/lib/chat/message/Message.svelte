<script>
import { beforeUpdate } from "svelte";

export let msg;

beforeUpdate(() => msg = msg || {})

const padZero = t => t < 10 ? "0" + t : t;

const t = new Date(msg.time * 1000);
let hours = t.getHours();
let ampm = hours >= 12 ? "PM" : "AM";
hours = hours % 12;
hours = hours ? hours : 12;

// const time = `${padZero(t.getDate())}/${padZero(t.getMonth())}/${t.getFullYear()} ${hours}:${padZero(t.getMinutes())} ${ampm}`;
const time = `${hours}:${padZero(t.getMinutes())} ${ampm}`;
</script>

<!-- Messages Bubble -->
<div class="message d-flex {msg.sent ? "sent" : ""}">
  <div class="info-section m{msg.sent ? "s" : "e"}-2">
    <img class="rounded-circle" src={msg.avatar} alt="User Avatar">
  </div>
    <div class="bubble mt-auto">
      {#if !msg.sent} <!-- TODO(SpeedFox198): rmb to udpate this! -->
        <div class="username">{msg.username}</div>
      {/if}
      <span class="text-wrap text-break">
        {msg.content}
      </span>
      <span class="hidden" aria-hidden="true">{time}</span>
      <span class="time d-block">{time}</span>
    </div>
</div>


<style>
.message {
  padding: 0 3rem;
  margin-bottom: 0.5rem;
  overflow-anchor: none;
}

.username {
  font-weight: bold;
  font-size: 0.85rem;
}

.bubble {
  max-width: 75%;
  padding: 0.5rem 0.6rem 0.65rem 0.8rem;
  background-color: var(--grey);
  border-radius: 1.1rem;
  text-align: left;
}

.sent .bubble {
  background-color: var(--primary);
  padding: 0.5rem 0.7rem 0.65rem 0.6rem;
  color: var(--white);
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

.sent {
  flex-direction: row-reverse;
}

span {
  vertical-align: top;
}
</style>
