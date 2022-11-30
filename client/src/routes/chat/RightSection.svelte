<script>
import MessageDisplay from "./MessageDisplay.svelte";
import { onMount } from "svelte";
import { io } from "socket.io-client";

const namespace = "localhost:5000";
const transports = {transports: ["websocket"]}
let attachmentInput;
let content = "";
let allMsgs = [];
let socket;

onMount(async () => {
  // SocketIO instance
  socket = io(namespace, transports);

  socket.on("connect", () => {
    socket.emit("test", {data: "connected to the SocketServer..."});
  })

  socket.on("response", (msg, cb) => {
    allMsgs.push("from socketio server: " + msg.data);
    allMsgs = allMsgs;
    if (cb) cb();
  });
});

async function sendMsg(event) {
  socket.emit("test", {data: content});
  allMsgs.push("Sent via socketio: " + content);
  allMsgs = allMsgs;
  content = "";
}

async function attachFile(event) {
  // Click the attachment input to prompt users to upload files
  attachmentInput.click();
}
</script>


<!-- Right Section -->
<div class="d-flex flex-column flex-grow-1 right-section">

  <!-- Room Info Section -->
  <div class="d-flex top-right">

  </div>

  <div class="d-flex flex-column bottom-right">

    <!-- Messages Display Section -->
    <MessageDisplay allMsgs={allMsgs}/>

    <!-- Texting Input Section -->
    <div class="container input-area">
      <form class="row justify-content-center align-items-center h-100" on:submit|preventDefault={sendMsg}>

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
    