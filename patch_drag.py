import sys
PATH = 'index.html'
s=open(PATH,encoding='utf-8').read()
if 'function editPickStart' in s:
    print('• مُطبّق مسبقاً — تخطّي.'); sys.exit(0)

PD_OLD = """      if(sec.side==='right'){ sec._pos=[7, -10 + ri*8]; sec._side=1; ri++; }
      else { sec._pos=[-7, -6 + li*8]; sec._side=-1; li++; }"""
PD_NEW = """      sec._side = (sec.side==='right') ? 1 : -1;
      if(typeof sec.x==='number' && typeof sec.z==='number'){ sec._pos=[sec.x, sec.z]; }
      else if(sec.side==='right'){ sec._pos=[7, -10 + ri*8]; ri++; }
      else { sec._pos=[-7, -6 + li*8]; li++; }"""
if PD_OLD not in s: print('✗ prepareData'); sys.exit(1)
s=s.replace(PD_OLD, PD_NEW, 1)

BB_OLD = "  function buildBuildings(){ BUILDINGS.forEach(b=> addBuilding(b.x, b.z, b.w, b.d, b.h, b.tint)); }"
BB_NEW = "  function buildBuildings(){ BUILDINGS.forEach(b=>{ addBuilding(b.x, b.z, b.w, b.d, b.h, b.tint); const g=buildingGroups[buildingGroups.length-1]; if(g) g.userData.editable={type:'building', ref:b, group:g}; }); }"
if BB_OLD not in s: print('✗ buildBuildings'); sys.exit(1)
s=s.replace(BB_OLD, BB_NEW, 1)

SS_OLD = "    scene.add(g); sectionGroups.push(g);"
SS_NEW = "    scene.add(g); sectionGroups.push(g); g.userData.editable={type:'section', ref:sec, group:g};"
if SS_OLD not in s: print('✗ buildSection scene.add'); sys.exit(1)
s=s.replace(SS_OLD, SS_NEW, 1)

PD2_OLD = """  canvas.addEventListener('pointerdown', e=>{
    if(!state.active) return;
    drag=true; moved=false; dragId=e.pointerId; lastX=e.clientX; lastY=e.clientY;
    canvas.setPointerCapture(e.pointerId);
  });"""
PD2_NEW = """  canvas.addEventListener('pointerdown', e=>{
    if(!state.active) return;
    if(state.admin && editPickStart(e)){ dragId=e.pointerId; canvas.setPointerCapture(e.pointerId); return; }
    drag=true; moved=false; dragId=e.pointerId; lastX=e.clientX; lastY=e.clientY;
    canvas.setPointerCapture(e.pointerId);
  });"""
if PD2_OLD not in s: print('✗ pointerdown'); sys.exit(1)
s=s.replace(PD2_OLD, PD2_NEW, 1)

PM_OLD = """  canvas.addEventListener('pointermove', e=>{
    if(!drag || e.pointerId!==dragId) return;
    const dx=e.clientX-lastX, dy=e.clientY-lastY; lastX=e.clientX; lastY=e.clientY;
    if(Math.abs(dx)+Math.abs(dy)>4) moved=true;
    cam.yaw   -= dx*0.005;
    cam.pitch  = Math.max(0.12, Math.min(1.1, cam.pitch - dy*0.005));
  });"""
PM_NEW = """  canvas.addEventListener('pointermove', e=>{
    if(editDrag.active && e.pointerId===dragId){ editDragMove(e); return; }
    if(!drag || e.pointerId!==dragId) return;
    const dx=e.clientX-lastX, dy=e.clientY-lastY; lastX=e.clientX; lastY=e.clientY;
    if(Math.abs(dx)+Math.abs(dy)>4) moved=true;
    cam.yaw   -= dx*0.005;
    cam.pitch  = Math.max(0.12, Math.min(1.1, cam.pitch - dy*0.005));
  });"""
if PM_OLD not in s: print('✗ pointermove'); sys.exit(1)
s=s.replace(PM_OLD, PM_NEW, 1)

PU_OLD = """  canvas.addEventListener('pointerup', e=>{
    if(e.pointerId!==dragId) return;
    if(!moved) selectAt(e.clientX, e.clientY);
    drag=false; dragId=null;
  });"""
