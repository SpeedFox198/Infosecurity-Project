<script>
import SlidingMenu from "$lib/settings/SlidingMenu.svelte";
import Option from "$lib/settings/Option.svelte";
import DevicesMenu from "../devices/DevicesMenu.svelte";
import { invalidate } from "$app/navigation"

export let displaySettings;
export let toggleSettings;

let displayGeneral = false;
let displaySecurity = false;
let displayDevices = false;

function toggleGeneral() {
  displayGeneral = !displayGeneral;
}

function toggleSecurity() {
  displaySecurity = !displaySecurity;
}

function toggleDevices() {
  displayDevices = !displayDevices;
}
</script>


<SlidingMenu title="Settings" display={displaySettings} on:click={toggleSettings} right={false}>
  <div class="">
    Profile things here...
  </div>
  <div class="d-flex flex-column">
    <Option name="General Settings" icon="gear" on:click={toggleGeneral}/>
    <Option name="Privacy and Security" icon="lock" on:click={toggleSecurity}/>
    <Option name="Devices" icon="desktop" on:click={toggleDevices}/>
  </div>
</SlidingMenu>


<SlidingMenu title="General Settings" display={displayGeneral} on:click={toggleGeneral} right={true}>
</SlidingMenu>


<SlidingMenu title="Privacy and Security" display={displaySecurity} on:click={toggleSecurity} right={true}>
</SlidingMenu>


<SlidingMenu title="Devices" display={displayDevices} on:click={toggleDevices} right={true}>
  <DevicesMenu />
</SlidingMenu>
