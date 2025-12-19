document.querySelectorAll(".drop-zone__input").forEach(input => {
    const box = input.closest(".drop-zone");

    box.addEventListener("click", () => input.click());

    input.addEventListener("change", () => {
        if (input.files.length) updateThumb(box, input.files);
    });

    box.addEventListener("dragover", e => {
        e.preventDefault();
        box.classList.add("over");
    });

    ["dragleave", "dragend"].forEach(type => {
        box.addEventListener(type, () => box.classList.remove("over"));
    });

    box.addEventListener("drop", e => {
        e.preventDefault();
        if (e.dataTransfer.files.length) {
            input.files = e.dataTransfer.files;
            updateThumb(box, e.dataTransfer.files);
        }
        box.classList.remove("over");
    });
});

function updateThumb(box, files) {
    let thumb = box.querySelector(".drop-zone__thumb");
    if (box.querySelector(".prompt")) box.querySelector(".prompt").style.display = "none";

    if (!thumb) {
        thumb = document.createElement("div");
        thumb.classList.add("drop-zone__thumb");
        box.appendChild(thumb);
    }
    thumb.textContent = `${files.length} files selected`;
}

document.getElementById('analyze-btn').addEventListener('click', async () => {
    const jd = document.getElementById('job-description').value;
    const input = document.getElementById('resume-upload');

    if (!jd) return alert("Enter a job description.");
    if (!input.files.length) return alert("Upload resumes.");

    const form = new FormData();
    form.append('job_description', jd);
    for (let f of input.files) form.append('resumes', f);

    const btn = document.getElementById('analyze-btn');
    const txt = btn.textContent;
    btn.textContent = 'Processing...';
    btn.disabled = true;

    try {
        const res = await fetch('/process', { method: 'POST', body: form });
        const data = await res.json();
        if (res.ok) showResults(data.results);
        else alert(data.error);
    } catch (e) {
        console.error(e);
        alert("Server error.");
    } finally {
        btn.textContent = txt;
        btn.disabled = false;
    }
});

function showResults(data) {
    const section = document.getElementById('results-section');
    const tbody = document.querySelector('tbody');
    tbody.innerHTML = '';

    data.forEach((item, i) => {
        const row = document.createElement('tr');
        let cls = 'score-low';
        if (item.score >= 70) cls = 'score-high';
        else if (item.score >= 40) cls = 'score-med';

        const skills = item.missing_skills.map(s => `<span class="skill-tag">${s}</span>`).join('');

        row.innerHTML = `
            <td>#${i + 1}</td>
            <td>
                <b>${item.filename}</b><br>
                <small style="color:#64748b">${item.experience_years} years</small>
            </td>
            <td>${item.job_fit}</td>
            <td>${item.experience_level}</td>
            <td><span class="score-badge ${cls}">${item.score}%</span></td>
            <td>${skills || '<small style="color:green">Match!</small>'}</td>
            <td>
                <div class="feedback-buttons">
                    <button class="feedback-btn" onclick="rate('${item.filename}', 'good', this)">👍</button>
                    <button class="feedback-btn" onclick="rate('${item.filename}', 'bad', this)">👎</button>
                </div>
            </td>
        `;
        tbody.appendChild(row);
    });

    section.classList.remove('hidden');
    section.scrollIntoView({ behavior: 'smooth' });
}

async function rate(name, type, btn) {
    try {
        await fetch('/feedback', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ filename: name, rating: type })
        });
        btn.parentElement.innerHTML = '<span style="color:green;font-size:0.8rem">Saved</span>';
    } catch (e) { console.error(e); }
}
