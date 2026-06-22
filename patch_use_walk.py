import sys
PATH = 'index.html'
s = open(PATH, encoding='utf-8').read()

if '[PATCH] character-mesh+walk-clip' in s:
    print('• مُطبّق مسبقاً — تخطّي.'); sys.exit(0)

A = 'const loader = new GLTFLoader();'
B = 'const interactables = ['
if A not in s or B not in s:
    print('✗ لم أجد المرساة المتوقعة — أوقفت التعديل.'); sys.exit(1)

start, end = s.index(A), s.index(B)

NEW = """const loader = new GLTFLoader();
  let mixer = null, walkAction = null;

  // [PATCH] character-mesh+walk-clip: الجسم من character.glb + المشي من walk_animation2.glb (بلا ثعلب)
  const CHARACTER_MESH = 'models/character.glb';        // الجسم الظاهر
  const WALK_FILE      = 'models/walk_animation2.glb';  // مصدر أنميشن المشي فقط
  const TARGET_HEIGHT  = 1.7;

  loader.load(CHARACTER_MESH, (charGltf) => {
    const model = charGltf.scene;
    let meshes = 0; model.traverse(o => { if (o.isMesh) meshes++; });
    console.log('[character] ميش=' + meshes, '| أنميشن داخلي=', charGltf.animations.map(a => a.name));

    const sz = new THREE.Vector3(); new THREE.Box3().setFromObject(model).getSize(sz);
    if (sz.y > 0) model.scale.setScalar(TARGET_HEIGHT / sz.y);
    const b = new THREE.Box3().setFromObject(model);
    model.position.y -= b.min.y;

    model.traverse(o => { if (o.isMesh) { o.castShadow = true; o.receiveShadow = true; o.frustumCulled = false; } });
    player.add(model);
    mixer = new THREE.AnimationMixer(model);

    const applyWalk = (clip) => {
      const names = new Set(); model.traverse(o => names.add(o.name));
      const bound = clip.tracks.filter(t => names.has(t.name.split('.')[0])).length;
      console.log('[walk] clip=' + clip.name + ' | مسارات مرتبطة=' + bound + '/' + clip.tracks.length);
      if (bound === 0) console.warn('⚠ هيكل العظام غير متطابق: أنميشن ' + WALK_FILE + ' لا يناسب ' + CHARACTER_MESH + ' (ستقف الشخصية بلا حركة).');
      walkAction = mixer.clipAction(clip); walkAction.play();
    };

    loader.load(WALK_FILE, (walkGltf) => {
      const clips = walkGltf.animations || [];
      const walk = clips.find(c => /walk/i.test(c.name)) || clips[1] || clips[0];
      if (walk) applyWalk(walk);
      else if (charGltf.animations.length) applyWalk(charGltf.animations[0]);
      else console.warn('⚠ لا يوجد أي clip للمشي.');
    }, undefined, e => {
      console.warn('تعذّر تحميل', WALK_FILE, e);
      if (charGltf.animations.length) applyWalk(charGltf.animations[0]);
    });
  }, undefined, e => console.warn('تعذّر تحميل', CHARACTER_MESH, e));"""

open(PATH, 'w', encoding='utf-8').write(s[:start] + NEW + "\n\n  " + s[end:])
print('✓ تم: الجسم من character.glb + أنميشن المشي من walk_animation2.glb (أُلغي الثعلب)')
