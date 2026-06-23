import sys
PATH = 'index.html'
s=open(PATH,encoding='utf-8').read()
if 'function rebuildScene' in s:
    print('• مُطبّق مسبقاً — تخطّي.'); sys.exit(0)

B1_OLD = "  const buildingBoxes=[];"
B1_NEW = "  const buildingBoxes=[];\n  const buildingGroups=[];"
if B1_OLD not in s: print('✗ buildingBoxes'); sys.exit(1)
s=s.replace(B1_OLD, B1_NEW, 1)

B2_OLD = """    scene.add(g);
    buildingBoxes.push({minX:x-w/2,maxX:x+w/2,minZ:z-d/2,maxZ:z+d/2});
  }"""
B2_NEW = """    scene.add(g);
    buildingGroups.push(g);
    buildingBoxes.push({minX:x-w/2,maxX:x+w/2,minZ:z-d/2,maxZ:z+d/2});
  }"""
if B2_OLD not in s: print('✗ نهاية addBuilding'); sys.exit(1)
s=s.replace(B2_OLD, B2_NEW, 1)

CITY_OLD = """  (function buildCity(){
    for(let z=-STREET.halfZ; z<=STREET.halfZ; z+=6.5){
      if(Math.random()<0.12) continue;
      const h1=6+Math.random()*11, h2=6+Math.random()*11;
      addBuilding(-10-Math.random()*1.5, z, 4+Math.random()*2, 5, h1, tints[(Math.random()*tints.length)|0]);
      addBuilding( 10+Math.random()*1.5, z, 4+Math.random()*2, 5, h2, tints[(Math.random()*tints.length)|0]);
    }
    for(let z=-18; z<=18; z+=12){
      [-6.6,6.6].forEach(x=>{
        const pole=new THREE.Mesh(new THREE.CylinderGeometry(0.06,0.06,3.2,8),
          new THREE.MeshStandardMaterial({color:0x2a2622}));
        pole.position.set(x,1.6,z); pole.castShadow=true; scene.add(pole);
        const bulb=new THREE.Mesh(new THREE.SphereGeometry(0.18,12,12),
          new THREE.MeshStandardMaterial({color:0xffe6a8, emissive:0xffcf73, emissiveIntensity:1.4}));
        bulb.position.set(x,3.3,z); scene.add(bulb);
      });
    }
  })();"""
CITY_NEW = """  // [المرحلة 2-أ] المباني صارت بيانات مخزّنة (قابلة للحفظ) بدل العشوائية وقت التشغيل
  const BUILDINGS = [];
  function genDefaultBuildings(){
    BUILDINGS.length = 0;
    for(let z=-STREET.halfZ; z<=STREET.halfZ; z+=6.5){
      if(Math.random()<0.12) continue;
      const h1=6+Math.random()*11, h2=6+Math.random()*11;
      BUILDINGS.push({ x:-10-Math.random()*1.5, z, w:4+Math.random()*2, d:5, h:h1, tint:tints[(Math.random()*tints.length)|0] });
      BUILDINGS.push({ x: 10+Math.random()*1.5, z, w:4+Math.random()*2, d:5, h:h2, tint:tints[(Math.random()*tints.length)|0] });
    }
  }
  function buildBuildings(){ BUILDINGS.forEach(b=> addBuilding(b.x, b.z, b.w, b.d, b.h, b.tint)); }
  function buildLights(){
    for(let z=-18; z<=18; z+=12){
      [-6.6,6.6].forEach(x=>{
        const pole=new THREE.Mesh(new THREE.CylinderGeometry(0.06,0.06,3.2,8),
          new THREE.MeshStandardMaterial({color:0x2a2622}));
        pole.position.set(x,1.6,z); pole.castShadow=true; scene.add(pole);
        const bulb=new THREE.Mesh(new THREE.SphereGeometry(0.18,12,12),
          new THREE.MeshStandardMaterial({color:0xffe6a8, emissive:0xffcf73, emissiveIntensity:1.4}));
        bulb.position.set(x,3.3,z); scene.add(bulb);
      });
    }
  }
  buildLights();"""
if CITY_OLD not in s: print('✗ buildCity'); sys.exit(1)
s=s.replace(CITY_OLD, CITY_NEW, 1)

SG_OLD = "  const shelfBoxes = [];"
SG_NEW = "  const shelfBoxes = [];\n  const sectionGroups = [];"
if SG_OLD not in s: print('✗ shelfBoxes'); sys.exit(1)
s=s.replace(SG_OLD, SG_NEW, 1)

SGADD_OLD = """    scene.add(g);
    g.updateWorldMatrix(true,true);
    const bb=new THREE.Box3().setFromObject(g);
    shelfBoxes.push({minX:bb.min.x,maxX:bb.max.x,minZ:bb.min.z,maxZ:bb.max.z});
  }"""
