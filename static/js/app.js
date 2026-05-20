const copyButton = document.querySelector("[data-copy-target]");
const copyStatus = document.querySelector(".copy-status");

if (copyButton) {
    copyButton.addEventListener("click", async () => {
        const targetId = copyButton.getAttribute("data-copy-target");
        const target = document.getElementById(targetId);

        if (!target) {
            return;
        }

        try {
            await navigator.clipboard.writeText(target.textContent.trim());
            if (copyStatus) {
                copyStatus.textContent = "Текст скопирован.";
            }
        } catch (error) {
            if (copyStatus) {
                copyStatus.textContent = "Не удалось скопировать текст.";
            }
        }
    });
}
