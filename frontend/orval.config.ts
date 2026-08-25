import { defineConfig } from "orval";

export default defineConfig({
    manga: {
        input: { target: "http://localhost:8000/openapi.json" },
        output: {
            client: "angular",
            mode: "split",
            target: "./src/app/api/manga.ts",
            schemas: "./src/app/api/model",
            clean: true,
        },
    },
});