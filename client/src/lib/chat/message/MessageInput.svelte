<script>
import { createEventDispatcher } from "svelte";
import Dropzone from "dropzone";


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

Dropzone.options.uploadForm = {
  // configurations
  url: "/api/upload",
  method: "post",
  clickable: "#dropZone",
  autoProcessQueue: false,
  maxFiles: 1,
  maxFilesize: 100000000 /* 100MB */,
  acceptedFiles: ".avi, .mp3, .mp4, .gif, .jpeg, .jpg, .png, .pdf, .pptx, .sldm, .xlsm, .rar, .txt, .zip",

  chunking: true,
  chunkSize: 1000000 /* 1MB */,
  retryChunks: true,
  retryChunksLimit: 3,

  createdImageThumbnails: true,
  maxThumbnailsize: 10,
  thumbnailWidth: 120,
  thumbnailHeight: 120,
  thumbnailMethod: "contain",

  init:function() {
    const dz = this;

    // Add the file to the queue when the user selects a file
    this.createElement.querySelector("button[type=submit]").addEventListener("click", function(e) {
      e.preventDefault();
      e.stopPropagation();
      dz.processQueue();
    });

    // Send the file to the server
    this.on("sending", function(file, xhr, formData) {
      formData.append("data", file);
    });

    this.on("success", function(file, response) {
      dispatch("message", response);
    });
  }
}
</script>


<!-- Texting Input Section -->
<div class="container input-area">
  <form id="upload-form" class="row justify-content-center align-items-center dropzone h-100" on:submit|preventDefault={onSend}>
    <!-- Dropzone preview -->
    <div class="previews"></div>

    <!-- Attachments Input -->
    <div class="col-1" id="dropZone">
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
  max-width: calc(100vw - var(--left-bar-length));
  background-color: var(--grey);
  border-left: 0.1rem solid var(--grey-shadow);
}

.icon {
  height: 1.5rem;
  max-width: 100%;
}
</style>
