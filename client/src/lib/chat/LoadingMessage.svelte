<script>
  import { ocrStatus } from "$lib/stores/ocr.js"
  
  export let runId
  
  $: progress = $ocrStatus.get(runId)
</script>

<div class="message d-flex sent corner">
  <div class="info-section me-2"></div>
  <div class="bubble-container d-flex justify-content-end flex-shrink-1">
    <div class="d-none tail"></div>
    <div class="bubble">
      Sending... This may take a while we are making sure your message is safe to send.
      <div class="progress">
        <div class="progress-bar bar-bg" role="progressbar" style="width: { progress }%" aria-valuenow={ progress } aria-valuemin="0" aria-valuemax="100">
          { progress }%
        </div>
      </div>
    </div>
  </div>
</div>

<style>
  .message {
    padding: 0 3rem;
    overflow-anchor: none;
  }
  
  .info-section {
    width: 3rem;
  }

  .sent {
    flex-direction: row-reverse;
  }
  .corner {
    padding-bottom: 0.2rem;
    margin-bottom: 0.6rem;
  }

  .bubble-container {
    max-width: 35rem;
    margin-top: 0.4rem;
    flex-direction: row-reverse;
  }
  
  .sent .bubble {
    border-radius: 1.3rem 0 0.7rem 1.3rem;
    padding: 0.5rem 0.8rem 0.65rem 0.6rem;
    background-color: var(--white);
  }

  .tail {
    width: 0;
    height: 0;
    border-bottom: 10px solid transparent;
    border-right: 10px solid var(--white);
    color: var(--white);
  }

  .sent .tail {
    border-right: 0;
    border-left: 10px solid var(--white);
  }

  .sent.corner .bubble {
    border-bottom-right-radius: 1.3rem;
  }
 
  .bar-bg {
    background-color: #98fb98;
  }
</style>
