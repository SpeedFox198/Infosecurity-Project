<script>
  export let settingName
</script>

<div class="group d-flex p-2">
  <div class="d-flex align-items-center">
    <span class="px-3">{settingName}</span>
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