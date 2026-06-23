import sys
PATH='server.js'
s=open(PATH,encoding='utf-8').read()
if '/api/scene' in s:
    print('• مُطبّق مسبقاً — تخطّي.'); sys.exit(0)
ANCHOR = "app.get('*', (req, res) => res.sendFile(path.join(__dirname, 'index.html')));"
if ANCHOR not in s:
    print('✗ لم أجد مرساة app.get(*) — أوقفت التعديل.'); sys.exit(1)
INSERT = """// ===== [المرحلة 1] تخطيط المشهد (Scene Layout) =====
app.get('/api/scene', async (req, res) => {
    if (!db) return res.json(null);
    try {
        const doc = await db.collection('scene').doc('layout').get();
        res.json(doc.exists ? doc.data() : null);
    } catch (e) {
        res.status(500).json({ error: 'فشل جلب المشهد' });
    }
});

function requireAdmin(req, res, next) {
    const token = req.get('x-admin-token');
    if (!process.env.ADMIN_TOKEN) return res.status(500).json({ error: 'ADMIN_TOKEN غير مضبوط على الخادم' });
    if (token !== process.env.ADMIN_TOKEN) return res.status(401).json({ error: 'غير مصرّح' });
    next();
}

app.post('/api/admin/check', requireAdmin, (req, res) => res.json({ ok: true }));

app.post('/api/admin/save', requireAdmin, async (req, res) => {
    if (!db) return res.status(500).json({ error: 'قاعدة البيانات غير متصلة' });
    try {
        const layout = req.body && req.body.layout;
        if (!layout || typeof layout !== 'object') return res.status(400).json({ error: 'تخطيط غير صالح' });
        await db.collection('scene').doc('layout').set({
            ...layout,
            updatedAt: FieldValue.serverTimestamp()
        });
        res.json({ success: true });
    } catch (e) {
        res.status(500).json({ error: 'فشل حفظ المشهد' });
    }
});

"""
s = s.replace(ANCHOR, INSERT + ANCHOR, 1)
open(PATH,'w',encoding='utf-8').write(s)
print('✓ تم: /api/scene + /api/admin/check + /api/admin/save')
