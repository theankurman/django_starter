import { defineConfig } from "vite"
import { resolve } from "path"
export default defineConfig({
    base: "/static/vite/",
    build: {
        manifest: "manifest.json",
        outDir: resolve("./core/static/vite"),
        rollupOptions: {
            input: [
                "core/resources/js/main.ts"
            ]
        }
    }
})