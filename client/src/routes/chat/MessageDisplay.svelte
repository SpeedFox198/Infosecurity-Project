<script>
export let allMsgs = [];
</script>


<!-- Messages Display Section -->
<div class="chat">
  <ul>
    {#each allMsgs as msg}
      <li>
        <span>{msg}</span>
      </li>
      <div class="message">
        <div class="message-avatar">
          <img src={msg.avatar} alt={msg.username}>
        </div>
        <div class="name">{msg.username}</div>
        <div class="message-bubble">
          <div class="message-content">
            {msg.content}
          </div>
          <div class="message-time">{msg.username}</div>
        </div>
      </div>
    {/each}
  </ul>
</div>


<style>
ul {
  overflow-y: auto;
  list-style: none;
}
</style>
