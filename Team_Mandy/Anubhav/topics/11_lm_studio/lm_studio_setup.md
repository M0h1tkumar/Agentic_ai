# Local LLM Setup with LM Studio

LM Studio is a desktop application that allows you to discover, download, and run local LLMs completely offline. It acts as a local drop-in replacement for the OpenAI API.

## 1. Installation
1. Navigate to [LMStudio.ai](https://lmstudio.ai/) and download the installer for your OS (Windows/Mac/Linux).
2. Run the installer and open the application.

## 2. Downloading a Model
LM Studio pulls models directly from Hugging Face in the `GGUF` format.
1. Open the **Search** tab (magnifying glass icon).
2. Search for a lightweight, capable model like `Llama-3-8B-Instruct` or `Qwen-2.5-7B`.
3. Look for models uploaded by trusted quantizers (e.g. `bartowski` or `MaziyarPanahi`).
4. Download a quantization level that fits your RAM:
   - `Q4_K_M` (4-bit, recommended for 8GB RAM).
   - `Q8_0` (8-bit, recommended for 16GB+ RAM).

## 3. Chatting Locally
1. Go to the **Chat** tab (speech bubble icon).
2. Load the model from the top dropdown menu.
3. Configure the hardware settings on the right panel (e.g., set `GPU Offload` to `Max` if you have a dedicated GPU).
4. Start chatting! The data never leaves your machine.

## 4. Running a Local API Server (OpenAI Compatible)
This is crucial if you want to connect external tools (like AnythingLLM or OpenHands) to your local model.
1. Go to the **Local Server** tab (double arrow icon).
2. Ensure the model is loaded.
3. Start the server. By default, it runs on `http://localhost:1234/v1`.
4. **Integration:** You can now point any software that asks for an OpenAI API key to `http://localhost:1234/v1` and use `lm-studio` as the API key. The software will think it's talking to ChatGPT, but it's actually talking to your local model!