SGADD_NEW = """    scene.add(g); sectionGroups.push(g);
    g.updateWorldMatrix(true,true);
    const bb=new THREE.Box3().setFromObject(g);
    shelfBoxes.push({minX:bb.min.x,maxX:bb.max.x,minZ:bb.min.z,maxZ:bb.max.z});
  }"""
if SGADD_OLD not in s: print('✗ نهاية buildSection'); sys.exit(1)
s=s.replace(SGADD_OLD, SGADD_NEW, 1)

SET_OLD = """      btn.style.color = on ? 'var(--ok)' : '';
    }
  }"""
SET_NEW = """      btn.style.color = on ? 'var(--ok)' : '';
    }
    if(typeof renderEditor==='function') renderEditor();
  }"""
if SET_OLD not in s: print('✗ setAdminUI'); sys.exit(1)
s=s.replace(SET_OLD, SET_NEW, 1)

ANCHOR = "  // [المرحلة 1] جلب المشهد من Firestore عبر الخادم (مع رجوع آمن للافتراضي) ثم البناء"
if ANCHOR not in s: print('✗ مرساة loadScene'); sys.exit(1)
EDITOR = r"""  // ===== [المرحلة 2-أ] إعادة بناء المشهد (تمسح القديم وتبني من SECTIONS/BUILDINGS) =====
  function _clearGroups(arr){ arr.forEach(g=>scene.remove(g)); arr.length=0; }
  function rebuildScene(){
    _clearGroups(sectionGroups);
    _clearGroups(buildingGroups);
    interactables.length = 0;
    for(const k in productMeshes) delete productMeshes[k];
    shelfBoxes.length = 0;
    buildingBoxes.length = 0;
    prepareData();
    buildSections();
    buildBuildings();
    buildGrid();
    renderCart();
  }

  // ===== [المرحلة 2-أ] لوحة تحرير المالك =====
  const editorEl = document.createElement('div');
  editorEl.id = 'editor';
  editorEl.style.cssText = 'position:fixed;top:70px;right:14px;z-index:55;width:300px;max-height:78vh;'
    + 'overflow-y:auto;background:var(--surface);border:1px solid var(--line);border-radius:14px;'
    + 'padding:16px;display:none;font-size:13px;box-shadow:0 10px 40px rgba(0,0,0,.5)';
  document.body.appendChild(editorEl);

  function _uid(p){ return p + Math.random().toString(36).slice(2,7); }

  function renderEditor(){
    if(!state.admin){ editorEl.style.display='none'; return; }
    editorEl.style.display='block';
    let h = '<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px">'
      + '<b style="font-size:15px">🛠 محرّر المتجر</b>'
      + '<button id="ed-save" style="border:none;background:var(--ok);color:#0f140c;padding:8px 14px;border-radius:9px;font-weight:700">💾 حفظ</button></div>';
    h += '<div style="color:var(--brass);margin:6px 0 8px">الأقسام</div>';
    SECTIONS.forEach((sec,si)=>{
      h += '<div style="background:var(--surface-2);border-radius:10px;padding:10px;margin-bottom:8px">'
        + '<div style="display:flex;justify-content:space-between;align-items:center">'
        + '<b>'+sec.name+'</b>'
        + '<button data-delsec="'+si+'" style="border:none;background:#0000;color:#c0392b;font-size:16px">🗑</button></div>'
        + '<div style="color:var(--muted);font-size:11px;margin:4px 0">'+(sec.side==='right'?'يمين':'يسار')+' · '+sec.products.length+' منتجات</div>';
      sec.products.forEach((pr,pi)=>{
        h += '<div style="display:flex;justify-content:space-between;align-items:center;padding:5px 0;border-top:1px solid var(--line)">'
          + '<span>'+pr.name+' · '+pr.price+'</span>'
          + '<button data-delprod="'+si+':'+pi+'" style="border:none;background:#0000;color:#c0392b">✕</button></div>';
      });
      h += '<button data-addprod="'+si+'" style="width:100%;margin-top:6px;border:1px dashed var(--line);background:#0000;color:var(--ink);padding:6px;border-radius:8px">+ منتج</button></div>';
    });
    h += '<button id="ed-addsec" style="width:100%;border:1px dashed var(--brass);background:#0000;color:var(--brass);padding:8px;border-radius:8px;margin-bottom:14px">+ قسم جديد</button>';
    h += '<div style="color:var(--brass);margin:6px 0 8px">المباني ('+BUILDINGS.length+')</div>';
    h += '<button id="ed-addbld" style="width:100%;border:1px dashed var(--brass);background:#0000;color:var(--brass);padding:8px;border-radius:8px">+ مبنى</button>';
    editorEl.innerHTML = h;
    _wireEditor();
  }

  function _wireEditor(){
    editorEl.querySelector('#ed-save').onclick = saveScene;
    editorEl.querySelector('#ed-addsec').onclick = _addSectionUI;
    editorEl.querySelector('#ed-addbld').onclick = _addBuildingUI;
    editorEl.querySelectorAll('[data-delsec]').forEach(b=> b.onclick=()=>{ SECTIONS.splice(+b.dataset.delsec,1); rebuildScene(); renderEditor(); });
    editorEl.querySelectorAll('[data-addprod]').forEach(b=> b.onclick=()=> _addProductUI(+b.dataset.addprod));
    editorEl.querySelectorAll('[data-delprod]').forEach(b=> b.onclick=()=>{ const a=b.dataset.delprod.split(':'); SECTIONS[+a[0]].products.splice(+a[1],1); rebuildScene(); renderEditor(); });
  }

  function _addSectionUI(){
    const name = prompt('اسم القسم:'); if(!name) return;
    const side = confirm('موافق = يمين الشارع · إلغاء = يسار') ? 'right' : 'left';
    const c = (prompt('لون القسم (hex مثل 2d6cdf):','2d6cdf')||'2d6cdf').replace('#','');
    SECTIONS.push({ id:_uid('sec'), name, side, edge:(parseInt(c,16)||0x2d6cdf), products:[] });
    rebuildScene(); renderEditor(); toast('أُضيف القسم');
  }
  function _addProductUI(si){
    const name = prompt('اسم المنتج:'); if(!name) return;
    const price = parseFloat(prompt('السعر:','10'))||0;
    SECTIONS[si].products.push({ id:_uid('p'), name, price });
    rebuildScene(); renderEditor(); toast('أُضيف المنتج');
  }
  function _addBuildingUI(){
    const side = confirm('موافق = يمين الشارع · إلغاء = يسار') ? 1 : -1;
    BUILDINGS.push({ x: side*(10+Math.random()*1.5), z:(Math.random()*2-1)*18, w:5, d:5, h:8, tint:tints[(Math.random()*tints.length)|0] });
    rebuildScene(); renderEditor(); toast('أُضيف مبنى');
  }

  async function saveScene(){
    const token = sessionStorage.getItem(ADMIN_KEY);
    if(!token){ toast('سجّل الدخول كمالك أولاً'); return; }
    const cleanSections = SECTIONS.map(sec=>({
      id: sec.id, name: sec.name, side: sec.side, edge: sec.edge,
      products: sec.products.map(pr=>({ id: pr.id, name: pr.name, price: pr.price }))
    }));
    const cleanBuildings = BUILDINGS.map(b=>({ x:b.x, z:b.z, w:b.w, d:b.d, h:b.h, tint:b.tint }));
    toast('جارٍ الحفظ…');
    try{
      const r = await fetch('/api/admin/save', { method:'POST',
        headers:{ 'Content-Type':'application/json', 'x-admin-token': token },
        body: JSON.stringify({ layout:{ sections:cleanSections, buildings:cleanBuildings } }) });
      if(r.ok) toast('تم الحفظ ✓ — يراه الزوّار الآن');
      else if(r.status===401){ toast('انتهت صلاحية الدخول'); setAdminUI(false); }
      else toast('فشل الحفظ');
    }catch(e){ toast('خطأ في الاتصال'); }
  }

"""
s=s.replace(ANCHOR, EDITOR + ANCHOR, 1)

