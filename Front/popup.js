document.addEventListener("DOMContentLoaded", () => {
  const processButton = document.getElementById("process-button");
  const videoUrlInput = document.getElementById("video-url");
  const languageSelect = document.getElementById("language");
  const responseDiv = document.getElementById("response");
  const spinner = document.getElementById("spinner");

  // Verificar se todos os elementos existem
  if (!processButton || !videoUrlInput || !languageSelect || !responseDiv || !spinner) {
    console.error("Erro: Alguns elementos do DOM não foram encontrados.");
    return;
  }

  processButton.addEventListener("click", async () => {
    const videoUrl = videoUrlInput.value.trim();
    const language = languageSelect.value;

    responseDiv.textContent = ""; // Limpa mensagens antigas
    spinner.style.display = "block"; // Mostra o spinner

    if (!videoUrl) {
      responseDiv.textContent = "Por favor, insira uma URL.";
      spinner.style.display = "none";
      return;
    }

    try {
      const response = await fetch("http://127.0.0.1:5000/process", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ video_url: videoUrl, language: language }),
      });

      spinner.style.display = "none"; // Esconde o spinner

      if (response.ok) {
        const data = await response.json();

        // Transformar os tópicos em uma lista enumerada
        const topicsList = data.topics
          .split(/\d+\.\s+/) // Divide os tópicos pelo padrão "1. ", "2. ", etc.
          .filter((topic) => topic.trim() !== "") // Remove entradas vazias
          .map(
            (topic, index) =>
              `<li><strong>${index + 1}:</strong> ${topic.trim()}</li>`
          ) // Formata como <li>
          .join(""); // Junta os itens

        responseDiv.innerHTML = `<span class="success">Tópicos:</span><ul>${topicsList}</ul>`;
      } else {
        responseDiv.innerHTML = `<span class="error">Erro ao processar o vídeo.</span>`;
      }
    } catch (error) {
      spinner.style.display = "none"; // Esconde o spinner
      responseDiv.innerHTML = `<span class="error">Erro ao conectar ao servidor.</span>`;
    }
  });
});
