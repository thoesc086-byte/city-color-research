import * as THREE from "./vendor/three.module.min.js";

const whites = [
  {
    id: "chapel",
    name: "礼堂白",
    color: "#ECE9DF",
    caption: "礼堂白 / 精神性、地标、仪式感",
    note: "白被提纯成一个可识别的精神符号。",
    material: "plaster"
  },
  {
    id: "fog",
    name: "海雾白",
    color: "#D8DDE0",
    caption: "海雾白 / 冷感、失焦、冬季海岸",
    note: "白被雾气降低对比，变得疏离而安静。",
    material: "mist"
  },
  {
    id: "dune",
    name: "沙丘白",
    color: "#D8C6AA",
    caption: "沙丘白 / 暖、粗粝、自然底色",
    note: "白不是纯净表面，而是带有颗粒和地形。",
    material: "sand"
  },
  {
    id: "cream",
    name: "奶油白",
    color: "#F1E8D8",
    caption: "奶油白 / 民宿、咖啡、温柔消费",
    note: "白被商业转译成柔软、可停留的日常。",
    material: "fabric"
  },
  {
    id: "stone",
    name: "图书馆灰",
    color: "#B9B1A5",
    caption: "图书馆灰 / 阴影、秩序、低饱和街区",
    note: "白成为降低视觉噪音的社区秩序。",
    material: "plaster"
  },
  {
    id: "glare",
    name: "过曝白",
    color: "#FBFAF4",
    caption: "过曝白 / 强光、照片、传播",
    note: "白在影像里被推向明亮、梦幻和可分享。",
    material: "glare"
  }
];

const systemLayers = [
  {
    title: "生态白",
    color: "#D8DDE0",
    label: "海 / 沙 / 雾 / 光",
    text: "海、沙、雾、光构成阿那亚白色的自然底色。"
  },
  {
    title: "建筑白",
    color: "#F4F3EE",
    label: "礼堂 / 图书馆 / 美术馆",
    text: "建筑把流动的自然白固定为精神性和地标感。"
  },
  {
    title: "商业白",
    color: "#F1E8D8",
    label: "民宿 / 咖啡 / 展陈",
    text: "商业把白转译成安静、舒适和可消费的生活方式。"
  },
  {
    title: "秩序白",
    color: "#D6D2C8",
    label: "街区 / 店招 / 规则",
    text: "低饱和视觉界面维持社区的统一和克制。"
  },
  {
    title: "传播白",
    color: "#FBFAF4",
    label: "照片 / 滤镜 / 城市品牌",
    text: "影像把白放大成阿那亚最容易被记住的城市符号。"
  }
];

const labState = {
  white: whites[0],
  sun: 58,
  fog: 28,
  roughness: 68,
  exposure: 34
};

const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

function makeRenderer(canvas) {
  const renderer = new THREE.WebGLRenderer({
    canvas,
    antialias: true,
    alpha: true
  });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.02;
  return renderer;
}

function resizeRenderer(renderer, camera, canvas) {
  const rect = canvas.parentElement.getBoundingClientRect();
  const width = Math.max(320, Math.floor(rect.width));
  const height = Math.max(360, Math.floor(rect.height));
  const needsResize = canvas.width !== Math.floor(width * renderer.getPixelRatio()) ||
    canvas.height !== Math.floor(height * renderer.getPixelRatio());

  if (needsResize) {
    renderer.setSize(width, height, false);
    camera.aspect = width / height;
    camera.updateProjectionMatrix();
  }
}

function createDuneGeometry() {
  const geometry = new THREE.PlaneGeometry(10, 5, 80, 32);
  geometry.rotateX(-Math.PI / 2);
  const positions = geometry.attributes.position;
  for (let i = 0; i < positions.count; i += 1) {
    const x = positions.getX(i);
    const z = positions.getZ(i);
    const ridge = Math.sin(x * 0.9) * 0.13 + Math.cos(z * 1.7) * 0.1;
    const slope = Math.max(0, (z + 2.5) / 5) * 0.6;
    positions.setY(i, ridge + slope);
  }
  geometry.computeVertexNormals();
  return geometry;
}

