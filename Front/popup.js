document.addEventListener("DOMContentLoaded", () => {
  const processButton = document.getElementById("process-button");
  const videoUrlInput = document.getElementById("video-url");
  const languageSelect = document.getElementById("language");
  const responseDiv = document.getElementById("response");
  const spinner = document.getElementById("spinner");

  if (!processButton || !videoUrlInput || !languageSelect || !responseDiv || !spinner) {
    console.error("Erro: Alguns elementos do DOM não foram encontrados.");
    return;
  }

  async function checkAPI() {
    try {
      const res = await fetch("http://127.0.0.1:5000/");
      return res.ok;
    } catch (error) {
      return false;
    }
  }

  processButton.addEventListener("click", async () => {
    const videoUrl = videoUrlInput.value.trim();
    const language = languageSelect.value;

    responseDiv.textContent = "";
    spinner.style.display = "block";

    if (!videoUrl) {
      responseDiv.textContent = "Por favor, insira uma URL.";
      spinner.style.display = "none";
      return;
    }

    if (!(await checkAPI())) {
      responseDiv.innerHTML = `<span class="error">Erro: O servidor não está acessível. Certifique-se de que a API está rodando.</span>`;
      spinner.style.display = "none";
      return;
    }

    try {
      const response = await fetch("http://127.0.0.1:5000/process", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ video_url: videoUrl, language: language }),
      });

      spinner.style.display = "none";

      if (response.ok) {
        const data = await response.json();
        const topicsList = data.topics
          .split(/\d+\.\s+/)
          .filter(topic => topic.trim() !== "")
          .map((topic, index) => `<li><strong>${index + 1}:</strong> ${topic.trim()}</li>`)
          .join("");
        responseDiv.innerHTML = `<span class="success">Tópicos:</span><ul>${topicsList}</ul>`;
      } else {
        const errorData = await response.json();
        responseDiv.innerHTML = `<span class="error">Erro: ${errorData.error || "Erro ao processar o vídeo."}</span>`;
      }
    } catch (error) {
      spinner.style.display = "none";
      responseDiv.innerHTML = `<span class="error">Erro ao conectar ao servidor.</span>`;
    }
  });
});
