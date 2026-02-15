<?php
// Cek apakah form dikirim
if (isset($_POST['crawl'])) {

    $namaPenulis = $_POST['namaPenulis']; 
    $keyword     = $_POST['keyword'];
    $jumlahData  = $_POST['jumlahData'];

    $nama = str_replace(' ','+', $namaPenulis); #Joko siswantoro --> Jika+siswantoro
    $keywords = str_replace(' ','+', $keyword); 

    $commands = "python crawlings.py " . $nama  . " " . $jumlahData .  " " . $keywords . " 2>&1";
    $output = shell_exec($commands);
    
    // echo "$output";
    // die();
} else {
    header("Location: index.php");
    exit;
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Hasil Pencarian</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
<div class="container">
    <a href="index.php" class="back-link">&lt; Back to Home</a>

    <div class="info-summary">
        <p><b>Nama Penulis :</b> <?php echo($namaPenulis) ?></p>
        <p><b>Keyword Artikel :</b> <?php echo($keyword) ?></p>
        <p><b>Jumlah data :</b> <?php echo($jumlahData) ?></p>
    </div>

    <h3>Hasil Pencarian</h3>

    <div class="table-container">
        <table>
            <thead>
                <tr>
                    <th>Judul Artikel</th>
                    <th>Penulis</th>
                    <th>Tanggal Rilis</th>
                    <th>Nama Jurnal</th>
                    <th>Jumlah Sitasi</th>
                    <th>Link Jurnal</th>
                    <th>Similaritas</th>
                </tr>
            </thead>
            <tbody>
                <?php
                $result = json_decode($output, true);
                if ($result) {
                    foreach ($result as $row) {
                        echo "
                        <tr>
                            <td class='left'>{$row['judul']}</td>
                            <td class='left'>{$row['pengarang']}</td>
                            <td class='center'>{$row['tanggal_terbit']}</td>
                            <td class='center'>{$row['jurnal']}</td>
                            <td class='center'>{$row['total_kutipan']}</td>
                            <td class='center'><a href='{$row['link']}'>Link</a></td>
                            <td class='center'>{$row['similarity']}</td>
                        </tr>";
                    }
                }
                ?>
            </tbody>
        </table>
    </div>
</div>
</body>
</html>
