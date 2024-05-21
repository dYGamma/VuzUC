<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Почтовый ящик</title>
    <style>
        /* Общие стили */
        .tabcontent {
            display: none;
            padding: 20px;
            border: 1px solid #ccc;
            border-top: none;
        }

        .tab {
            overflow: hidden;
            border: 1px solid #ccc;
            background-color: #f1f1f1;
        }

        .tab button {
            background-color: inherit;
            float: left;
            border: none;
            outline: none;
            cursor: pointer;
            padding: 14px 16px;
            transition: 0.3s;
        }

        .tab button:hover {
            background-color: #ddd;
        }

        .tab button.active {
            background-color: #ccc;
        }

        #compose {
            border: 1px solid #ccc;
            padding: 20px;
            margin-top: 20px;
        }

        /* Стили для вкладки "Входящие" */
        .mail-item {
            border-bottom: 1px solid #ddd;
            padding: 10px;
            overflow: hidden;
        }

        .mail-item:hover {
            background-color: #f9f9f9;
        }

        .mail-item:last-child {
            border-bottom: none;
        }

        .mail-item h4 {
            margin-top: 0;
        }

        .mail-item p {
            margin: 5px 0;
            color: #777;
        }
    </style>
</head>
<body>
    <h2>Почтовый ящик</h2>
    <!-- Вкладки -->
    <div class="tab">
        <button class="tablinks" onclick="openTab(event, 'Входящие')">Входящие</button>
        <button class="tablinks" onclick="openTab(event, 'Отправленные')">Отправленные</button>
        <button class="tablinks" onclick="openTab(event, 'Черновики')">Черновики</button>
        <button onclick="openCompose()">Написать письмо</button>
    </div>

    <!-- Содержимое вкладок -->
    <div id="Входящие" class="tabcontent">
        <div class="mail-item">
            <h4>Новое письмо от John Doe</h4>
            <p>Дата: 2024-05-05</p>
            <p>Сообщение: Привет, как дела?</p>
        </div>
        <div class="mail-item">
            <h4>Приглашение на встречу</h4>
            <p>Дата: 2024-05-03</p>
            <p>Сообщение: Приглашаем вас на нашу следующую встречу в понедельник.</p>
        </div>
        <!-- Здесь можно добавить код для отображения входящих писем -->
    </div>

    <div id="Отправленные" class="tabcontent">
        <div class="mail-item">
            <h4>Тема письма 1</h4>
            <p>Кому: example@example.com</p>
            <p>Дата: 2024-05-01</p>
            <p>Сообщение: ....</p>
        </div>
        <div class="mail-item">
            <h4>Тема письма 2</h4>
            <p>Кому: test@test.com</p>
            <p>Дата: 2024-05-02</p>
            <p>Сообщение: ....</p>
        </div>
        <!-- Здесь можно добавить код для отображения отправленных писем -->
    </div>

    <div id="Черновики" class="tabcontent">
        <div class="mail-item">
            <h4>Черновик 1</h4>
            <p>Текст черновика 1...</p>
        </div>
        <div class="mail-item">
            <h4>Черновик 2</h4>
            <p>Текст черновика 2...</p>
        </div>
        <!-- Здесь можно добавить код для отображения черновиков -->
    </div>

    <!-- Форма для написания письма -->
    <div id="compose" style="display:none;">
        <h3>Новое письмо</h3>
        <form action="send_mail.php" method="post">
            <label for="to">Кому:</label><br>
            <input type="text" id="to" name="to"><br>
            <label for="subject">Тема:</label><br>
            <input type="text" id="subject" name="subject"><br>
            <label for="message">Сообщение:</label><br>
            <textarea id="message" name="message" rows="4" cols="50"></textarea><br>
            <input type="submit" value="Отправить">
        </form>
    </div>

    <script>
        // Функция для открытия вкладок
        function openTab(evt, tabName) {
            var i, tabcontent, tablinks;
            tabcontent = document.getElementsByClassName("tabcontent");
            for (i = 0; i < tabcontent.length; i++) {
                tabcontent[i].style.display = "none";
            }
            tablinks = document.getElementsByClassName("tablinks");
            for (i = 0; i < tablinks.length; i++) {
                tablinks[i].className = tablinks[i].className.replace(" active", "");
            }
            document.getElementById(tabName).style.display = "block";
            evt.currentTarget.className += " active";
        }

        // Функция для открытия формы написания письма
        function openCompose() {
            var compose = document.getElementById("compose");
            if (compose.style.display === "none") {
                compose.style.display = "block";
            } else {
                compose.style.display = "none";
            }
        }

        // По умолчанию открыть вкладку "Входящие"
        document.getElementById("Входящие").style.display = "block";
    </script>
</body>
</html>
