# LG STORE

Учебный проект — магазин приложений LG.

## ДЗ 21: Покупки и лёгкие списки

### Промежуточная модель
- **Модель:** `Purchase`
- **Связывает:** `User` ↔ `App`
- **Свои поля:** `price_paid` (уплачено), `purchased_at` (дата покупки)

### Значение поля `price_paid`
Берётся **из view** (`app.price` в момент нажатия кнопки «Купить»). Это снимок цены на момент покупки: распродажа потом меняет цену карточки, а уплаченная сумма остаётся прежней.

### Может ли автор купить своё приложение
**Нет.** Автор не покупает своё приложение — у него уже есть доступ. Кнопка «Купить» автору не показывается, а прямой POST отклоняется сообщением «Это ваше приложение, покупать его не нужно».

### Текст ошибки `add()` без `through_defaults`

django.db.utils.IntegrityError: NOT NULL constraint failed: main_purchase.price_paid

### Текст ошибки повторного `create()
django.db.utils.IntegrityError: UNIQUE constraint failed: main_purchase.user_id, main_purchase.app_id

### `defer` в списках
- `category_detail` — `.defer('description')`
- `NewAppView` — `.defer('description')`

### Замеры запросов
- `defer('description')` без чтения описания: **1 запрос** (N строк)
- `defer('description')` с чтением описания: **N + 1 запросов**
- `Purchase.objects.filter` + `only`: **1 запрос**
- `user.purchases` + `only`: **N + 1 запросов**

