import sys
PATH='index.html'
s=open(PATH,encoding='utf-8').read()

if '[PATCH] manual-scale' in s:
    print('• مُطبّق مسبقاً — تخطّي.'); sys.exit(0)

OLD = """    // [PATCH] robust-fit: نضيف ثم نحدّث المصفوفات ثم نقيس ونصغّر فعلياً
    model.traverse(o => { if (o.isMesh) { o.castShadow = true; o.receiveShadow = true; o.frustumCulled = false; } });
    player.add(model);
    player.updateWorldMatrix(true, true);
    let bb = new THREE.Box3().setFromObject(model);
    const size = new THREE.Vector3(); bb.getSize(size);
    const h = size.y || 1;
    model.scale.multiplyScalar(TARGET_HEIGHT / h);          // تطبيع الارتفاع إلى TARGET_HEIGHT
    player.updateWorldMatrix(true, true);
    bb = new THREE.Box3().setFromObject(model);
    model.position.y -= bb.min.y;                           // القدمان عند الأرض
    console.log('[scale] ارتفاع أصلي=' + h.toFixed(2) + ' → مضبوط=' + TARGET_HEIGHT);"""

NEW = """    // [PATCH] manual-scale: حجم يدوي موثوق (auto-fit غير دقيق مع موديلات الـrig)
    const MODEL_SCALE = 1;     // ← اضبط هذا حتى يناسب الحجم (مثلاً 0.5 ، 0.1 ، 0.05 أو 5 ، 10)
    const MODEL_Y     = 0;     // رفع/خفض الشخصية عمودياً إن لزم
    model.traverse(o => { if (o.isMesh) { o.castShadow = true; o.receiveShadow = true; o.frustumCulled = false; } });
    model.scale.setScalar(MODEL_SCALE);
    model.position.set(0, MODEL_Y, 0);
    player.add(model);
    try {
      const _b = new THREE.Box3().setFromObject(model); const _s = new THREE.Vector3(); _b.getSize(_s);
      console.log('[size] الارتفاع الحالي ≈ ' + _s.y.toFixed(2) + 'م | للوصول لـ1.7م اجعل MODEL_SCALE ≈ ' + (MODEL_SCALE * 1.7 / (_s.y || 1)).toFixed(4));
    } catch (e) {}"""

if OLD not in s:
    print('✗ لم أجد كتلة robust-fit المتوقعة — أوقفت التعديل.'); sys.exit(1)

open(PATH,'w',encoding='utf-8').write(s.replace(OLD,NEW,1))
print('✓ تم: مقياس يدوي + طباعة الرقم المقترح في الـConsole')
