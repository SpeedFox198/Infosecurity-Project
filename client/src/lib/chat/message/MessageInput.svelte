<script>
import { createEventDispatcher } from "svelte";
import FilePond, { registerPlugin } from 'svelte-filepond';
import FilePondPluginImageExifOrientation from 'filepond-plugin-image-exif-orientation';
import FilePondPluginImagePreview from 'filepond-plugin-image-preview';
import FilePondPluginFileValidateSize from 'filepond-plugin-file-validate-size';
import FilePondPluginFileValidateType from 'filepond-plugin-file-validate-type';
import 'filepond/dist/filepond.css';

const dispatch = createEventDispatcher();

// Register the plugins
registerPlugin(
  FilePondPluginImageExifOrientation
, FilePondPluginImagePreview
, FilePondPluginFileValidateSize
, FilePondPluginFileValidateType
);

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
<div class="card filepond-card">
  <div class="filePond">
  <FilePond 
        bind:this={pond} {name}
        server="/upload"
        allowMultiple={false}
        oninit={handleinit}
        onaddfile={handleAddfile}
        
        allowFileSizeValidation={true}
        maxFileSize="5MB"
        maxTotalFileSize="10MB"
        labelMaxFileSizeExceeded="File is too large"
        labelMaxTotalFileSizeExceeded="Total file size is too large"

        allowFileTypeValidation={true}
        acceptedFileTypes={['image/*', 'video/*', 'audio/*', 'application/pdf', 'text/*']}
        labelFileTypeNotAllowed="File type is not allowed"
        fileValidateTypeLabelExpectedTypes="Expects image/*, video/*, audio/* files"
        fileValidateTypeLabelExpectedTypesMap={null}

        allowImagePreview={true}
        imagePreviewMinHeight={50}
        imagePreviewMaxHeight={120}

        allowImageExifOrientation={true}
        />
  </div>
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
  z-index: 30;
  bottom: 0;
  height: var(--bottom-bar-height);
  max-width: calc(100vw - var(--side-bar-length));
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

.filepond-card {
  position: absolute;
  width: 20em;
  bottom: 4em;
  z-index: 20;

  animation-name: slidein;
  animation-duration: 1s;
  animation-fill-mode: forwards;

}

@keyframes slidein {
  from {
    transform: translateY(100%);
  }

  to {
    transform: translateY(0%);
  }
}
</style>