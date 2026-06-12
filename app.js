const API_URL = "http://localhost:8000";
let uploadedResumeText = "";
let fullResumeText = ""; // Store full text separately

// File Upload Handling
const uploadArea = document.getElementById("uploadArea");
const resumeFile = document.getElementById("resumeFile");

uploadArea.addEventListener("click", () => resumeFile.click());

uploadArea.addEventListener("dragover", (e) => {
    e.preventDefault();
    uploadArea.classList.add("drag-over");
});

uploadArea.addEventListener("dragleave", () => {
    uploadArea.classList.remove("drag-over");
});

uploadArea.addEventListener("drop", (e) => {
    e.preventDefault();
    uploadArea.classList.remove("drag-over");
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFileSelect(files[0]);
    }
});

resumeFile.addEventListener("change", (e) => {
    if (e.target.files.length > 0) {
        handleFileSelect(e.target.files[0]);
    }
});

async function handleFileSelect(file) {
    if (!file) return;
    
    // Validate file type
    const validTypes = [
        'application/pdf',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'application/msword',
        'text/plain'
    ];
    
    if (!validTypes.includes(file.type)) {
        alert("Please upload a PDF, DOCX, or TXT file");
        document.getElementById("fileStatus").textContent = "✗ Invalid file type";
        return;
    }
    
    const formData = new FormData();
    formData.append("file", file);
    
    try {
        document.getElementById("fileStatus").textContent = "⏳ Uploading...";
        
        const response = await fetch(`${API_URL}/upload-resume`, {
            method: "POST",
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            uploadedResumeText = data.resume_text;
            // Store full length for reference
            const totalChars = data.full_length;
            document.getElementById("fileStatus").textContent = 
                `✓ Uploaded: ${file.name} (${totalChars.toLocaleString()} characters)`;
        } else {
            document.getElementById("fileStatus").textContent = `✗ Error: ${data.error}`;
        }
    } catch (error) {
        console.error("Upload error:", error);
        document.getElementById("fileStatus").textContent = `✗ Error: ${error.message}`;
    }
}

function clearResume() {
    resumeFile.value = "";
    uploadedResumeText = "";
    fullResumeText = "";
    document.getElementById("fileStatus").textContent = "";
}

function clearJobDesc() {
    document.getElementById("jobDescription").value = "";
}

async function analyzeResume() {
    // Validate inputs
    if (!uploadedResumeText.trim()) {
        alert("Please upload a resume first");
        return;
    }
    
    const jobDescription = document.getElementById("jobDescription").value.trim();
    if (!jobDescription) {
        alert("Please paste a job description");
        return;
    }
    
    // Show loading state
    document.getElementById("loading").classList.add("show");
    document.getElementById("results").classList.remove("show");
    document.getElementById("analyzeBtn").disabled = true;
    
    try {
        const response = await fetch(`${API_URL}/analyze`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                resume_text: uploadedResumeText,
                job_description: jobDescription
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            // data.analysis contains the parsed JSON from AI
            displayResults(data.analysis);
        } else {
            alert(`Analysis Error: ${data.error}`);
        }
    } catch (error) {
        console.error("Analysis error:", error);
        alert(`Error: ${error.message}`);
    } finally {
        document.getElementById("loading").classList.remove("show");
        document.getElementById("analyzeBtn").disabled = false;
    }
}

function displayResults(analysis) {
    // Validate analysis object
    if (!analysis || typeof analysis !== 'object') {
        alert("Invalid analysis response");
        return;
    }
    
    const score = analysis.match_score || 0;
    const scoreCircle = document.getElementById("scoreCircle");
    
    // Set score with color coding
    scoreCircle.textContent = score;
    scoreCircle.classList.remove("excellent", "good", "poor");
    
    if (score >= 80) {
        scoreCircle.classList.add("excellent");
    } else if (score >= 60) {
        scoreCircle.classList.add("good");
    } else {
        scoreCircle.classList.add("poor");
    }
    
    // Set explanation
    const explanation = analysis.score_explanation || "Analysis complete";
    document.getElementById("scoreExplanation").textContent = explanation;
    
    // Populate lists with error handling
    populateList("strengths", analysis.key_strengths || []);
    populateList("gaps", analysis.key_gaps || []);
    populateList("keywords", analysis.missing_keywords || []);
    populateList("suggestions", analysis.improvement_suggestions || []);
    
    // Show results
    document.getElementById("results").classList.add("show");
    document.getElementById("results").scrollIntoView({ behavior: "smooth" });
}

function populateList(elementId, items) {
    const ul = document.getElementById(elementId);
    ul.innerHTML = "";
    
    if (!Array.isArray(items)) {
        items = [];
    }
    
    items.forEach(item => {
        if (item && typeof item === 'string') {
            const li = document.createElement("li");
            li.textContent = item;
            ul.appendChild(li);
        }
    });
}

function downloadReport() {
    const score = document.getElementById("scoreCircle").textContent;
    const explanation = document.getElementById("scoreExplanation").textContent;
    
    let report = `Resume Job Match Report\n`;
    report += `============================\n\n`;
    report += `Match Score: ${score}/100\n`;
    report += `${explanation}\n\n`;
    
    report += `Key Strengths:\n`;
    document.querySelectorAll("#strengths li").forEach(li => {
        report += `- ${li.textContent}\n`;
    });
    
    report += `\nKey Gaps:\n`;
    document.querySelectorAll("#gaps li").forEach(li => {
        report += `- ${li.textContent}\n`;
    });
    
    report += `\nMissing Keywords:\n`;
    document.querySelectorAll("#keywords li").forEach(li => {
        report += `- ${li.textContent}\n`;
    });
    
    report += `\nImprovement Suggestions:\n`;
    document.querySelectorAll("#suggestions li").forEach(li => {
        report += `- ${li.textContent}\n`;
    });
    
    const blob = new Blob([report], { type: "text/plain" });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "resume-analysis.txt";
    a.click();
    window.URL.revokeObjectURL(url);
}

function copyResults() {
    let text = `Match Score: ${document.getElementById("scoreCircle").textContent}/100\n\n`;
    text += `Improvement Suggestions:\n`;
    document.querySelectorAll("#suggestions li").forEach(li => {
        text += `• ${li.textContent}\n`;
    });
    
    navigator.clipboard.writeText(text).then(() => {
        alert("Suggestions copied to clipboard!");
    }).catch(err => {
        console.error("Failed to copy:", err);
        alert("Failed to copy to clipboard");
    });
}

function newAnalysis() {
    document.getElementById("results").classList.remove("show");
    clearResume();
    clearJobDesc();
    document.getElementById("resumeFile").focus();
}