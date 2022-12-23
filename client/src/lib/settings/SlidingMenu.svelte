<script>
export let display;
export let right;
export let title;
</script>

<!--
  Template for sliding menu
  Set right to true for animation sliding in from right
  Place contents of menu in slot
-->
<div class="settings-section" class:display class:right>
  <div class="section-title d-flex flex-row align-items-center p-2">
    <div class="d-flex">
      <button class="back d-flex align-items-center" type="button" disabled={!display} on:click>
        <!-- TODO(UI)(SpeedFox198): rounded-circle, onhover ?? -->
        <i class="fa-solid fa-arrow-left fs-5"></i>
      </button>
    </div>
    <div class="d-flex">
      <div class="ms-4 fs-5 fw-bold user-select-none">{title}</div>
    </div>
  </div>
  <div class="content">
    <!-- Put settings content here -->
    <!-- TODO(UI)(SpeedFox198): remove default values when unused -->
    <slot>Nothing here yet</slot>
  </div>
</div>


<style>
.settings-section {
  visibility: hidden;
  height: 100%;
  width: 100%;
  position: absolute;
  left: -100%;
  right: initial;
  z-index: 1;
  background-color: var(--primary-light);
  overflow-x: hidden;
  transition: 0.15s;
}

.display {
  visibility: visible;
  left: 0;
}

.right {
  left: initial;
  right: -100%;
}

.right.display {
  left: initial;
  right: 0;
}

.section-title {
  height: 4rem;
  background-color: var(--primary);
  color: var(--white);
}

.back {
  background-color: inherit;
  border: 0;
  color: var(--grey);
}

.content {
  height: calc(100vh - 4rem);
  overflow-y: auto;
}
</style>
