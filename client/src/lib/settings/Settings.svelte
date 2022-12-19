<script>
export let display;
export let toggleSettings;

let settingsSection;

let title = "Settings";

</script>


<div class="settings-section" class:display bind:this={settingsSection}>
  <div class="section-title d-flex flex-row align-items-center p-2">
    <div class="d-flex">
      <button class="back d-flex align-items-center" type="button" disabled={!display} on:click={toggleSettings}>
        <i class="fa-solid fa-arrow-left fs-5"></i>
      </button>
    </div>
    <div class="d-flex">
      <div class="ms-4 fs-5 fw-bold user-select-none">{title}</div>
    </div>
  </div>
  <div class="row">
    <!-- TODO(SpeedFox198): Continue from here, do the rows of settings options, make -->
    <!-- Later on make a component for it -->
  </div>
</div>


<style>
.settings-section {
  height: 100%;
  width: 0;
  position: absolute;
  z-index: 1;
  background-color: var(--primary-light);
  overflow-x: hidden;
  transition: 0.2s;
}


.display {
  width: 100%;
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
