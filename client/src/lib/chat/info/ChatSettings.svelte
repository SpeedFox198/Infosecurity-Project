<script>
export let icon;
export let name;
export let red;
export let good;
export let bad;
export let arrow;
if (!red) red = false;
if (!good) good = false;
if (!bad) bad = false;
if (!arrow) arrow = false;
</script>


<div
  class="option d-flex flex-column user-select-none p-3"
  class:red
  class:good
  class:bad
  on:click
  on:keydown>

  <div class="d-flex flex-row">
    <div class="icon d-flex align-items-center justify-content-center">
      <i class="fa-solid fa-{icon} fs-5"></i>
    </div>
    <div class="d-flex align-items-center">
      <span class="fs-5">{name}</span>
    </div>
    {#if arrow}
      <div class="icon d-flex align-items-center justify-content-center">
        <i class="fa-solid fa-angle-right fs-5"></i>
      </div>
    {/if}
  </div>
  <div class="text">
    <slot />
  </div>
</div>


<style>
:root {
  --icon-width: 4rem;
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

.red, .red .icon, .red .text {
  color: var(--red);
}

.good, .good .icon, .good .text {
  color: var(--primary);
}

.bad, .bad .icon, .bad .text {
  color: var(--orange);
}
</style>
