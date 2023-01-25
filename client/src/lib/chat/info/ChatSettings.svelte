<script>
export let icon;
export let name;
export let red;
if (!red) red = false;
</script>


<div
  class="option d-flex flex-column user-select-none p-3"
  class:red
  on:click
  on:keydown>

  <div class="d-flex flex-row">
    <div class="icon d-flex align-items-center justify-content-center">
      <i class="fa-solid fa-{icon} fs-4"></i>
    </div>
    <div class="d-flex align-items-center">
      <span class="fs-5">{name}</span>
    </div>
  </div>
  <div class="text">
    <slot />
  </div>
</div>


<style>
:root {
  --icon-width: 4.5rem;
}

.option:hover {
  cursor: pointer;
  background-color: var(--grey-light);
}

.option:focus {
  background-color: var(--grey-light-shadow);
}

.icon {
  color: var(--grey-dark);
  width: var(--icon-width);
}

.text {
  color: var(--grey-dark);
  margin-left: var(--icon-width);
}

.red {
  color: var(--red);
}

.red .icon {
  color: var(--red);
}
</style>
