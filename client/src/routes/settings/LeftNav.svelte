<script>
	import SettingBlock from "$lib/settings/SettingBlock.svelte";

</script>

<div class="d-flex flex-column flex-shrink-0 sidebar">
  
  <!-- Chat List Section -->
  <div class="d-flex flex-column bottom-left">
    <SettingBlock settingName="Profile" />
    <SettingBlock settingName="Devices" />
    <SettingBlock settingName="Privacy" />
  </div>

</div>


<style>
.sidebar {
  width: var(--left-bar-length);
  background-color: var(--primary-light);
}

.top-left {
  /* position: absolute;
  top: 0; */
  height: 4rem;
  width: var(--left-bar-length);
  background-color: var(--primary);
}

.bottom-left {
  height: 100%;
  overflow-y: scroll;
}

::-webkit-scrollbar {
  width: 0.5rem;
}

::-webkit-scrollbar-track {
  background: var(--grey-shadow);
}

::-webkit-scrollbar-thumb {
  background: var(--primary);
  border-radius: 0.6rem;
}
</style>