LOAD_OLD = """  async function loadScene(){
    try{
      const r = await fetch('/api/scene');
      if(r.ok){
        const data = await r.json();
        if(data && Array.isArray(data.sections) && data.sections.length){
          SECTIONS.length = 0; data.sections.forEach(sec=>SECTIONS.push(sec));
          console.log('[scene] حُمِّل من الخادم:', data.sections.length, 'أقسام');
        }
      }
    }catch(e){ console.warn('[scene] تعذّر الجلب — استخدام الافتراضي', e); }
    prepareData();
    buildSections();
    buildGrid();
    renderCart();
  }
  loadScene();
  animate();"""
LOAD_NEW = """  async function loadScene(){
    let loadedBuildings = false;
    try{
      const r = await fetch('/api/scene');
      if(r.ok){
        const data = await r.json();
        if(data && Array.isArray(data.sections) && data.sections.length){
          SECTIONS.length = 0; data.sections.forEach(sec=>SECTIONS.push(sec));
        }
        if(data && Array.isArray(data.buildings)){
          BUILDINGS.length = 0; data.buildings.forEach(b=>BUILDINGS.push(b)); loadedBuildings = true;
        }
        console.log('[scene] حُمِّل من الخادم');
      }
    }catch(e){ console.warn('[scene] تعذّر الجلب — استخدام الافتراضي', e); }
    if(!loadedBuildings) genDefaultBuildings();
    rebuildScene();
    renderEditor();
  }
  loadScene();
  animate();"""
if LOAD_OLD not in s: print('✗ loadScene'); sys.exit(1)
s=s.replace(LOAD_OLD, LOAD_NEW, 1)

open(PATH,'w',encoding='utf-8').write(s)
print('✓ تم: لوحة التحرير + مباني مخزّنة + إعادة بناء + حفظ')
