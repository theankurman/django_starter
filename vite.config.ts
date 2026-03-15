import { defineConfig } from "vite";
import { resolve } from "path";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
    base: "/static/vite/",
    plugins: [
        //
        tailwindcss(),
    ],
    build: {
        manifest: "manifest.json",
        outDir: resolve("./core/static/vite"),
        rollupOptions: {
            input: [
                //
                "core/resources/js/main.ts",
            ],
        },
    },
});
