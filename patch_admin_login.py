import sys
PATH = 'index.html'
s=open(PATH,encoding='utf-8').read()
if 'function adminLogin' in s:
    print('• مُطبّق مسبقاً — تخطّي.'); sys.exit(0)

# 1) زر 🔧 أسفل زر الخروج (يسار)
BTN_OLD = '<button class="btn btn-exit" id="exit-3d">⤢ الخروج تعبت امشي</button>'
BTN_NEW = (BTN_OLD +
  '\n      <button class="btn" id="admin-toggle" title="دخول المالك" '
  'style="align-self:flex-end;margin-top:4px">🔧</button>')
if BTN_OLD not in s: print('✗ لم أجد زر الخروج'); sys.exit(1)
s=s.replace(BTN_OLD, BTN_NEW, 1)

# 2) علم admin في state
ST_OLD = "const state = { cart:new Map(), mode:'3d', activeProduct:null, active:false };"
ST_NEW = "const state = { cart:new Map(), mode:'3d', activeProduct:null, active:false, admin:false };"
if ST_OLD not in s: print('✗ لم أجد كائن state'); sys.exit(1)
s=s.replace(ST_OLD, ST_NEW, 1)

# 3) منطق دخول المالك — يُحقن قبل loadScene()
ANCHOR = "  // [المرحلة 1] جلب المشهد من Firestore عبر الخادم (مع رجوع آمن للافتراضي) ثم البناء"
if ANCHOR not in s: print('✗ لم أجد مرساة loadScene'); sys.exit(1)

ADMIN = """  // ===== [المرحلة 2-أ] دخول المالك (مرة واحدة) =====
  // السر يُحفظ في sessionStorage (للجلسة فقط) ويُرسل لاحقاً في ترويسة x-admin-token.
  // الحارس الحقيقي في الخادم (ADMIN_TOKEN) — إخفاء الأدوات في الواجهة للراحة فقط.
  const ADMIN_KEY = 'tr_admin_token';

  async function verifyToken(token){
    try{
      const r = await fetch('/api/admin/check', { method:'POST',
        headers:{ 'Content-Type':'application/json', 'x-admin-token': token } });
      return r.ok;
    }catch(e){ return false; }
  }

  function setAdminUI(on){
    state.admin = on;
    const btn = document.getElementById('admin-toggle');
    if(btn){
      btn.textContent = on ? '🔧 مالك' : '🔧';
      btn.style.borderColor = on ? 'var(--ok)' : '';
      btn.style.color = on ? 'var(--ok)' : '';
    }
  }

  async function adminLogin(){
    if(state.admin){
      sessionStorage.removeItem(ADMIN_KEY); setAdminUI(false); toast('خرجت من وضع المالك'); return;
    }
    const token = prompt('أدخل سر المالك:');
    if(!token) return;
    toast('جارٍ التحقق…');
    const ok = await verifyToken(token);
    if(ok){ sessionStorage.setItem(ADMIN_KEY, token); setAdminUI(true); toast('أهلاً بك أيها المالك ✓'); }
    else { toast('سر غير صحيح'); }
  }

  (async function restoreAdmin(){
    const saved = sessionStorage.getItem(ADMIN_KEY);
    if(saved && await verifyToken(saved)) setAdminUI(true);
    else sessionStorage.removeItem(ADMIN_KEY);
  })();

  const _adminBtn = document.getElementById('admin-toggle');
  if(_adminBtn) _adminBtn.addEventListener('click', adminLogin);

"""
s=s.replace(ANCHOR, ADMIN + ANCHOR, 1)

open(PATH,'w',encoding='utf-8').write(s)
print('✓ تم: دخول المالك (زر 🔧 + تحقق + sessionStorage + state.admin)')
