<script>
import { createEventDispatcher } from "svelte";
import FilePond, { registerPlugin } from "svelte-filepond";
import FilePondPluginImageExifOrientation from 'filepond-plugin-image-exif-orientation';
import FilePondPluginImagePreview from 'filepond-plugin-image-preview';
import FilePondPluginFileValidateSize from 'filepond-plugin-file-validate-size';
import FilePondPluginFileValidateType from 'filepond-plugin-file-validate-type';
import 'filepond/dist/filepond.css';
import 'filepond-plugin-image-preview/dist/filepond-plugin-image-preview.css';

const dispatch = createEventDispatcher();

// Register the plugins
registerPlugin(
  FilePondPluginImageExifOrientation,
  FilePondPluginImagePreview,
  FilePondPluginFileValidateSize,
  FilePondPluginFileValidateType
);

let filePondDisplay = false;

const toggleFilePondOn = () => {
  filePondDisplay = !filePondDisplay;
}

// a reference to the component, used to call FilePond methods
let pond;

// name to use for the internal file input
const name = "filepond";

let content = "";

// handling filepond events
function handleinit() {
  console.log('FilePond instance has initialised');
}

function handleAddfile(err, fileItem) {
  console.log('A file has been added', fileItem);
  console.log('A file has been added', fileItem.file);
}

function getFileType(file) {
  if (file.type.match("image.*"))
    return "image";

  if (file.type.match("video.*"))
    return "video";

  return "document";
}

async function onSend(event) {
  let file;

  // If file pond is opened, check for file to upload
  if (pond) {
    const fileItem = pond.getFile();
    if (fileItem) {
      ({ file } = fileItem);
      pond.removeFile();
      toggleFilePondOn();
    }
  }

  // Get the message type
  let type;
  if (file) {
    type = getFileType(file);
  } else {
    type = "text";
  }

  // Dispatch message if there is something to send
  if (content || file) {
    dispatch("message", { content, file, type });
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
        allowMultiple={false}
        oninit={handleinit}
        onaddfile={handleAddfile}
        instantUpload={false}
        
        allowFileSizeValidation={true}
        maxFileSize="5MB"
        maxTotalFileSize="10MB"
        labelMaxFileSizeExceeded="File is too large"
        labelMaxTotalFileSizeExceeded="Total file size is too large"

        allowFileTypeValidation={true}
        acceptedFileTypes={['image/*', 'video/*', 'audio/*', 'application/pdf', 'text/*']}
        labelFileTypeNotAllowed="File type is not allowed"
        fileValidateTypeLabelExpectedTypes="Expects image/*, video/*, audio/*, application/pdf, text/* files"
        fileValidateTypeLabelExpectedTypesMap={null}

        allowImagePreview={true}
        imagePreviewMinHeight={50}
        imagePreviewMaxHeight={200}

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