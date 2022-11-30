<script>
import MessageDisplay from "./MessageDisplay.svelte";
import MessageInput from "./MessageInput.svelte";
let allMsgs;
</script>


<!-- Right Section -->
<div class="d-flex flex-column flex-grow-1 right-section">

  <!-- Room Info Section -->
  <div class="d-flex top-right">

  </div>

  <div class="d-flex flex-column bottom-right">

    <!-- Messages Display Section -->
    <MessageDisplay allMsgs={allMsgs}/>

    <!-- Messages Display Section -->
    <MessageInput/>


  </div>
</div>


<style>
.top-right {
  height: 4rem;
  border-top: 0.1rem solid var(--primary-shadow);
  border-right: 0.1rem solid var(--primary-shadow);
  background-color: var(--primary);
}

.bottom-right {
  height: 100%;
  border-right: 0.1rem solid var(--grey);
}

.input-area {
  height: 4rem;
  max-width: 100vw;
  background-color: var(--grey);
}

.icon {
  height: 1.5rem;
  max-width: 100%;
}
</style>
    