PU_NEW = """  canvas.addEventListener('pointerup', e=>{
    if(editDrag.active && e.pointerId===dragId){ editDragEnd(); drag=false; dragId=null; return; }
    if(e.pointerId!==dragId) return;
    if(state.admin){ if(!moved) clearEditSelection(); drag=false; dragId=null; return; }
    if(!moved) selectAt(e.clientX, e.clientY);
    drag=false; dragId=null;
  });"""
if PU_OLD not in s: print('✗ pointerup'); sys.exit(1)
s=s.replace(PU_OLD, PU_NEW, 1)

RB_OLD = """  function rebuildScene(){
    _clearGroups(sectionGroups);"""
RB_NEW = """  function rebuildScene(){
    if(typeof clearEditSelection==='function') clearEditSelection();
    _clearGroups(sectionGroups);"""
if RB_OLD not in s: print('✗ rebuildScene'); sys.exit(1)
s=s.replace(RB_OLD, RB_NEW, 1)

SV_OLD = """    const cleanSections = SECTIONS.map(sec=>({
      id: sec.id, name: sec.name, side: sec.side, edge: sec.edge,
      products: sec.products.map(pr=>({ id: pr.id, name: pr.name, price: pr.price }))
    }));"""
SV_NEW = """    const cleanSections = SECTIONS.map(sec=>({
      id: sec.id, name: sec.name, side: sec.side, edge: sec.edge,
      x: sec._pos ? sec._pos[0] : undefined,
      z: sec._pos ? sec._pos[1] : undefined,
      products: sec.products.map(pr=>({ id: pr.id, name: pr.name, price: pr.price }))
    }));"""
if SV_OLD not in s: print('✗ saveScene'); sys.exit(1)
s=s.replace(SV_OLD, SV_NEW, 1)

ANCHOR = "  // [المرحلة 1] جلب المشهد من Firestore عبر الخادم (مع رجوع آمن للافتراضي) ثم البناء"
if ANCHOR not in s: print('✗ مرساة loadScene'); sys.exit(1)
DRAG = """  // ===== [المرحلة 2-ب-1] تحديد العناصر وسحبها (للمالك) =====
  let selectedEdit = null;
  const editDrag = { active:false, target:null };
  let _hl = null;
  const _groundPlane = new THREE.Plane(new THREE.Vector3(0,1,0), 0);
  const _gpHit = new THREE.Vector3();

  function _ndc(e){ return new THREE.Vector2((e.clientX/innerWidth)*2-1, -(e.clientY/innerHeight)*2+1); }

  function _placeHighlight(group){
    if(!_hl){ _hl = new THREE.BoxHelper(group, 0xC9A24B); scene.add(_hl); }
    _hl.setFromObject(group); _hl.visible = true;
  }
  function selectEdit(ed){
    selectedEdit = ed; _placeHighlight(ed.group);
    if(typeof renderEditor==='function') renderEditor();
  }
  function clearEditSelection(){
    selectedEdit = null; if(_hl) _hl.visible = false;
    if(typeof renderEditor==='function') renderEditor();
  }

  function editPickStart(e){
    raycaster.setFromCamera(_ndc(e), camera);
    const groups = sectionGroups.concat(buildingGroups);
    const hit = raycaster.intersectObjects(groups, true)[0];
    if(!hit) return false;
    let o = hit.object; while(o && !o.userData.editable) o = o.parent;
    if(!o) return false;
    selectEdit(o.userData.editable);
    editDrag.active = true; editDrag.target = o.userData.editable;
    return true;
  }
  function editDragMove(e){
    const ed = editDrag.target; if(!ed) return;
    raycaster.setFromCamera(_ndc(e), camera);
    if(!raycaster.ray.intersectPlane(_groundPlane, _gpHit)) return;
    const x = Math.max(-STREET.halfX-2, Math.min(STREET.halfX+2, _gpHit.x));
    const z = Math.max(-STREET.halfZ, Math.min(STREET.halfZ, _gpHit.z));
    ed.group.position.x = x; ed.group.position.z = z;
    ed.ref.x = x; ed.ref.z = z;
    if(ed.type==='section') ed.ref._pos = [x, z];
    if(_hl) _hl.setFromObject(ed.group);
  }
  function editDragEnd(){ editDrag.active = false; editDrag.target = null; }

"""
s=s.replace(ANCHOR, DRAG + ANCHOR, 1)

open(PATH,'w',encoding='utf-8').write(s)
print('✓ تم: تحديد + سحب + حفظ المواضع')
