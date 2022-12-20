<script>
export let display;
export let right;
export let title;
</script>


<div class="settings-section" class:display class:right>
  <div class="section-title d-flex flex-row align-items-center p-2">
    <div class="d-flex">
      <button class="back d-flex align-items-center" type="button" disabled={!display} on:click>
        <!-- TODO(SpeedFox198): rounded-circle, onhover ?? -->
        <i class="fa-solid fa-arrow-left fs-5"></i>
      </button>
    </div>
    <div class="d-flex">
      <div class="ms-4 fs-5 fw-bold user-select-none">{title}</div>
    </div>
  </div>
  <!-- Put settings content here -->
  <slot></slot>
</div>


<style>
.settings-section {
  height: 100%;
  width: 100%;
  left: -100%;
  right: initial;
  position: absolute;
  z-index: 1;
  background-color: var(--primary-light);
  overflow-x: hidden;
  transition: 0.2s;
}

.settings-section.right {
  left: initial;
  right: -100%;
  transition: 0.2s;
}

.display {
  left: 0 !important;
  right: 0 !important;
  transition: 0.2s;
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
</style>
