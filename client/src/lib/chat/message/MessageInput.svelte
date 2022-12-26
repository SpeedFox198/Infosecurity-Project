<script>
import { createEventDispatcher } from "svelte";
import FilePond, { registerPlugin } from 'svelte-filepond';
import FilePondPluginImageExifOrientation from 'filepond-plugin-image-exif-orientation';
import FilePondPluginImagePreview from 'filepond-plugin-image-preview';
import 'filepond/dist/filepond.css';

const dispatch = createEventDispatcher();

// Register the plugins
registerPlugin(FilePondPluginImageExifOrientation, 
FilePondPluginImagePreview);

let filePondDisplay = false;

// get a file input reference
const input = document.querySelector('import[type="file"]');

const toggleFilePondOn = () => {
  filePondDisplay = !filePondDisplay;
}

// a reference to the component, used to call FilePond methods
let pond;
// name to use for the internal file input
let name = 'filepond';

let attachmentInput;
let content = "";

// handling filepond events
function handleinit() {
  console.log('FilePond instance has initialised');
}

function handleAddfile(err, fileItem) {
  console.log('A file has been added', fileItem);
}

async function onSend(event) {
  if (content) {
    dispatch("message", content);
    content = "";
  }
}

</script>


<!-- Texting Input Section -->
{#if (filePondDisplay)}
<div class="container">
  <FilePond bind:this={pond} {name}
        server="/upload"
        allowMultiple={true}
        oninit={handleinit}
        onaddfile={handleAddfile}/>
</div>
{/if}
<div class="container input-area">
  <form class="row justify-content-center align-items-center h-100" on:submit|preventDefault={onSend}>

    <!-- Attachments Input -->
    
    <div class="col-1" >
      <button class="btn" type="button" on:click={toggleFilePondOn}>
        <img class="icon" src="/icons/paperclip.svg" alt="AttachFile">
      </button>
      
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

/**
 * FilePond Custom Styles
 */
.filepond--drop-label {
	color: #4c4e53;
}

.filepond--label-action {
	text-decoration-color: #babdc0;
}

.filepond--panel-root {
	border-radius: 2em;
	background-color: #edf0f4;
	height: 1em;
}

.filepond--item-panel {
	background-color: #595e68;
}

.filepond--drip-blob {
	background-color: #7f8a9a;
}

</style>