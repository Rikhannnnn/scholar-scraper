<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <h1>Pencarian Data Artikel Ilmiah</h1>
        <form action="hasilPencarian.php" method="POST">
            <div class="form-group">
                <label>Nama Penulis</label>
                <input type="text" name="namaPenulis" placeholder="Nama Penulis" required>
            </div>
            <div class="form-group">
                <label>Keyword Artikel</label>
                <input type="text" name="keyword" placeholder="Kata Kunci" required>
            </div>
            <div class="form-group">
                <label>Jumlah Data</label>
                <input type="number" name="jumlahData" value="5" required>
            </div>
            <input type="submit" name="crawl" value="Search">
        </form>
    </div>
</body>
</html>