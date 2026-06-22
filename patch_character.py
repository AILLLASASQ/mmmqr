import re, sys
PATH = 'index.html'
s = open(PATH, encoding='utf-8').read()

if '[PATCH] character+walk' in s:
    print('• مُطبّق مسبقاً — تخطّي.'); sys.exit(0)

A = 'const loader = new GLTFLoader();'
B = 'const interactables = ['
if A not in s or B not in s:
    print('✗ لم أجد المرساة المتوقعة — أوقفت التعديل لتفادي الإفساد.'); sys.exit(1)

start, end = s.index(A), s.index(B)

NEW = """const loader = new GLTFLoader();
  let mixer = null, walkAction = null;

  // [PATCH] character+walk: الجسم من character.glb + المشي من walk_animation2.glb
  const CHARACTER_MESH = 'models/character.glb';
  const WALK_CLIP      = 'models/walk_animation2.glb';
  const TARGET_HEIGHT  = 1.7;   // ارتفاع تقريبي لضبط المقياس تلقائياً

  function logGltf(tag, g){
    let meshes = 0; g.scene.traverse(o => { if (o.isMesh) meshes++; });
    const sz = new THREE.Vector3(); new THREE.Box3().setFromObject(g.scene).getSize(sz);
    console.log(`[${tag}] ميش=${meshes} | الحجم=${sz.x.toFixed(2)},${sz.y.toFixed(2)},${sz.z.toFixed(2)} | أنميشن=`, g.animations.map(a => a.name));
  }

  loader.load(CHARACTER_MESH, (charGltf) => {
    logGltf('character', charGltf);
    const model = charGltf.scene;

    // مقياس تلقائي حسب الارتفاع + إنزال القدمين إلى الأرض
    const sz = new THREE.Vector3(); new THREE.Box3().setFromObject(model).getSize(sz);
    if (sz.y > 0) model.scale.setScalar(TARGET_HEIGHT / sz.y);
    const b2 = new THREE.Box3().setFromObject(model);
    model.position.y -= b2.min.y;

    model.traverse(o => { if (o.isMesh) { o.castShadow = true; o.receiveShadow = true; o.frustumCulled = false; } });
    player.add(model);
    mixer = new THREE.AnimationMixer(model);

    const play = (clip) => { walkAction = mixer.clipAction(clip); walkAction.play(); };

    if (charGltf.animations && charGltf.animations.length) {
      play(charGltf.animations[0]);                 // أنميشن داخل ملف الشخصية
    } else {
      loader.load(WALK_CLIP, (walkGltf) => {        // أو من ملف المشي المنفصل
        logGltf('walk', walkGltf);
        if (walkGltf.animations.length) play(walkGltf.animations[0]);
        else console.warn('⚠ walk_animation2.glb لا يحتوي أي clip.');
      }, undefined, e => console.warn('تعذّر تحميل', WALK_CLIP, e));
    }
  }, undefined, e => console.warn('تعذّر تحميل', CHARACTER_MESH, e));"""

open(PATH, 'w', encoding='utf-8').write(s[:start] + NEW + "\n\n  " + s[end:])
print('✓ تم تعديل index.html')