function createSoftCircleTexture() {
  const canvas = document.createElement("canvas");
  canvas.width = 128;
  canvas.height = 128;
  const ctx = canvas.getContext("2d");
  const gradient = ctx.createRadialGradient(64, 64, 2, 64, 64, 62);
  gradient.addColorStop(0, "rgba(255,255,255,0.42)");
  gradient.addColorStop(0.48, "rgba(255,255,255,0.12)");
  gradient.addColorStop(1, "rgba(255,255,255,0)");
  ctx.fillStyle = gradient;
  ctx.fillRect(0, 0, 128, 128);
  const texture = new THREE.CanvasTexture(canvas);
  texture.colorSpace = THREE.SRGBColorSpace;
  return texture;
}

function initWhiteLab() {
  const canvas = document.querySelector("#whiteLabCanvas");
  const caption = document.querySelector("#labCaption");
  if (!canvas || !caption) return;
  const renderer = makeRenderer(canvas);
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(38, 1, 0.1, 100);
  camera.position.set(5.2, 3.2, 7.2);
  camera.lookAt(0, 0.55, 0);

  const ambient = new THREE.HemisphereLight(0xf8f5ea, 0xb9b1a2, 1.6);
  scene.add(ambient);

  const sun = new THREE.DirectionalLight(0xfff6df, 2.4);
  sun.position.set(2, 5, 4);
  scene.add(sun);

  const group = new THREE.Group();
  scene.add(group);

  const duneMaterial = new THREE.MeshStandardMaterial({
    color: 0xe8dfcf,
    roughness: 0.92,
    metalness: 0
  });
  const dune = new THREE.Mesh(createDuneGeometry(), duneMaterial);
  dune.position.set(0, -0.08, 0.1);
  group.add(dune);

  const sea = new THREE.Mesh(
    new THREE.PlaneGeometry(11, 6, 1, 1),
    new THREE.MeshStandardMaterial({
      color: 0xd9dedb,
      transparent: true,
      opacity: 0.48,
      roughness: 0.62
    })
  );
  sea.rotation.x = -Math.PI / 2;
  sea.position.set(0, -0.13, -3.12);
  group.add(sea);

  const chapelMaterial = new THREE.MeshStandardMaterial({
    color: new THREE.Color(labState.white.color),
    roughness: 0.68,
    metalness: 0,
    envMapIntensity: 0.4
  });

  const base = new THREE.Mesh(new THREE.BoxGeometry(1.15, 1.05, 1.7), chapelMaterial);
  base.position.set(0, 0.76, 0);
  const roof = new THREE.Mesh(new THREE.ConeGeometry(0.88, 1.15, 4), chapelMaterial);
  roof.position.set(0, 1.86, 0);
  roof.rotation.y = Math.PI / 4;
  const wall = new THREE.Mesh(new THREE.BoxGeometry(2.2, 0.12, 1.4), chapelMaterial);
  wall.position.set(-1.72, 0.48, 0.18);
  group.add(base, roof, wall);

  const materialSphere = new THREE.Mesh(
    new THREE.SphereGeometry(0.42, 48, 32),
    chapelMaterial
  );
  materialSphere.position.set(2.1, 0.78, 0.7);
  group.add(materialSphere);

  const fogTexture = createSoftCircleTexture();
  const fogGroup = new THREE.Group();
  for (let i = 0; i < 18; i += 1) {
    const sprite = new THREE.Sprite(new THREE.SpriteMaterial({
      map: fogTexture,
      transparent: true,
      depthWrite: false,
      opacity: 0.18
    }));
    sprite.position.set(
      -4.6 + (i % 6) * 1.72,
      0.28 + Math.floor(i / 6) * 0.28,
      -1.55 + Math.sin(i) * 0.45
    );
    sprite.scale.setScalar(1.65 + (i % 3) * 0.42);
    fogGroup.add(sprite);
  }
  scene.add(fogGroup);

  const pointer = { x: 0, y: 0 };
  canvas.addEventListener("pointermove", (event) => {
    const rect = canvas.getBoundingClientRect();
    pointer.x = ((event.clientX - rect.left) / rect.width - 0.5) * 2;
    pointer.y = ((event.clientY - rect.top) / rect.height - 0.5) * 2;
  });

  function updateLab() {
    const color = new THREE.Color(labState.white.color);
    const exposure = 0.92 + labState.exposure / 100 * 0.72;
    const roughness = THREE.MathUtils.clamp(labState.roughness / 100, 0.12, 0.98);
    chapelMaterial.color.copy(color).lerp(new THREE.Color(0xffffff), labState.exposure / 360);
    chapelMaterial.roughness = roughness;
    chapelMaterial.needsUpdate = true;
    duneMaterial.color.set(labState.white.id === "dune" ? "#e8dfcf" : "#dfd6c6");
    renderer.toneMappingExposure = exposure;
    caption.textContent = labState.white.caption;

    const sunAngle = THREE.MathUtils.lerp(-0.9, 1.05, labState.sun / 100);
    sun.position.set(Math.sin(sunAngle) * 5.2, 2.6 + labState.sun / 100 * 3.2, Math.cos(sunAngle) * 5.4);
    sun.intensity = 1.4 + labState.sun / 100 * 2.6;

    const fogAmount = labState.fog / 100;
    scene.fog = new THREE.Fog(new THREE.Color("#f3efe6"), 5.8 - fogAmount * 2.4, 12 - fogAmount * 3.2);
    fogGroup.children.forEach((sprite, index) => {
      sprite.material.opacity = 0.04 + fogAmount * 0.34;
      sprite.position.x += Math.sin(Date.now() * 0.00012 + index) * 0.0008;
    });
  }

  function animate() {
    resizeRenderer(renderer, camera, canvas);
    updateLab();
    if (!prefersReducedMotion) {
      const t = performance.now() * 0.00025;
      group.rotation.y = -0.18 + pointer.x * 0.08 + Math.sin(t) * 0.035;
      group.rotation.x = pointer.y * 0.025;
      sea.material.opacity = 0.36 + Math.sin(t * 3) * 0.035;
    }
    renderer.render(scene, camera);
    requestAnimationFrame(animate);
  }

  animate();
}

