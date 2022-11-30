<script>
import LeftSection from "./LeftSection.svelte";
import RightSection, { content, allMsgs } from "./RightSection.svelte";
import { onMount } from "svelte";
import { io } from "socket.io-client";

const namespace = "localhost:5000";
const transports = {transports: ["websocket"]}
let socket;

onMount(async () => {
    // SocketIO instance
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

<style>
main {
    background-color: var(--white);
}
</style>

<main class="d-flex flex-nowrap h-100">
    <LeftSection/>
    <RightSection on:submit={sendMsg}/>
</main>
