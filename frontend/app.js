const API_BASE = window.TALENTLENS_API_BASE
  || (window.location.port === "8001" ? "http://127.0.0.1:8000" : "");
const allowedJdExtensions = new Set(["txt", "pdf", "docx"]);
const allowedResumeExtensions = new Set(["pdf", "docx", "txt"]);

let currentResults = [];
let lastFocusedElement = null;
let authRequired = false;
const scoreChart = createScoreChart();
const skillChart = createSkillChart();

function escapeHTML(value) {
  return String(value ?? "").replace(/[&<>"']/g, (character) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#39;",
  })[character]);
}

function getExtension(filename) {
  return filename.includes(".") ? filename.split(".").pop().toLowerCase() : "";
}

function showAuthGate(providers) {
  document.getElementById("appShell").hidden = true;
  document.getElementById("authGate").hidden = false;
  const providerContainer = document.getElementById("authProviders");
  providerContainer.replaceChildren();

  const providerNames = {
    google: "Continue with Google",
    microsoft: "Continue with Microsoft",
  };
  providers.forEach((provider) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "auth-provider-button";
    button.textContent = providerNames[provider] || `Continue with ${provider}`;
    button.addEventListener("click", () => {
      window.location.assign(`${API_BASE}/auth/login/${encodeURIComponent(provider)}`);
    });
    providerContainer.append(button);
  });

  if (!providers.length) {
    const error = document.getElementById("authError");
    error.textContent = "Sign-in providers are not configured. Contact the application administrator.";
    error.hidden = false;
  }
}

async function initializeAuthentication() {
  const response = await fetch(`${API_BASE}/auth/config`, { credentials: "include" });
  if (!response.ok) throw new Error("Unable to check sign-in status.");
  const config = await response.json();
  authRequired = Boolean(config.auth_required);

  if (config.auth_required && !config.user) {
    showAuthGate(config.providers || []);
    return false;
  }

  document.getElementById("authGate").hidden = true;
  document.getElementById("appShell").hidden = false;
  const signedInUser = document.getElementById("signedInUser");
  const signOutButton = document.getElementById("signOutButton");
  if (config.user) {
    signedInUser.textContent = config.user.email;
    signedInUser.hidden = false;
    signOutButton.hidden = false;
  } else {
    signedInUser.hidden = true;
    signOutButton.hidden = true;
  }
  document.getElementById("loadDataButton").hidden = authRequired;
  if (authRequired) {
    renderDashboard({ resumes: [] });
    setNotice(
      "For privacy, uploaded resumes are processed for this screening and are not saved to the server.",
      "success",
    );
  }
  return true;
}

function applyTheme(theme, persist = false) {
  const isLight = theme === "light";
  document.body.dataset.theme = isLight ? "light" : "dark";
  const toggle = document.getElementById("themeToggle");
  if (toggle) {
    toggle.textContent = isLight ? "Dark theme" : "Light theme";
    toggle.setAttribute("aria-label", `Switch to ${isLight ? "dark" : "light"} theme`);
    toggle.setAttribute("aria-pressed", String(isLight));
  }

  const metaThemeColor = document.querySelector('meta[name="theme-color"]');
  if (metaThemeColor) metaThemeColor.content = isLight ? "#f3f5f7" : "#171a1f";

  const chartText = isLight ? "#687584" : "#89939f";
  const chartGrid = isLight ? "rgba(53, 68, 84, .12)" : "rgba(165, 184, 207, .07)";
  if (scoreChart) {
    scoreChart.options.scales.x.ticks.color = chartText;
    scoreChart.options.scales.y.ticks.color = chartText;
    scoreChart.options.scales.y.grid.color = chartGrid;
    scoreChart.update();
  }
  if (skillChart) {
    skillChart.options.plugins.legend.labels.color = chartText;
    skillChart.update();
  }

  if (persist) {
    try {
      localStorage.setItem("talentlens-theme", isLight ? "light" : "dark");
    } catch {
      // The selected theme remains applied for this page even if storage is unavailable.
    }
  }
}

function createScoreChart() {
  const canvas = document.getElementById("scoreChart");
  if (!canvas || typeof Chart === "undefined") return null;

  return new Chart(canvas, {
    type: "bar",
    data: {
      labels: [],
      datasets: [{
        data: [],
        borderRadius: 5,
        maxBarThickness: 38,
        backgroundColor: "rgba(125, 170, 150, .82)",
        hoverBackgroundColor: "#9bc0aa",
      }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true,
          max: 100,
          border: { display: false },
          grid: { color: "rgba(165, 184, 207, .07)" },
          ticks: { color: "#89939f", stepSize: 25, font: { size: 9 } },
        },
        x: {
          border: { display: false },
          grid: { display: false },
          ticks: {
            color: "#89939f",
            font: { size: 8 },
            maxRotation: 0,
            callback(index) {
              const label = this.getLabelForValue(index);
              return label.length > 16 ? `${label.slice(0, 14)}…` : label;
            },
          },
        },
      },
      plugins: {
        legend: { display: false },
        tooltip: { callbacks: { label: (context) => ` ${context.parsed.y}% match` } },
      },
    },
  });
}