function initWhiteChoices() {
  const choices = document.querySelector("#whiteChoices");
  if (!choices) return;
  choices.innerHTML = whites.map((white, index) => `
    <button class="white-choice" type="button" data-index="${index}" aria-pressed="${index === 0}">
      <span class="white-chip" style="background:${white.color}"></span>
      <span>${white.name}</span>
    </button>
  `).join("");

  choices.addEventListener("click", (event) => {
    const button = event.target.closest("button");
    if (!button) return;
    const index = Number(button.dataset.index);
    labState.white = whites[index];
    choices.querySelectorAll("button").forEach((item, itemIndex) => {
      item.setAttribute("aria-pressed", String(itemIndex === index));
    });
  });

  const controlMap = [
    ["#sunRange", "sun"],
    ["#fogRange", "fog"],
    ["#roughnessRange", "roughness"],
    ["#exposureRange", "exposure"]
  ];
  controlMap.forEach(([selector, key]) => {
    const input = document.querySelector(selector);
    if (!input) return;
    input.addEventListener("input", () => {
      labState[key] = Number(input.value);
    });
  });
}

function createTextSprite(text) {
  const canvas = document.createElement("canvas");
  canvas.width = 512;
  canvas.height = 128;
  const ctx = canvas.getContext("2d");
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.fillStyle = "rgba(24,23,19,0.78)";
  ctx.font = "30px 'Yu Mincho', 'Songti SC', serif";
  ctx.textAlign = "center";
  ctx.fillText(text, 256, 72);
  const texture = new THREE.CanvasTexture(canvas);
  texture.colorSpace = THREE.SRGBColorSpace;
  const sprite = new THREE.Sprite(new THREE.SpriteMaterial({
    map: texture,
    transparent: true,
    depthWrite: false
  }));
  sprite.scale.set(2.45, 0.62, 1);
  return sprite;
}

