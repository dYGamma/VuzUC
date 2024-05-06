<?php
// Проверяем, была ли отправлена форма
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Получаем данные из формы
    $to = $_POST['to'];
    $subject = $_POST['subject'];
    $message = $_POST['message'];
    error_reporting(E_ALL);
ini_set('display_errors', 1);
    // Настройки SMTP
    $smtpHost = 'smtp.gmail.com';
    $smtpPort = 587;
    $smtpUsername = 'samarindima4@gmail.com'; 
    $smtpPassword = 'actottsuiwjthpvo'; 
    $smtpTimeout = 30;

    // Формируем заголовки для письма
    $headers = [
        'MIME-Version: 1.0',
        'Content-type: text/html; charset=utf-8',
        'From: ' . $smtpUsername,
        'Reply-To: ' . $smtpUsername,
        'X-Mailer: PHP/' . phpversion()
    ];

    // Формируем строку параметров для отправки письма через SMTP
    $params = [
        'ssl' => [
            'verify_peer' => false,
            'verify_peer_name' => false,
            'allow_self_signed' => true
        ],
        'socket' => [
            'tcp_nodelay' => true
        ]
    ];
    $smtpAddress = sprintf('tcp://%s:%d', $smtpHost, $smtpPort);
    $context = stream_context_create($params);

    // Устанавливаем соединение с SMTP-сервером
    $smtpConnection = stream_socket_client($smtpAddress, $errno, $errstr, $smtpTimeout, STREAM_CLIENT_CONNECT, $context);

    if ($smtpConnection) {
        // Авторизуемся на сервере
        fputs($smtpConnection, 'EHLO ' . $smtpHost . "\r\n");
        fputs($smtpConnection, 'STARTTLS' . "\r\n");
        fputs($smtpConnection, 'AUTH LOGIN' . "\r\n");
        fputs($smtpConnection, base64_encode($smtpUsername) . "\r\n");
        fputs($smtpConnection, base64_encode($smtpPassword) . "\r\n");

        // Отправляем данные письма
        fputs($smtpConnection, 'MAIL FROM: <' . $smtpUsername . ">\r\n");
        fputs($smtpConnection, 'RCPT TO: <' . $to . ">\r\n");
        fputs($smtpConnection, 'DATA' . "\r\n");
        fputs($smtpConnection, 'Subject: ' . $subject . "\r\n");
        foreach ($headers as $header) {
            fputs($smtpConnection, $header . "\r\n");
        }
        fputs($smtpConnection, "\r\n");
        fputs($smtpConnection, $message . "\r\n.\r\n");

        // Завершаем сеанс
        fputs($smtpConnection, 'QUIT' . "\r\n");

        // Закрываем соединение
        fclose($smtpConnection);

        echo "Письмо успешно отправлено.";
    } else {
        echo "Ошибка при отправке письма.";
    }
} else {
    // Если форма не была отправлена, перенаправляем обратно на страницу
    header("Location: index.html");
}
?>
