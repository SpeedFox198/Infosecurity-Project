<script>
import { onMount } from "svelte";

let socket;
let allMsgs = [];
let content = "";

onMount(async () => {
    socket = new WebSocket("ws://localhost:5000/ws");

    // Connection opened
    socket.addEventListener("open", event => {
        socket.send("Hello Server!");
    });

    // Listen for messages
    socket.addEventListener("message", event => {
        allMsgs.push(event.data);
        allMsgs = allMsgs;
        console.log(allMsgs);
    });
});

async function sendMsg(event) {
    socket.send(content);
    content = "";
}

</script>

<h1>Server Echoing</h1>

<form on:submit|preventDefault={sendMsg}>
    <input type="text" name="data" bind:value={content}>
    <input type="submit" name="Send Message">
</form>

<h3>Messages:</h3>
<ul>
    {#each allMsgs as msg}
        <li>
            <span>{msg}</span>
        </li>
    {/each}
</ul>
