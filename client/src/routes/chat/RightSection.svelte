<script>
let content = "";
let allMsgs = [];
let attachmentInput;

async function attachFile(event) {
    // Click the attachment input to prompt users to upload files
    attachmentInput.click();
}

// Export variables for page to use
export { content, allMsgs };
</script>

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


<!-- Right Section -->
<div class="d-flex flex-column flex-grow-1 right-section">

    <!-- Room Info Section -->
    <div class="d-flex top-right">

    </div>

    <div class="d-flex flex-column bottom-right">

        <!-- Messages Display Section -->
        <div class="chat flex-grow-1">
            {#each allMsgs as msg}
                <li>
                    <span>{msg}</span>
                </li>
            {/each}
        </div>

        <!-- Texting Input Section -->
        <div class="container input-area">
            <form class="row justify-content-center align-items-center h-100" on:submit|preventDefault>

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
