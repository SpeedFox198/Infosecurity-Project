<script>
export let name;
</script>


<!-- Blocking state input section display -->
<div class="d-flex flex-container w-100 input-area">
  <div class="d-flex flex-row justify-content-center align-items-center h-100 w-100">

    <!-- Message Area -->
    <div class="d-flex flex-grow-1 mx-4 justify-content-center">
      <span>Cannot send messages to blocked user <strong>{name}</strong></span>
    </div>

  </div>
</div>


<style>
.input-area {
  position: absolute;
  bottom: 0;
  height: var(--bottom-bar-height);
  background-color: var(--grey);
  border-left: 0.1rem solid var(--grey-shadow);
}

strong {
  color: var(--primary);
}
</style>
