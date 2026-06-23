import sys
PATH = 'index.html'
s=open(PATH,encoding='utf-8').read()
if 'const CHARACTERS' in s:
    print('• مُطبّق مسبقاً — تخطّي.'); sys.exit(0)

LOAD_OLD = """  // [PATCH] character-mesh+walk-clip: الجسم من character.glb + المشي من walk_animation2.glb (بلا ثعلب)
  const CHARACTER_MESH = 'models/walk_animation.glb';        // الجسم الظاهر
  const WALK_FILE      = 'models/walk_animation.glb';  // مصدر أنميشن المشي فقط
  const TARGET_HEIGHT  = 1.7;

  loader.load(CHARACTER_MESH, (charGltf) => {"""
LOAD_NEW = """  // [char-select] قائمة الشخصيات — أضِف سطراً لكل شخصية جديدة (ملفها في models/)
  const CHARACTERS = [
    { id:'c1', name:'الشخصية الأولى', file:'models/walk_animation.glb' },
    { id:'c2', name:'الشخصية الثانية', file:'models/walk_animation2.glb' },
  ];
  let charIndex = 0;
  let _charLoaded = false;
  const TARGET_HEIGHT  = 1.7;

  // تُحمَّل الشخصية المختارة عند الضغط على «ابدأ» (لا عند بدء الصفحة)
  function loadCharacter(file){
    const CHARACTER_MESH = file;   // الجسم الظاهر
    const WALK_FILE      = file;   // الأنميشن من نفس الملف
    loader.load(CHARACTER_MESH, (charGltf) => {"""
if LOAD_OLD not in s: print('✗ كتلة بداية التحميل'); sys.exit(1)
s=s.replace(LOAD_OLD, LOAD_NEW, 1)

CLOSE_OLD = """  }, undefined, e => console.warn('تعذّر تحميل', CHARACTER_MESH, e));

  const interactables = [];"""
CLOSE_NEW = """    }, undefined, e => console.warn('تعذّر تحميل', CHARACTER_MESH, e));
  }

  const interactables = [];"""
if CLOSE_OLD not in s: print('✗ إغلاق كتلة التحميل'); sys.exit(1)
s=s.replace(CLOSE_OLD, CLOSE_NEW, 1)

ENTER_OLD = """  <div id="enter">
    <div>
      <div class="ring">
        <svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="#C9A24B" stroke-width="1.5"><path d="M5 12h14M13 6l6 6-6 6"/></svg>
      </div>
      <h1>ابدأ التجوّل</h1>
      <p>انقر للبدء. تمشي الشخصية بـ <kbd>W A S D</kbd> أو العصا، تُدار الكاميرا بالسحب، وتنقر على أي منتج في الشارع لعرض تفاصيله.</p>
    </div>
  </div>"""
ENTER_NEW = """  <div id="enter">
    <div>
      <h1>اختر شخصيتك</h1>
      <div style="display:flex;align-items:center;justify-content:center;gap:24px;margin:22px 0">
        <button id="char-prev" class="btn" style="font-size:22px;padding:10px 18px">◀</button>
        <div id="char-name" style="font-family:var(--serif);font-size:22px;min-width:180px;color:var(--brass)"></div>
        <button id="char-next" class="btn" style="font-size:22px;padding:10px 18px">▶</button>
      </div>
      <p>اختر بالسهمين، ثم اضغط «ابدأ». تتحرّك بـ <kbd>W A S D</kbd> أو العصا.</p>
      <button id="char-start" class="btn btn-exit" style="margin-top:18px;font-size:16px;padding:13px 40px">ابدأ ▶</button>
    </div>
  </div>"""
if ENTER_OLD not in s: print('✗ شاشة enter'); sys.exit(1)
s=s.replace(ENTER_OLD, ENTER_NEW, 1)

WIRE_OLD = "  enterScreen.addEventListener('click', startWalk);"
WIRE_NEW = """  // [char-select] منطق اختيار الشخصية
  const _charNameEl = document.getElementById('char-name');
  function _renderCharName(){ if(_charNameEl) _charNameEl.textContent = CHARACTERS[charIndex].name; }
  _renderCharName();
  document.getElementById('char-prev').addEventListener('click', ()=>{
    charIndex = (charIndex - 1 + CHARACTERS.length) % CHARACTERS.length; _renderCharName();
  });
  document.getElementById('char-next').addEventListener('click', ()=>{
    charIndex = (charIndex + 1) % CHARACTERS.length; _renderCharName();
  });
  addEventListener('keydown', e=>{
    if(state.active) return;
    if(e.key==='ArrowLeft'){ charIndex=(charIndex-1+CHARACTERS.length)%CHARACTERS.length; _renderCharName(); }
    else if(e.key==='ArrowRight'){ charIndex=(charIndex+1)%CHARACTERS.length; _renderCharName(); }
  });
  document.getElementById('char-start').addEventListener('click', ()=>{
    if(!_charLoaded){ _charLoaded = true; loadCharacter(CHARACTERS[charIndex].file); }
    startWalk();
  });"""
if WIRE_OLD not in s: print('✗ enterScreen click'); sys.exit(1)
s=s.replace(WIRE_OLD, WIRE_NEW, 1)

open(PATH,'w',encoding='utf-8').write(s)
print('✓ تم: شاشة اختيار الشخصية + تأجيل التحميل')
