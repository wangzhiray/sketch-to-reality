// static/chat.js

const SKY_RADIUS = 50;
const addBtn   = document.getElementById('addBtn');
const recBtn   = document.getElementById('recBtn');
const stopBtn  = document.getElementById('stopBtn');
const toast    = document.getElementById('toast');
const hover    = document.getElementById('hover');
const sceneEl  = document.querySelector('a-scene');
const skyEl    = document.getElementById('sky');
const cameraEl = document.getElementById('camera');
const prevBtn  = document.getElementById('prev');
const nextBtn  = document.getElementById('next');

// Panorama switching state
let currentPan = 1;
const maxPan = 3;       // ← set this to the total number of panoramas you have
const tagsByPan = {};

// Helper: show toast
function showToast(msg) {
  toast.innerText = msg;
  toast.style.display = 'block';
  setTimeout(() => toast.style.display = 'none', 1500);
}

// Project from 3D to screen coords
function project(vec3) {
  const cam = cameraEl.getObject3D('camera');
  const proj = vec3.clone().project(cam);
  return {
    x: (proj.x * 0.5 + 0.5) * window.innerWidth,
    y: (-proj.y * 0.5 + 0.5) * window.innerHeight
  };
}

// Clear all note dots
function clearDots() {
  sceneEl.querySelectorAll('.note-dot').forEach(d => sceneEl.removeChild(d));
}

// Redraw stored dots for the active panorama
function drawDots() {
  (tagsByPan[currentPan] || []).forEach(tag => {
    const dot = document.createElement('a-sphere');
    dot.classList.add('note-dot');
    dot.setAttribute('position', `${tag.pos.x} ${tag.pos.y} ${tag.pos.z}`);
    dot.setAttribute('radius', '0.5');
    dot.setAttribute('material', 'shader: flat; color: red; side: double');
    sceneEl.appendChild(dot);
    dot.object3D.position.copy(new THREE.Vector3(tag.pos.x, tag.pos.y, tag.pos.z));
    dot.setAttribute('data-text', tag.text);
    dot.addEventListener('mouseenter', onHoverEnter);
    dot.addEventListener('mouseleave', onHoverLeave);
  });
}

// Switch panorama by cycling through files
function switchPan(offset) {
  currentPan = ((currentPan - 1 + offset + maxPan) % maxPan) + 1;
  skyEl.setAttribute('src', `/static/panorama_input/panorama_${currentPan}.jpg`);
  clearDots();
  drawDots();
  showToast(`Panorama ${currentPan}`);
}

// Wire arrow buttons
prevBtn.addEventListener('click', () => switchPan(-1));
nextBtn.addEventListener('click', () => switchPan(1));

// Hover tooltip handlers
function onHoverEnter(evt) {
  const dot = evt.target;
  const text = dot.getAttribute('data-text') || '';
  if (!text) return;
  const pos = dot.object3D.position;
  const { x, y } = project(pos);
  hover.style.left = x + 'px';
  hover.style.top  = y + 'px';
  hover.textContent = text;
  hover.style.display = 'block';
}
function onHoverLeave() {
  hover.style.display = 'none';
}

// 1) Add Notes
let awaitingDot = false;
let currentDot  = null;
addBtn.addEventListener('click', () => {
  awaitingDot = true;
  addBtn.disabled = true;
  recBtn.disabled = true;
  stopBtn.disabled = true;
  showToast('Click on panorama to place a dot');
});

// 2) Place dot on sky click
sceneEl.addEventListener('click', (evt) => {
  if (!awaitingDot) return;
  awaitingDot = false;
  addBtn.disabled = false;
  recBtn.disabled = false;
  stopBtn.disabled = true;

  const pt = evt.detail.intersection.point;
  const pos = new THREE.Vector3(pt.x, pt.y, pt.z)
    .normalize()
    .multiplyScalar(SKY_RADIUS - 0.1);

  const dot = document.createElement('a-sphere');
  dot.classList.add('note-dot');
  dot.setAttribute('position', `${pos.x} ${pos.y} ${pos.z}`);
  dot.setAttribute('radius', '0.5');
  dot.setAttribute('material', 'shader: flat; color: red; side: double');
  sceneEl.appendChild(dot);
  dot.object3D.position.copy(pos);

  dot.setAttribute('data-text', '');
  dot.addEventListener('mouseenter', onHoverEnter);
  dot.addEventListener('mouseleave', onHoverLeave);

  if (!tagsByPan[currentPan]) tagsByPan[currentPan] = [];
  tagsByPan[currentPan].push({
    pos: { x: pos.x, y: pos.y, z: pos.z },
    text: ''
  });

  currentDot = dot;
  showToast('Click Record to add note');
});

// 3) Record audio
let recorder, audioChunks = [];
recBtn.addEventListener('click', async () => {
  recBtn.disabled = true;
  stopBtn.disabled = false;
  audioChunks = [];
  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  recorder = new MediaRecorder(stream);
  recorder.ondataavailable = e => audioChunks.push(e.data);
  recorder.start();
});

// 4) Stop & transcribe
stopBtn.addEventListener('click', () => {
  recorder.onstop = async () => {
    const blob = new Blob(audioChunks, { type: 'audio/webm' });
    const fd = new FormData();
    fd.append('file', blob, 'audio.webm');
    fd.append('model', 'whisper-1');
    const res = await fetch('/transcribe', { method: 'POST', body: fd });
    const data = await res.json();
    const text = data.text || data.error || '';

    currentDot.setAttribute('data-text', text);
    const arr = tagsByPan[currentPan];
    if (arr && arr.length) arr[arr.length - 1].text = text;
    showToast(text);

    stopBtn.disabled = true;
    recBtn.disabled = false;
    addBtn.disabled = false;
  };
  recorder.stop();
});
