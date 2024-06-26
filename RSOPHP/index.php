<?php

// Connexion à la base de données
$servername = "192.168.1.64";
$username = "adminAbdallah";
$password = "azerty";
$dbname = "RESEAU_IRO_O";

$conn = new mysqli($servername, $username, $password, $dbname);

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

echo '<!DOCTYPE html>';
echo '<html lang="en">';
echo '<head>';
echo '<meta charset="UTF-8">';
echo '<meta name="viewport" content="width=device-width, initial-scale=1.0">';
echo '<title>Visualisation des Périphériques dans le réseau</title>';
echo '<link rel="stylesheet" href="./style/style.css">';
echo '</head>';
echo '<body>';
echo '<h1>Visualisation des Périphériques dans le réseau</h1>';
echo '<div class="container">';

foreach ($types as $type) {
    echo "<h2>" . ucfirst($type) . "s</h2>";
    echo '<table><tr>';

    foreach ($data['postes'] as $poste) {
        if ($poste['categorie'] == $type) {
            // Utilise les données pour générer le contenu
            $icon = strtolower($poste['categorie']) . '-co.png';

            echo '<td>';
            echo '<div class="device">';
            echo "<img src='images/$icon' alt='{$poste['categorie']}'>";
            echo '<div class="device-info">';
            echo '<p>Nom de l\'appareil: ' . $poste['nom'] . '</p>';
            echo '<p>Adresse IP: ' . $poste['ip'] . '</p>';
            echo '<p class="device-status online">Statut: En ligne</p>';
            echo '</div>';
            echo '</div>';
            echo '</td>';
        }
    }

    echo '</tr></table>';
}

echo '</div>';
echo '</body>';
echo '</html>';

$conn->close();
?>
