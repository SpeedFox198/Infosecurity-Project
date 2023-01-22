<script>
import { onMount } from 'svelte';
import { getFlash } from "sveltekit-flash-message/client"
import { page } from "$app/stores"

import { room_id, roomStorage, roomList } from '$lib/stores/room';
import { count } from '$lib/stores/count';
import { selectedMsgs } from '$lib/stores/select';
import { allMsgs } from "$lib/stores/message";

import Group from '$lib/chat/group/Group.svelte';
import Nav from './Nav.svelte';
import Settings from '$lib/settings/Settings.svelte';
import NewGroup from '$lib/settings/NewGroup.svelte';
import Friends from '$lib/settings/Friends.svelte';

// SocketIO instance
/** @type {import('socket.io-client').Socket}*/
export let socket;
export let getRoomMsgs;

const flash = getFlash(page)

let displaySettings = false;
let displayNewGroup = false;
let displayFriends = false;
let roomSearchInput = "" 

$: unfilteredRooms = $roomList.map(room_id => $roomStorage[room_id]);
$: currentRooms = unfilteredRooms.filter(room => room.name
                                          .toLowerCase()
                                          .includes(roomSearchInput))


async function selectGrp(new_room) {
  // Set selected room_id
  room_id.set(new_room);

  // Clear any selected messages in previous room
  selectedMsgs.clear();

  // Get room messages via socket if n is 0
  if (!($count[$room_id] || {}).n) {
    const { n, extra } = count.nextN($room_id);
    getRoomMsgs($room_id, n, extra);
  }
}

const toggleSettings = async () => displaySettings = !displaySettings;
const toggleNewGroup = async () => displayNewGroup = !displayNewGroup;
const toggleFriends = async () => displayFriends = !displayFriends;


const sendNewGroup = async (event) => {
  let { group_metadata } = event.detail
  socket.emit("create_group", group_metadata)
}

onMount(() => {
  socket.on("group_created", async () => {
    $flash = {type: 'success', message: 'Group created!'}
  })
  
  socket.on("create_group_error", async (data) => {
    $flash = {type: 'failure', message: `Group failed to create! Reason: ${data.message}`}
  })
  
  socket.on("group_invite", async (data) => {
    let newRoomStorage = {};

    const newRoomList = data.map(room => room.room_id)
    data.forEach(room => {
      newRoomStorage[room.room_id] = room
    });
    

    // Initialise rooms
    roomList.set(newRoomList);           // Set list of room_id
    roomStorage.set(newRoomStorage);     // Set collection of rooms
    allMsgs.initRooms(newRoomList)       // Initialise empty arrays for rooms
  })
})
</script>

<!-- Left Sidebar -->
<div class="d-flex flex-column flex-shrink-0 sidebar">

  <!-- Settings Display Section -->
  <Settings {displaySettings} {toggleSettings}/>
  <NewGroup {displayNewGroup} {toggleNewGroup} on:create-group={sendNewGroup}/>
  <Friends {displayFriends} {toggleFriends} socket={socket}/>
  <!-- Profile & Settings Section -->
  <Nav bind:roomSearchInput={roomSearchInput} {toggleSettings} {toggleNewGroup} {toggleFriends}/>

  <!-- Chat List Section -->
  <div class="d-flex flex-column bottom-left">
    {#each currentRooms as grp (grp.room_id)} 
      <Group {grp} {selectGrp}/>
    {/each}
  </div>
</div>

<style>
.sidebar {
  position: relative;
  width: var(--side-bar-length);
  background-color: var(--primary-light);
  overflow-x: hidden;
}

.bottom-left {
  height: 100%;
  overflow-y: scroll;
}
</style>
