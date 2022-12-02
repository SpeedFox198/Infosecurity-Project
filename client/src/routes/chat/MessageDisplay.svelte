<script>
export let allMsgs;
</script>


<!-- Messages Display Section -->
<div class="chat">
  <div class="my-2"></div>
  {#each allMsgs as msg}
    <div class="message d-flex {!msg.received ? "sent": ""}">
      <div class="info-section m{msg.received ? "e": "s"}-2">
        <img class="rounded-circle" src={msg.avatar} alt={msg.username}>
        <span class="time">{msg.time}</span>
      </div>
      <div class="bubble">
        {#if msg.received}
          <div class="username">{msg.username}</div>
        {/if}
        <div class="content text-wrap text-break">
          {msg.content}
        </div>
      </div>
    </div>
  {/each}
  <div id="anchor"></div>
</div>


<style>
.chat {
  height: calc(100vh - 8rem);
  overflow-y: scroll;
  border-left: 0.1rem solid var(--grey);
}

.chat * {
  overflow-anchor: none;
}

.message {
  padding: 0 3rem;
  margin-bottom: 0.5rem;
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

#anchor {
  overflow-anchor: auto;
  height: 1rem;
}

.sent {
  flex-direction: row-reverse;
}
</style>
