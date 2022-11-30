<script>
export let allMsgs;
</script>

<!-- Messages Display Section -->
<div class="chat flex-grow-1">
  <ul>
    {#each allMsgs as msg}
      <li>
        <span>{msg}</span>
      </li>
    {/each}
  </ul>
</div>

<style>
  ul {
    list-style: none;
  }
</style>
