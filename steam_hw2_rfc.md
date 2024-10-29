# RFC: Реализация функции отложенных сообщений в сервисе чатов Steam

- **RFC:** Реализация функции отложенных сообщений в сервисе чатов Steam
- **Created:** 27-10-2024
- **Last Update:** 29-10-2024


## 1. Бизнес цель решаемой задачи

### Описание системы
Система чатов Steam предоставляет пользователям возможность общаться в реальном времени в текстовом формате. В данный момент пользователи могут отправлять и получать мгновенные сообщения, но отсутствует возможность планирования сообщений к отправке в будущем. Это ограничивает гибкость и удобство общения, особенно при координации мероприятий или напоминаниях, которые не требуют мгновенной доставки.

### Цель проекта
Добавление функции отложенных сообщений в систему чатов Steam позволит пользователям выбирать время, когда сообщение должно быть отправлено, что повысит удобство использования чата. Функция будет полезна для:

- Напоминаний о событиях или задачах
- Запланированной отправки сообщений при ожидании времени, удобного для получателя
- Расширения возможностей системы, что в перспективе может повысить лояльность и активность пользователей


## 2. Архитектура решения

Функция будет спроектирована на основе модели C4, чтобы дать представление об архитектуре с различными уровнями детализации.

---

### Контекстная диаграмма (C1)

#### **Основные элементы:**
- **Пользователь:** Мобильный или настольный клиент Steam, который взаимодействует с системой чатов.
- **Сервис Чатов Steam:** Внутренняя система Steam для обработки сообщений в реальном времени.
- **Сервис Запланированных Сообщений:** Новый сервис, отвечающий за обработку и доставку отложенных сообщений.
- **База Данных Сообщений:** Существующая база данных для хранения сообщений.
- **Сервис Уведомлений:** Отправляет уведомления пользователю при доставке запланированного сообщения.

**Диаграмма C1:** Пользователь → Сервис Чатов Steam → Сервис Запланированных Сообщений → База Данных Сообщений, Сервис Уведомлений

---

### Диаграмма контейнеров (C2)

- **Steam Client:** Клиентская часть, где пользователь выбирает текст сообщения, устанавливает время отправки и отправляет запрос на создание отложенного сообщения.
- **API Gateway:** Прокси, принимающий запросы от клиента и направляющий их в нужный сервис.
- **Message Scheduling Service (MSS):** Основной сервис для обработки запросов на создание отложенного сообщения, хранения времени отправки и периодической проверки времени отправки сообщений.
- **Message Service:** Существующий сервис для обработки сообщений, куда MSS отправляет отложенные сообщения для их отправки.
- **Message DB:** Хранит запланированные и уже отправленные сообщения.
- **Notification Service:** Отправляет уведомления при доставке отложенных сообщений пользователю.

---

### Диаграмма компонентов (C3)

- **API Gateway:** Прокси, отвечающий за обработку запросов от клиентов и направление их в соответствующие сервисы.
- **Message Scheduling Service:**
  - **Scheduled Message Processor:** Обрабатывает запросы на создание и удаление запланированных сообщений.
  - **Scheduler:** Компонент, который периодически проверяет, какие сообщения нужно отправить.
  - **Message Dispatcher:** Отправляет сообщение в **Message Service** в нужное время.
- **Message Service:** Отправляет сообщение и уведомления пользователю.
- **Message DB:** Таблицы для хранения текста, времени отправки, статуса запланированных сообщений.


## 3. Возможные проблемы и недочеты решения

1. **Синхронизация времени:** У пользователей из разных временных зон могут возникнуть трудности с выбором времени отправки. Решение – ввод привязки ко времени пользователя с указанием его временной зоны.
  
2. **Нагрузка на Scheduler:** Периодическая проверка запланированных сообщений может вызывать нагрузку на сервис. Решение – оптимизация проверки с использованием очередей сообщений и сегментированных проверок по временным промежуткам.

3. **Конфликты при изменении сообщений:** Пользователь может изменить время отправки или отменить сообщение после его создания, что требует обновления данных в базе и учета этих изменений в Scheduler. Для решения понадобится механизм блокировок или оптимистических транзакций.

4. **Ошибки в доставке:** При высокой нагрузке или сетевых ошибках возможны задержки в доставке сообщений, поэтому необходим механизм повторной попытки.


## 4. Секвенс-схема

На основе диаграмм C2 и C3 представлена секвенс-схема, которая описывает последовательность шагов для отправки отложенного сообщения. Ссылка для визуализации секвенс-схемы: [Sequence Diagram](https://sequencediagram.org)

### Шаги:

1. **User** → **Steam Client**: Отправка текста сообщения, времени отправки.
2. **Steam Client** → **API Gateway**: Запрос на создание запланированного сообщения.
3. **API Gateway** → **Message Scheduling Service (MSS)**: Создание записи о запланированном сообщении в базе данных.
4. **MSS** → **Message DB**: Сохранение текста сообщения и времени отправки.
5. **Scheduler (MSS)**: Периодическая проверка времени отправки запланированных сообщений.
6. **Scheduler (MSS)** → **Message Dispatcher (MSS)**: По наступлению времени отправки сообщение передается в Message Service.
7. **Message Dispatcher** → **Message Service**: Отправка сообщения пользователю.
8. **Message Service** → **Notification Service**: Отправка уведомления о доставке сообщения.
9. **Notification Service** → **User**: Пользователь получает уведомление об отправленном сообщении.

---

### Сссылки на ресурсы
- [Доска Draw.io с диаграммами](https://app.diagrams.net/#G1SFrvZ-4JnOCyRrZPpUBmBkQpdAtNryAU#%7B%22pageId%22%3A%223V0q8ZhMyobrDDrFFbST%22%7D)