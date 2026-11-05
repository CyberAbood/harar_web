# موقع مقهى هرر

صفحة واحدة ثابتة، بلا JavaScript وبلا طلبات لمواقع خارجية. الملف `index.html` جاهز للرفع كما هو.

## المحتويات

| المسار | الوصف |
|---|---|
| `index.html` | الموقع النهائي، والخطوط والشعار مدمجة داخله |
| `qr/harar-qr.png` و`qr/harar-qr.svg` | كود QR، والـSVG للطباعة بأي مقاس |
| `qr/harar-qr-card.png` | بطاقة جاهزة فيها الشعار والكود |
| `src/build.py` | مصدر الموقع: المحتوى والأسعار والمراجعات والتصميم، ويبني `index.html` |
| `src/assets.py` | يرسم الشعار من صورة المنيو ويولّد الرسوم الخطية |
| `src/make_qr.py` | يولّد كود QR والبطاقة |

عدّل المحتوى من `src/build.py` ثم أعد البناء. لا تعدّل `index.html` يدويًا، لأن بصمة CSP تتغير مع أي تعديل في التنسيق.

## البناء (PowerShell)

```powershell
cd src
npm ci
python build.py
```

تحتاج `assets.py` فقط إذا غيّرت الشعار أو الرسوم:

```powershell
pip install numpy pillow potracer
python assets.py
```

## كود QR

الكود الحالي يفتح `https://cyberabood.github.io/harar/` ولن يعمل قبل نشر الموقع على هذا الرابط. لرابط آخر:

```powershell
pip install segno pillow
cd src
python make_qr.py https://your-domain.example/
```

## النشر على GitHub Pages

1. أنشئ مستودعًا باسم `harar` في حساب CyberAbood وارفع هذه الملفات إليه.
2. من Settings ثم Pages اختر الفرع `main` والمجلد `/ (root)`.
3. امسح الكود وتأكد أنه يفتح الموقع قبل الطباعة.

GitHub Pages لا يتيح إضافة ترويسات HTTP. عند الانتقال لاستضافة تتيحها أضف `frame-ancestors 'none'` و`Strict-Transport-Security`.

## قبل النشر العام

- موافقة المالك على الاسم والشعار والمراجعات وذكر الموظفين.
- التأكد من العنوان والهاتف وحساب الانستقرام وسعرَي V60.
- إضافة ساعات العمل، وهي غير موجودة حاليًا.
