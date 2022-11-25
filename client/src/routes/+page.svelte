<script>
import { onMount } from "svelte";
import { io } from "socket.io-client";

let socketio;
let socket;
let allMsgs = [];
let content = "";

onMount(async () => {
    const namespace = "localhost:8000";
    const transports = {transports: ["websocket"]}
    socketio = io(namespace, transports);

    socketio.on("connect", () => {
        socketio.emit("test", {data: "connected to the SocketServer..."});
    })

    socketio.on("response", (msg, cb) => {
        allMsgs.push("from socketio server: " + msg.data);
        allMsgs = allMsgs;
        if (cb) cb();
    });


    // socket = new WebSocket("ws://localhost:8000/ws");

    // // Connection opened
    // socket.addEventListener("open", event => {
    //     socket.send("Hello Server!");
    // });

    // // Listen for messages
    // socket.addEventListener("message", event => {
    //     allMsgs.push("Received: " + event.data);
    //     allMsgs = allMsgs;
    // });
});

async function sendMsg(event) {
    // socket.send(content);
    // allMsgs.push("Sent: " + content);
    // allMsgs = allMsgs;
    socketio.emit("test", {data: content});
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
<ul>
    {#each allMsgs as msg}
        <li>
            <span>{msg}</span>
        </li>
    {/each}
</ul>
