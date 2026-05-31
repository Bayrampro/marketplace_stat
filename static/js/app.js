const copyButton = document.querySelector("[data-copy-target]");
const copyStatus = document.querySelector(".copy-status");
const loadingForms = document.querySelectorAll("[data-loading-form]");
const imageInputs = document.querySelectorAll("input[type='file'][data-max-size]");

const ensureUploadError = (input) => {
    let error = input.closest(".field-group")?.querySelector("[data-upload-error]");

    if (!error) {
        error = document.createElement("div");
        error.className = "field-error upload-error";
        error.dataset.uploadError = "";
        input.insertAdjacentElement("afterend", error);
    }

    return error;
};

const validateImageInput = (input) => {
    const file = input.files?.[0];
    const maxSize = Number(input.dataset.maxSize || 0);
    const maxSizeMb = input.dataset.maxSizeMb || Math.round(maxSize / 1024 / 1024);
    const error = ensureUploadError(input);

    if (file && maxSize && file.size > maxSize) {
        error.textContent = `Файл слишком большой. Максимум ${maxSizeMb} MB.`;
        input.setCustomValidity(`Размер изображения не должен превышать ${maxSizeMb} MB.`);
        return false;
    }

    error.textContent = "";
    input.setCustomValidity("");
    return true;
};

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

imageInputs.forEach((input) => {
    input.addEventListener("change", () => {
        validateImageInput(input);
    });
});

loadingForms.forEach((form) => {
    form.addEventListener("submit", (event) => {
        const invalidImageInput = Array.from(form.querySelectorAll("input[type='file'][data-max-size]")).find(
            (input) => !validateImageInput(input),
        );

        if (invalidImageInput) {
            event.preventDefault();
            invalidImageInput.reportValidity();
            return;
        }

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
