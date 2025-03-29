document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("upload-form");
  const fileInput = document.getElementById("pdf-file");
  const statusMessage = document.getElementById("status-message");
  const downloadSection = document.getElementById("download-section");
  const downloadLink = document.getElementById("download-link");

  form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const file = fileInput.files[0];
    if (!file) {
      statusMessage.textContent = "PDF 파일을 선택해주세요.";
      return;
    }

    statusMessage.textContent = "업로드 중... 변환을 기다려주세요.";
    downloadSection.style.display = "none";

    const formData = new FormData();
    formData.append("pdf", file);

    try {
      const response = await fetch("/convert", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("서버 오류 또는 변환 실패");
      }

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);

      downloadLink.href = url;
      downloadLink.download = "converted.zip"; // 서버에서 zip으로 반환하는 경우
      downloadSection.style.display = "block";
      statusMessage.textContent = "변환 완료! 아래 버튼으로 다운로드하세요.";

    } catch (error) {
      console.error(error);
      statusMessage.textContent = "변환 중 오류가 발생했습니다. 다시 시도해주세요.";
    }
  });
});
