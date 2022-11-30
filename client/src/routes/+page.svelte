<script>
import { onMount } from "svelte";
import { io } from "socket.io-client";

let socket;
let allMsgs = [];
let content = "";

onMount(async () => {
    const namespace = "localhost:5000";
    const transports = {transports: ["websocket"]}
    socket = io(namespace, transports);

    socket.on("connect", () => {
        socket.emit("test", {data: "connected to the SocketServer..."});
    })

    socket.on("response", (msg, cb) => {
        allMsgs.push("from socketio server: " + msg.data);
        allMsgs = allMsgs;
        if (cb) cb();
    });
});

async function sendMsg(event) {
    socket.emit("test", {data: content});
    allMsgs.push("Sent via socketio: " + content);
    allMsgs = allMsgs;
    content = "";
}

</script>

<h1>Server Echoing</h1>

<form on:submit|preventDefault={sendMsg}>
    <input type="text" name="data" bind:value={content}>
    <input type="submit" name="Send Message">
</form>

<h3>Messages:</h3>
<ol>
    {#each allMsgs as msg}
        <li>
            <span>{msg}</span>
        </li>
    {/each}
</ol>
