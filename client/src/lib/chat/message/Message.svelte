<script>
export let msg;
export let sent;
</script>

<!-- Messages Bubble -->
<div class="message d-flex {sent ? "sent": ""}">
  <div class="info-section m{sent ? "s": "e"}-2">
    <img class="rounded-circle" src={msg.avatar} alt="User Avatar">
    <span class="time">{msg.time}</span>
  </div>
  <div class="bubble">
    <!-- {#if !sent} --> <!-- TODO(SpeedFox198): rmb to change this! -->
      <div class="username">{msg.username}</div>
    <!-- {/if} -->
    <div class="content text-wrap text-break">
      {msg.content}
    </div>
  </div>
</div>


<style>
.message {
  padding: 0 3rem;
  margin-bottom: 0.5rem;
  overflow-anchor: none;
}

.bubble {
  max-width: 75%;
  padding: 0.5rem 0.6rem 0.5rem 0.8rem;
  background-color: var(--grey);
  border-radius: 1rem;
}

.info-section {
  width: 3rem;
}

.time {
  font-size: 0.8rem;
  text-align: center;
  float: left;
  margin: 0rem 0.25rem -0.5rem;
}

.sent {
  flex-direction: row-reverse;
}

.sent .username {
  text-align: right;
}
</style>
