<script>
import { createEventDispatcher } from "svelte";


const dispatch = createEventDispatcher();
let attachmentInput;
let content = "";


async function onSend(event) {
  if (content) {
    dispatch("message", content);
    content = "";
  }
}

async function attachFile(event) {
  // Click the attachment input to prompt users to upload files
  attachmentInput.click();
}

</script>


<!-- Texting Input Section -->
<div class="container input-area">
  <form class="row justify-content-center align-items-center h-100" on:submit|preventDefault={onSend}>

    <!-- Attachments Input -->
    <div class="col-1">
      <button class="btn" type="button" on:click={attachFile}>
        <img class="icon" src="/icons/paperclip.svg" alt="AttachFile">
      </button>
      <input type="file" class="d-none" bind:this={attachmentInput}>
    </div>

    <!-- Text Input -->
    <div class="col-10">
      <input class="form-control" type="text" name="data" bind:value={content}>
    </div>

    <!-- Submit Button -->
    <div class="col-1">
      <button class="btn" type="submit">
        <img class="icon" src="/icons/plane.svg" alt="Send">
      </button>
    </div>
  </form>
</div>


<style>
.input-area {
  position: absolute;
  bottom: 0;
  height: 4rem;
  max-width: calc(100vw - 25rem);
  background-color: var(--grey);
}

.icon {
  height: 1.5rem;
  max-width: 100%;
}
</style>