function initSystemMap() {
  const canvas = document.querySelector("#systemCanvas");
  const panel = document.querySelector("#systemPanel");
  const renderer = makeRenderer(canvas);
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(34, 1, 0.1, 100);
  camera.position.set(5.8, 4.3, 8.2);
  camera.lookAt(0, 0.6, 0);
  scene.add(new THREE.HemisphereLight(0xfaf6ec, 0xc1b9a9, 1.8));

  const group = new THREE.Group();
  group.position.x = 0.42;
  group.scale.setScalar(0.94);
  scene.add(group);

  const raycaster = new THREE.Raycaster();
  const pointer = new THREE.Vector2(99, 99);
  const panels = [];
  const rings = [];

  systemLayers.forEach((layer, index) => {
    const geometry = new THREE.CylinderGeometry(1.25 + index * 0.62, 1.25 + index * 0.62, 0.055, 96, 1, true);
    const material = new THREE.MeshStandardMaterial({
      color: layer.color,
      transparent: true,
      opacity: 0.38,
      roughness: 0.78,
      side: THREE.DoubleSide
    });
    const mesh = new THREE.Mesh(geometry, material);
    mesh.position.y = index * 0.48;
    mesh.rotation.x = Math.PI / 2;
    mesh.userData.layerIndex = index;
    group.add(mesh);
    rings.push(mesh);

    const label = createTextSprite(layer.title);
    label.position.set(-2.18, index * 0.48, 0.05 + index * 0.18);
    group.add(label);
    panels.push(label);
  });

  const axisMaterial = new THREE.LineBasicMaterial({ color: 0x8c8374, transparent: true, opacity: 0.45 });
  const points = [];
  for (let i = 0; i < systemLayers.length; i += 1) {
    points.push(new THREE.Vector3(0, i * 0.48, 0));
  }
  const axis = new THREE.Line(new THREE.BufferGeometry().setFromPoints(points), axisMaterial);
  group.add(axis);

  const active = { index: 0 };

  function setActive(index) {
    active.index = index;
    const layer = systemLayers[index];
    panel.innerHTML = `
      <p class="panel-kicker">当前层级</p>
      <h3>${layer.title}</h3>
      <p>${layer.text}</p>
    `;
  }

  canvas.addEventListener("pointermove", (event) => {
    const rect = canvas.getBoundingClientRect();
    pointer.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
    pointer.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;
  });

  canvas.addEventListener("click", () => {
    raycaster.setFromCamera(pointer, camera);
    const hit = raycaster.intersectObjects(rings)[0];
    if (hit) setActive(hit.object.userData.layerIndex);
  });

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      const ratio = entry.intersectionRatio;
      const index = Math.min(systemLayers.length - 1, Math.max(0, Math.floor(ratio * systemLayers.length)));
      setActive(index);
    });
  }, { threshold: [0.2, 0.35, 0.5, 0.65, 0.8] });
  observer.observe(document.querySelector("#system"));

  function animate() {
    resizeRenderer(renderer, camera, canvas);
    raycaster.setFromCamera(pointer, camera);
    const hit = raycaster.intersectObjects(rings)[0];
    if (hit) setActive(hit.object.userData.layerIndex);

    if (!prefersReducedMotion) {
      group.rotation.y = Math.sin(performance.now() * 0.00022) * 0.08;
    }

    rings.forEach((ring, index) => {
      const isActive = index === active.index;
      ring.material.opacity += ((isActive ? 0.72 : 0.32) - ring.material.opacity) * 0.08;
      ring.position.y += ((index * 0.48) - ring.position.y) * 0.06;
      ring.scale.x += ((isActive ? 1.03 : 1) - ring.scale.x) * 0.06;
      ring.scale.y = ring.scale.x;
    });

    renderer.render(scene, camera);
    requestAnimationFrame(animate);
  }

  animate();
}

initWhiteChoices();
initWhiteLab();
initSystemMap();
