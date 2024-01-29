<?php
// Exécute le script Python et récupère la sortie
$output = shell_exec('./scanreseau-2.py 2>&1');
// Si vous avez des erreurs dans la sortie, elles seront également affichées à des fins de débogage

// Connexion à la base de données
$servername = "localhost";
$username = "adminJonathan";
$password = "azerty";
$dbname = "RESEAU_IRO_O";

$conn = new mysqli($servername, $username, $password, $dbname);

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

$types = ['PC', 'IMP', 'Routeur', 'Switch'];

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

// Utilise les données récupérées du script Python
$postes_detectes = json_decode($output, true);  // Assurez-vous que le format de sortie est adapté à votre besoin

foreach ($types as $type) {
    echo "<h2>$type</h2>";
    echo '<table><tr>';

    foreach ($postes_detectes as $poste) {
        // Utilise les données pour générer le contenu
        $icon = strtolower($type) . '-co.png';

        echo '<td>';
        echo '<div class="device">';
        echo "<img src='images/$icon' alt='$type'>";
        echo '<div class="device-info">';
        echo '<p>Nom de l\'appareil: ' . $poste['nom'] . '</p>';
        echo '<p>Adresse IP: ' . $poste['ip'] . '</p>';
        echo '<p class="device-status online">Statut: En ligne</p>';
        echo '</div>';
        echo '</div>';
        echo '</td>';
    }

    echo '</tr></table>';
}

echo '</div>';
echo '</body>';
echo '</html>';

$conn->close();
?>
