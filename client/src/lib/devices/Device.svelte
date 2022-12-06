<script>
    export let device
    export let current_device_id
    
    let time = new Date(device.time * 1000).toLocaleString("en-SG") // JS uses milliseconds instead of seconds

</script>

<div class="rounded border device-box p-3 mb-3 w-25 flex-row d-flex">
  <div class="flex-column d-flex flex-grow-1">
    {#if (current_device_id === device.id)}
      <span class="fw-bold fs-4 pb-2">Current device</span>
    {/if}
    <div class="py-2">
      <span>
        {time}
      </span>
    </div>
    <div class="py-2">
      <span>
        {device.browser}, {device.os}
      </span>
    </div>
    <div class="py-2">
      <span>Location: {device.location}</span>
    </div>
  </div>
  <div class="d-flex justify-content-center">
    <button class="btn" title="Remove device">
      <i class="fa-solid fa-xmark fs-1"></i>
    </button>
  </div>
</div>

<style>
  .device-box {
    background-color: var(--grey);
  }
</style>