const copyButton = document.querySelector("[data-copy-target]");
const copyStatus = document.querySelector(".copy-status");
const loadingForms = document.querySelectorAll("[data-loading-form]");

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

loadingForms.forEach((form) => {
    form.addEventListener("submit", () => {
        const submitButton = form.querySelector("[data-loading-button]");
        const resultPanel = form.closest(".workspace")?.querySelector("[data-loading-result]");
        const loadingTitle = resultPanel?.querySelector("[data-loading-result-title]");
        const loadingText = resultPanel?.querySelector("[data-loading-result-text]");
        const title = form.dataset.loadingTitle;
        const text = form.dataset.loadingText;

        if (submitButton) {
            submitButton.dataset.defaultLabel = submitButton.textContent.trim();
            submitButton.textContent = submitButton.dataset.loadingLabel || "Генерируется...";
            submitButton.disabled = true;
            submitButton.classList.add("button-loading");
        }

        if (resultPanel) {
            resultPanel
                .closest(".result-panel")
                ?.querySelectorAll(".generated-result, .empty-result, .image-preview, .result-meta, .secondary-button, .copy-status")
                .forEach((element) => {
                    element.hidden = true;
                });
            if (loadingTitle && title) {
                loadingTitle.textContent = title;
            }
            if (loadingText && text) {
                loadingText.textContent = text;
            }
            resultPanel.hidden = false;
            resultPanel.scrollIntoView({ behavior: "smooth", block: "nearest" });
        }
    });
});
