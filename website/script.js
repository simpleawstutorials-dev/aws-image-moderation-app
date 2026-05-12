const API_URL = "Your API Gateway URL HERE";
const MAX_FILE_SIZE_BYTES = 5 * 1024 * 1024;
const ALLOWED_FILE_TYPES = ["image/jpeg", "image/png"];
const ALLOWED_EXTENSIONS = [".jpg", ".jpeg", ".png"];

const form = document.getElementById("upload-form");
const nameInput = document.getElementById("name");
const emailInput = document.getElementById("email");
const fileInput = document.getElementById("file");
const clearButton = document.getElementById("clear-button");
const uploadButton = document.getElementById("upload-button");
const selectedFileText = document.getElementById("selected-file");
const statusMessage = document.getElementById("status-message");

const nameError = document.getElementById("name-error");
const emailError = document.getElementById("email-error");
const fileError = document.getElementById("file-error");

function setFieldError(element, message) {
  element.textContent = message;
}

function clearFieldErrors() {
  setFieldError(nameError, "");
  setFieldError(emailError, "");
  setFieldError(fileError, "");
}

function setStatus(message, type = "") {
  statusMessage.textContent = message;
  statusMessage.className = "status-message";

  if (type) {
    statusMessage.classList.add(type);
  }
}

function isValidEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

function hasAllowedExtension(fileName) {
  const lowerCaseName = fileName.toLowerCase();
  return ALLOWED_EXTENSIONS.some((extension) => lowerCaseName.endsWith(extension));
}

function validateTextFields() {
  let isValid = true;
  const name = nameInput.value.trim();
  const email = emailInput.value.trim();

  if (!name) {
    setFieldError(nameError, "Name is required.");
    isValid = false;
  }

  if (!email) {
    setFieldError(emailError, "Email is required.");
    isValid = false;
  } else if (!isValidEmail(email)) {
    setFieldError(emailError, "Enter a valid email address.");
    isValid = false;
  }

  return isValid;
}

function validateFile() {
  const files = fileInput.files;

  if (!files || files.length === 0) {
    setFieldError(fileError, "Please select an image file.");
    return null;
  }

  if (files.length > 1) {
    setFieldError(fileError, "Please select only one file.");
    return null;
  }

  const file = files[0];

  if (!ALLOWED_FILE_TYPES.includes(file.type) || !hasAllowedExtension(file.name)) {
    setFieldError(fileError, "Only JPG and PNG files are allowed.");
    return null;
  }

  if (file.size > MAX_FILE_SIZE_BYTES) {
    setFieldError(fileError, "The selected file must be 5 MB or smaller.");
    return null;
  }

  return file;
}

function resetFormState() {
  form.reset();
  clearFieldErrors();
  setStatus("");
  selectedFileText.textContent = "No file selected.";
}

async function requestPresignedUrl(payload) {
  const response = await fetch(API_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(payload)
  });

  if (!response.ok) {
    throw new Error(`Failed to get presigned URL. Status: ${response.status}`);
  }

  const data = await response.json();

  if (!data || !data.presignedUrl) {
    throw new Error("API response did not include presigned URL.");
  }

  return data.presignedUrl;
}

async function uploadFileToS3(uploadUrl, file) {
  const response = await fetch(uploadUrl, {
    method: "PUT",
    headers: {
      "Content-Type": file.type
    },
    body: file
  });

  if (!response.ok) {
    throw new Error(`S3 upload failed. Status: ${response.status}`);
  }
}

fileInput.addEventListener("change", () => {
  clearFieldErrors();
  setStatus("");

  const files = fileInput.files;
  if (!files || files.length === 0) {
    selectedFileText.textContent = "No file selected.";
    return;
  }

  const file = files[0];
  selectedFileText.textContent = `Selected file: ${file.name}`;
});

clearButton.addEventListener("click", () => {
  resetFormState();
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  clearFieldErrors();
  setStatus("");

  const textFieldsValid = validateTextFields();
  const file = validateFile();

  if (!textFieldsValid || !file) {
    setStatus("Please correct the errors above and try again.", "error");
    return;
  }

  const payload = {
    userName: nameInput.value.trim(),
    userEmail: emailInput.value.trim(),
    fileName: file.name,
    contentType: file.type,
    contentLength: file.size
  };

  uploadButton.disabled = true;
  clearButton.disabled = true;
  setStatus("Uploading file. Please wait...");

  try {
    const uploadUrl = await requestPresignedUrl(payload);
    await uploadFileToS3(uploadUrl, file);
    setStatus("File upload is successful.", "success");
  } catch (error) {
    console.error("Upload process failed:", error);
    setStatus("File upload failed. Please try again.", "error");
  } finally {
    uploadButton.disabled = false;
    clearButton.disabled = false;
  }
});
