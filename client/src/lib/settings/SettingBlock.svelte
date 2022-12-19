<script>
  export let settingName
</script>

<div class="group d-flex py-2"
  on:keydown>
  <div class="d-flex align-items-center">
    <span>{settingName}</span>
  </div>
</div>

<style>
.group {
  border-bottom: 0.1rem solid var(--primary-light-shadow);
}

.group:hover {
  cursor: pointer;
  background-color: var(--primary-light-shadow);
}

</style>