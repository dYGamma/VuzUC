<?php
// Проверяем, была ли отправлена форма
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Получаем данные из формы
    $to = $_POST['to'];
    $subject = $_POST['subject'];
    $message = $_POST['message'];

    // Путь к файлу, куда будет сохранено сообщение
    $filePath = 'C:/Users/Dmitry/Desktop/6 сем/WEBKR/message.txt'; // Указать полный путь к файлу

    // Формируем содержимое файла (в текстовом формате)
    $fileContent = "To: " . $to . "\n";
    $fileContent .= "Subject: " . $subject . "\n";
    $fileContent .= "\n";
    $fileContent .= $message;

    // Записываем содержимое в файл
    file_put_contents($filePath, $fileContent);

    // Выводим сообщение об успешной отправке письма и кнопку для возврата на главную страницу
    echo "Письмо успешно отправлено.";
    echo "<br>";
    echo '<a href="index.php">Вернуться на главную страницу</a>';
} else {
    // Если форма не была отправлена, перенаправляем обратно на страницу
    header("Location: index.html");
}
?>
