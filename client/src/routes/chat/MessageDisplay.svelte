<script>
export let allMsgs;
</script>


<!-- Messages Display Section -->
<div class="chat">
  {#each allMsgs as msg}
    <div class="message">
      <div class="avatar">
        <img src={msg.avatar} alt={msg.username}>
      </div>
      <div class="container px-5">
        <div class="name">{msg.username}</div>
        <div class="bubble">
            <div class="content">
              <!-- {msg.content} --> {msg}
            </div>
            <div class="time">{msg.username}</div>
        </div>
      </div>
    </div>
  {/each}
</div>


<style>
.chat {
  height: calc(100vh - 8rem);
  overflow-y: auto;
}

.bubble {
  padding: 0.5rem 0.6rem 0.7rem 0.8rem;
  background-color: var(--grey);
  border-radius: 1rem;
}
</style>
