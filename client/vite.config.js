import { sveltekit } from "@sveltejs/kit/vite";
import { readFileSync } from "fs";

const config = {
	plugins: [sveltekit()],
	server: {
		https: {
			key: readFileSync( "../key.pem"),
			cert: readFileSync("../cert.pem"),
		}
	},
};

export default config;
