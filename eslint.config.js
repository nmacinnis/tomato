import js from "@eslint/js";
import prettierConfig from "eslint-config-prettier";
import globals from "globals";

export default [
  js.configs.recommended,
  prettierConfig,
  {
    languageOptions: {
      ecmaVersion: 2022,
      // script (not module) — files share globals via <script> tags in the HTML
      sourceType: "script",
      globals: {
        ...globals.browser,
      },
    },
    rules: {
      // Cross-file shared vars (e.g. escHtml, apiFetch, char) are false positives
      // in a multi-file vanilla JS setup without a module system.
      "no-undef": "warn",
      "no-unused-vars": "warn",
    },
  },
];