function createSkillChart() {
  const canvas = document.getElementById("skillChart");
  if (!canvas || typeof Chart === "undefined") return null;

  return new Chart(canvas, {
    type: "doughnut",
    data: {
      labels: ["Matched skills", "Missing skills"],
      datasets: [{
        data: [0, 0],
        backgroundColor: ["#7daa97", "#c8a667"],
        hoverOffset: 4,
        borderWidth: 0,
        spacing: 3,
      }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      cutout: "74%",
      plugins: {
        legend: {
          position: "bottom",
          labels: { color: "#9aa3ae", boxWidth: 7, boxHeight: 7, padding: 16, font: { size: 9 } },
        },
      },
    },
  });
}

function recommendationClass(recommendation) {
  const value = (recommendation || "").toLowerCase();
  if (value.includes("excellent") || value.includes("strong")) return "tag-good";
  if (value.includes("poor")) return "tag-poor";
  return "tag-medium";
}

function setNotice(message, type = "error") {
  const notice = document.getElementById("notice");
  notice.textContent = message;
  notice.classList.toggle("success", type === "success");
  notice.hidden = !message;
}

function setProgress({ title, message, percent, state = "" }) {
  const panel = document.getElementById("progressPanel");
  panel.hidden = false;
  panel.classList.toggle("is-processing", state === "processing");
  panel.classList.toggle("is-complete", state === "complete");
  document.getElementById("progressTitle").textContent = title;
  document.getElementById("progressMessage").textContent = message;
  document.getElementById("progressPercent").textContent = `${percent}%`;
  document.getElementById("progressFill").style.width = `${percent}%`;
}

function setBusy(isBusy) {
  document.getElementById("analyzeButton").disabled = isBusy;
  document.getElementById("loadDataButton").disabled = isBusy;
  document.getElementById("analyzeButton").querySelector("span:first-child").textContent =
    isBusy ? "Screening…" : "Screen resumes";
}

function renderStats(data) {
  const candidates = data.resumes || [];
  const avgScore = candidates.length
    ? Math.round(candidates.reduce((sum, candidate) => sum + Number(candidate.score || 0), 0) / candidates.length)
    : 0;
  const topCandidate = candidates[0];
  const matchedCount = candidates.reduce((sum, candidate) => sum + (candidate.matched_skills || []).length, 0);

  document.getElementById("totalCandidates").textContent = candidates.length;
  document.getElementById("candidateFoot").textContent = candidates.length === 1
    ? "Candidate in this screening batch"
    : `${candidates.length} candidates in this screening batch`;
  document.getElementById("avgScore").textContent = `${avgScore}%`;
  document.getElementById("topCandidateName").textContent = topCandidate?.filename || "—";
  document.getElementById("topCandidateFoot").textContent = topCandidate
    ? `${Number(topCandidate.score || 0)}% role match`
    : "Highest role match";
  document.getElementById("matchedSkillsCount").textContent = matchedCount;
}

function renderCharts(data) {
  const candidates = data.resumes || [];
  const scoreCard = document.getElementById("scoreChart").closest(".chart-card");
  const skillCard = document.getElementById("skillChart").closest(".chart-card");
  const hasResults = candidates.length > 0;

  scoreCard.classList.toggle("has-data", hasResults && Boolean(scoreChart));
  skillCard.classList.toggle("has-data", hasResults && Boolean(skillChart));

  if (scoreChart) {
    scoreChart.data.labels = candidates.map((candidate) => candidate.filename || "Candidate");
    scoreChart.data.datasets[0].data = candidates.map((candidate) => Number(candidate.score || 0));
    scoreChart.update();
  }

  const matched = candidates.reduce((sum, candidate) => sum + (candidate.matched_skills || []).length, 0);
  const missing = candidates.reduce((sum, candidate) => sum + (candidate.missing_skills || []).length, 0);
  if (skillChart) {
    skillChart.data.datasets[0].data = [matched, missing];
    skillChart.update();
  }
  document.getElementById("skillCaption").textContent = hasResults
    ? `${matched} matched · ${missing} missing`
    : "No skills analyzed";
}

function candidateInitials(filename) {
  const stem = String(filename || "Candidate").replace(/\.[^.]+$/, "");
  const words = stem.trim().split(/\s+/).filter(Boolean);
  return words.length > 1
    ? `${words[0][0]}${words[1][0]}`.toUpperCase()
    : stem.slice(0, 2).toUpperCase();
}

function renderSkills(skills, className = "") {
  if (!skills?.length) return '<span class="skill-overflow">None listed</span>';
  return skills.map((skill) => `<span class="skill-pill ${className}">${escapeHTML(skill)}</span>`).join("");
}

function renderTable(data) {
  const body = document.getElementById("resultsTableBody");
  const candidates = data.resumes || [];
  document.getElementById("tableCount").textContent =
    `${candidates.length} ${candidates.length === 1 ? "candidate" : "candidates"}`;

  if (!candidates.length) {
    body.innerHTML = '<tr class="empty-row"><td colspan="6">No candidates were returned for this screening.</td></tr>';
    return;
  }

  body.innerHTML = candidates.map((candidate, index) => {
    const score = Math.max(0, Math.min(100, Number(candidate.score || 0)));
    const recommendation = candidate.recommendation || "Review";
    const matched = candidate.matched_skills || [];
    const visibleSkills = matched.slice(0, 3).map((skill) =>
      `<span class="skill-pill">${escapeHTML(skill)}</span>`).join("");
    const moreSkills = matched.length > 3
      ? `<span class="skill-overflow">+${matched.length - 3}</span>`
      : "";

    return `<tr>
      <td class="rank-cell">#${index + 1}</td>
      <td><div class="candidate-cell">
        <span class="candidate-avatar">${escapeHTML(candidateInitials(candidate.filename))}</span>
        <span><span class="candidate-name">${escapeHTML(candidate.filename || `Candidate ${index + 1}`)}</span>
          ${candidate.email ? `<span class="candidate-email">${escapeHTML(candidate.email)}</span>` : ""}
        </span>
      </div></td>
      <td><div class="score-cell"><div class="score-label"><span>${score}%</span></div>
        <div class="score-track"><div class="score-fill" style="width:${score}%"></div></div>
      </div></td>
      <td><div class="skill-pills">${visibleSkills || '<span class="skill-overflow">No direct matches</span>'}${moreSkills}</div></td>
      <td><span class="recommendation-tag ${recommendationClass(recommendation)}">${escapeHTML(recommendation)}</span></td>
      <td><button class="detail-button" type="button" data-candidate-index="${index}">View profile</button></td>
    </tr>`;
  }).join("");
}

function renderDashboard(data) {
  currentResults = data.resumes || [];
  renderStats(data);
  renderCharts(data);
  renderTable(data);
  document.getElementById("dataState").classList.toggle("loaded", currentResults.length > 0);
  document.getElementById("dataState").innerHTML = currentResults.length
    ? '<span class="state-dot"></span> Results loaded'
    : '<span class="state-dot"></span> No results';
  document.getElementById("lastUpdated").textContent = currentResults.length
    ? `Updated ${new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}`
    : "No screening results";
}

async function loadAnalysisFromBackend() {
  setNotice("");
  const button = document.getElementById("loadDataButton");
  button.disabled = true;
  try {
    const response = await fetch(`${API_BASE}/analysis/`, { credentials: "include" });
    const data = await response.json();
    if (response.status === 401) {
      const authResponse = await fetch(`${API_BASE}/auth/config`, { credentials: "include" });
      const authConfig = await authResponse.json();
      showAuthGate(authConfig.providers || []);
      return;
    }
    if (!response.ok || data.success === false) {
      throw new Error(data.message || "No saved screening results were found.");
    }
    renderDashboard(data);
  } catch (error) {
    setNotice(`${error.message || "Could not connect to the screening service."} Check that the TalentLens API is running, then try again.`);
  } finally {
    button.disabled = false;
  }
}

function validateFiles(jdFile, resumeFiles) {
  if (!jdFile) return "Choose a job description before starting the analysis.";
  if (!allowedJdExtensions.has(getExtension(jdFile.name))) {
    return "The job description must be a .txt, .pdf, or .docx file.";
  }
  if (!resumeFiles.length) return "Choose at least one candidate resume.";
  const unsupported = resumeFiles.find((file) => !allowedResumeExtensions.has(getExtension(file.name)));
  if (unsupported) return `${unsupported.name} is not supported. Use PDF, DOCX, or TXT resumes.`;
  return "";
}

function submitAnalysis(event) {
  event.preventDefault();
  const jdFile = document.getElementById("jdInput").files[0];
  const resumeFiles = Array.from(document.getElementById("resumeInput").files);
  const validationError = validateFiles(jdFile, resumeFiles);
  setNotice(validationError);
  if (validationError) return;

  const formData = new FormData();
  formData.append("job_description", jdFile);
  resumeFiles.forEach((file) => formData.append("resumes", file));
  setBusy(true);
  setNotice("");
  setProgress({
    title: "Uploading files",
    message: `Sending the job description and ${resumeFiles.length} ${resumeFiles.length === 1 ? "resume" : "resumes"} securely to the screening API.`,
    percent: 0,
  });

  const request = new XMLHttpRequest();
  request.open("POST", `${API_BASE}/analysis/`);
  request.withCredentials = true;
  request.timeout = 300000;

  request.upload.addEventListener("progress", (progressEvent) => {
    if (!progressEvent.lengthComputable) {
      setProgress({
        title: "Uploading files",
        message: "Files are being transferred to the screening API.",
        percent: 12,
      });
      return;
    }
    const percent = Math.min(88, Math.round((progressEvent.loaded / progressEvent.total) * 88));
    setProgress({
      title: "Uploading files",
      message: `${resumeFiles.length} ${resumeFiles.length === 1 ? "resume" : "resumes"} · ${Math.round(progressEvent.loaded / 1024)} KB sent`,
      percent,
    });
  });

  request.upload.addEventListener("load", () => {
    setProgress({
      title: "Screening resumes",
      message: "Files received. Extracting skills and comparing resumes with the role.",
      percent: 92,
      state: "processing",
    });
  });

  request.addEventListener("load", () => {
    setBusy(false);
    let data;
    try {
      data = JSON.parse(request.responseText);
    } catch {
      setNotice("The screening service returned an unreadable response. Please retry.");
      return;
    }
    if (request.status === 401) {
      window.location.reload();
      return;
    }
    if (request.status < 200 || request.status >= 300 || data.success === false) {
      setNotice(data.detail || data.message || `Analysis failed (HTTP ${request.status}). Please check the files and retry.`);
      return;
    }

    renderDashboard(data);
    document.getElementById("analysisForm").reset();
    updateFileLabels();
    setProgress({
      title: "Screening complete",
      message: `${data.total_resumes ?? data.resumes?.length ?? 0} candidate results are ready to review.`,
      percent: 100,
      state: "complete",
    });
    setNotice("Candidate analysis completed successfully.", "success");
  });

  request.addEventListener("error", () => {
    setBusy(false);
    setNotice("Could not reach the screening API. Check that the backend is running and accessible, then retry.");
  });
  request.addEventListener("timeout", () => {
    setBusy(false);
    setNotice("The screening request timed out. Try a smaller batch of resumes.");
  });
  request.send(formData);
}

function openCandidateModal(index) {
  const candidate = currentResults[index];
  if (!candidate) return;
  lastFocusedElement = document.activeElement;
  const modal = document.getElementById("candidateModal");
  const matched = candidate.matched_skills || [];
  const missing = candidate.missing_skills || [];
  const skills = candidate.skills || [];
  const recommendation = candidate.recommendation || "Review";
  const score = Number(candidate.score || 0);

  document.getElementById("modalContent").innerHTML = `
    <div class="modal-profile">
      <span class="modal-avatar">${escapeHTML(candidateInitials(candidate.filename))}</span>
      <span><p class="eyebrow">CANDIDATE PROFILE</p>
        <h2 id="modalName">${escapeHTML(candidate.filename || "Candidate")}</h2>
        <p>${escapeHTML(candidate.email || "Email not available")}${candidate.phone ? ` · ${escapeHTML(candidate.phone)}` : ""}</p>
      </span>
    </div>
    <div class="modal-score-row">
      <span><p class="eyebrow">ROLE MATCH</p><span class="modal-score">${escapeHTML(score)}<small>% match</small></span></span>
      <span class="recommendation-tag ${recommendationClass(recommendation)}">${escapeHTML(recommendation)}</span>
    </div>
    <div class="modal-meta modal-section">
      <div><small>Resume length</small><strong>${escapeHTML(candidate.characters ?? "—")} characters</strong></div>
      <div><small>Candidate skills detected</small><strong>${skills.length} skills</strong></div>
    </div>
    <div class="modal-section"><h3>Matched skills · ${matched.length}</h3>
      <div class="modal-skills">${matched.length
    ? matched.map((skill) => `<span class="modal-skill matched">${escapeHTML(skill)}</span>`).join("")
    : '<span class="modal-skill">No direct skill matches</span>'}</div>
    </div>
    <div class="modal-section"><h3>Skills to explore · ${missing.length}</h3>
      <div class="modal-skills">${missing.length
    ? missing.map((skill) => `<span class="modal-skill missing">${escapeHTML(skill)}</span>`).join("")
    : '<span class="modal-skill">No role skills missing</span>'}</div>
    </div>
    <div class="modal-section"><h3>Screening summary</h3>
      <p class="modal-decision">${escapeHTML(candidate.ai_decision || "No additional screening summary is available.")}</p>
    </div>
    <div class="modal-section"><h3>All detected skills</h3>
      <div class="modal-skills">${skills.length
    ? skills.map((skill) => `<span class="modal-skill">${escapeHTML(skill)}</span>`).join("")
    : '<span class="modal-skill">No skills detected</span>'}</div>
    </div>`;
  modal.hidden = false;
  document.body.classList.add("modal-open");
  document.getElementById("modalClose").focus();
}

function closeCandidateModal() {
  document.getElementById("candidateModal").hidden = true;
  document.body.classList.remove("modal-open");
  lastFocusedElement?.focus();
}

function updateFileLabels() {
  const jdFile = document.getElementById("jdInput").files[0];
  const resumeFiles = Array.from(document.getElementById("resumeInput").files);
  document.getElementById("jdFileName").textContent = jdFile?.name || "Choose a role description";
  document.getElementById("resumeFileName").textContent = resumeFiles.length
    ? resumeFiles.length === 1 ? resumeFiles[0].name : `${resumeFiles.length} resumes selected`
    : "Choose candidate resumes";
}

function bindFileDropzone(dropzoneId, inputId) {
  const dropzone = document.getElementById(dropzoneId);
  const input = document.getElementById(inputId);
  ["dragenter", "dragover"].forEach((eventName) => dropzone.addEventListener(eventName, (event) => {
    event.preventDefault();
    dropzone.classList.add("drag-over");
  }));
  ["dragleave", "drop"].forEach((eventName) => dropzone.addEventListener(eventName, (event) => {
    event.preventDefault();
    dropzone.classList.remove("drag-over");
  }));
  dropzone.addEventListener("drop", (event) => {
    if (event.dataTransfer?.files?.length) {
      input.files = event.dataTransfer.files;
      updateFileLabels();
    }
  });
}

document.addEventListener("DOMContentLoaded", () => {
  let savedTheme = "dark";
  try {
    savedTheme = localStorage.getItem("talentlens-theme") || "dark";
  } catch {
    // Use the default theme if browser storage is unavailable.
  }
  applyTheme(savedTheme);
  document.getElementById("themeToggle").addEventListener("click", () => {
    const nextTheme = document.body.dataset.theme === "light" ? "dark" : "light";
    applyTheme(nextTheme, true);
  });
  document.getElementById("loadDataButton").addEventListener("click", loadAnalysisFromBackend);
  document.getElementById("signOutButton").addEventListener("click", async (event) => {
    const button = event.currentTarget;
    button.disabled = true;
    try {
      const response = await fetch(`${API_BASE}/auth/logout`, {
        method: "POST",
        credentials: "include",
      });
      if (!response.ok) throw new Error("Sign out failed. Please try again.");
      window.location.reload();
    } catch (error) {
      setNotice(error.message || "Sign out failed. Please try again.");
      button.disabled = false;
    }
  });
  document.getElementById("analysisForm").addEventListener("submit", submitAnalysis);
  document.getElementById("jdInput").addEventListener("change", updateFileLabels);
  document.getElementById("resumeInput").addEventListener("change", updateFileLabels);
  document.getElementById("resultsTableBody").addEventListener("click", (event) => {
    const button = event.target.closest("[data-candidate-index]");
    if (button) openCandidateModal(Number(button.dataset.candidateIndex));
  });
  document.getElementById("modalClose").addEventListener("click", closeCandidateModal);
  document.getElementById("candidateModal").addEventListener("click", (event) => {
    if (event.target.id === "candidateModal") closeCandidateModal();
  });
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && !document.getElementById("candidateModal").hidden) {
      closeCandidateModal();
    }
  });
  bindFileDropzone("jdDropzone", "jdInput");
  bindFileDropzone("resumeDropzone", "resumeInput");
  initializeAuthentication()
    .then((authenticated) => {
      if (authenticated && !authRequired) loadAnalysisFromBackend();
    })
    .catch((error) => {
      document.getElementById("appShell").hidden = false;
      setNotice(`${error.message} Check that the TalentLens API is running, then refresh.`);
    });
});
