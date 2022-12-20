<script>
import SlidingMenu from "$lib/settings/SlidingMenu.svelte";
import Option from "$lib/settings/Option.svelte";
import DevicesMenu from "../devices/DevicesMenu.svelte";
import { invalidate } from "$app/navigation";

export let displaySettings;
export let toggleSettings;

let displayGeneral = false;
let displaySecurity = false;
let displaySusFiles = false;  // Scan suspicious files menu 
let displayMagic = false;     // Disappearing messages menu, *MAGIC! POOF!* (๑°༥°๑)
let displayData = false;
let displayDevices = false;

const toggleGeneral = () => displayGeneral = !displayGeneral;
const toggleSecurity = () => displaySecurity = !displaySecurity;
const toggleSusFiles = () => displaySusFiles = !displaySusFiles;
const toggleMagic = () => displayMagic = !displayMagic;
const toggleData = () => displayData = !displayData;

function toggleDevices() {
  displayDevices = !displayDevices;
  invalidate("app:devices");
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
  <Option name="Scan incoming files" icon="file-shield" on:click={toggleSusFiles}/>
  <Option name="Disappearing messages" icon="stopwatch" on:click={toggleMagic}/>
  <Option name="Request personal data" icon="file-zipper" on:click={toggleData}/>
</SlidingMenu>
<SlidingMenu title="Scan incoming files" display={displaySusFiles} on:click={toggleSusFiles} right={true}>
</SlidingMenu>
<SlidingMenu title="Disappearing messages" display={displayMagic} on:click={toggleMagic} right={true}>
</SlidingMenu>
<SlidingMenu title="Request personal data" display={displayData} on:click={toggleData} right={true}>
</SlidingMenu>


<SlidingMenu title="Devices" display={displayDevices} on:click={toggleDevices} right={true}>
  <DevicesMenu />
</SlidingMenu>
